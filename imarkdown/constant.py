from enum import Enum
from typing import Dict


class MdAdapterType(str, Enum):
    Local = "Local"
    Aliyun = "Aliyun"


_MdAdapterType: Dict[str, str] = {
    MdAdapterType.Local: MdAdapterType.Local,
    MdAdapterType.Aliyun: MdAdapterType.Aliyun
}
