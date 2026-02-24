'''utilities for interacting with git repos'''
import subprocess
from typing import Tuple

def _git_clone(url: str):
    '''Programatically clones a git repo'''
    try:
        # check will raise an Error if the subprocess returns a non-zero exit status
        subprocess.run(["mkdir", "temp"], check = True)
        subprocess.run(
            ["git", "clone", url, "./temp"],
            check = True,
            stdout = subprocess.DEVNULL,
            stderr = subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def _clean_up():
    try:
        subprocess.run(["rm", "-rf", "temp"], check = True)
    except subprocess.CalledProcessError as e:
        print(f"An error ocurred: {e}")
