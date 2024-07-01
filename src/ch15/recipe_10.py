# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Mocking external resources


# Subsection: Getting ready

from pathlib import Path
import csv
from dataclasses import dataclass, asdict, fields

@dataclass
class Quotient:
    numerator: int
    denominator: int

def save_data(output_path: Path, data: Quotient) -> None:
    with output_path.open("w", newline="") as output_file:
        headers = [f.name for f in fields(Quotient)]
        writer = csv.DictWriter(output_file, headers)
        writer.writeheader()
        writer.writerow(asdict(data))





def safe_write(output_path: Path, data: Quotient) -> None:
    ext = output_path.suffix
    output_new_path = output_path.with_suffix(f"{ext}.new")
    save_data(output_new_path, data)
    # Clear any previous .{ext}.old
    output_old_path = output_path.with_suffix(f"{ext}.old")
    output_old_path.unlink(missing_ok=True)
    # Try to preserve current as old
    try:
        output_path.rename(output_old_path)
    except FileNotFoundError as ex:
        # No previous file. That's okay.
        pass
    # Try to replace current .{ext} with new .{ext}.new
    try:
        output_new_path.rename(output_path)
    except IOError as ex:
        # Possible recovery...
        output_old_path.rename(output_path)


# End of Mocking external resources

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
