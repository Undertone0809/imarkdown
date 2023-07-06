from imarkdown import MdConverter
from imarkdown.adapter import LocalFileAdapter


def main():
    adapter = LocalFileAdapter()
    md_converter = MdConverter(adapter=adapter)
    md_converter.convert("markdown.md")


if __name__ == "__main__":
    main()
