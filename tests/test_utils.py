import logging
from unittest import TestCase

from imarkdown.converter import supplementary_file_path, calculate_relative_path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestUtils(TestCase):
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

    def test_calculate_relative_path(self):
        image_storage_directory = "E:/project_hub/md-img-convert/tests/images/pic.png"
        md_storage_directory = "E:/project_hub/md-img-convert/tests"
        result = calculate_relative_path(
            image_storage_directory, md_storage_directory
        )
        logger.info(result)

        image_storage_directory = "E:/project_hub/md-img-convert/tests/hh/aaa/pic.png"
        md_storage_directory = "E:/project_hub/md-img-convert/tests/"
        result = calculate_relative_path(
            image_storage_directory, md_storage_directory
        )
        logger.info(result)

        image_storage_directory = "E:/project_hub/md-img-convert/tests/images/pic.png"
        md_storage_directory = "E:/project_hub/md-img-convert/where/sub/sub"
        result = calculate_relative_path(
            image_storage_directory, md_storage_directory
        )
        logger.info(result)