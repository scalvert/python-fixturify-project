from pathlib import Path


def write_to_file(file_path, contents):
    with open(Path(file_path), "w") as f:
        f.write(contents)


def create_directory(file_path):
    Path(file_path).mkdir(parents=True, exist_ok=True)
