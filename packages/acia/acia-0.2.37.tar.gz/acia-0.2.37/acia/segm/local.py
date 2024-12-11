""" Local segmentation functionality dealing with files from HDD.
"""

import os
import os.path as osp

import cv2
import numpy as np
import roifile
import tifffile

from acia.base import BaseImage, Contour, ImageSequenceSource, Overlay, RoISource


def prepare_image(image, normalize_image=True):
    """Normalize and convert image to RGB.

    Args:
        image ([type]): [description]
        normalize_image (bool, optional): Whether to normalize the image into uint8 domain (0-255). Defaults to True.
    Returns:
        [np.array]: RGB image (Width, height, 3 color channels)
    """
    # normalize image space
    if normalize_image:
        min_val = np.min(image)
        max_val = np.max(image)
        image = np.floor((image - min_val) / (max_val - min_val) * 255).astype(np.uint8)

    if len(image.shape) == 2:
        # make it artificially rgb
        image = np.repeat(image[:, :, None], 3, axis=-1)

    return image


class LocalImage(BaseImage):
    """Class for a single image"""

    def __init__(self, content, frame=None):
        self.content = content
        self.frame = frame

    @property
    def raw(self):
        return self.content

    @property
    def num_channels(self):
        if len(self.raw.shape) == 2:
            # only width and height -> 1 channel
            return 1
        else:
            # multiple channels -> channels are specified at the end
            return self.raw.shape[-1]

    def get_channel(self, channel: int):
        assert channel < self.num_channels

        if self.num_channels == 1 and len(self.raw.shape) == 2:
            return self.raw
        else:
            return self.raw[..., channel]

    def __getitem__(self, item):
        return self.raw[item]


class LocalImageSource(ImageSequenceSource):
    """Source for a single image only"""

    def __init__(self, image: LocalImage):
        self.image = image

    def __get_image(self):
        return self.image

    def __iter__(self):
        yield self.__get_image()

    def get_frame(self, frame: int):
        assert frame == 0, f"We only have a single frame, but frame={frame}"

        return self.__get_image()

    @property
    def num_channels(self) -> int:
        return self.__get_image().num_channels

    @property
    def num_frames(self) -> int:
        return 1

    def __len__(self):
        return 1

    @staticmethod
    def from_file(file_path: str, normalize_image=True):
        image = LocalImage(prepare_image(cv2.imread(file_path), normalize_image))

        return LocalImageSource(image)

    @staticmethod
    def from_array(array):
        image = LocalImage(array)

        return LocalImageSource(image)


class InMemorySequenceSource(ImageSequenceSource):
    """Image sequence for an in memory image stack"""

    def __init__(self, image_stack):
        self.image_stack = image_stack

    def get_frame(self, frame: int) -> BaseImage:
        assert frame < len(self.image_stack)

        return LocalImage(self.image_stack[frame])

    def __len__(self):
        return len(self.image_stack)

    def __iter__(self):
        for i in range(len(self)):
            yield self.get_frame(i)

    @property
    def num_channels(self) -> int:
        return self.get_frame(0).num_channels


class LocalSequenceSource(ImageSequenceSource):
    """Image sequence source for files in the local file system (e.g. a tif)."""

    def __init__(
        self, tif_file: str, normalize_image=True, luts=None, channel_index: int = 0
    ):
        """Create a new local image source

        Args:
            tif_file (str): path to the image file
            normalize_image (bool, optional): Normalizes the image pixels t0 [0, 255]. Defaults to True.
            luts: (List, optional): List of lut functions applied to the channels
            channel_index (int, optional): index in image of the channel. For example, for H,W,C dims where C is channel we should have a 2.
        """
        self.filename = tif_file
        self.normalize_image = normalize_image
        self.luts = luts
        self.channel_index = channel_index

    def __iter__(self):
        images = tifffile.imread(self.filename)

        for image in images:
            if self.luts is not None:
                if len(image.shape) == 2:
                    # just a single channel
                    num_image_channels = 1
                else:
                    num_image_channels = image.shape[self.channel_index]

                assert (
                    len(self.luts) == num_image_channels
                ), f"We need a LUTs function for every channel! We have {num_image_channels} channels but only {len(self.luts)} LUTs!"
                # apply luts to image
                if len(image.shape) == 2:
                    # we only have one channel
                    image = self.luts[0](image)
                elif len(image.shape) == 3:
                    # we have N channels (at the front)
                    for channel in range(image.shape[self.channel_index]):
                        image[channel] = self.luts[channel](
                            image.take(channel, axis=self.channel_index)
                        )

            image = prepare_image(image, self.normalize_image)

            yield LocalImage(image)

    def get_frame(self, frame: int) -> BaseImage:
        # TODO: this is super slow access for indiviudal images
        images = tifffile.imread(self.filename)
        assert frame < len(images)

        return LocalImage(prepare_image(images[frame]))

    @property
    def num_channels(self) -> int:
        return self.get_frame(0).num_channels

    def slice(self, start, end):
        images = tifffile.imread(self.filename)

        for image in images[start:end]:
            # normalize image space
            if self.normalize_image:
                min_val = np.min(image)
                max_val = np.max(image)
                image = np.floor((image - min_val) / (max_val - min_val) * 255).astype(
                    np.uint8
                )

            if len(image.shape) > 2:
                # select only the first channel
                image = image[0]

            if len(image.shape) == 2:
                # make it artificially rgb
                image = np.repeat(image[:, :, None], 3, axis=-1)

            yield LocalImage(image)


class ImageJRoISource(RoISource):
    """Source fro ImageJ RoI file format"""

    def __init__(self, filename, range=None):
        self.overlay = RoiStorer.load(filename)
        self.range = range

    def __iter__(self):
        return self.overlay.timeIterator(frame_range=self.range)

    def __len__(self) -> int:
        if self.range:
            min(len(self.overlay), len(self.range))
        return len(self.overlay)


class RoiStorer:
    """
    Stores and loads overlay results in the roi format (readable by ImageJ)
    """

    @staticmethod
    def store(overlay: Overlay, filename: str, append=False):
        """
        Stores overlay results in the roi format (readable by fiji)

        overlay: the overlay to store
        filename: filename of the roi collection (e.g. rois.zip)
        append: appends the rois if the file already exists
        """

        # generate imagej rois from the overlay
        rois = [
            roifile.ImagejRoi.frompoints(contour.coordinates, t=contour.frame)
            for contour in overlay
        ]

        if not append and osp.isfile(filename):
            os.remove(filename)

        # write them to file
        roifile.roiwrite(filename, rois)

    @staticmethod
    def load(filename: str):
        # read the imagej rois from file
        rois = roifile.roiread(filename)

        id = -1
        # convert them into contours (recover time position)
        contours = [
            Contour(roi.coordinates(), -1.0, roi.position - 1, id=id) for roi in rois
        ]

        # return the overlay
        return Overlay(contours)
