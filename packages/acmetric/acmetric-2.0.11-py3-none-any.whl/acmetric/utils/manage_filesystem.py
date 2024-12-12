"""Module for managing the filesystem."""

from pathlib import Path


def create_directory(path: Path) -> None:
    """
    Create directory.

    Parameters
    ----------
    path : Path
        Path to directory.
    """
    path.mkdir(parents=True, exist_ok=True)


def create_file(path: Path) -> None:
    """
    Create file.

    Parameters
    ----------
    path : Path
        Path to file.
    """
    path.touch()


def create_file_in_directory_if_not_exists(path: Path) -> None:
    """
    Create file in directory if not exists.

    Parameters
    ----------
    path : Path
        Path to file.
    """
    if not check_if_file_exists(path):
        create_directory(path.parent)
        create_file(path)


def write_string_to_file(string: str, path: Path) -> None:
    """
    Write string to file.

    This function fills the file with the string.

    Parameters
    ----------
    string : str
        String to write.
    path : Path
        Path to file.
    """
    with open(path, "w") as f:
        f.write(string)


def check_if_file_exists(path: Path) -> bool:
    """
    Check if file exists.

    Parameters
    ----------
    path : Path
        Path to file.

    Returns
    -------
    bool
        True if file exists, False otherwise.
    """
    return path.exists()


def extract_relative_path(path: Path) -> Path:
    """
    Extract relative path.

    This function extracts the relative path from the current working directory.

    Parameters
    ----------
    path : Path
        Path to file.

    Returns
    -------
    Path
        Relative path.
    """
    return path.relative_to(Path.cwd())
