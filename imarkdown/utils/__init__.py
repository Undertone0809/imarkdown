def polish_path(path: str, enable_prefix: bool = True, enable_suffix: bool = True):
    if enable_suffix and (path[-1] != "/" or path[-1] != "\\"):
        path += "/"
    if enable_prefix and (path[0] == "/" or path[0] == "\\"):
        path = path[1:]
    return path
