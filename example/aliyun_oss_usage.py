from imarkdown import AliyunAdapter, MdFile, MdImageConverter


def main():
    aliyun_config = {
        "access_key_id": "key_id",
        "access_key_secret": "key_secret",
        "bucket_name": "bucket_name",
        "place": "bucket_place",
        "storage_path_prefix": "prefix",
    }
    adapter = AliyunAdapter(**aliyun_config)
    md_converter = MdImageConverter(adapter=adapter)
    md_file = MdFile(name="markdown.md")
    md_converter.convert(md_file)


if __name__ == "__main__":
    main()
