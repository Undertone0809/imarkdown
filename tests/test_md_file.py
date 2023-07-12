import logging
from typing import List
from unittest import TestCase

from pydantic.error_wrappers import ValidationError

from imarkdown.schema import MdFile, MdFolder, MdMediumManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestMdFile(TestCase):
    def test_md_file_initialization(self):
        md_file = MdFile(name="test.md", image_type="remote")
        logger.info(md_file.__dict__)

        md_file = MdFile(name="test.md", image_type="local", image_directory="images")
        logger.info(md_file.__dict__)

        try:
            MdFile(name="not_exist.md")
            assert 1 == 0
        except ValidationError as e:
            pass

        try:
            MdFile(name="test.md", image_type="local")
            assert 1 == 0
        except ValidationError as e:
            pass

    def test_md_file_to_convert_params(self):
        md_file = MdFile(name="test.md", image_type="remote")
        params = md_file.to_convert_params
        logger.info(params)

    def test_md_folder_initialization(self):
        md_folder = MdFolder(name="mds")
        for node in md_folder.sub_nodes:
            logger.info(f"{type(node)} {node.absolute_path_name}")

        try:
            MdFolder(name="mds", image_type="local")
            assert 1 == 0
        except ValidationError as e:
            pass

        md_folder = MdFolder(
            name="mds/sub_mds", image_type="local", image_directory="mds\\images"
        )
        logger.info(md_folder.__dict__)


class TestMdMediumManager(TestCase):
    def test_get_all_files(self):
        manager = MdMediumManager()
        md_folder = MdFolder(name="single_mds", output_directory="converted")
        md_files: List[MdFile] = manager.init_md_files([md_folder])
        for md_file in md_files:
            print(md_file.to_convert_params)

    def test_update_config(self):
        manager = MdMediumManager()
        md_folder = MdFolder(name="mds")
        manager.init_md_files([md_folder])
        manager.update_config(output_directory="converted")
        for md_file in manager.md_files:
            print(md_file.to_convert_params)
