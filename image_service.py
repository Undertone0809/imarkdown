import os
import time
import requests
import logging
import random
from adapter import *

logger = logging.getLogger(__name__)
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


def get_new_url(origin_image_url, adapter: Adapter) -> str:
    """ input old img url return new url of your graph bed """
    img_path = _download_img(origin_image_url)

    if yaml_service.get_adapter_type() == 'Local':
        return f".\images\{os.path.basename(img_path)}"
    else:
        with open(img_path, "rb") as f:
            # custom your key here
            key = "images/" + f.name.split(ROOT_PATH + "\images\\")[-1]
            file_data = f.read()
            adapter.upload(key, file_data)
            new_url = adapter.get_url(key)
            logger.info(f"url: {new_url}")

    if not yaml_service.get_is_save_img():
        os.remove(img_path)
    return new_url


def _download_img(url: str):
    """ download image from website and stored in file """
    try:
        res = requests.get(url)
        nowtime = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        img_dir = ROOT_PATH + '\images\\'
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)

        file_dir = f"{img_dir}{nowtime}{random.randint(1000, 10000)}.png"
        with open(file_dir, "wb") as f:
            f.write(res.content)
        logger.info(f"filename: {file_dir} has stored successfully")
        return file_dir
    except Exception as e:
        logger.warning(f"download_img failed, reason: {e}")
        return None
