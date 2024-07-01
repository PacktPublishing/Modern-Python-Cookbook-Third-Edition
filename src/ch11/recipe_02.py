# Python Cookbook, 3rd Ed.
#
# Chapter: Input/Output, Physical Format, and Logical Layout
# Recipe: Replacing a file while preserving the previous version


# Subection: Getting ready

from dataclasses import dataclass, asdict, fields

@dataclass
class Quotient:
    numerator: int
    denominator: int
import csv
from collections.abc import Iterable
from pathlib import Path

def save_data(
    output_path: Path, data: Iterable[Quotient]
) -> None:
    with output_path.open("w", newline="") as output_file:
        headers = [f.name for f in fields(Quotient)]
        writer = csv.DictWriter(output_file, headers)
        writer.writeheader()
        for q in data:
            writer.writerow(asdict(q))

expected_output = """
numerator,denominator
87,32
"""

# Subection: How to do it...

def safe_write(
    output_path: Path, data: Iterable[Quotient]
) -> None:
    ext = output_path.suffix
    output_new_path = output_path.with_suffix(f'{ext}.new')
    save_data(output_new_path, data)
    output_old_path = output_path.with_suffix(f'{ext}.old')
    output_old_path.unlink(missing_ok=True)
    try:
        output_path.rename(output_old_path)
    except FileNotFoundError as ex:
        # No previous file. That's okay.
        pass
    try:
        output_new_path.rename(output_path)
    except IOError as ex:
        # Possible recovery...
        output_old_path.rename(output_path)

# Subection: There's more...

def syntax_check() -> None:
    archive_path = Path("/path/to/archive")

    import datetime
    from datetime import timezone

    today = datetime.datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    working_path = archive_path / today
    working_path.mkdir(parents=True, exist_ok=True)


# End of Replacing a file while preserving the previous version

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
