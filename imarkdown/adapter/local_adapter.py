from pydantic import validator

from imarkdown.adapter.base import BaseMdAdapter


class LocalFileAdapter(BaseMdAdapter):
    name: str = "Local"

    @validator("storage_path_prefix")
    def show_warnings(cls, v: str):
        assert v == "", (
            "LocalFileAdapter can not use storage_path_prefix. You should set image_directory in MdFile or MdFolder "
            "if you want to set your local image directory."
        )

    def upload(self, key: str, file):
        """This adapter does not require upload."""
        pass

    def get_replaced_url(self, key):
        path = f"./{self.storage_path_prefix}/{key}"
        if self.storage_path_prefix == "":
            path = f"./images/{key}"
        return path
