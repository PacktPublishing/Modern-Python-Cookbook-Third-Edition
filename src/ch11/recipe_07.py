# Python Cookbook, 3rd Ed.
#
# Chapter: Input/Output, Physical Format, and Logical Layout
# Recipe: Reading XML documents


example_xml_1 = """
<team><name>Team SCA</name><position>...</position></team>
<team>
    <name>Team SCA</name>
    <position>...</position>
</team>
<?xml version="1.0"?>
<results>
	<teams>
		<team>
			<name>
				Abu Dhabi Ocean Racing
			</name>
			<position>
				<leg n="1">
					1
				</leg>
                ...
             </position>
             ...
         </team>
         ...
    </teams>
	<legs>
		<leg n="1">
			ALICANTE - CAPE TOWN
		</leg>
        ...
	</legs>
</results>
"""

# Subection: Getting ready

example_xml_2 = """
<?xml version="1.0"?>
<results>
	<teams>
		<team>
			<name>
				Abu Dhabi Ocean Racing
			</name>
			<position>
				<leg n="1">
					1
				</leg>
				<leg n="2">
					3
				</leg>
				<leg n="3">
					2
				</leg>
				<leg n="4">
					2
				</leg>
				<leg n="5">
					1
				</leg>
				<leg n="6">
					2
				</leg>
				<leg n="7">
					5
				</leg>
				<leg n="8">
					3
				</leg>
				<leg n="9">
					5
				</leg>
			</position>
		</team>
		...
    </teams>
<p>
This has <strong>mixed</strong> content.
</p>
"""

# Subection: How to do it...

import xml.etree.ElementTree as XML
from pathlib import Path
from typing import cast

def race_summary(source_path: Path) -> None:
    source_text = source_path.read_text(encoding='UTF-8')
    document = XML.fromstring(source_text)
    legs = cast(XML.Element, document.find('legs'))
    teams = cast(XML.Element, document.find('teams'))
    for leg in legs.findall('leg'):
        print(cast(str, leg.text).strip())
        n = leg.attrib['n']
        for team in teams.findall('team'):
            position_leg = cast(XML.Element,
                team.find(f"position/leg[@n='{n}']"))
            name = cast(XML.Element, team.find('name'))
            print(
                cast(str, name.text).strip(),
                cast(str, position_leg.text).strip()
            )

example_xml_3 = """	
<leg n="1">ALICANTE - CAPE TOWN</leg>
"""

# Subection: How it works...

example_xml_4 = """	
<name>Team SCA</name>
<position>|...</position>
"""


# Subection: There's more...


test_example_5_1 = """
>>> source_path = Path("data") / "race_result.xml"
>>> source_text = source_path.read_text(encoding='UTF-8')
>>> document = XML.fromstring(source_text)

>>> for tag in document.findall('teams/team/name'):
...     print(tag.text.strip())
Abu Dhabi Ocean Racing
Team Brunel
Dongfeng Race Team
MAPFRE
Team Alvimedica
Team SCA
Team Vestas Wind


>>> for tag in document.findall("teams/team/position/leg[@n='8']"):
...     print(tag.text.strip())
3
5
7
4
6
1
2
"""


# End of Reading XML documents

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
