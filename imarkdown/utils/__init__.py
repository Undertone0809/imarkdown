import os


def polish_path(path: str, enable_prefix: bool = True, enable_suffix: bool = True):
    if enable_suffix and (path[-1] != "/" or path[-1] != "\\"):
        path += "/"
    if enable_prefix and (path[0] == "/" or path[0] == "\\"):
        path = path[1:]
    return path


def supplementary_file_path(file_path: str) -> str:
    """Get absolute file path.

    Args:
        file_path: absolute file path or relative file path

    Returns:
        return absolute file path
    """
    if os.path.isabs(file_path):
        return file_path
    else:
        current_dir = os.getcwd()

        if file_path.startswith("../"):
            while file_path.startswith("../"):
                current_dir = os.path.dirname(current_dir)
                file_path = file_path[3:]
        elif file_path.startswith("./"):
            file_path = file_path[2:]

        absolute_path = os.path.join(current_dir, file_path)
        return convert_backslashes(absolute_path)


def get_file_name_from_relative_path(relative_path: str) -> str:
    """Get file name, image name, markdown name from relative path."""
    if relative_path.startswith("../"):
        while relative_path.startswith("../"):
            relative_path = relative_path[3:]
    elif relative_path.startswith("./"):
        relative_path = relative_path[2:]
    return relative_path.split("/")[-1]


def convert_backslashes(path):
    """Convert all \\ to / of file path."""
    return path.replace("\\", "/")


def calculate_relative_path(image_path, md_directory):
    image_path = os.path.abspath(image_path)
    md_directory = os.path.abspath(md_directory)

    image_parts = image_path.split(os.path.sep)
    md_parts = md_directory.split(os.path.sep)
    if not os.path.isdir(md_directory):
        md_parts = md_parts[:-1]

    common_parts = os.path.commonpath([image_path, md_directory])
    common_index = len(common_parts.split(os.path.sep))

    relative_parts = []
    if common_index == len(md_parts):
        relative_parts.append(".")
    else:
        relative_parts.extend([".."] * (len(md_parts) - common_index))

    relative_parts.extend(image_parts[common_index:])

    relative_path = os.path.join(*relative_parts)
    return convert_backslashes(relative_path)


def exist_markdown_file(path: str) -> bool:
    """Determine whether there are markdown file in the folder directory.

    Args:
        path: folder absolute path

    Returns:
        True means existence, False otherwise.
    """
    if path.endswith(".md"):
        return True
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".md"):
                return True
    return False
