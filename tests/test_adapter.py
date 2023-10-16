import logging
from unittest import TestCase

from imarkdown.adapter import AliyunAdapter, LocalFileAdapter
from imarkdown.converter import MdFile, MdFolder, MdImageConverter

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

        md_file = MdFile(name="test.md")
        md_converter.convert(md_file)

    def test_convert_folder(self):
        adapter = LocalFileAdapter()
        md_converter = MdImageConverter(adapter=adapter)

        folder = MdFolder(name="mds")
        md_converter.convert(folder, output_directory="converted")


class TestAliyunAdapter(TestCase):
    def test_aliyun_adapter_init(self):
        AliyunAdapter()

    def test_convert_md_file(self):
        adapter = AliyunAdapter()
        md_converter = MdImageConverter(adapter=adapter)

        md_file = MdFile(name="test.md")
        md_converter.convert(md_file)

    def test_convert_with_storage_prefix(self):
        adapter = AliyunAdapter(storage_path_prefix="imarkdown")
        md_converter = MdImageConverter(adapter=adapter)

        md_file = MdFile(name="test.md")
        md_converter.convert(md_file)

    def test_convert_file(self):
        adapter = AliyunAdapter()
        md_converter = MdImageConverter(adapter=adapter)

        md_folder = MdFolder(name="mds")
        md_converter.convert(md_folder, output_directory="converted")

    def test_local_to_remote(self):
        adapter = LocalFileAdapter()
        md_converter = MdImageConverter(adapter=adapter)
        md_folder = MdFolder(name="mds")
        md_converter.convert(md_folder, output_directory="local_mds")

        adapter = AliyunAdapter()
        md_converter = MdImageConverter(adapter=adapter)
        md_folder = MdFolder(
            name="local_mds", image_type="local", image_directory="local_mds/images"
        )
        md_converter.convert(md_folder, output_directory="aliyun_converted")
