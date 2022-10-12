from typing import Any, Dict

import glob
import os
import shutil
import tempfile

from dict_path import extract_dict, inject_dict
from wcmatch.pathlib import DOTGLOB, GLOBSTAR, Path

from python_fixturify_project.exceptions import InvalidProjectError
from python_fixturify_project.path_utils import create_directory, write_to_file
from python_fixturify_project.utils import deep_merge, keys_exists

DEFAULT_IGNORE_PATTERNS = ["**/.git", "**/.git/**"]


class Project:
    def __init__(self, files=None, ignore_patterns=[]):
        self._base_dir = ""
        self._files = files or {}
        self._ignore_patterns = DEFAULT_IGNORE_PATTERNS + ignore_patterns

        self.write(self._files)

    def __del__(self):
        # Ensure we clean up the temp dir structure on delete
        self.dispose()

    @property
    def base_dir(self):
        """Gets the base directory path, usually a tmp directory unless a baseDir has been explicitly set."""
        if self._base_dir == "":
            raise Exception(
                "Project has no base_dir yet. Either set one manually or call write to have one chosen for you."
            )

        return self._base_dir

    @base_dir.setter
    def base_dir(self, value):
        """Sets the base directory of the project."""
        if self._base_dir != "":
            raise Exception("Project already has a base_dir")

        self._base_dir = value

    @base_dir.deleter
    def base_dir(self):
        """Deletes the base directory."""
        del self._base_dir

    @property
    def files(self):
        """Gets the files containing the project's directory structure."""
        if not self._files:
            self._files = self.read()

        return self._files

    @files.setter
    def files(self, value):
        """Sets the files corresponding to the project's directory structure."""
        self._files = value

    @files.deleter
    def files(self):
        """Deletes the files corresponding to the project's directory structure."""
        del self._files

    def dispose(self):
        try:
            shutil.rmtree(self._base_dir)
        except FileNotFoundError:
            # No need to do anything, file structure has already been cleaned up!
            pass

    def merge_files(self, dir_json):
        """Merges an object containing a directory represention with the existing files."""
        self.files = deep_merge(self.files, dir_json)

    def write(self, dir_json):
        """Writes the existing files property containing a directory representation to the tmp directory."""
        if dir_json:
            self.merge_files(dir_json)

        self.__write_project()

    def read(self):
        """Reads the contents of the base_dir to a dict and ignores any files/dirs matched by the glob expressions"""
        files: Dict[str, Any] = {}

        for path in Path(self.base_dir).rglob(
            "*", exclude=self._ignore_patterns, flags=DOTGLOB | GLOBSTAR
        ):
            rel_path = path.relative_to(self.base_dir)

            if str(rel_path) == ".":
                continue

            if path.is_file():
                with open(path) as f:
                    self.__add_file(files, rel_path, f.read())
            else:
                self.__add_dir(files, rel_path)

        self._files = files

        return files

    def get(self, object_path):
        if self._files == {}:
            self._files = self.read()

        return extract_dict(self._files, object_path)

    def __auto_base_dir(self):
        """Creates and sets the base_dir if not explicitly configured during init"""
        if not self._base_dir:
            self._base_dir = tempfile.mkdtemp()

    def __add_file(self, files, path, contents):
        file = os.path.basename(path)
        dir_name = os.path.dirname(path)

        if dir_name != "":
            self.__add_dir(files, dir_name)[file] = contents
        else:
            files[file] = contents

    def __add_dir(self, files, path):
        path = str(path)
        if not keys_exists(files, *path.split("/")):
            inject_dict(files, path, {})

        return extract_dict(files, path)

    def __write_project(self):
        self.__auto_base_dir()
        self.__write(self.files, self.base_dir)

    def __write(self, files, full_path):
        """Recursive write helper function. Does the bulk of the work in terms of writing the directory structure"""
        if not files or not isinstance(files, dict):
            return

        original_dir = Path(full_path)

        for entry in files:
            full_path = Path(full_path, entry)

            if not isinstance(entry, str) or entry == "":
                raise InvalidProjectError(
                    "Invalid directory structure given. Each key must be a non-empty string"
                )

            if isinstance(files[entry], str):
                write_to_file(full_path, files[entry])
            else:
                if entry == "." or entry == "..":
                    raise InvalidProjectError('Directory entry must not be "." or ".."')

                create_directory(full_path)
                # Our recursion step, which should only happen if we find ourselves a nested directory
                self.__write(files=files[entry], full_path=full_path)

            # Reset the original path because Python will still remember the value of `full_path` even after we return from recursion
            full_path = original_dir
