'''Generates an html report based on git repo data'''
# "compiler" directives
from __future__ import annotations

# python std library
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple

# external packages
from jinja2 import Environment, FileSystemLoader

# local imports
from git import _git_clone, _clean_up
from files import _compute_file_details
from languages import get_language

FILES: List[FileEntry] = []
FILE_LANG_MAP: Dict[str, Tuple[List[FileEntry], int]] = {}

@dataclass(frozen = True)
class FileEntry:
    '''Schema for a program file'''
    language: str
    line_count: int
    chr_count: int
    relative_path: str

def _compute_per_lang_chr_count(language: str):
    chr_count = 0
    for fe in FILES:
        chr_count += fe.chr_count if fe.language == language else 0

    return chr_count

def _link_langstr_to_f():
    for fe in FILES:
        assert isinstance(fe, FileEntry)
        if not fe.language in FILE_LANG_MAP:
            FILE_LANG_MAP[fe.language] = ([fe], _compute_per_lang_chr_count(fe.language))
        else:
            FILE_LANG_MAP[fe.language][0].append(fe)

def generate_report(url: str):
    '''Return jinja2 templated html string from github url'''
    FILES.clear()
    FILE_LANG_MAP.clear()

    _git_clone(url)

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
    _clean_up() # delete git repo
    _link_langstr_to_f()

    total_chr_count = sum([fe.chr_count for fe in FILES])

    jinja_data = {
        "project_name" : "TODO",
        "total_chars" : total_chr_count,
        "languages": [
            {
            "name" : name,
            "chars" : lang_cnt,
            "pct_total" : lang_cnt / total_chr_count * 100,
            "files" : [
                {
                    "path" : fe.relative_path,
                    "chars" : fe.chr_count,
                    "pct_total" : fe.chr_count / total_chr_count * 100,
                    "pct_lang" : fe.chr_count / lang_cnt * 100
                }
                for fe in sorted(
                    lst,
                    key = lambda fe: fe.chr_count,
                    reverse = True
                )
            ]
            } for name, (lst, lang_cnt) in sorted(
                FILE_LANG_MAP.items(),
                key = lambda elem: elem[1][1],
                reverse = True
        )]
    }

    env = Environment(loader = FileSystemLoader("templates"))
    template = env.get_template("template.html")
    report = template.render(report = jinja_data)

    return report
