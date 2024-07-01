# Python Cookbook, 3rd Ed.
#
# Chapter: Input/Output, Physical Format, and Logical Layout
# Recipe: Reading HTML documents



# Subection: Getting ready

example_html_1 = """
<!DOCTYPE html>
<html>
<head>...</head>
<body>...</body>
</html>
"""

example_html_2 = """
<table>
    <thead>
        <tr>
            <th>...</th>
            ...
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>...</td>
            ...
        </tr>
        ...
    </tbody>
</table>
"""

example_html_3 = """
<th tooltipster data-title="<strong>ALICANTE - CAPE TOWN</strong>
" data-theme="tooltipster-shadow" data-htmlcontent="true" data-position="top">
LEG 1</th>
"""
example_html_4 = """
<tr class="ranking-item">
    <td class="ranking-position">3</td>
    <td class="ranking-avatar"><img src="..."></td>
    <td class="ranking-team"> Dongfeng Race Team</td>
    <td class="ranking-number">2</td>
    <td class="ranking-number">2</td>
    <td class="ranking-number">1</td>
    <td class="ranking-number">3</td>

    <td class="ranking-number" tooltipster
    data-title="<center><strong>RETIRED</strong><br> Click for more info</center>" data-theme="tooltipster-3"
    data-position="bottom" data-htmlcontent="true">
    <a href="/en/news/8674_Dongfeng-Race-Team-breaks-mast-crew-safe.html"
    target="_blank">8</a>
    <div class="status-dot dot-3"></div></td>

    <td class="ranking-number">1</td>
    <td class="ranking-number">4</td>
    <td class="ranking-number">7</td>
    <td class="ranking-number">4</td>
    <td class="ranking-number total">33<spanclass="asterix">*</span></td>
</tr>
"""


# Subection: How to do it...

from bs4 import BeautifulSoup
from pathlib import Path
from typing import Any

def race_extract(source_path: Path) -> dict[str, Any]:
    with source_path.open(encoding="utf8") as source_file:
        soup = BeautifulSoup(source_file, "html.parser")
    thead_row = soup.table.thead.tr  # type: ignore [union-attr]
    legs: list[tuple[str, str | None]] = []
    for tag in thead_row.find_all("th"): # type: ignore [union-attr]
        leg_description = (
            tag.string, tag.attrs.get("data-title")
        )
        legs.append(leg_description)
    tbody = soup.table.tbody # type: ignore [union-attr]
    teams: list[dict[str, Any]] = []
    for row in tbody.find_all("tr"): # type: ignore [union-attr]
        team: dict[str, Any] = {
            "name": None,
            "position": []}
        for col in row.find_all("td"):
            if "ranking-team" in col.attrs.get("class"):
                team["name"] = col.string
            elif (
                    "ranking-number" in col.attrs.get("class")
                ):
                team["position"].append(col.string)
            elif "data-title" in col.attrs:
                # Complicated explanation with nested HTML
                # print(col.attrs, col.string)
                pass
        teams.append(team)
    document = {
        "legs": legs,
        "teams": teams,
    }
    return document

example_output = """
>>> source_path = Path("data") / "Volvo Ocean Race.html"
>>> race_extract(source_path)
{'legs': [(None, None),
          ('LEG 1', '<strong>ALICANTE - CAPE TOWN'),
          ('LEG 2', '<strong>CAPE TOWN - ABU DHABI</strong>'),
          ('LEG 3', '<strong>ABU DHABI - SANYA</strong>'),
          ('LEG 4', '<strong>SANYA - AUCKLAND</strong>'),
          ('LEG 5', '<strong>AUCKLAND - ITAJAÍ</strong>'),
          ('LEG 6', '<strong>ITAJAÍ - NEWPORT</strong>'),
          ('LEG 7', '<strong>NEWPORT - LISBON</strong>'),
          ('LEG 8', '<strong>LISBON - LORIENT</strong>'),
          ('LEG 9', '<strong>LORIENT - GOTHENBURG</strong>'),
          ('TOTAL', None)],
 'teams': [
    {'name': 'Abu Dhabi Ocean Racing',
     'position': ['1', '3',
              '2', '2',
              '1', '2',
              '5', '3',
              '5', '24']},
    {'name': 'Team Brunel',
     'position': ['3', '1',
                '5', '5',
                '4', '3',
                '1', '5',
                '2',
                '29']},
    {'name': 'Dongfeng Race Team',
     'position': ['2', '2',
                '1', '3',
                None, '1',
                '4', '7',
                '4', None]},
    {'name': 'MAPFRE',
     'position': ['7', '4',
                '4', '1',
                '2', '4',
                '2', '4',
                '3', None]},
    {'name': 'Team Alvimedica',
     'position': ['5', None,
                '3', '4',
                '3', '5',
                '3', '6',
                '1',
                '34']},
    {'name': 'Team SCA',
     'position': ['6', '6',
                '6', '6',
                '5', '6',
                '6', '1',
                '7', None]},
    {'name': 'Team Vestas Wind',
     'position': ['4',
                None,
                None,
                None,
                None,
                None,
                None,
                '2',
                '6',
                '60']}]}
"""


# Subection: How it works...

example_html_5 = """
<tr>
    <td>Data</td>
</tr>
"""

test_example_4_2 = """
>>> example = BeautifulSoup('''
... <tr>
... <td>data</td>
... </tr>
... ''', 'html.parser')

>>> list(example.tr.children)
['\\n', <td>data</td>, '\\n']
"""

# Subection: There's more...


test_example_5_1 = """
>>> source_path = Path("data") / "Volvo Ocean Race.html"
>>> with source_path.open(encoding="utf8") as source_file:
...     soup = BeautifulSoup(source_file, "html.parser")

>>> ranking_table = soup.find('table', class_="ranking-list")

>>> list(tag.name for tag in ranking_table.parents)
['section', 'div', 'div', 'div', 'div', 'body', 'html', '[document]']
"""


# End of Reading HTML documents

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
