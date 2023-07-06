from abc import abstractmethod

from pydantic import BaseModel


class BaseMdAdapter(BaseModel):
    name: str
    """Adapter name"""
    path_prefix: str = ""
    """Image path file prefix of in bucket. Final key is `{path_prefix}/{key}`"""

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def upload(self, key: str, file):
        """upload image to Image Server"""
        raise NotImplementedError("Your adapter should implement `upload` method")

    @abstractmethod
    def get_replaced_url(self, key):
        """get replaced url or image path"""
        raise NotImplementedError(
            "Your adapter should implement `get_replaced_url` method"
        )
