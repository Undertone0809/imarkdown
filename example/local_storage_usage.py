from imarkdown import LocalFileAdapter, MdFile, MdImageConverter


def main():
    adapter = LocalFileAdapter()
    md_converter = MdImageConverter(adapter=adapter)
    md_file = MdFile(name="test.md")
    # md_converter.convert(md_file, name_prefix="new_", name_suffix="_converted")
    md_converter.convert(md_file, new_name="A new markdown.md")


if __name__ == "__main__":
    main()
