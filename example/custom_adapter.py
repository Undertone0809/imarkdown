from imarkdown import MdImageConverter
from imarkdown.adapter import BaseMdAdapter


class CustomMdAdapter(BaseMdAdapter):
    pass


def main():
    adapter = CustomMdAdapter()
    md_converter = MdImageConverter(adapter=adapter)
    md_converter.convert("markdown.md")


if __name__ == "__main__":
    main()
