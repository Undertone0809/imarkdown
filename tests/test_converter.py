import logging
from unittest import TestCase

from imarkdown.adapter import (
    AliyunAdapter,
    MdAdapterType,
)
from imarkdown.converter import MdConverter, supplementary_file_path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestConverter(TestCase):
    def test_last_adapter(self):
        md_adapter = AliyunAdapter()
        md_converter = MdConverter(adapter=md_adapter)
        self.assertEqual(md_converter.adapter.name, MdAdapterType.Aliyun.value)
        md_converter = MdConverter()
        self.assertEqual(md_converter.adapter.name, MdAdapterType.Aliyun.value)

    def test_supplementary_file_path(self):
        a = supplementary_file_path("markdown.md")
        b = supplementary_file_path("./markdown.md")
        logger.info(f"<{a}> <{b}>")
        self.assertEqual(a, b)
        c = supplementary_file_path("../markdown.md")
        logger.info(c)
        d = supplementary_file_path("../../markdown.md")
        logger.info(d)
        e = supplementary_file_path("E:\\markdown.md")
        logger.info(e)
        f = supplementary_file_path("E:\\file")
        logger.info(f)
