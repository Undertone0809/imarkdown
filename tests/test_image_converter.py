import logging
from unittest import TestCase

from imarkdown.adapter import AliyunAdapter, LocalFileAdapter
from imarkdown.constant import MdAdapterType
from imarkdown.converter import MdImageConverter, BaseMdImageConverter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestBaseImageConverter(TestCase):
    def test_base_usage(self):
        adapter = LocalFileAdapter(storage_path_prefix="images")
        converter = BaseMdImageConverter(adapter=adapter)
        converter.convert("test.md")

        # md_file = MdFile(name="test.md", image_path="images")
        # md_folder = MdFolder(name="mds", image_path="images")
        # adapter = AliyunAdapter(storage_path_prefix="images")
        # converter = MdImageConverter(adapter=adapter)
        # converter.convert(md_folder)


class TestImageConverter(TestCase):
    def test_last_adapter(self):
        md_adapter = AliyunAdapter()
        md_converter = MdImageConverter(adapter=md_adapter)
        self.assertEqual(md_converter.adapter.name, MdAdapterType.Aliyun.value)
        md_converter = MdImageConverter()
        self.assertEqual(md_converter.adapter.name, MdAdapterType.Aliyun.value)
