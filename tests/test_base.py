from unittest import TestCase
from main import *
from image_service import get_new_url, _download_img
import yaml_service

class TestBase(TestCase):
    """
    This test mainly test 4 points:
    1. file path, remote images url convert to local images url
    2. file path, remote images url convert to remote images url
    2. folder path, remote images url convert to local images url
    2. folder path, remote images url convert to remote images url
    """

    def test_file_and_local(self):
        pass

    def test_file_and_remote(self):
        pass

    def test_folder_and_local(self):
        pass

    def test_folder_and_remote(self):
        pass
