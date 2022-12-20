import os
import time
import requests
import logging
import random
from adapter import *

logger = logging.getLogger(__name__)


""" input old img url return new url of your graph bed """
def get_new_url(origin_image_url, adapter: Adapter, save_img=False) -> str:
    file_path = _download_img(origin_image_url)
    with open(file_path, "rb") as f:
        key = "typora_img/" + f.name.split(os.getcwd() + "\images\\")[-1]
        file_data = f.read()
        adapter.upload(key, file_data)
        new_url = adapter.get_url(key)
        logger.info(f"url: {new_url}")
    if not save_img:
        os.remove(file_path)
    return new_url

def _download_img(url: str):
    """ download image from website and stored in file """
    try:
        res = requests.get(url)
        nowtime = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        img_dir = os.getcwd() + '\images\\'
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
