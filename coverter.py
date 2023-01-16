import re
import logging
from typing import Optional
from adapter import Adapter
import image_service

logger = logging.getLogger(__name__)


class Coverter:

    def __init__(self, adapter: Optional[Adapter] = None) -> None:
        """
        When you initialize a Coverter, you need choose a adapter.If you choose 
        Aliyun adapter, it means that the image link will be converted to Aliyun link.


        Args:
            adapter (Adapter, optional): Defaults is None. It means that your image link
            will be coverted to local link.
        """
        self.adapter = adapter

    def covert(self, file_path: str):
        """
        input a markdown file path, this function will replace img address
        attention: markdown image must be a website url ranther than a file path.
        """
        ori_data = self._read_md(file_path)
        pre_data = self._find_img_and_replace(ori_data)
        self._write_data(file_path, pre_data)
        logger.info("task end")

    def _read_md(self, file_path: str) -> str:
        """ read markdown file and return markdown data """
        with open(file_path, "r", encoding="utf-8") as f:
            res = f.read()
            logger.info("read file successfully")
        return res

    def _find_img_and_replace(self, md_str: str) -> str:
        """ input original markdown str and replace images address """
        images = list(map(lambda item: item[1], re.findall(
            r'(?:!\[(.*?)\]\((.*?)\))|<img.*?src=[\'\"](.*?)[\'\"].*?>', md_str)))

        for image in images:
            md_str = self._replace_url(md_str, image)
        return md_str

    def _replace_url(self, md_str: str, origin_image_url: str) -> str:
        """ replace single image address """
        new_image_url = image_service.get_new_url(
            origin_image_url, adapter=self.adapter)
        md_str = md_str.replace(origin_image_url, new_image_url)
        return md_str

    def _write_data(self, file_path: str, md_str: str):
        new_file_url = file_path.replace(".md", "_converted.md")
        with open(f"{new_file_url}", "w", encoding="utf-8") as f:
            f.write(md_str)
            logger.info("write successfully")
