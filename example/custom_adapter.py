from imarkdown import MdImageConverter, BaseMdAdapter, MdFile


class CustomMdAdapter(BaseMdAdapter):
    name = ""

    def upload(self, key: str, file):
        ...

    def get_replaced_url(self, key):
        ...


def main():
    adapter = CustomMdAdapter()
    md_converter = MdImageConverter(adapter=adapter)
    md_file = MdFile(name="markdown.md")
    md_converter.convert(md_file)


if __name__ == "__main__":
    main()
