from imarkdown import MdConverter
from imarkdown.adapter import AliyunAdapter


def main():
    aliyun_config = {
        "access_key_id": "key_id",
        "access_key_secret": "key_secret",
        "bucket_name": "bucket_name",
        "place": "bucket_place",
        "path_prefix": "prefix",
    }
    adapter = AliyunAdapter(**aliyun_config)
    md_converter = MdConverter(adapter=adapter)
    md_converter.convert("markdown.md")


if __name__ == "__main__":
    main()
