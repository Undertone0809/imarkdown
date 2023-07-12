import logging
from unittest import TestCase

from imarkdown.adapter import AliyunAdapter, LocalFileAdapter
from imarkdown.constant import MdAdapterType
from imarkdown.converter import MdImageConverter, BaseMdImageConverter
from imarkdown.schema import MdFile, MdFolder

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestBaseImageConverter(TestCase):
    def test_base_usage(self):
        # adapter = LocalFileAdapter()
        adapter = AliyunAdapter()
        converter = BaseMdImageConverter(adapter=adapter)
        converter.convert(
            "test.md",
            image_local_storage_directory="mds/images",
            output_md_directory="mds",
            name_prefix="prefix_",
            name_suffix="_converted",
        )


class TestImageConverter(TestCase):
    def test_use_md_file(self):
        adapter = LocalFileAdapter()
        converter = MdImageConverter(adapter=adapter)

        md_file = MdFile(name="test.md")
        converter.convert(md_file)

    def test_use_md_file_with_custom_name(self):
        adapter = LocalFileAdapter()
        converter = MdImageConverter(adapter=adapter)

        md_file = MdFile(name="test.md")
        converter.convert(md_file, name_prefix="prefix", name_suffix="_new")

    def test_use_md_file_with_custom_image_path(self):
        adapter = LocalFileAdapter()
        converter = MdImageConverter(adapter=adapter)

        md_file = MdFile(name="test.md", image_directory="custom_images")
        converter.convert(md_file)

    def test_use_md_folder(self):
        adapter = LocalFileAdapter()
        converter = MdImageConverter(adapter=adapter)

        md_folder = MdFolder(name="mds")
        converter.convert(md_folder, output_directory="converted")
        for md_file in converter.md_medium_manager.md_files:
            print(md_file.to_convert_params)

    def test_last_adapter(self):
        md_adapter = AliyunAdapter()
        md_converter = MdImageConverter(adapter=md_adapter)
        self.assertEqual(md_converter.adapter.name, MdAdapterType.Aliyun.value)
        md_converter = MdImageConverter()
        self.assertEqual(md_converter.adapter.name, MdAdapterType.Aliyun.value)
