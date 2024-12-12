"""Manage filesystem."""

from dataclasses import dataclass, field
from pathlib import Path

from acmetric.utils.manage_filesystem import (
    check_if_file_exists,
    create_file_in_directory_if_not_exists,
    write_string_to_file,
)


@dataclass
class FileManager:
    """
    File manager.

    This class manages files. It checks if file exists, creates directory and empty file,
    writes file.

    Parameters
    ----------
    name : str
        Name of the table.
    path : Path
        Path to the directory where the schema script is stored.
    """

    name: str
    path: Path
    file_path: Path = field(init=False)

    def __post_init__(self) -> None:
        """
        Extract full filename.

        This method extracts the full filename from the name and path.

        Returns
        -------
        Path
            Full filename.
        """
        self.file_path = self.create_full_path()

    def check_if_file_exists(self) -> bool:
        """
        Check if file exists.

        Returns
        -------
        bool
            True if file exists, False otherwise.
        """
        return check_if_file_exists(self.file_path)

    def create_directory_and_empty_file(self) -> None:
        """Create directory and empty file."""
        create_file_in_directory_if_not_exists(self.file_path)

    def split_table_name_into_subfolder_and_filename(self) -> tuple[str, str]:
        """
        Split table name into subfolder and filename.

        This method splits the table name into subfolder and filename.
        """
        table_name_splitted = self.name.split(".")
        subfolder_name = table_name_splitted[0]
        filename = table_name_splitted[1] + ".py"
        return subfolder_name, filename

    def create_full_path(self) -> Path:
        """
        Create full path.

        This method creates full path to the file.
        """
        subfolder_name, filename = self.split_table_name_into_subfolder_and_filename()
        return self.path / subfolder_name / filename

    def write_file(self, string: str) -> None:
        """Write file."""
        write_string_to_file(string, self.file_path)
