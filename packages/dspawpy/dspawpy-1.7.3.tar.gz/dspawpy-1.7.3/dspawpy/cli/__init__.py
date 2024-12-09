import json
import os

from prompt_toolkit.completion import (
    FuzzyCompleter,
    PathCompleter,
)

from dspawpy import auto_test_cli

pc = FuzzyCompleter(PathCompleter(expanduser=True))  # path completion
pc_h5 = FuzzyCompleter(
    PathCompleter(expanduser=True, file_filter=lambda p: p.endswith(".h5"))
)  # path completion

list_ds = []
if auto_test_cli:
    json_file = os.path.abspath("cli_input.json")
    if os.path.isfile(json_file):
        with open(json_file, "r") as fin:
            list_ds: list[dict] = [
                json.loads(line) for line in fin.readlines() if line.strip()
            ]
    else:
        raise FileNotFoundError(
            f"dspawpy_cli_test set to auto but {json_file} not found"
        )
