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
    if relative_path.startswith("../"):
        while relative_path.startswith("../"):
            relative_path = relative_path[3:]
    elif relative_path.startswith("./"):
        relative_path = relative_path[2:]
    return relative_path


def convert_backslashes(path):
    """Convert all \\ to / of file path."""
    return path.replace("\\", "/")


def calculate_relative_path(image_path, md_directory):
    image_path = os.path.abspath(image_path)
    md_directory = os.path.abspath(md_directory)
    image_parts = image_path.split(os.path.sep)
    md_parts = md_directory.split(os.path.sep)

    common_index = 0
    for i in range(min(len(image_parts), len(md_parts))):
        if image_parts[i] != md_parts[i]:
            break
        common_index += 1

    relative_parts = []
    if common_index == len(md_parts):
        relative_parts.append(".")
    else:
        relative_parts.extend([".."] * (len(md_parts) - common_index - 1))

    relative_parts.extend(image_parts[common_index:])
    relative_path = os.path.join(*relative_parts)
    return convert_backslashes(relative_path)
