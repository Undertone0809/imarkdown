from unittest import TestCase
from main import *
from image_service import get_new_url, _download_img
import yaml_service
"""
This test is abandoned now.
"""


original_image_url = "https://cdn.nlark.com/yuque/0/2022/png/26910220/1670091709979-52f8c3c4-a00f-4668-a236-29ad2c09d0da.png#averageHue=%23272c34&clientId=ubb991e0d-3414-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=928&id=u4a7a8376&margin=%5Bobject%20Object%5D&name=image.png&originHeight=928&originWidth=1050&originalType=binary&ratio=1&rotation=0&showTitle=false&size=201083&status=done&style=none&taskId=u27493dc0-9d78-4c07-929c-cc946d41409&title=&width=1050"

class TestFunc(TestCase):

    def test_read_yaml_file_path(self):
        res = yaml_service.get_file_path()
        self.assertIsNotNone(res)

    def test_read_yaml_adapter_config(self):
        config = yaml_service.get_adapter_config()
        self.assertIsNotNone(config)

    def test_read_md(self):
        app = Application()
        res = app._read_md()
        self.assertIsNotNone(res)

    def test_download(self):
        file_dir = _download_img(original_image_url)
        self.assertIsNotNone(file_dir)

    def test_uplolad(self):
        aliyun_adapter = AliyunAdapter()
        file_dir = _download_img(original_image_url)
        aliyun_adapter.upload(key=file_dir, file=file_dir)
        aliyun_adapter.delete(key=file_dir)

    def test_replace_single_url(self):
        new_image_url = get_new_url(original_image_url, adapter=AliyunAdapter())
        self.assertIsNotNone(new_image_url)

    def test_replace_md_single_addr(self):
        app = Application()
        ori_data = app._read_md()
        pre_data = app._replace_url(ori_data, original_image_url)
        self.assertNotEqual(pre_data, ori_data)

    def test_write(self):
        app = Application()
        app._write_data("helloworld")
