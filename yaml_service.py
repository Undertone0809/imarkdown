import os
import yaml
import adapter

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


def yaml_check():
    """ check some yaml arguments. """
    # check file_path
    with open(f"{get_file_path()}", 'r') as f:
        pass
    # check adapter
    if get_adapter_type() not in adapter.ADAPTER_ENUM:
        raise ValueError("Please check your yaml adapter config")


def yaml_dict() -> dict:
    with open(f"{ROOT_PATH}\config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_file_path() -> str:
    """ get file_path"""
    path = yaml_dict()["file_path"]
    return f"{ROOT_PATH}\{path}"


def get_is_save_img() -> bool:
    """ get whether save_image """
    if get_adapter_type() is 'Local':
        whether_to_save_img = False
    else:
        whether_to_save_img = yaml_dict()["save_image"]
    return whether_to_save_img


def get_adapter_type() -> str:
    """ get adapter """
    return yaml_dict()["adapter"]


def get_adapter_config() -> dict:
    """ It need to append more chooses if add more graph bed """
    if get_adapter_type() in adapter.ADAPTER_ENUM and get_adapter_type() is not "local":
        return yaml_dict()[get_adapter_type()]
