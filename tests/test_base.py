# -*- coding: utf-8 -*-

import typing as T
import dataclasses

import pytest

from atlas_doc_parser.base import Base, T_BASE
from atlas_doc_parser.arg import REQ, NA
from atlas_doc_parser.exc import ParamError
from atlas_doc_parser.tests import check_seder


@dataclasses.dataclass
class Model1(Base):
    attr1: int = dataclasses.field(default_factory=REQ)
    attr2: int = dataclasses.field(default_factory=NA)


verbose = False


@dataclasses.dataclass
class Data(Base):
    value: int = dataclasses.field(default_factory=REQ)

    def special_data_method(self):
        if verbose:
            print("call special_data_method")


@dataclasses.dataclass
class Profile(Base):
    """
    firstname, lastname, ssn are generic data type field.
    """

    firstname: str = dataclasses.field(default_factory=REQ)
    lastname: str = dataclasses.field(default_factory=REQ)
    ssn: str = dataclasses.field(default_factory=REQ)

    def special_profile_method(self):
        if verbose:
            print("call special_profile_method")


@dataclasses.dataclass
class Degree(Base):
    name: str = dataclasses.field(default_factory=REQ)
    year: int = dataclasses.field(default_factory=REQ)

    def special_degree_method(self):
        if verbose:
            print("call special_degree_method")


@dataclasses.dataclass
class People(Base):
    """
    - ``profile`` is nested field.
    - ``degrees`` is collection type field.
    """

    # fmt: off
    id: int = dataclasses.field(default_factory=REQ)
    profile: T.Optional[Profile] = Profile.nested_field(default=None)
    degrees: T.Optional[T.List[Degree]] = Degree.list_of_nested_field(default_factory=list)
    # fmt: on

    def special_people_method(self):
        if verbose:
            print("call special_people_method")


@dataclasses.dataclass
class Record(Base):
    record_id: str = dataclasses.field(default_factory=REQ)


@dataclasses.dataclass
class Batch(Base):
    batch_id: str = dataclasses.field(default_factory=REQ)
    records: T.Dict[str, Record] = Record.map_of_nested_field(default_factory=REQ)


class TestBase:
    def test_model1(self):
        model1 = Model1(attr1=1)
        check_seder(model1)

        model1 = Model1(attr1=1, attr2=2)
        check_seder(model1)

        with pytest.raises(ParamError):
            model1 = Model1()

        model1 = Model1.from_dict(dict(attr1=1))
        check_seder(model1)

        model1 = Model1.from_dict(dict(attr1=1, attr2=2))
        check_seder(model1)

        with pytest.raises(ParamError):
            model1 = Model1.from_dict(dict())

        model1 = Model1.from_dict(dict(attr1=1, attr2=2, attr3=3))

    def test_nested(self):
        data = Data.from_dict({"value": 1})
        assert isinstance(data, Data)
        data.special_data_method()  # type hint OK

        data = Data.from_dict(Data(value=1))
        assert isinstance(data, Data)
        data.special_data_method()  # type hint OK

        data = Data.from_dict(None)
        assert data is None

        data_list = Data.from_list([{"value": 1}])
        assert isinstance(data_list[0], Data)
        data_list.copy()  # type hint OK
        data_list[0].special_data_method()  # type hint OK

        data_list = Data.from_list([Data(value=1)])
        assert isinstance(data_list[0], Data)
        data_list.copy()  # type hint OK
        data_list[0].special_data_method()  # type hint OK

        data_list = Data.from_list([None])
        assert data_list == [None]
        data_list.copy()  # type hint OK

        data_list = Data.from_list([{"value": 1}, Data(value=1), None])
        data_list[0].special_data_method()  # type hint OK
        data_list[1].special_data_method()  # type hint OK

    def test_nested_2(self):
        """
        nested value is None.
        """
        people = People(
            id=1,
            profile=None,
            degrees=None,
        )
        people_data = people.to_dict()
        people1 = People.from_dict(people_data)
        people1_data = people1.to_dict()
        assert people == people1
        assert people_data == people1_data

    def test_profile_degrees_default_value(self):
        people = People(id=1)
        assert people.profile is None
        assert people.degrees == list()

        people_data = people.to_dict()
        people1 = People.from_dict(people_data)
        assert people == people1
        assert people1.profile is None
        assert people1.degrees == list()


def test_nested_mapper():
    batch = Batch(
        batch_id="b-1",
        records={"r-1": Record(record_id="r-1")},
    )
    batch_data = batch.to_dict()
    batch1 = Batch.from_dict(batch_data)
    batch1_data = batch.to_dict()
    assert batch == batch1
    assert batch_data == batch1_data


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(__file__, "atlas_doc_parser.base", preview=False)
