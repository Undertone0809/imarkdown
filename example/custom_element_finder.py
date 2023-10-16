import re
from typing import List

from imarkdown import BaseElementFinder, LocalFileAdapter, MdFile, MdImageConverter


class CustomElementFinder(BaseElementFinder):
    def find_all_elements(self, md_str, *args, **kwargs) -> List[str]:
        re_rule: str = r"(?:!\[(.*?)\]\((.*?)\))|<img.*?src=[\'\"](.*?)[\'\"].*?>"
        images = re.findall(re_rule, md_str)
        return list(map(lambda item: item[1], images))


def main():
    adapter = LocalFileAdapter()
    converter = MdImageConverter(adapter=adapter)
    element_finder = CustomElementFinder()

    md_file = MdFile(name="test.md")
    converter.convert(md_file, element_finder=element_finder)


if __name__ == "__main__":
    main()
