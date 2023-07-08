import logging
from unittest import TestCase

from imarkdown.adapter import AliyunAdapter, LocalFileAdapter
from imarkdown.converter import MdImageConverter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
aliyun_config = {
    "access_key_id": "key_id",
    "access_key_secret": "key_secret",
    "bucket_name": "bucket_name",
    "place": "bucket_place",
    "storage_path_prefix": "prefix",
}


class TestLocalFileAdapter(TestCase):
    def test_local_adapter_init(self):
        LocalFileAdapter()

    def test_convert_md_file(self):
        adapter = LocalFileAdapter()
        md_converter = MdImageConverter(adapter=adapter)
        md_converter.convert("test.md")

    def test_convert_file(self):
        adapter = LocalFileAdapter(storage_path_prefix="img")
        md_converter = MdImageConverter(adapter=adapter)
        md_converter.convert("mds")


class TestAliyunAdapter(TestCase):
    def test_aliyun_adapter_init(self):
        AliyunAdapter()

    def test_convert_md_file(self):
        adapter = AliyunAdapter()
        md_converter = MdImageConverter(adapter=adapter)
        md_converter.convert("test.md")

    def test_convert_file(self):
        adapter = AliyunAdapter()
        md_converter = MdImageConverter(adapter=adapter)
        md_converter.convert("mds")
