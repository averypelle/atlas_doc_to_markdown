# -*- coding: utf-8 -*-

import typing as T
import enum
import dataclasses

from .arg import REQ, rm_na
from .exc import ParamError


class MetadataKeyEnum(str, enum.Enum):
    CONVERTER = "_better_dataclass_converter"


T_DATA = T.Dict[str, T.Any]
T_FIELDS = T.Dict[str, dataclasses.Field]

_class_fields: T.Dict[T.Any, T_FIELDS] = {}  # class fields cache
T_DATA_LIKE = T.Union[T_DATA, "T_BASE", None]


@dataclasses.dataclass
class Base:
    @classmethod
    def get_fields(cls) -> T_FIELDS:
        """
        Get the dict view of the ``dataclasses.Field`` in this class.
        It leverages the cache to avoid the overhead of ``dataclasses.fields``
        function call.
        """
        try:
            return _class_fields[cls]
        except KeyError:
            _class_fields[cls] = {
                field.name: field for field in dataclasses.fields(cls)
            }
            return _class_fields[cls]

    def to_dict(
        self,
    ) -> T.Dict[str, T.Any]:
        dct = dataclasses.asdict(self)
        return rm_na(**dct)

    def _validate(self):
        for field in dataclasses.fields(self.__class__):
            if field.init:
                k = field.name
                if isinstance(getattr(self, k), REQ):  # pragma: no cover
                    raise ParamError(f"Field {k!r} is required for {self.__class__}.")

    def __post_init__(self):
        self._validate()

    @classmethod
    def from_dict(
        cls,
        dct_or_obj: T_DATA_LIKE,
    ) -> T.Optional["Base"]:
        """
        Construct an instance from dataclass-like data.
        It could be a dictionary, an instance of this class, or None.
        """
        if isinstance(dct_or_obj, dict):
            _fields = cls.get_fields()
            kwargs = {}
            for field_name, field in _fields.items():
                if field_name in dct_or_obj:
                    v = dct_or_obj[field_name]
                    if MetadataKeyEnum.CONVERTER.value in field.metadata:
                        kwargs[field_name] = field.metadata[MetadataKeyEnum.CONVERTER](
                            v
                        )
                    else:
                        kwargs[field_name] = v
            return cls(**kwargs)
        elif isinstance(dct_or_obj, cls):
            return dct_or_obj
        elif dct_or_obj is None:
            return None
        else:  # pragma: no cover
            raise TypeError(f"Unknown type {dct_or_obj.__class__.__name__}")

    @classmethod
    def from_list(
        cls: T.Type["T_BASE"],
        list_of_dct_or_obj: T.Optional[T.List[T_DATA_LIKE]],
    ) -> T.Optional[T.List[T.Optional["T_BASE"]]]:
        """
        Construct list of instance from list of dataclass-like data.
        It could be a dictionary, an instance of this class, or None.
        """
        if isinstance(list_of_dct_or_obj, list):
            return [cls.from_dict(item) for item in list_of_dct_or_obj]
        elif list_of_dct_or_obj is None:
            return None
        else:  # pragma: no cover
            raise TypeError

    @classmethod
    def _from_mapper(
        cls: T.Type["T_BASE"],
        map_of_dct_or_obj: T.Optional[T.Dict[str, T_DATA_LIKE]],
    ) -> T.Optional[T.Dict[str, T.Optional["T_BASE"]]]:
        """
        Construct dict of instance from dict of dataclass-like data.
        It could be a dictionary, an instance of this class, or None.
        """
        if isinstance(map_of_dct_or_obj, dict):
            return {k: cls.from_dict(v) for k, v in map_of_dct_or_obj.items()}
        elif map_of_dct_or_obj is None:
            return None
        else:  # pragma: no cover
            raise TypeError

    @classmethod
    def nested_field(
        cls,
        default=dataclasses.MISSING,
        default_factory=dataclasses.MISSING,
        init=True,
        repr=True,
        hash=None,
        compare=True,
        metadata=None,
        **kwargs,
    ):
        """
        Declare a field that is another dataclass.
        """
        if metadata is None:
            metadata = {}
        metadata[MetadataKeyEnum.CONVERTER.value] = cls.from_dict
        params = dict(
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=metadata,
        )
        if default is not dataclasses.MISSING:
            params["default"] = default
        if default_factory is not dataclasses.MISSING:
            params["default_factory"] = default_factory
        params.update(kwargs)
        return dataclasses.field(**params)

    @classmethod
    def list_of_nested_field(
        cls,
        default=dataclasses.MISSING,
        default_factory=dataclasses.MISSING,
        init=True,
        repr=True,
        hash=None,
        compare=True,
        metadata=None,
        **kwargs,
    ):
        """
        Declare a field that is a list of other dataclass.
        """
        if metadata is None:
            metadata = {}
        metadata[MetadataKeyEnum.CONVERTER.value] = cls.from_list
        params = dict(
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=metadata,
        )
        if default is not dataclasses.MISSING:
            params["default"] = default
        if default_factory is not dataclasses.MISSING:
            params["default_factory"] = default_factory
        params.update(kwargs)
        return dataclasses.field(**params)

    @classmethod
    def map_of_nested_field(
        cls,
        default=dataclasses.MISSING,
        default_factory=dataclasses.MISSING,
        init=True,
        repr=True,
        hash=None,
        compare=True,
        metadata=None,
        **kwargs,
    ):
        """
        Declare a field that is a list of other dataclass.
        """
        if metadata is None:
            metadata = {}
        metadata[MetadataKeyEnum.CONVERTER.value] = cls._from_mapper
        params = dict(
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=metadata,
        )
        if default is not dataclasses.MISSING:
            params["default"] = default
        if default_factory is not dataclasses.MISSING:
            params["default_factory"] = default_factory
        params.update(kwargs)
        return dataclasses.field(**params)


T_BASE = T.TypeVar("T_BASE", bound=Base)
