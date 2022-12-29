from python_fixturify_project.project import DirJSON

BAD_DIR_NAME: DirJSON = {"test_dir": {"..": {}}}

BAD_EMPTY_NAME: DirJSON = {
    "test_dir": {
        "valid_dir": {"valid_empty_file.txt": ""},
        "valid_file.txt": "some text",
        "": "This should not pass",
    }
}

GOOD_SINGLE_FILE: DirJSON = {"valid_file.txt": "some text"}

GOOD_NESTED_DIRS: DirJSON = {
    ".a_hidden_folder": {
        "nested_dir": {
            ".a_hidden_file": "some text",
        },
    },
    "valid_file.txt": "some text",
    "nested_dir": {
        "valid_empty_file.txt": "",
        "another_nested_empty_dir": {},
        "another_nested_dir": {
            "last_nested_empty_dir": {},
            "final_text_file.txt": "some text",
        },
    },
}
