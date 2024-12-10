from datetime import date, datetime
from typing import TYPE_CHECKING, Any

from ..filters import BaseFilter
from .model import GenericSession

if TYPE_CHECKING:
    from .db import GenericQueryManager
    from .interface import GenericInterface

__all__ = [
    "GenericBaseFilter",
    "GenericFilterStartsWith",
    "GenericFilterNotStartsWith",
    "GenericFilterEndsWith",
    "GenericFilterNotEndsWith",
    "GenericFilterContains",
    "GenericFilterIContains",
    "GenericFilterNotContains",
    "GenericFilterEqual",
    "GenericFilterNotEqual",
    "GenericFilterGreater",
    "GenericFilterSmaller",
    "GenericFilterGreaterEqual",
    "GenericFilterSmallerEqual",
    "GenericFilterIn",
    "GenericFilterConverter",
]


class GenericBaseFilter(BaseFilter):
    datamodel: "GenericInterface" = None
    query: "GenericQueryManager" = None

    def apply(self, session: GenericSession, col: str, value: Any) -> GenericSession:
        value = self._cast_value(col, value)
        return super().apply(session, col, value)


class GenericFilterStartsWith(GenericBaseFilter):
    name = "Starts with"
    arg_name = "sw"

    def apply(self, session: GenericSession, col: str, value: Any) -> GenericSession:
        value = self._cast_value(col, value)
        return session.starts_with(col, value)


class GenericFilterNotStartsWith(GenericBaseFilter):
    name = "Not Starts with"
    arg_name = "nsw"

    def apply(self, session: GenericSession, col: str, value: Any) -> GenericSession:
        value = self._cast_value(col, value)
        return session.not_starts_with(col, value)


class GenericFilterEndsWith(GenericBaseFilter):
    name = "Ends with"
    arg_name = "ew"

    def apply(self, session: GenericSession, col: str, value: Any) -> GenericSession:
        value = self._cast_value(col, value)
        return session.ends_with(col, value)


class GenericFilterNotEndsWith(GenericBaseFilter):
    name = "Not Ends with"
    arg_name = "new"

    def apply(self, session: GenericSession, col: str, value: Any) -> GenericSession:
        value = self._cast_value(col, value)
        return session.not_ends_with(col, value)


class GenericFilterContains(GenericBaseFilter):
    name = "Contains"
    arg_name = "ct"

    def apply(self, session: GenericSession, col: str, value: Any) -> GenericSession:
        value = self._cast_value(col, value)
        return session.like(col, value)


class GenericFilterIContains(GenericBaseFilter):
    name = "Contains (insensitive)"
    arg_name = "ict"

    def apply(self, session: GenericSession, col: str, value: Any) -> GenericSession:
        value = self._cast_value(col, value)
        return session.ilike(col, value)


class GenericFilterNotContains(GenericBaseFilter):
    name = "Not Contains"
    arg_name = "nct"

    def apply(self, session: GenericSession, col: str, value: Any) -> GenericSession:
        value = self._cast_value(col, value)
        return session.not_like(col, value)


class GenericFilterEqual(GenericBaseFilter):
    name = "Equal to"
    arg_name = "eq"

    def apply(
        self,
        session: GenericSession,
        col: str,
        value: str | bool | int | date | datetime,
    ) -> GenericSession:
        value = self._cast_value(col, value)
        return session.equal(col, value)


class GenericFilterNotEqual(GenericBaseFilter):
    name = "Not Equal to"
    arg_name = "neq"

    def apply(
        self,
        session: GenericSession,
        col: str,
        value: str | bool | int | date | datetime,
    ) -> GenericSession:
        value = self._cast_value(col, value)
        return session.not_equal(col, value)


class GenericFilterGreater(GenericBaseFilter):
    name = "Greater than"
    arg_name = "gt"

    def apply(
        self, session: GenericSession, col: str, value: int | date | datetime
    ) -> GenericSession:
        value = self._cast_value(col, value)
        return session.greater(col, value)


class GenericFilterSmaller(GenericBaseFilter):
    name = "Smaller than"
    arg_name = "lt"

    def apply(
        self, session: GenericSession, col: str, value: int | date | datetime
    ) -> GenericSession:
        value = self._cast_value(col, value)
        return session.smaller(col, value)


class GenericFilterGreaterEqual(GenericBaseFilter):
    name = "Greater equal"
    arg_name = "ge"

    def apply(
        self, session: GenericSession, col: str, value: int | date | datetime
    ) -> GenericSession:
        value = self._cast_value(col, value)
        return session.greater_equal(col, value)


class GenericFilterSmallerEqual(GenericBaseFilter):
    name = "Smaller equal"
    arg_name = "le"

    def apply(
        self, session: GenericSession, col: str, value: int | date | datetime
    ) -> GenericSession:
        value = self._cast_value(col, value)
        return session.smaller_equal(col, value)


class GenericFilterIn(GenericBaseFilter):
    name = "One of"
    arg_name = "in"

    def apply(
        self, session: GenericSession, col: str, value: list[str | bool | int]
    ) -> GenericSession:
        value = self._cast_value(col, value)
        return session.in_(col, value)


class GenericFilterConverter:
    """
    Helper class to get available filters for a generic column type.
    """

    conversion_table = (
        ("is_enum", [GenericFilterEqual, GenericFilterNotEqual, GenericFilterIn]),
        ("is_boolean", [GenericFilterEqual, GenericFilterNotEqual]),
        (
            "is_text",
            [
                GenericFilterStartsWith,
                GenericFilterNotStartsWith,
                GenericFilterEndsWith,
                GenericFilterNotEndsWith,
                GenericFilterContains,
                GenericFilterIContains,
                GenericFilterNotContains,
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterIn,
            ],
        ),
        (
            "is_string",
            [
                GenericFilterStartsWith,
                GenericFilterNotStartsWith,
                GenericFilterEndsWith,
                GenericFilterNotEndsWith,
                GenericFilterContains,
                GenericFilterIContains,
                GenericFilterNotContains,
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterIn,
            ],
        ),
        (
            "is_integer",
            [
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterGreater,
                GenericFilterSmaller,
                GenericFilterGreaterEqual,
                GenericFilterSmallerEqual,
                GenericFilterIn,
            ],
        ),
        (
            "is_date",
            [
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterGreater,
                GenericFilterSmaller,
                GenericFilterGreaterEqual,
                GenericFilterSmallerEqual,
                GenericFilterIn,
            ],
        ),
    )
