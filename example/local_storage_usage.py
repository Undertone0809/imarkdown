from imarkdown import MdImageConverter
from imarkdown.adapter import LocalFileAdapter


def main():
    adapter = LocalFileAdapter()
    md_converter = MdImageConverter(adapter=adapter)
    md_converter.convert("markdown.md")


if __name__ == "__main__":
    main()
