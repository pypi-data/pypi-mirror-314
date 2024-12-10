from pathlib import Path
from typing import Optional


def parse_paths(ctx, param, value) -> list[Path]:
    """ Parse a list of click paths to a list of pathlib Path objects. """
    return None if value is None else list([Path(x) for x in value])


def parse_path(ctx, param, value) -> Path:
    """ Parse a click path to a pathlib Path object. """
    return None if value is None else Path(value)


def parse_suffix(ctx, param, value) -> Optional[str]:
    """ Parses a string to a valid suffix. """
    if value is None:
        return None
    return value if value.startswith('.') else f'.{value}'

def expand_paths(paths: list[Path], glob: str = '*') -> list[Path]:
    """ Expands a list of paths by unpacking directories. """
    path_list = []
    for path in paths:
        if path.is_dir():
            path_list.extend(sorted([fp for fp in path.glob(glob) if fp.is_file()]))
        else:
            path_list.append(path)
    return path_list


def expand_path(path: Path, glob: str = '*') -> list[Path]:
    """ Expand a path with a glob expression. """
    if not path.is_dir():
        return [path]
    return list(sorted([fp for fp in path.glob(glob) if fp.is_file()]))
