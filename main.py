import logging

from adapter import *
from converter import Converter

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class Application:
    """
    This application Helps you convert the image address
    in markdown to the address of the specified graph bed.

    Attention:
        1.All your markdown images must be a website url ranther than a file path.
        2.Now only support aliyun-oss and local. Welcome PRs to add more supports.
    """

    def __init__(self) -> None:
        """
        initialize application and read coverter strategy from config.yaml
        """
        yaml_service.yaml_check()
        self.file_path = yaml_service.get_file_path()
        self.adapter_type = yaml_service.get_adapter_type()
        self.adapter = None

        if self.adapter_type == 'Aliyun':
            self.adapter = AliyunAdapter()
        elif self.adapter_type == 'Local':
            self.adapter = LocalAdapter()

    def run(self):
        converter = Converter(self.adapter)
        converter.convert(self.file_path)


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
