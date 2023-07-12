import logging
from typing import Optional, Any, Dict

from pydantic import root_validator

from imarkdown.adapter.base import BaseMdAdapter
from imarkdown.config import IMarkdownConfig
from imarkdown.utils import polish_path

logger = logging.getLogger(__name__)
cfg: IMarkdownConfig = IMarkdownConfig()


class AliyunAdapter(BaseMdAdapter):
    name: str = "Aliyun"
    enable_https: bool = True
    """You can use https image url if you set true, otherwise http."""
    url_prefix: str = "https"
    """Used in request url prefix"""
    access_key_id: str
    """Necessary parameter when initialization."""
    access_key_secret: str
    """Necessary parameter when initialization."""
    bucket_name: str
    """Necessary parameter when initialization."""
    place: str
    """Necessary parameter when initialization."""
    endpoint: Optional[str] = None
    auth: Any
    bucket: Any

    @root_validator(pre=True)
    def validate_environment(cls, values: Optional[Dict]) -> Dict:
        env_config: Dict[str, Any] = cfg.load_variable(cls.__name__)
        if env_config:
            if not values:
                values = {}
            for env_key in env_config.keys():
                if env_key not in values:
                    values.update({env_key: env_config[env_key]})
        cfg.store_variable(cls.__name__, values)

        if not values:
            raise ValueError("Please initialize your AliyunAdapter with parameters.")
        logger.debug(f"[imarkdown aliyun adapter] params: {values}")

        try:
            import oss2

            values["endpoint"] = f'https://oss-cn-{values["place"]}.aliyuncs.com'
            values["auth"] = oss2.Auth(
                values["access_key_id"], values["access_key_secret"]
            )
            values["bucket"] = oss2.Bucket(
                values["auth"], values["endpoint"], values["bucket_name"]
            )
        except ImportError:
            raise ValueError(
                "Could not import oss2 python package. "
                "Please install it with `pip install oss2`."
            )
        return values

    def set_enable_https(cls, v: bool, values: Dict[str, Any]) -> bool:
        import oss2

        if v:
            cls.url_prefix = "https"
        else:
            cls.url_prefix = "http"

        values["endpoint"] = f'{cls.url_prefix}://oss-cn-{values["place"]}.aliyuncs.com'
        values["bucket"] = oss2.Bucket(
            values["auth"], values["endpoint"], values["bucket_name"]
        )
        return v

    def upload(self, key: str, file):
        path = polish_path(f"{self.storage_path_prefix}/{key}", enable_suffix=False)
        self.bucket.put_object(path, file)

    def get_replaced_url(self, key):
        return f"{self.url_prefix}://{self.bucket_name}.oss-cn-{self.place}.aliyuncs.com/{self.storage_path_prefix}/{key}"
