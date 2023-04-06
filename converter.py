import os
import re
import logging
import shutil
from typing import Optional
from adapter import Adapter
import image_service

logger = logging.getLogger(__name__)


class Converter:

    def __init__(self, adapter: Optional[Adapter] = None) -> None:
        """
        When you initialize a converter, you need choose an adapter.If you choose
        Aliyun adapter, it means that the image link will be converted to Aliyun link.


        Args:
            adapter (Adapter, optional): Defaults is None. It means that your image link
            will be converted to local link.
        """
        self.adapter = adapter
        self._convert_mode = 'file'
        self._converted_path = ''
        self.newfile = ""

    def convert(self, file_or_dir_path: str):
        self._converted_path = file_or_dir_path

        if os.path.isdir(file_or_dir_path):
            self._convert_mode = 'dir'
            self._convert_dir(file_or_dir_path)
        else:
            self._convert_mode = 'file'
            self._convert_file(file_or_dir_path)

    def _convert_file(self, file_path: str):
        """
        input a markdown file path, this function will replace img address
        attention: markdown image must be a website url rather than a file path.
        """
        self.newfile = "\\".join(file_path.split("\\")[:-1])
        print("newfile1: ", self.newfile)

        ori_data = self._read_md(file_path)
        pre_data = self._find_img_and_replace(ori_data)
        self._write_data(file_path, pre_data)
        logger.info("task end")

    def _convert_dir(self, dir_path: str):

        """
        input a directory path, this function will recursively convert all markdown files in sub folders.
        """
        self.newfile = "\\".join(dir_path.split("\\")[:-1])
        print("newfile2: ", self.newfile)

        new_dir_path = dir_path + "_converted_" + str(hash(self))[0:8]
        shutil.copytree(dir_path, new_dir_path)

        for path, _, file_list in os.walk(new_dir_path):
            for file_name in file_list:
                to_convert = os.path.join(path, file_name)
                self._convert_file(to_convert)

    def _read_md(self, file_path: str) -> str:
        """ read markdown file and return markdown data """
        with open(file_path, "r", encoding="utf-8") as f:
            res = f.read()
            logger.info("read file successfully")
        return res

    def _find_img_and_replace(self, md_str: str) -> str:
        """ input original markdown str and replace images address """
        # todo: when _convert_mode is 'dir' mode, images path are still replaced as relative like `.\images\20230218_1733048462.png` which is invalid
        images = list(map(lambda item: item[1], re.findall(
            r'(?:!\[(.*?)\]\((.*?)\))|<img.*?src=[\'\"](.*?)[\'\"].*?>', md_str)))

        for image in images:
            md_str = self._replace_url(md_str, image)
        return md_str

    def _replace_url(self, md_str: str, origin_image_url: str) -> str:
        """ replace single image address """
        new_image_url = image_service.get_new_url(self.newfile,
                                                  origin_image_url, adapter=self.adapter)
        md_str = md_str.replace(origin_image_url, new_image_url)
        return md_str

    def _write_data(self, file_path: str, md_str: str):
        new_file_url = file_path.replace(".md", "_converted.md") if self._convert_mode == 'file' else file_path

        with open(f"{new_file_url}", "w", encoding="utf-8") as f:
            f.write(md_str)
            logger.info(f"write successfully to {new_file_url}")
