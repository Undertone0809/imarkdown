import logging
import os
import random
import re
import shutil
import time
import traceback
from typing import List, Optional, Any, Union, Dict

import requests
from pydantic import BaseModel, Field, root_validator, validator

from imarkdown.adapter import BaseMdAdapter, MdAdapterMapper
from imarkdown.config import IMarkdownConfig
from imarkdown.constant import MdAdapterType
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
        logger.info(f"write successfully to {new_file_path}")


def _download_img(image_local_storage_directory, image_url: str) -> Optional[str]:
    """download image from website and stored in image_local_storage_directory"""
    try:
        response = requests.get(image_url)
        now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
        image_local_storage_directory = polish_path(image_local_storage_directory)
        if not os.path.exists(image_local_storage_directory):
            os.mkdir(image_local_storage_directory)

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


class MdImageConverter(BaseModel):
    adapter: BaseMdAdapter = Field(default_factory=_load_default_adapter)
    is_local_images: bool = False
    enable_save_images: bool = True
    convert_mode: str = "file"
    newfile: str = ""

    @root_validator(pre=True)
    def variables_check(
        cls, values: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        logger.debug(f"[imarkdown] MdImageConverter initialization params: {values}")
        if "adapter" in values and values["adapter"]:
            cfg.last_adapter_name = values["adapter"].name
        return values

    def convert(self, file_paths: Union[str, List[str]]):
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        for file_path in file_paths:
            self._convert(file_path)

    def _convert(self, file_or_dir_path: str):
        """This method is used to judge convert a .md file or file path.
        If pass the file path, converter will convert all .md file in this file path.

        Args:
            file_or_dir_path: the .md file or file path
        """
        file_or_dir_path = supplementary_file_path(file_or_dir_path)
        if os.path.isdir(file_or_dir_path):
            self.convert_mode = "dir"
            self._convert_dir(file_or_dir_path)
        else:
            self.convert_mode = "file"
            self._convert_file(file_or_dir_path)

    def _convert_dir(self, dir_path: str):
        """input a directory path, this function will recursively convert all markdown files in sub folders."""
        self.newfile = "\\".join(dir_path.split("\\")[:-1])
        logger.info(f"[imarkdown] new file path: {self.newfile}")

        new_dir_path = dir_path + "_converted_" + str(hash(dir_path))[1:8]
        shutil.copytree(dir_path, new_dir_path)

        for path, _, file_list in os.walk(new_dir_path):
            for file_name in file_list:
                to_convert = os.path.join(path, file_name)
                self._convert_file(to_convert)

    def _convert_file(self, file_path: str):
        """
        input a markdown file path, this function will replace img address
        attention: markdown image must be a website url rather than a file path.
        """
        if not file_path.endswith(".md"):
            return
        self.newfile = "\\".join(file_path.split("\\")[:-1])
        logger.info(f"[imarkdown] new file path: {self.newfile}")

        original_data = _read_md(file_path)
        modified_data = self._find_img_and_replace(original_data)
        self._write_data(file_path, modified_data)
        logger.info("[imarkdown] task end")

    def _find_img_and_replace(self, md_str: str) -> str:
        """Input original markdown str and replace images address
        It can find `[]()` type image url and `<img/>` type image url

        Args:
            md_str: markdown original data

        Returns:
            Markdown data for the image url has been changed.
        """
        images = list(
            map(
                lambda item: item[1],
                re.findall(
                    r"(?:!\[(.*?)\]\((.*?)\))|<img.*?src=[\'\"](.*?)[\'\"].*?>", md_str
                ),
            )
        )

        for image in images:
            md_str = self._replace_image_url(md_str, image)
        return md_str

    def _replace_image_url(self, md_str: str, original_image_url: str) -> str:
        """replace single image address"""
        new_image_url = self.get_new_url(
            self.newfile, original_image_url, adapter=self.adapter
        )
        md_str = md_str.replace(original_image_url, new_image_url)
        return md_str

    def _write_data(self, file_path: str, md_str: str):
        new_file_url = (
            file_path.replace(".md", "_converted.md")
            if self.convert_mode == "file"
            else file_path
        )

        with open(f"{new_file_url}", "w", encoding="utf-8") as f:
            f.write(md_str)
            logger.info(f"write successfully to {new_file_url}")

    def get_new_url(
        self, file_path: str, original_image_url: str, adapter: BaseMdAdapter
    ) -> str:
        """Input old img url return converted url.

        Args:
            file_path: location of the markdown file or markdown file
            original_image_url: links to images that needs to be converted
            adapter: Markdown adapter

        Returns:
            converted url
        """
        file_path = f"{file_path}/{self.adapter.storage_path_prefix}"
        if self.adapter.storage_path_prefix == "":
            file_path = f"{file_path}/images"

        img_path = f"{file_path}/{original_image_url}"
        if not self.is_local_images:
            img_path = _download_img(file_path, original_image_url)
        new_url = None

        if not img_path:
            raise Exception("get a empty image path")

        image_name = os.path.basename(img_path)
        if self.adapter.name == MdAdapterType.Local:
            return self.adapter.get_replaced_url(image_name)
        else:
            with open(img_path, "rb") as f:
                file_data = f.read()
                adapter.upload(image_name, file_data)
                new_url = adapter.get_replaced_url(image_name)
                logger.info(f"url: {new_url}")

        if not self.enable_save_images:
            os.remove(img_path)
        if not new_url:
            raise Exception(f"<{new_url}> try to get new url but return None.")
        return new_url


class BaseMdImageConverter(BaseModel):
    adapter: BaseMdAdapter = Field(default_factory=_load_default_adapter)
    is_local_images: bool = False
    """You should set True if you want your local images upload to your picture server and you
    Markdown image url is originally local. Attention, enable_save_images can not be False if
    is_local_images is True."""
    enable_save_images: bool = True
    """It will delete images file after downloading the images if it is False."""
    newfile: str = ""
    image_local_storage_directory: str = "images"
    md_file_directory: str = ""

    @root_validator(pre=True)
    def variables_check(
        cls, values: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """update IMarkdownConfig last_adapter_name"""
        logger.debug(f"[imarkdown] MdImageConverter initialization params: {values}")
        if "adapter" in values and values["adapter"]:
            cfg.last_adapter_name = values["adapter"].name
        return values

    @validator("image_local_storage_directory", always=True)
    def update_image_storage_path(cls, path: str) -> str:
        result = supplementary_file_path(path)
        logger.debug(f"[imarkdown] image_local_storage_directory: {result}")
        return result

    def convert(
        self, md_file_path: str, image_local_storage_directory: Optional[str] = None
    ):
        """Convert Markdown image url and generate a new Markdown file.

        Args:
            md_file_path: Markdown file path
            image_local_storage_directory: Specified image storage path. You can pass an absolute or a
                relative path. Default image directory path is the Markdown directory named
                `markdown_dir/images`.

        Returns:
            A converted markdown file or a list of converted directory.
        """
        if not md_file_path.endswith(".md"):
            return
        if image_local_storage_directory:
            self.image_local_storage_directory = image_local_storage_directory

        self.md_file_directory = supplementary_file_path(md_file_path)
        self.md_file_directory = "/".join(self.md_file_directory.split("/")[:-1])
        logger.info(f"[imarkdown] md_file_directory: {self.md_file_directory}")

        original_data: str = _read_md(md_file_path)
        modified_data: str = self._find_img_and_replace(original_data)
        new_file_path: str = md_file_path.replace(".md", "_converted.md")
        _write_data(new_file_path, modified_data)
        logger.info("[imarkdown] task end")

    def _find_img_and_replace(self, md_str: str) -> str:
        """Input original markdown str and replace images address
        It can find `[]()` type image url and `<img/>` type image url

        Args:
            md_str: markdown original data

        Returns:
            Markdown data for the image url has been changed.
        """
        images = list(
            map(
                lambda item: item[1],
                re.findall(
                    r"(?:!\[(.*?)\]\((.*?)\))|<img.*?src=[\'\"](.*?)[\'\"].*?>", md_str
                ),
            )
        )

        for image in images:
            converted_image_url = self._get_converted_image_url(image)
            md_str = md_str.replace(image, converted_image_url)
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
            local_image_path = (
                f"{self.image_local_storage_directory}/{original_image_url}"
            )
        else:
            local_image_path = _download_img(
                self.image_local_storage_directory, original_image_url
            )

        if not local_image_path:
            raise Exception("get a empty image path")

        logger.debug(f"[imarkdown] local image path: {local_image_path}")
        image_name = os.path.basename(local_image_path)
        if self.adapter.name == MdAdapterType.Local:
            return calculate_relative_path(local_image_path, self.md_file_directory)

        # other adapter
        with open(local_image_path, "rb") as f:
            file_data = f.read()
            self.adapter.upload(image_name, file_data)
            converted_url = self.adapter.get_replaced_url(image_name)
            logger.debug(f"[imarkdown] converted image url: {converted_url}")
        if not self.enable_save_images:
            os.remove(local_image_path)
        if not converted_url:
            raise Exception(f"<{converted_url}> try to get new url but return None.")
        return converted_url
