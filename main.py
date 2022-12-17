import re
import logging

from adapter import AliyunApater, Adapter
import image_service
import yaml_service

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class Application:
    """
    This application Helps you convert the image address
    in markdown to the address of the specified graph bed.

    Attention: 
        1.All your markdown images must be a website url ranther than a file path.
        2.Now only support aliyun-oss. Welcome PRs to add more supports.
    """

    def __init__(self, file_path=None, adapter: Adapter = AliyunApater()):
        """
        cofig markdown file path and adapter
        
        :file_path: original markdown file path
        :adapter: use adapter to upload to your graph bed. You can custom your third-party adapter
        """
        self.file_path = yaml_service.get_file_path() if not file_path else file_path
        self.adapter = adapter
        self.save_img_to_local = yaml_service.get_adapter_config

    def run(self):
        """
        input a markdown file, this function will replace img address
        attention: markdown image must be a website url ranther than a file path.
        """
        ori_data = self._read_md()
        pre_data = self._find_img_and_replace(ori_data)
        self._write_data(pre_data)
        logger.info("task end")

    def _write_data(self, data):
        new_file_url = self.file_path.replace(".md","_converted.md")
        with open(f"{new_file_url}", "w", encoding="utf-8") as f:
            f.write(data)
            logger.info("write successfully")

    def _read_md(self) -> str:
        """ read markdown file and return markdown data """
        with open(self.file_path, "r", encoding="utf-8") as f:
            res = f.read()
            logger.info("read file successfully")
        return res

    def _find_img_and_replace(self, data) -> str:
        """ input original markdown data and replace images address """
        images = list(map(lambda item: item[1],
            re.findall(r'(?:!\[(.*?)\]\((.*?)\))|<img.*?src=[\'\"](.*?)[\'\"].*?>', data)))
        
        for image in images:
            data = self._replace_url(data, image)
        return data

    def _replace_url(self, data: str, origin_image_url) -> str:
        """ replace single image address """
        new_image_url = image_service.get_new_url(origin_image_url, adapter=self.adapter, save_img=self.save_img_to_local)
        data = data.replace(origin_image_url, new_image_url)
        return data


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
