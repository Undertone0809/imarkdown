from typing import Dict

from imarkdown.adapter.aliyun_adapter import AliyunAdapter
from imarkdown.adapter.base import BaseMdAdapter
from imarkdown.adapter.local_adapter import LocalFileAdapter
from imarkdown.constant import MdAdapterType

__all__ = ["BaseMdAdapter", "AliyunAdapter", "LocalFileAdapter", "MdAdapterMapper"]

MdAdapterMapper: Dict[str, type(BaseMdAdapter)] = {
    MdAdapterType.Local: LocalFileAdapter,
    MdAdapterType.Aliyun: AliyunAdapter,
}
