from typing import Any, Dict

BAD_DIR_NAME: Dict[str, Any] = {"test_dir": {"..": {}}}

BAD_EMPTY_NAME: Dict[str, Any] = {
    "test_dir": {
        "valid_dir": {"valid_empty_file.txt": ""},
        "valid_file.txt": "some text",
        "": "This should not pass",
    }
}

GOOD_SINGLE_FILE: Dict[str, Any] = {"valid_file.txt": "some text"}

GOOD_NESTED_DIRS: Dict[str, Any] = {
    "valid_file.txt": "some text",
    "nested_dir": {
        "valid_empty_file": "",
        "another_nested_empty_dir": {},
        "another_nested_dir": {
            "last_nested_empty_dir": None,
            "final_text_file": "some text",
        },
    },
}
