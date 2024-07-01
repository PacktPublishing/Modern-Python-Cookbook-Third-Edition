# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Testing things that involve dates or times


# Subsection: Getting ready

import datetime
import json
from pathlib import Path
from typing import Any


def save_data(base: Path, some_payload: Any) -> None:
    now_date = datetime.datetime.now(tz=datetime.timezone.utc)
    now_text = now_date.strftime("extract_%Y%m%d%H%M%S")
    file_path = (base / now_text).with_suffix(".json")
    with file_path.open("w") as target_file:
        json.dump(some_payload, target_file, indent=2)


# End of Testing things that involve dates or times

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
