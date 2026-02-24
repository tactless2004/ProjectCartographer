from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple

# local imports
from git import _git_clone, _clean_up
from files import _compute_file_details
from languages import get_language

TEST_URL = "git@github.com:TheRenegadeCoder/sample-programs.git"
FILES: List[FileEntry] = []
FILE_LANG_MAP: Dict[str, List[int]] = {}

@dataclass(frozen = True)
class FileEntry:
    language: str
    line_count: int
    chr_count: int
    relative_path: str

def _link_langstr_to_f():
    for i, fe in enumerate(FILES):
        if not fe.language in FILE_LANG_MAP:
            FILE_LANG_MAP[fe.language] = [i]
        else:
            FILE_LANG_MAP[fe.language].append(i)

def _compute_per_lang_chr_count(language: str):
    chr_count = 0
    for fe in FILES:
        chr_count += fe.chr_count if fe.language == language else 0

    return chr_count

def main():
    '''Main Method'''
    _git_clone(TEST_URL)
    for root, _, files in os.walk("temp"):
        for file in files:
            full_path = str(Path(root) / file)
            lang = get_language(full_path)

            if not lang:
                continue

            # For now just take the first option if there are multiple
            if isinstance(lang, list):
                lang = lang[0]

            line_count, char_count = _compute_file_details(full_path)
            FILES.append(FileEntry(
                language = lang,
                line_count = line_count,
                chr_count = char_count,
                relative_path = full_path.lstrip("temp/")
            ))

    _link_langstr_to_f()
    total_chr_count = sum([fe.chr_count for fe in FILES])

    # The type hinting helps me think
    print_map: Dict[str, Tuple[List[Tuple[str, float]], float]] = {}


    for language, idxs in FILE_LANG_MAP.items():
        language_prop = round(_compute_per_lang_chr_count(language)/total_chr_count, 4)
        print_map[language] = ([], language_prop)

        for idx in idxs:
            fe = FILES[idx]
            file_prop = round(fe.chr_count/total_chr_count, 4)
            print_map[language][0].append((fe.relative_path, file_prop))


    for name, (lst, prop) in sorted(
        print_map.items(),
        key = lambda item: item[1][1],
        reverse = True # descending order
    ):
        print(f"{name} ({prop*100}%)")
        for elem in sorted(
            lst,
            key = lambda elem: elem[1],
            reverse = True
        ):
            print(f"\t{elem[0]} {elem[1]*100}%")

    _clean_up()

if __name__ == "__main__":
    main()
