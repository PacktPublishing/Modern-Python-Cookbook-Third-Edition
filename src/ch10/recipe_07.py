# Python Cookbook, 3rd Ed.
#
# Chapter: Working with Type Matching and Annotations
# Recipe: Introspection of types with the inspect module

import inspect

class SomeType:
    def __init__(self, value: str) -> None:
        self.value = value
    def __repr__(self) -> str:
        return f"SomeType({self.value!r})"

class Complicated:
    def __init__(self, value: str) -> None:
        self.value = value
    def __repr__(self) -> str:
        return f"Complicated({self.value!r})"
    @classmethod
    def conversion(cls, value: str, format: str) -> "Complicated":
        return Complicated(value)

from dataclasses import dataclass

@dataclass
class SomeNewClass:
    a_field: str
    a_conversion: SomeType
    complicated_conversion: Complicated

def make_somenewclass_from_dict(source: dict[str, str]) -> SomeNewClass:
    return SomeNewClass(
        a_field = source['column1'],
        a_conversion = SomeType(
            source['column2']),
        complicated_conversion = Complicated.conversion(
            source['column3'], "some format")
    )

test_from_dict = """
>>> row = {"column1": "x", "column2": "y", "column3": "z"}
>>> make_somenewclass_from_dict(row)
SomeNewClass(a_field='x', a_conversion=SomeType('y'), complicated_conversion=Complicated('z'))
"""


from collections.abc import Callable, Sequence
from typing import Any

def field_convert(
        target: str,
        column: str,
        conversion: Callable[..., Any],
        arg_list: Sequence[Any],
        row: dict[str, str]
) -> tuple[str, Any]:
    return (target, conversion(row[column], *arg_list))

def make_somenewclass_from_dict_2(source: dict[str, str]) -> SomeNewClass:
    converted = [
        field_convert('a_field', 'column1', str, [], source),
        field_convert('a_conversion', 'column2', SomeType, [], source),
        field_convert('complicated_conversion', 'column3', Complicated.conversion, ["some format"], source),
    ]
    return SomeNewClass(**dict(converted))

test_field_convert = """
>>> row = {"column1": "x", "column2": "y", "column3": "z"}
>>> make_somenewclass_from_dict_2(row)
SomeNewClass(a_field='x', a_conversion=SomeType('y'), complicated_conversion=Complicated('z'))
"""


from functools import partial
from typing import TypeAlias
from collections.abc import Callable

Schema_Func: TypeAlias = Callable[[dict[str, Any]], Any]

schema: list[Schema_Func] = [
    partial(field_convert,'a_field', 'column1', str, []),
    partial(field_convert,'a_conversion', 'column2', SomeType, []),
    partial(field_convert,'complicated_conversion', 'column3', Complicated.conversion, ["some format"]),
]

from typing import TypeVar

T = TypeVar("T")
def make_from_dict_3(
        cls: type[T],
        schema: list[Schema_Func],
        source: dict[str, str]
) -> T:
    converted = [
        conv_func(source) for conv_func in schema
    ]
    return cls(**dict(converted))

test_schema = """
>>> row = {"column1": "x", "column2": "y", "column3": "z"}
>>> make_from_dict_3(SomeNewClass, schema, row)
SomeNewClass(a_field='x', a_conversion=SomeType('y'), complicated_conversion=Complicated('z'))
"""

class Source:
    def __init__(self, name: str) -> None:
        self.name = name

class ConversionFunction:
    def __init__(self, convert: Callable[..., Any]) -> None:
        self.convert = convert

from typing import Annotated

@dataclass
class SomeNewClass2:
    a_field: Annotated[str, Source('column1')]
    a_conversion: Annotated[SomeType, Source('column2')]
    complicated_conversion: Annotated[
        Complicated,
        Source('column3'),
        ConversionFunction(
            lambda s: Complicated.conversion(s, "some format")
        )
    ]

# from typing_extensions import _AnnotatedAlias
from typing import get_type_hints, get_args

class Converter:
    def __init__(self, annotated: Any) -> None:
        self.args = get_args(annotated)
        self.source: str = ""
        # Default conversion is the annotated type
        self.convert: type | Callable[[str], Any] = self.args[0]
        for arg in self.args:
            match arg:
                case Source() as src:
                    self.source = src.name
                case ConversionFunction() as cvtfun:
                    # Override to the default conversion
                    self.convert = cvtfun.convert

    def __call__(self, source_dict: dict[str, str]) -> Any:
        return self.convert(source_dict[self.source])


def make_from_dict_a(cls: type[T], source: dict[str, str]) -> T:
    attrs = get_type_hints(cls, include_extras=True)
    schema = {
        attr_name: Converter(attr_annotation)
        for attr_name, attr_annotation in attrs.items()
    }
    converted = {
        name: conv_func(source)
        for name, conv_func in schema.items()
    }
    return cls(**converted)

test_annotations = """
>>> row = {"column1": "x", "column2": "y", "column3": "z"}
>>> make_from_dict_a(SomeNewClass2, row)
SomeNewClass2(a_field='x', a_conversion=SomeType('y'), complicated_conversion=Complicated('z'))
"""

import datetime

@dataclass
class Waypoint:
    latitude: Annotated[float, Source('lat')]
    longitude: Annotated[float, Source('lon')]
    date: Annotated[datetime.date, Source('date'), ConversionFunction(lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date())]
    time: Annotated[datetime.time, Source('time'), ConversionFunction(lambda s: datetime.datetime.strptime(s, "%H:%M:%S").time())]

test_anno_2 = """
>>> row = {"lat": "32.8321666666667", "lon": "-79.9338333333333", "date": "2012-11-27", "time": "09:15:00"}
>>> make_from_dict_a(Waypoint, row)
Waypoint(latitude=32.8321666666667, longitude=-79.9338333333333, date=datetime.date(2012, 11, 27), time=datetime.time(9, 15))
"""

@dataclass
class SomeNewClass2A(SomeNewClass2):
    new_field: Annotated[int, Source('column4')]

test_subclass_annotations = """
>>> row = {"column1": "x", "column2": "y", "column3": "z", "column4": "42"}
>>> make_from_dict_a(SomeNewClass2A, row)
SomeNewClass2A(a_field='x', a_conversion=SomeType('y'), complicated_conversion=Complicated('z'), new_field=42)
"""

from pydantic.fields import FieldInfo

def quality_check(some_class: type) -> None:
    assert some_class.__doc__, (
        "No class-level docstring for {some_class.__name__}"
    )
    attrs = get_type_hints(some_class, include_extras=True)
    for name, attribute in attrs.items():
        args = get_args(attribute)
        for arg_detail in args:
            match arg_detail:
                case FieldInfo() as field:
                    assert field.description, (
                        f"No Field description {some_class.__name__}.{name}"
                    )


from pydantic import BaseModel, Field

class Waypoint2(BaseModel):
    """A Waypoint on a voyage"""
    latitude: Annotated[
        float,
        Field(alias='lat', description="latitude of waypoint")]
    longitude: Annotated[
        float,
        Field(alias='lon', description="longitude of wayoiint")]
    date: Annotated[
        datetime.date,
        Field(alias='date')]
    time: Annotated[
        datetime.time,
        Field(alias='time', description="time of arrival in H:M:S format")]

test_wp2 = """
>>> row = {"lat": "32.8321666666667", "lon": "-79.9338333333333", "date": "2012-11-27", "time": "09:15:00"}
>>> wp = Waypoint2.model_validate(row)
>>> wp
Waypoint2(latitude=32.8321666666667, longitude=-79.9338333333333, date=datetime.date(2012, 11, 27), time=datetime.time(9, 15))

>>> quality_check(Waypoint2)
Traceback (most recent call last):
...
AssertionError: No Field description Waypoint2.date
"""

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
