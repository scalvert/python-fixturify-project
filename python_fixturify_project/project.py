import tempfile

from pathlib import Path

def deep_merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                deep_merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

class Project(object):
    def __init__(self):
        self._base_dir = None
        self._tmp = None
        self._files = {}

    @property
    def base_dir(self):
        """Gets the base directory path, usually a tmp directory unless a baseDir has been explicitly set."""
        return self._base_dir

    @base_dir.setter
    def base_dir(self, value):
        """Sets the base directory of the project."""
        self._base_dir = value

    @base_dir.deleter
    def base_dir(self):
        """Deletes the base directory."""
        del self._base_dir

    @property
    def files(self):
        """Gets the files containing the project's directory structure."""
        return self._files

    @files.setter
    def files(self, value):
        """Sets the files corresponding to the project's directory structure."""
        self._files = value

    @files.deleter
    def files(self):
        """Deletes the files corresponding to the project's directory structure."""
        del self._files


    def __auto_base_dir(self):
        """"""
        if not self.base_dir:
            self.base_dir = tempfile.mkdtemp()

        return self.base_dir

    def merge_files(self, dir_json):
        """Merges an object containing a directory represention with the existing files."""
        self.files = deep_merge(self.files, dir_json)

    def write(self, dir_json):
        """Writes the existing files property containing a directory representation to the tmp directory."""
        if dir_json:
            self.merge_files(dir_json)

        self.write_project()

    def write_project(self):
        self.__auto_base_dir()


    def __write(self):
        Path(self.base_dir).mkdir(parents=True, exist_ok=True)

