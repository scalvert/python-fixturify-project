from __future__ import annotations

from typing import Dict, Union, cast

import os
import shutil
import tempfile

from dict_path import extract_dict, inject_dict
from wcmatch.pathlib import DOTGLOB, GLOBSTAR, Path

from python_fixturify_project.exceptions import InvalidProjectError
from python_fixturify_project.utils import deep_merge, keys_exists

DEFAULT_IGNORE_PATTERNS: list[str] = ["**/.git", "**/.git/**"]

DirJSON = Dict[str, Union["DirJSON", str, None]]


class Project:
    """
    Represents a project directory structure.

    Attributes:
        _base_dir (str): The base directory of the project.
        _files (DirJSON): The files corresponding to the project's directory structure.
        _ignore_patterns (list[str]): The patterns to ignore when reading the project's directory structure.
    """

    def __init__(self, files: DirJSON | None = None, ignore_patterns: list[str] = []):
        """
        Initializes the Project with the given files and ignore patterns.

        Args:
            files (DirJSON | None): The files corresponding to the project's directory structure.
            ignore_patterns (list[str]): The patterns to ignore when reading the project's directory structure.
        """
        self._base_dir: str = ""
        self._files: DirJSON = files or {}
        self._ignore_patterns: list[str] = DEFAULT_IGNORE_PATTERNS + (
            ignore_patterns or []
        )

        self.write(self._files)

    def __del__(self):
        """
        Cleans up the temp dir structure on delete.
        """
        self.dispose()

    @property
    def base_dir(self) -> str:
        """
        Gets the base directory path, usually a tmp directory unless a baseDir has been explicitly set.

        Returns:
            str: The base directory path.

        Raises:
            Exception: If the base directory has not been set yet.
        """
        if self._base_dir == "":
            raise Exception(
                "Project has no base_dir yet. Either set one manually or call write to have one chosen for you."
            )

        return self._base_dir

    @base_dir.setter
    def base_dir(self, value: str) -> None:
        """
        Sets the base directory of the project.

        Args:
            value (str): The new base directory.

        Raises:
            Exception: If the base directory has already been set.
        """
        if self._base_dir != "":
            raise Exception("Project already has a base_dir")

        self._base_dir = value

    @base_dir.deleter
    def base_dir(self) -> None:
        """
        Deletes the base directory.
        """
        del self._base_dir

    @property
    def files(self) -> DirJSON:
        """
        Gets the files containing the project's directory structure.

        Returns:
            DirJSON: The files containing the project's directory structure.
        """
        if not self._files:
            self._files = self.read()

        return self._files

    @files.setter
    def files(self, value: DirJSON) -> None:
        """
        Sets the files corresponding to the project's directory structure.

        Args:
            value (DirJSON): The new files.
        """
        self._files = value

    @files.deleter
    def files(self) -> None:
        """
        Deletes the files corresponding to the project's directory structure.
        """
        del self._files

    def dispose(self) -> None:
        """
        Deletes the base directory and its contents.
        """
        try:
            skip_dispose = os.environ.get("FIXTURIFY_SKIP_DISPOSE", False)

            if skip_dispose:
                return

            shutil.rmtree(self._base_dir)
        except FileNotFoundError:
            # No need to do anything, file structure has already been cleaned up!
            pass

    def merge_files(self, dir_json: DirJSON) -> None:
        """
        Merges an object containing a directory representation with the existing files.

        Args:
            dir_json (DirJSON): The directory representation to merge with the existing files.
        """
        self.files = deep_merge(self.files, dir_json)

    def write(self, dir_json: DirJSON) -> None:
        """
        Writes the existing files property containing a directory representation to the tmp directory.

        Args:
            dir_json (DirJSON): The directory representation to write to the tmp directory.
        """
        if dir_json:
            self.merge_files(dir_json)

        self.__write_project()

    def read(self) -> DirJSON:
        """
        Reads the contents of the base_dir to a dict and ignores any files/dirs matched by the glob expressions.

        Returns:
            DirJSON: The contents of the base_dir.
        """
        files: DirJSON = {}

        for path in Path(self.base_dir).rglob(
            "*", exclude=self._ignore_patterns, flags=DOTGLOB | GLOBSTAR
        ):
            rel_path = str(path.relative_to(self.base_dir))

            if str(rel_path) == ".":
                continue

            if path.is_file():
                with open(path) as f:
                    self.__add_file(files, rel_path, f.read())
            else:
                self.__add_dir(files, rel_path)

        self._files = files

        return files

    def get(self, object_path: str) -> DirJSON:
        """
        Gets the value at the given path in the files.

        Args:
            object_path (str): The path to the value in the files.

        Returns:
            DirJSON: The value at the given path in the files.
        """
        if self._files == {}:
            self._files = self.read()

        return cast(DirJSON, extract_dict(self._files, object_path))

    def __auto_base_dir(self) -> None:
        """
        Creates and sets the base_dir if not explicitly configured during init.
        """
        if not self._base_dir:
            self._base_dir = tempfile.mkdtemp()

    def __add_file(self, files: DirJSON, path: str, contents: str) -> None:
        """
        Adds a file to the given files at the given path with the given contents.

        Args:
            files (DirJSON): The files to add the file to.
            path (str): The path to add the file at.
            contents (str): The contents of the file.
        """
        file = os.path.basename(path)
        dir_name = os.path.dirname(path)

        if dir_name != "":
            self.__add_dir(files, dir_name)[file] = contents
        else:
            files[file] = contents

    def __add_dir(self, files: DirJSON, path: str) -> DirJSON:
        """
        Adds a directory to the given files at the given path.

        Args:
            files (DirJSON): The files to add the directory to.
            path (str): The path to add the directory at.

        Returns:
            DirJSON: The updated files.
        """
        path = str(path)
        if not keys_exists(files, *path.split("/")):
            inject_dict(files, path, {})

        return cast(DirJSON, extract_dict(files, path))

    def __write_project(self) -> None:
        """
        Writes the project to the base_dir.
        """
        self.__auto_base_dir()
        self.__write(self.files, self.base_dir)

    def __write(self, files: DirJSON, full_path: str) -> None:
        """
        Writes the given files to the given path.

        Args:
            files (DirJSON): The files to write.
            full_path (str): The path to write the files to.

        Raises:
            InvalidProjectError: If the directory structure is invalid.
        """
        if not files or not isinstance(files, Dict):
            return

        original_dir = str(Path(full_path))

        for entry in files:
            full_path = str(Path(full_path, entry))

            if not isinstance(entry, str) or entry == "":
                raise InvalidProjectError(
                    "Invalid directory structure given. Each key must be a non-empty string"
                )

            if isinstance(files[entry], str):
                with open(Path(full_path), "w") as f:
                    f.write(cast(str, files[entry]))
            else:
                if entry == "." or entry == "..":
                    raise InvalidProjectError('Directory entry must not be "." or ".."')

                Path(full_path).mkdir(parents=True, exist_ok=True)
                # Our recursion step, which should only happen if we find ourselves a nested directory
                self.__write(cast(DirJSON, files[entry]), str(full_path))

            # Reset the original path because Python will still remember the value of `full_path` even after we return from recursion
            full_path = original_dir
