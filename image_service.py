import os
import time
import requests
import logging
import random
from adapter import *
from typing import Optional

logger = logging.getLogger(__name__)
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


def get_new_url(file_path: str, origin_image_url: str, adapter: Adapter) -> str:
    """
    input old img url return converted url.

    :param file_path: Location of the markdown file or markdown file
    :param origin_image_url: links to images that needs to be converted
    :param adapter: graph adapter
    :return: converted url
    """
    img_path = _download_img(file_path, origin_image_url)
    new_url = None

    if not img_path:
        raise Exception("get a empty image path")

    if yaml_service.get_adapter_type() == 'Local':
        return f".\\images\\{os.path.basename(img_path)}"
    else:
        with open(img_path, "rb") as f:
            # custom your key here
            key = "images\\" + f.name.split(file_path + "\\images\\")[-1]
            file_data = f.read()
            adapter.upload(key, file_data)
            new_url = adapter.get_url(key)
            logger.info(f"url: {new_url}")

    if not yaml_service.get_is_save_img():
        os.remove(img_path)
    if not new_url:
        raise Exception("get a empty image path ")
    return new_url


def _download_img(file_path, url: str) -> Optional[str]:
    """ download image from website and stored in file_path """
    try:
        res = requests.get(url)
        nowtime = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        img_dir = f"{file_path}\\images\\"
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)

        img_dir = f"{img_dir}{nowtime}{random.randint(1000, 10000)}.png"
        with open(img_dir, "wb") as f:
            f.write(res.content)
        logger.info(f"filename: {img_dir} has stored successfully")
        return img_dir
    except Exception as e:
        logger.warning(f"download_img failed, reason: {e}")
        return None
