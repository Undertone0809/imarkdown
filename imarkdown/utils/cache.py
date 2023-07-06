import tempfile

from cushy_storage import CushyDict

from imarkdown.utils.singleton import singleton


@singleton()
class Cache(CushyDict):
    def __init__(self):
        self.cache_path = f"{tempfile.gettempdir()}\imarkdown"
        super().__init__(self.cache_path)
