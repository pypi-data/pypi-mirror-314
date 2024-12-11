"""
Utilities for image handling
"""
import io
import logging
from cgi import FieldStorage

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)
from pi_heif import register_heif_opener
from typing import IO, Tuple, Union, Optional

from caerp.utils.sys_environment import resource_filename

from .files import DeformFileDict


logger = logging.getLogger(__name__)


mimetypes = {
    "PNG": "image/png",
    "PDF": "application/pdf",
    "JPG": "image/jpeg",
}


# Enable HEIC image format with Pillow
register_heif_opener()


class ImageTools:
    def rename_file(self, filename: str, file_format: str) -> str:
        """Replace extension of the filename with file_format"""
        splitted = filename.rsplit(".")
        if len(splitted) > 1:
            return f"{splitted[0]}.{file_format.lower()}"
        return filename

    def ensure_rgb(self, image):
        """
        Ensure the image is in RGB format
        """
        if image.mode == "RGBA":
            # required for the split
            image.load()
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        elif image.mode != "RGB":
            image = image.convert("RGB")
        return image

    def set_deform_file_dict_data(
        self, file_dict: DeformFileDict, image: io.BytesIO, filename: str, mimetype: str
    ) -> DeformFileDict:
        file_dict["fp"] = image
        file_dict["filename"] = filename
        file_dict["mimetype"] = mimetype
        file_dict["size"] = image.getbuffer().nbytes
        return file_dict

    def set_fieldstorage_data(
        self, field: FieldStorage, image: io.BytesIO, filename: str, mimetype: str
    ) -> FieldStorage:
        field.file = image
        field.filename = filename
        field.type = mimetype
        return field

    def set_file_data(
        self, uploaded_data, image, filename, mimetype
    ) -> Union[FieldStorage, DeformFileDict]:
        if isinstance(uploaded_data, FieldStorage):
            res = self.set_fieldstorage_data(uploaded_data, image, filename, mimetype)
        else:
            res = self.set_deform_file_dict_data(
                uploaded_data, image, filename, mimetype
            )
        return res

    def get_file_data(
        self, uploaded_data: Union[FieldStorage, DeformFileDict]
    ) -> Tuple[Optional[IO[bytes]], Optional[str]]:
        if isinstance(uploaded_data, FieldStorage):
            if uploaded_data.file is None:
                return None, uploaded_data.filename
            else:
                return uploaded_data.file, uploaded_data.filename
        else:
            return uploaded_data.get("fp"), uploaded_data["filename"]


class ImageRatio(ImageTools):
    """
    Ensure images respect the given proportions by adding white spaces

    r = ImageRatio(height_proportion, width_proportion, default_color)
    resized_image_buffer = r.complete(image_buffer)

    resized_image_buffer will respect the given proportions and
    will be filed with the given color

    height : The destination height used to compile the dest ratio
    width : The destination width used to compile the dest ratio
    color : The RGB tuple describing the filling color to use
    """

    def __init__(
        self,
        width,
        height,
        color=(
            255,
            255,
            255,
        ),
        file_format="PNG",
    ):
        self.proportions = float(width) / float(height)
        self.color = color
        self.file_format = file_format

    def get_white_layer(self, width, height):
        """
        Returns a white layer that will be our image background
        """
        size = (width, height)
        return Image.new("RGB", size, self.color)

    def complete_file(self, file_data: IO[bytes]) -> io.BytesIO:
        """
        Complete the image if proportions are smaller we complete the image with white
        """
        img_obj = Image.open(file_data)
        img_obj = self.ensure_rgb(img_obj)
        mybuffer = io.BytesIO()
        width, height = img_obj.size
        if height > 0:
            img_proportions = float(width) / float(height)
            if img_proportions >= self.proportions:
                img_obj.save(mybuffer, format="PNG", mode="RGB")
            else:
                new_width = int(height * self.proportions)
                new_height = height
                padding = int((new_width - width) / 2)
                layer = self.get_white_layer(new_width, new_height)
                layer.paste(img_obj, (padding, 0))
                mybuffer = io.BytesIO()
                layer.save(mybuffer, format="PNG", mode="RGB")
        mybuffer.seek(0)
        return mybuffer

    def __call__(
        self, value: Union[DeformFileDict, FieldStorage]
    ) -> Union[DeformFileDict, FieldStorage]:
        """
        Complete the image to get at last my proportions, not more
        """
        file_data, filename = self.get_file_data(value)
        if file_data is None or filename is None:
            return value
        image = self.complete_file(file_data)
        new_filename = self.rename_file(filename, self.file_format)
        mimetype = mimetypes[self.file_format]
        value = self.set_file_data(value, image, new_filename, mimetype)
        return value


class ImageResizer(ImageTools):
    """
    Ensure image fit inside the given box

    if the image's width or height are larger than the provided one, the image
    is resized accordingly
    """

    def __init__(self, width, height, file_format="PNG"):
        self.width = width
        self.height = height
        self.file_format = file_format

    def resize_data(self, file_data: IO[bytes]) -> IO[bytes]:
        file_data.seek(0)
        img_obj = Image.open(file_data)
        img_obj = self.ensure_rgb(img_obj)
        img_obj.thumbnail((self.width, self.height), Image.Resampling.LANCZOS)
        file_data = io.BytesIO()
        img_obj.save(file_data, format=self.file_format, mode="RGB")
        file_data.seek(0)
        return file_data

    def __call__(
        self, value: Union[DeformFileDict, FieldStorage]
    ) -> Union[DeformFileDict, FieldStorage]:
        file_data, filename = self.get_file_data(value)
        if file_data is None or filename is None:
            return value
        else:
            image = self.resize_data(file_data)
            new_filename = self.rename_file(filename, self.file_format)
            mimetype = mimetypes[self.file_format]
            value = self.set_file_data(value, image, new_filename, mimetype)

        return value


def build_header(text: str, size=(1000, 250)) -> io.BytesIO:
    """
    Build a header image containing text

    :param str text: The text to write
    :returns: The header image
    """
    img = Image.new("RGB", size, (255, 255, 255))
    fontpath = resource_filename("static/fonts/playfair_display_regular.ttf")
    font = ImageFont.truetype(fontpath, 30)

    d = ImageDraw.Draw(img)
    d.text((100, 100), text, font=font, fill=(0, 0, 0))
    mybuffer = io.BytesIO()
    img.save(mybuffer, "PNG")
    mybuffer.seek(0)
    return mybuffer
