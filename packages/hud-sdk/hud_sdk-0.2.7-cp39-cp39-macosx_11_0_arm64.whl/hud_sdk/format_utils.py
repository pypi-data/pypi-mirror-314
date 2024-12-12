def format_path(path: str) -> str:
    if path.endswith("/"):
        path = path[:-1]
    if not path.startswith("/"):
        path = "/" + path
    path = path.split("?")[0]
    return path
