from imarkdown import MdImageConverter, LocalFileAdapter, MdFile


def main():
    adapter = LocalFileAdapter()
    md_converter = MdImageConverter(adapter=adapter)
    md_file = MdFile(name="markdown.md")
    md_converter.convert(md_file)


if __name__ == "__main__":
    main()
