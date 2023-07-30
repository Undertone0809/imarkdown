import logging
import os
import random
import re
import time
import traceback
from typing import List, Optional, Any, Union, Dict

import requests
from pydantic import BaseModel, Field, root_validator

from imarkdown.adapter import BaseMdAdapter, MdAdapterMapper
from imarkdown.config import IMarkdownConfig
from imarkdown.constant import MdAdapterType
from imarkdown.schema import MdMediumManager, MdFile, MdFolder
from imarkdown.utils import (
    polish_path,
    supplementary_file_path,
    get_file_name_from_relative_path,
    calculate_relative_path,
)

logger = logging.getLogger(__name__)
cfg = IMarkdownConfig()


def _read_md(file_path: str) -> str:
    """read markdown file and return markdown data"""
    with open(file_path, "r", encoding="utf-8") as f:
        res = f.read()
        logger.info(f"[imarkdown] read file <{file_path}> successfully")
    return res


def _write_data(new_file_path: str, md_str: str):
    new_file_path = supplementary_file_path(new_file_path)

    with open(f"{new_file_path}", "w", encoding="utf-8") as f:
        f.write(md_str)
        logger.info(f"[imarkdown] write successfully to <{new_file_path}>")


def _download_img(image_local_storage_directory: str, image_url: str) -> Optional[str]:
    """Download image from website and stored in image_local_storage_directory

    Args:
        image_local_storage_directory: image local storage directory
        image_url: image web url

    Returns:
        Return converted image absolute path
    """
    try:
        response = requests.get(image_url)
        now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
        image_local_storage_directory = polish_path(image_local_storage_directory)
        if not os.path.exists(image_local_storage_directory):
            os.makedirs(image_local_storage_directory, exist_ok=True)

        images_path = f"{image_local_storage_directory}{now_time}{random.randint(1000, 10000)}.png"
        with open(images_path, "wb") as f:
            f.write(response.content)
        logger.info(f"[imarkdown] <{images_path}> has stored in local successfully")
        return images_path
    except Exception as e:
        traceback.print_exc()
        logger.error(f"[imarkdown] download_img failed, reason: {e}")
        return None


def _load_default_adapter() -> BaseMdAdapter:
    logger.debug(f"[imarkdown] local default adapter <{cfg.last_adapter_name}>")
    return MdAdapterMapper[cfg.last_adapter_name]()


class BaseMdImageConverter(BaseModel):
    adapter: BaseMdAdapter = Field(default_factory=_load_default_adapter)
    """Adapter determines the convert method you choose."""
    is_local_images: bool = False
    """You should set True if you want your local images upload to your picture server and you
    Markdown image url is originally local. Attention, enable_save_images can not be False if
    is_local_images is True."""
    enable_save_images: bool = True
    """It will delete images file after downloading the images if it is False."""
    image_local_storage_directory: Optional[str] = None
    """Local storage directory of images"""
    md_file_original_directory: Optional[str] = None
    """The storage directory of original markdown file."""
    md_file_output_directory: Optional[str] = None
    """The storage directory of converted markdown file."""
    converted_md_file_name: Optional[str] = None

    @root_validator(pre=True)
    def variables_check(
        cls, values: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """update IMarkdownConfig last_adapter_name"""
        logger.debug(
            f"[imarkdown] BaseMdImageConverter initialization params: {values}"
        )
        if "adapter" in values and values["adapter"]:
            cfg.last_adapter_name = values["adapter"].name
        return values

    def set_md_file_original_directory(self, md_file_path: str):
        result = supplementary_file_path(md_file_path)
        result = "/".join(result.split("/")[:-1])
        logger.debug(
            f"[imarkdown] BaseMdImageConverter md_file_original_directory: {result}"
        )
        self.md_file_original_directory = result

    def set_md_file_output_directory(self, path: str):
        result = supplementary_file_path(path)
        logger.debug(
            f"[imarkdown] BaseMdImageConverter md_file_output_directory: {result}"
        )
        self.md_file_output_directory = result

    def set_image_local_storage_directory(self, path: str):
        result = supplementary_file_path(path)
        logger.debug(
            f"[imarkdown] BaseMdImageConverter set image_local_storage_directory: {result}"
        )
        self.image_local_storage_directory = result

    def set_converted_md_file_name(
        self,
        md_file_path: str,
        enable_rename: bool = True,
        new_name: str = "",
        name_prefix: str = "",
        name_suffix: str = "_converted",
        **kwargs,
    ):
        """Set converted markdown file name.

        Args:
            md_file_path: Original markdown file path.
            enable_rename: Default is true, it means the generated markdown file will receive a new name.
            new_name: Custom converted markdown file name. If you pass it, you can not use name_prefix and name_suffix/
            name_prefix: Prefix name of generated markdown file.
            name_suffix: Suffix name of generated markdown file.
        """
        md_file_path = supplementary_file_path(md_file_path)
        md_name = md_file_path.split("/")[-1][:-3]

        if enable_rename:
            if new_name != "":
                if name_prefix or name_prefix:
                    raise ValueError(
                        "You can not set `name_prefix` and `name_prefix` if you set `new_name`."
                    )
                self.converted_md_file_name = new_name
            else:
                self.converted_md_file_name = f"{name_prefix}{md_name}{name_suffix}.md"
            logger.debug(
                f"[imarkdown] BaseMdImageConverter set converted_md_file_name {self.converted_md_file_name}"
            )
            return
        logger.debug(f"[imarkdown] BaseMdImageConverter not rename.")
        self.converted_md_file_name = f"{md_name}.md"

    def convert(
        self,
        md_file_path: str,
        image_local_storage_directory: Optional[str] = None,
        output_md_directory: Optional[str] = None,
        is_local_images: Optional[bool] = None,
        **kwargs,
    ):
        """Convert Markdown image url and generate a new Markdown file.

        Args:
            md_file_path(str): Markdown file path.
            image_local_storage_directory(Optional[str]): Specified image storage path. You can pass an absolute or a
                relative path. Default image directory path is the Markdown directory named `markdown_dir/images`.
            output_md_directory(Optional[str]): The storage directory of converted markdown file.
            is_local_images:
            **kwargs:
                enable_rename(bool): Default is true, it means the generated markdown file will receive a new name.
                name_prefix(Optional[str]): Prefix name of generated markdown file.
                name_suffix(Optional[str]): Suffix name of generated markdown file.

        Returns:
            A converted markdown file or a list of converted directory.
        """
        if not md_file_path.endswith(".md"):
            return
        if is_local_images:
            self.is_local_images = is_local_images

        self.set_converted_md_file_name(md_file_path, **kwargs)
        self.set_md_file_original_directory(md_file_path)
        if output_md_directory:
            self.set_md_file_output_directory(output_md_directory)
        else:
            self.set_md_file_output_directory(self.md_file_original_directory)
        if image_local_storage_directory:
            self.set_image_local_storage_directory(image_local_storage_directory)
        else:
            self.set_image_local_storage_directory(
                f"{self.md_file_output_directory}/images"
            )

        original_data: str = _read_md(md_file_path)
        modified_data: str = self._find_img_and_replace(original_data)

        converted_md_path = (
            f"{self.md_file_output_directory}/{self.converted_md_file_name}"
        )
        _write_data(converted_md_path, modified_data)
        logger.info(f"[imarkdown] <{md_file_path}> converted task end")

    def _find_img_and_replace(self, md_str: str) -> str:
        """Input original markdown str and replace images address
        It can find `[]()` type image url and `<img/>` type image url

        Args:
            md_str: markdown original data

        Returns:
            Markdown data for the image url has been changed.
        """
        _images = re.findall(
            r"(?:!\[(.*?)\]\((.*?)\))|<img.*?src=[\'\"](.*?)[\'\"].*?>", md_str
        )

        images = []
        for image in _images:
            if image[1] == "":
                continue
            # If current image link is local path URL and you need to web URL to a local path,
            # the local path url will not be converted.
            if not self.is_local_images and not image[1].startswith("http"):
                continue
            images.append(image[1])

        for image in images:
            converted_image_url = self._get_converted_image_url(image)
            md_str = md_str.replace(image, converted_image_url)
        logger.info(
            f"[imarkdown] All images conversion for this md file have been completed, ready to save to file."
        )
        return md_str

    def _get_converted_image_url(self, original_image_url: str) -> str:
        """Get converted image url by adapter.

        Args:
            original_image_url: links to images that needs to be converted

        Returns:
            converted url
        """
        if self.is_local_images:
            original_image_url = get_file_name_from_relative_path(original_image_url)
            converted_image_path = (
                f"{self.image_local_storage_directory}/{original_image_url}"
            )
        else:
            converted_image_path = _download_img(
                self.image_local_storage_directory, original_image_url
            )

        if not converted_image_path:
            raise Exception("get a empty image path")

        logger.debug(f"[imarkdown] local image path: {converted_image_path}")
        image_name = os.path.basename(converted_image_path)
        if self.adapter.name == MdAdapterType.Local:
            return calculate_relative_path(
                converted_image_path, self.md_file_output_directory
            )

        # other adapter
        with open(converted_image_path, "rb") as f:
            file_data = f.read()
            self.adapter.upload(image_name, file_data)
            converted_url = self.adapter.get_replaced_url(image_name)
            logger.debug(f"[imarkdown] converted image url: {converted_url}")
        if not self.enable_save_images:
            os.remove(converted_image_path)
        if not converted_url:
            raise Exception(
                f"<{original_image_url}> try to get new url but return None."
            )
        return converted_url


class MdImageConverter:
    def __init__(
        self, adapter: Optional[BaseMdAdapter] = None, enable_log: bool = True
    ):
        self.adapter = _load_default_adapter()
        if adapter:
            self.adapter: BaseMdAdapter = adapter
            cfg.last_adapter_name = adapter.name

        self.converter: BaseMdImageConverter = BaseMdImageConverter(
            adapter=self.adapter
        )
        self.md_medium_manager: Optional[MdMediumManager] = MdMediumManager()
        if enable_log:
            logging.basicConfig(level=logging.INFO)

    def convert(
        self,
        mediums: Union[MdFile, MdFolder, List[Union[MdFile, MdFolder]]],
        output_directory: Optional[str] = None,
        enable_save_images: bool = True,
        **kwargs,
    ):
        def check_warning(medium: Union[MdFile, MdFolder]):
            if not output_directory and isinstance(medium, MdFolder):
                raise ValueError(
                    "Missing argument output_directory. If you pass a MdFolder, you must set output directory."
                )

        if not isinstance(mediums, List):
            mediums = [mediums]
        [check_warning(medium) for medium in mediums]

        self.md_medium_manager.init_md_files(mediums)
        self.md_medium_manager.update_config(
            output_directory=output_directory, enable_save_images=enable_save_images
        )
        for md_files in self.md_medium_manager.md_files:
            kwargs.update(**md_files.to_convert_params)
            self.converter.convert(**kwargs)
