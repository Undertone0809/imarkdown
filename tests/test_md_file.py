import logging
from unittest import TestCase

from pydantic.error_wrappers import ValidationError

from imarkdown.schema import MdFile, MdFolder, MdMediumManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestMdFile(TestCase):
    def test_md_file_initialization(self):
        md_file = MdFile(name="test.md", image_type="remote")
        logger.info(md_file.__dict__)

        md_file = MdFile(name="test.md", image_type="local", image_path="images")
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

    def test_md_folder_initialization(self):
        md_folder = MdFolder(name="mds")
        for node in md_folder.sub_nodes:
            logger.info(node.absolute_path_name)

        try:
            MdFolder(name="mds", image_type="local")
            assert 1 == 0
        except ValidationError as e:
            pass

        md_folder = MdFolder(
            name="mds/sub_mds", image_type="local", image_path="mds\\images"
        )
        logger.info(md_folder.__dict__)


class TestMdMediumManager(TestCase):
    def test_get_all_files(self):
        md_folder = MdFolder(name="mds")
        manager = MdMediumManager(mediums=[md_folder])

        self.assertEqual(len(manager.md_files), 7)
        for md_file in manager.md_files:
            logger.info(md_file.name)
