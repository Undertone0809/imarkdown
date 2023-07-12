import logging
import os
from typing import Any

from imarkdown.constant import MdAdapterType, _MdAdapterType
from imarkdown.utils.cache import Cache
from imarkdown.utils.singleton import Singleton

logger = logging.getLogger(__name__)


class IMarkdownConfig(metaclass=Singleton):
    def __init__(self):
        self.cache = Cache()
        self.root_path = os.path.abspath(os.path.dirname(__file__))

    @property
    def last_adapter_name(self) -> str:
        """Obtain the last executed MdAdapter, return LocalFileAdapter if obtain None.
        Custom MdAdapter currently can not use last adapter name.
        """
        adapter_name = self.cache.get("last_adapter", None)
        logger.debug(f"[imarkdown] get last adapter <{adapter_name}>")
        if not adapter_name or adapter_name not in _MdAdapterType.keys():
            return MdAdapterType.Local
        return _MdAdapterType[str(adapter_name)]

    @last_adapter_name.setter
    def last_adapter_name(self, value: str):
        # if value not in _MdAdapterType.keys():
        #     raise ValueError(f"<{value}> type adapter not exist.")
        self.cache["last_adapter"] = value

    def load_variable(self, key: str) -> Any:
        return self.cache.get(key, None)

    def store_variable(self, key: str, value: Any) -> Any:
        self.cache[key] = value
