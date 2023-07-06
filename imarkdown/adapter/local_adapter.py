from imarkdown.adapter.base import BaseMdAdapter


class LocalFileAdapter(BaseMdAdapter):
    name: str = "Local"

    def upload(self, key: str, file):
        """This adapter does not require upload."""
        pass

    def get_replaced_url(self, key):
        return f"./{self.path_prefix}/{key}"
