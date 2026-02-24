'''File parsing utilities'''
from typing import Tuple

def _compute_file_details(path: str) -> Tuple[int, int]:
    line_count = 0
    char_count = 0

    # Yes, the two opens() are necessary
    with open(path, "r", encoding = "utf-8") as f:
        line_count = len(f.readlines())

    with open(path, "r", encoding = "utf-8") as f:
        # TODO: consider len(f.read()) what is the maximum character count before this fails?
        char_count = len([
            chr for chr in f.read() if chr not in [
                "\n", "\t"
            ]
        ])

    return (line_count, char_count)
