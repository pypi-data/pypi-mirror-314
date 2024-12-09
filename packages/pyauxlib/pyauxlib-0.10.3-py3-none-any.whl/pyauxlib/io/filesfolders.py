"""Functions related to files and folders."""

import logging
import re
import time
from collections.abc import Generator
from fnmatch import fnmatch
from pathlib import Path
from typing import IO, Any, NamedTuple

from pyauxlib.io.utils import clean_file_extension

logger = logging.getLogger(__name__)


class FileRelPath(NamedTuple):
    """Named tuple with the path of a file and the relative path to a parent path.

    Attributes
    ----------
    file : Path
        The absolute path of the file.
    rel_path : Path
        The relative path of the file with respect to a parent directory.
    """

    file: Path
    rel_path: Path


def iterate_files(
    pathobject: Path, file_extensions: list[str] | None = None
) -> Generator[FileRelPath, None, None]:
    """Yield files from a given path with optional file extension filtering.

    This function takes a Path object and yields files from it. If the Path is a file,
    it yields the file itself. If the Path is a directory, it yields all files in the
    directory with a given extension, without recursing into subdirectories.

    Parameters
    ----------
    pathobject : Path
        The Path object to search for files.
    file_extensions : list[str], optional
        A list of file extensions to filter the files. If None (default), all files are yielded.
        This parameter is ignored if `pathobject` is a file.

    Returns
    -------
    Generator[FileRelPath, None, None]
        A generator yielding FileRelPath objects for each found file. Each FileRelPath includes
        the absolute path of the file and its path relative to `pathobject`.

    Raises
    ------
    FileNotFoundError
        If `pathobject` does not exist.
    """
    if not pathobject.exists():
        error_msg = f"File or folder '{pathobject}' does not exist."
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    if pathobject.is_file():
        yield FileRelPath(pathobject, pathobject.relative_to(pathobject))

    if pathobject.is_dir():
        yield from iterate_folder(
            folder=pathobject,
            file_extensions=file_extensions,
            subfolders=False,
            parent_path=pathobject,
        )


def iterate_folder(  # noqa: PLR0913
    folder: str | Path,
    file_extensions: list[str] | None = None,
    file_patterns: list[str] | None = None,
    exclude_patterns: bool = False,
    subfolders: bool = True,
    parent_path: Path | None = None,
) -> Generator[FileRelPath, None, None]:
    """Yield files from a given folder, optionally filtering by extension and pattern.

    This function iterates through a folder and its subfolders (if `subfolders` is True),
    yielding files with specified extensions and name patterns. If the folder is a file,
    it yields the file itself.

    Parameters
    ----------
    folder : str | Path
        The parent folder to start the search.
    file_extensions : list[str], optional
        List of file extensions to filter by. If None (default), all files are yielded.
    file_patterns : list[str], optional
        List of patterns that the file names should match. If None (default), all files are yielded.
        If multiple patterns are provided, a file is returned if its name matches any pattern.
        Patterns can include wildcards like '*' and '?', to match multiple
        characters or a single character, respectively. For example:
            - ["*before*"]: matches all files that have the word "before" in their name.
            - ["*.txt"]: matches all files with the '.txt' extension.
            - ["file_?.txt"]: matches all files with names like 'file_1.txt', 'file_2.txt', etc.
            - ["file_[0-9].txt"]: equivalent to the previous example, but uses a character set
              to match any digit between 0 and 9.
    exclude_patterns : bool, optional
        If True, returns files that do not match `file_patterns`.
    subfolders : bool, optional
        If True (default), includes subfolders in the search.
    parent_path : Path, optional
        The path of the parent, used to return the relative paths to reconstruct the folder
        hierarchy

    Yields
    ------
    FileRelPath
        A FileRelPath object for each found file, including the absolute path and
        the path relative to `parent_path`.

    Raises
    ------
    FileNotFoundError
        If `folder` does not exist.
    """
    current_folder = Path(folder).parent if Path(folder).is_file() else Path(folder)

    if not current_folder.exists():
        msg = f"The folder '{current_folder}' does not exist."
        raise FileNotFoundError(msg)

    file_extensions = (
        [".*"]
        if file_extensions is None
        else [clean_file_extension(ext) for ext in file_extensions]
    )

    parent_path = parent_path or current_folder
    for entry in current_folder.rglob("*" if subfolders else "*.*"):
        # Only returns files, not folders
        if entry.is_file() and any(re.match(ext, entry.suffix.lower()) for ext in file_extensions):  # noqa: SIM102
            if (
                file_patterns is None
                or any(fnmatch(entry.name, pattern) for pattern in file_patterns)
                != exclude_patterns
            ):
                yield FileRelPath(entry, entry.relative_to(parent_path))


def open_file(path: Path, mode: str = "w", encoding: str | None = None) -> IO[Any]:
    """Safely open a file using the provided path, mode, and encoding.

    This function ensures that the folder containing the file exists before attempting to open it.

    Parameters
    ----------
    path : Path
        The path to the file to be opened.
    mode : str, optional
        The mode in which the file is to be opened, by default 'w'.
    encoding : str | None, optional
        The encoding to be used when opening the file, by default None.

    Returns
    -------
    IO[Any]
        The opened file.

    Raises
    ------
    PermissionError
        If the function does not have permission to create the directory or open the file.
    """
    try:
        return path.open(mode=mode, encoding=encoding)
    except FileNotFoundError:
        if mode in {"r", "r+"}:
            # If trying to read but the file doesn't exist, re-raise the exception
            raise

        folder_created = create_folder(path, True)
        try:
            return path.open(mode=mode, encoding=encoding)
        except Exception:
            if folder_created and not any(path.iterdir()):
                path.rmdir()
            raise


def create_folder(path: Path, includes_file: bool = False) -> bool:
    """Create the folder passed in the 'path' if it doesn't exist.

    Useful to be sure that a folder exists before saving a file.

    Parameters
    ----------
    path : Path
        Path object for the folder (can also include the file)
    includes_file : bool, optional
        The path includes a file at the end, by default 'False'.

    Returns
    -------
    bool
        True if the folder was created, False otherwise.
    """
    path = path.parent if includes_file else path

    if path.exists():
        return False

    try:
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        logger.warning("Failed to create folder '%s': no permission", path)
        raise
    else:
        return True


def clean_filename(filename: str, replacement: str = "_") -> str:
    """Remove illegal characters from a filename.

    Parameters
    ----------
    filename : str
        name of the file

    replacement : str
        character to replace the illegal characters

    Returns
    -------
    str
        clean name
    """
    illegal_characters = "!@#$%^&*()[]{};:,/<>?'\\'|`~-=_+"

    replacement = "_" if replacement in illegal_characters else replacement

    filename = filename.translate({ord(c): replacement for c in illegal_characters})
    return filename


def generate_unique_filename(file: Path | str) -> Path:
    """Generate a unique filename by appending numbers if a file with the same name exists.

    Parameters
    ----------
    file : Union[str, Path]
        The original file path.

    Returns
    -------
    Path
        The unique file path.

    Examples
    --------
    >>> print(get_unique_filename("/path/to/file.txt")) # doctest: +SKIP
    /path/to/file_2.txt
    """
    counter = 1
    file = Path(file)

    while True:
        new_filename = f"{file.stem}{f'_{counter}' if counter > 1 else ''}{file.suffix}"
        file_path = Path(file.parent / new_filename)
        if not file_path.exists():
            break
        counter += 1
    return file_path


def add_folder_timestamp(rootdir: str | Path, fmt: str = "run_%Y_%m_%d-%H_%M_%S") -> Path:
    """Create a new folder with a timestamp in the given directory.

    This function takes a directory path and creates a new folder within that directory.
    The name of the new folder is a timestamp formatted according to the provided format string.

    Parameters
    ----------
    rootdir : str | Path
        The path of the directory where the new folder will be created.
    fmt : str, optional
        The format of the timestamp to be used as the new folder's name.
        The format is defined using strftime directives. Default is "run_%Y_%m_%d-%H_%M_%S".

    Returns
    -------
    Path
        The path of the newly created folder.

    Examples
    --------
    ```python
    new_folder_path = add_folder_timestamp("/path/to/directory", "run_%Y_%m_%d-%H_%M_%S")
    print(new_folder_path)
    # Output: /path/to/directory/run_2023_04_05-16_25_03
    ```
    """
    run_id = time.strftime(fmt)
    return Path(rootdir, run_id)
