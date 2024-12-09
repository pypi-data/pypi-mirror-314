import pathlib
from typing import List, TypeVar


ShellCommand = TypeVar('ShellCommand', str, List[str])
PathLike = TypeVar('PathLike', str, pathlib.Path)
