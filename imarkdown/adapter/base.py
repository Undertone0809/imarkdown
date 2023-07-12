from abc import abstractmethod

from pydantic import BaseModel


class BaseMdAdapter(BaseModel):
    name: str
    """Adapter name"""
    storage_path_prefix: str = ""
    """Image path file prefix. Final image name is `{storage_path_prefix}/{key}`"""

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def upload(self, key: str, file):
        """Upload image to Image Server.

        Args:
            key: image name
            file: markdown string data
        """
        raise NotImplementedError("Your adapter should implement `upload` method")

    @abstractmethod
    def get_replaced_url(self, key):
        """get replaced url or image path"""
        raise NotImplementedError(
            "Your adapter should implement `get_replaced_url` method"
        )
