from datetime import date, datetime
from enum import Enum
from typing import Any, List, Type

from pydantic import EmailStr

from ..api import SQLAInterface
from .filters import GenericBaseFilter, GenericFilterConverter
from .model import GenericModel, GenericSession

__all__ = ["GenericInterface"]


class GenericInterface(SQLAInterface):
    """
    Represents an interface for a Generic model (Based on pydantic).
    """

    obj: Type[GenericModel]
    filter_converter: GenericFilterConverter = GenericFilterConverter()
    session: Type[GenericSession] = None
    with_fk: bool = True

    list_columns: dict[str, Any]
    list_properties: dict[str, Any]

    _filters: dict[str, list[GenericBaseFilter]] = None

    def __init__(self, obj: Type[GenericModel], session: Type[GenericSession]):
        if not isinstance(session, type):
            raise ValueError("session must be a class, do not instantiate it")
        self.session = session
        super().__init__(obj)

    def get_type(self, col: str, optional=False) -> Type:
        return self.obj.properties[col].col_type

    def get_type_name(self, col: str) -> str:
        if self.is_string(col):
            return "String"
        if self.is_integer(col):
            return "Integer"
        if self.is_boolean(col):
            return "Boolean"
        if self.is_date(col):
            return "DateTime"
        return "Raw"

    def _init_properties(self):
        """
        Initialize the properties of the object.

        This method initializes the properties of the object by creating a dictionary of the object's columns and their corresponding types.

        Returns:
            None
        """
        self._list_columns = self.obj.properties
        self._list_properties = self.obj.properties

    """
    ------------------------------
     FUNCTIONS FOR RELATED MODELS
    ------------------------------
    """

    def get_related_model(self, col_name: str) -> Type[GenericModel]:
        if self.is_relation(col_name):
            return self.list_properties[col_name].__class__

        raise ValueError(f"{col_name} is not a relation")

    """
    -------------
     GET METHODS
    -------------
    """

    def get_search_column_list(self) -> List[str]:
        return [x for x in self.obj.columns if not self.is_pk(x)]

    def get_file_column_list(self) -> List[str]:
        return []

    def get_image_column_list(self) -> List[str]:
        return []

    """
    -----------------------------------------
         FUNCTIONS for Testing TYPES
    -----------------------------------------
    """

    def is_image(self, col_name: str) -> bool:
        return False

    def is_file(self, col_name: str) -> bool:
        return False

    def is_string(self, col_name: str) -> bool:
        return (
            self.obj.properties[col_name].col_type == str
            or self.obj.properties[col_name].col_type == EmailStr
        )

    def is_text(self, col_name: str) -> bool:
        return self.is_string(col_name)

    def is_binary(self, col_name: str) -> bool:
        return False

    def is_integer(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == int

    def is_numeric(self, col_name: str) -> bool:
        return self.is_integer(col_name)

    def is_float(self, col_name: str) -> bool:
        return self.is_integer(col_name)

    def is_boolean(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == bool

    def is_date(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == date or self.is_datetime(
            col_name
        )

    def is_datetime(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == datetime

    def is_enum(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == Enum

    def is_json(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == dict

    def is_relation(self, col_name: str) -> bool:
        return self.is_relation_one_to_one(col_name) or self.is_relation_one_to_many(
            col_name
        )

    def is_relation_many_to_one(self, col_name: str) -> bool:
        # TODO: AS OF NOW, cant detect
        return False

    def is_relation_many_to_many(self, col_name: str) -> bool:
        # TODO: AS OF NOW, cant detect
        return False

    def is_relation_many_to_many_special(self, col_name: str) -> bool:
        return False

    def is_relation_one_to_one(self, col_name: str) -> bool:
        return isinstance(self.list_properties[col_name], GenericModel)

    def is_relation_one_to_many(self, col_name: str) -> bool:
        if not isinstance(self.list_properties[col_name], list):
            return False
        for prop in self.list_properties[col_name]:
            if not isinstance(prop, GenericModel):
                return False

        return True

    def is_pk_composite(self) -> bool:
        return False

    def is_fk(self, col_name: str) -> bool:
        return False

    def get_max_length(self, col_name: str) -> int:
        return -1
