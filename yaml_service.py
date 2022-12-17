import os
import yaml


def yaml_dict() -> dict:
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_file_path() -> str:
    path = yaml_dict()["file_path"]
    return f"{os.getcwd()}\{path}"


def get_save_image() -> str:
    return yaml_dict()["save_image"]


def get_adapter() -> str:
    return yaml_dict()["adapter"]


def get_adapter_config() -> dict:
    """ It need to append more chooses if add more graph bed """
    if yaml_dict()["adapter"] == "Aliyun":
        return yaml_dict()["Aliyun"]
