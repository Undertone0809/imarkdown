import logging
import os
import random
import re
import shutil
import time
from typing import List, Optional, Any, Union, Dict

import requests
from pydantic import BaseModel, Field, root_validator

from imarkdown.adapter import BaseMdAdapter, MdAdapterMapper
from imarkdown.config import IMarkdownConfig
from imarkdown.constant import MdAdapterType
from imarkdown.utils import polish_path

logger = logging.getLogger(__name__)
cfg = IMarkdownConfig()


def _download_img(file_path, url: str) -> Optional[str]:
    """download image from website and stored in file_path"""
    try:
        response = requests.get(url)
        now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
        file_path = polish_path(file_path)
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        images_path = f"{file_path}{now_time}{random.randint(1000, 10000)}.png"
        with open(images_path, "wb") as f:
            f.write(response.content)
        logger.info(f"[imarkdown] <{images_path}> has stored in local successfully")
        return images_path
    except Exception as e:
        logger.error(f"download_img failed, reason: {e}")
        return None


def supplementary_file_path(file_path: str) -> str:
    """get absolute file path

    Args:
        file_path: absolute file path or relative file path

    Returns:
        return absolute file path
    """
    if os.path.isabs(file_path):
        return file_path
    else:
        current_dir = os.getcwd()

        if file_path.startswith("../"):
            while file_path.startswith("../"):
                current_dir = os.path.dirname(current_dir)
                file_path = file_path[3:]
        elif file_path.startswith("./"):
            file_path = file_path[2:]

        absolute_path = os.path.join(current_dir, file_path)
        return absolute_path


def _load_default_adapter() -> BaseMdAdapter:
    logger.debug(f"[imarkdown] local default adapter <{cfg.last_adapter_name}>")
    return MdAdapterMapper[cfg.last_adapter_name]()


class MdConverter(BaseModel):
    adapter: BaseMdAdapter = Field(default_factory=_load_default_adapter)
    enable_save_images: bool = True
    convert_mode: str = "file"
    newfile: str = ""

    @root_validator(pre=True)
    def data_check(cls, values: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        logger.debug(f"[imarkdown] MdConverter initialization {values}")
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
        print(new_dir_path)
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
        self.newfile = "\\".join(file_path.split("\\")[:-1])
        logger.info(f"[imarkdown] new file path: {self.newfile}")

        original_data = self._read_md(file_path)
        modified_data = self._find_img_and_replace(original_data)
        self._write_data(file_path, modified_data)
        logger.info("[imarkdown] task end")

    def _read_md(self, file_path: str) -> str:
        """read markdown file and return markdown data"""
        with open(file_path, "r", encoding="utf-8") as f:
            res = f.read()
            logger.info(f"[imarkdown] read file <{file_path}> successfully")
        return res

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
        file_path = f"{file_path}/{self.adapter.path_prefix}"
        if self.adapter.path_prefix == "":
            file_path = f"{file_path}/images"
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
