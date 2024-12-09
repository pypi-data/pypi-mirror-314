import enum
from datetime import date, datetime
from typing import Annotated, Any, List, Literal, Optional, Tuple, Type, overload

import marshmallow_sqlalchemy
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    create_model,
)
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import SynonymProperty, class_mapper
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty
from sqlalchemy.sql import sqltypes as sa_types
from sqlalchemy_utils.types.uuid import UUIDType

from ..db import (
    AsyncSession,
    QueryManager,
    Session,
)
from ..filters import BaseFilter, SQLAFilterConverter
from ..globals import g
from ..models import Model
from ..schemas import PRIMARY_KEY, DatetimeUTC, QuerySchema
from ..types import FileColumn, ImageColumn
from ..utils import is_sqla_type

__all__ = ["Params", "SQLAInterface"]


class Params(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: PRIMARY_KEY | None = None
    ids: List[PRIMARY_KEY] | None = None
    q: QuerySchema | None = None
    query: QueryManager | None = None
    session: AsyncSession | Session | None = None
    body: BaseModel | None = None
    item: Model | Any | None = None
    items: List[Model | Any] | None = None
    extra: Any | None = None


class P_ID(Params):
    id: PRIMARY_KEY


class P_IDS(Params):
    ids: List[PRIMARY_KEY]


class P_Q(Params):
    q: QuerySchema


class P_QUERY(Params):
    query: QueryManager


class P_SESSION(Params):
    session: AsyncSession | Session


class P_BODY(Params):
    body: BaseModel


class P_ITEM(Params):
    item: Model | Any


class P_ITEMS(Params):
    items: List[Model | Any]


class PARAM_Q_QUERY(P_Q, P_QUERY):
    pass


class PARAM_IDS_Q_QUERY_SESSION_ITEMS(P_IDS, P_Q, P_QUERY, P_SESSION, P_ITEMS):
    pass


class PARAM_ID_QUERY_SESSION(P_ID, P_QUERY, P_SESSION):
    pass


class PARAM_ID_QUERY_SESSION_ITEM(P_ID, P_QUERY, P_SESSION, P_ITEM):
    pass


class PARAM_BODY_QUERY_SESSION(P_BODY, P_QUERY, P_SESSION):
    pass


class SQLAInterface:
    """
    Represents an interface for a SQLAlchemy model. It provides methods for creating a pydantic schema for the model, as well as for testing the types of the model's columns.
    """

    obj: Type[Model]
    filter_converter: SQLAFilterConverter = SQLAFilterConverter()
    with_fk: bool

    _id_schema: dict[str, type] = {}
    _schema: Type[BaseModel] = None
    _schema_optional: Type[BaseModel] = None
    _list_columns: dict[str, Column] = None
    _list_properties: dict[str, Column] = None
    _filters: dict[str, list[BaseFilter]] = None
    _cache_schema: dict[str, Type[BaseModel]] = {}
    _cache_field: dict[str, str] = {}

    def __init__(self, obj: Type[Model], with_fk: bool = True):
        self.obj = obj
        self.with_fk = with_fk

    def generate_schema(
        self,
        columns: List[str] | None = None,
        with_name_=True,
        with_id_=True,
        optional=False,
        name: str | None = None,
        hide_sensitive_columns=True,
    ) -> Type[BaseModel]:
        """
        Generate a Pydantic schema based on the object's properties.

        Args:
            columns (List[str], optional): A list of columns to include in the schema. Returns an empty schema if not specified. Defaults to None.
            with_name_ (bool, optional): Whether to include the name_ column. Defaults to True.
            with_id_ (bool, optional): Whether to include the id_ column. Defaults to True.
            optional (bool, optional): Whether the columns should be optional. Required for PUT or PATCH requests. Defaults to False.
            name (str, optional): The name of the schema. Defaults to None.
            hide_sensitive_columns (bool, optional): Whether to hide sensitive columns. Defaults to True.

        Returns:
            BaseModel: The Pydantic schema for the object.
        """
        schema_dict = {
            "__config__": ConfigDict(from_attributes=True),
        }
        model_name = f"{self.obj.__name__}-Schema"
        if columns:
            model_name += f"-{'-'.join(columns)}"
        if with_name_:
            model_name += "-WithName"
            schema_dict["name_"] = (str, Field())
        if with_id_:
            model_name += "-WithID"
            schema_dict["id_"] = (PRIMARY_KEY, Field())
        if optional:
            model_name += "-Optional"
        if hide_sensitive_columns:
            model_name += "-HideSensitive"
        if self.with_fk:
            model_name += "-WithFK"
        model_name = name or model_name
        if model_name in self._cache_schema:
            return self._cache_schema[model_name]

        if not columns:
            self._cache_schema[model_name] = create_model(model_name, **schema_dict)
            return self._cache_schema[model_name]

        columns_to_generate = list(columns)
        if hide_sensitive_columns:
            sensitive_columns = g.sensitive_data.get(self.obj.__name__, [])
            columns_to_generate = [
                col for col in columns if col not in sensitive_columns
            ]

        self._generate_schema_properties(
            columns_to_generate, optional, schema_dict, self.with_fk
        )

        if self.is_pk_composite():
            self.id_schema = str

        self._cache_schema[model_name] = create_model(model_name, **schema_dict)
        return self._cache_schema[model_name]

    def get_type(
        self, col: str, optional: bool = False, related_columns: list[str] = None
    ):
        """
        Get the Python type corresponding to the specified column name.

        Args:
            col (str): The name of the column.
            optional (bool, optional): Whether the column should be optional. Only works for related models. Defaults to False.

        Returns:
            Type: The Python type corresponding to the column.

        """
        if self.is_enum(col):
            col_type = None
            enum_val = self.get_enum_value(col)
            enum_values = list(enum_val)

            for val in enum_values:
                new_val = Literal[val]  # type: ignore
                if isinstance(val, enum.Enum):
                    new_val = (
                        new_val
                        | Annotated[
                            Literal[val.value], AfterValidator(lambda x: enum_val(x))  # type: ignore
                        ]
                    )
                if col_type is None:
                    col_type = new_val
                else:
                    col_type = col_type | new_val
            return col_type
        elif self.is_text(col) or self.is_string(col):
            return str
        elif self.is_integer(col) or self.is_numeric(col) or self.is_float(col):
            return int | float
        elif self.is_boolean(col):
            return bool
        elif self.is_date(col):
            return date
        elif self.is_datetime(col):
            return DatetimeUTC | datetime
        elif self.is_geometry(col):
            from geoalchemy2 import Geometry

            return Geometry
        elif self.is_relation(col):
            related_interface = self.get_related_interface(col, with_fk=False)
            if related_columns:
                schema = related_interface.generate_schema(
                    related_columns,
                    with_name_=False,
                    with_id_=False,
                )
            else:
                schema = (
                    related_interface.schema
                    if not optional
                    else related_interface.schema_optional
                )
            if self.is_relation_one_to_one(col) or self.is_relation_many_to_one(col):
                return schema
            return list[schema]
        else:
            return Any

    def get_type_name(self, col: str) -> str:
        """
        Get the name of the Python type corresponding to the specified column name.

        Args:
            col (str): The name of the column.

        Returns:
            str: The name of the Python type corresponding to the column.

        """
        cache_key = f"{self.obj.__name__}.{col}"
        if not self._cache_field.get(cache_key):
            # Check for geometry
            if self.is_geometry(col):
                self._cache_field[cache_key] = "Geometry"
            elif self.is_enum(col):
                self._cache_field[cache_key] = "Enum"
            else:
                self._cache_field[cache_key] = marshmallow_sqlalchemy.field_for(
                    self.obj, col
                ).__class__.__name__
        return self._cache_field[cache_key]

    def get_pk_attr(self) -> str:
        """
        Returns the name of the primary key attribute for the object.

        Returns:
            str: The name of the primary key attribute.
        """
        for key in self.list_columns.keys():
            if self.is_pk(key):
                return key

    def get_pk_attrs(self) -> List[str]:
        """
        Returns the names of the primary key attributes for the object.

        Returns:
            List[str]: The names of the primary key attributes.
        """
        return [key for key in self.list_columns.keys() if self.is_pk(key)]

    def _init_properties(self):
        """
        Initialize the properties of the object.

        This method initializes the properties of the object by creating a dictionary of the object's columns and their corresponding types.

        Returns:
            None
        """
        self._list_columns = dict()
        self._list_properties = dict()
        for prop in class_mapper(self.obj).iterate_properties:
            if type(prop) is not SynonymProperty:
                self._list_properties[prop.key] = prop
        for col_name in self.obj.__mapper__.columns.keys():
            if col_name in self._list_properties:
                self._list_columns[col_name] = self.obj.__mapper__.columns[col_name]

    def _init_filters(self):
        """
        Initializes the filters dictionary by iterating over the keys of the `list_properties` dictionary.
        For each key, it checks if the class has the corresponding attribute specified in the `conversion_table`
        of the `filter_converter` object. If the attribute exists, it adds the corresponding filters to the
        `_filters` dictionary.

        Parameters:
            None

        Returns:
            None
        """
        self._filters = dict()
        for col in self.list_properties.keys():
            for func_attr, filters in self.filter_converter.conversion_table:
                if getattr(self, func_attr)(col):
                    self._filters[col] = filters
                    break

    """
    ------------------------------
     FUNCTIONS FOR PROPERTIES
    ------------------------------
    """

    @property
    def id_schema(self):
        if not self._id_schema.get(self.obj.__name__):
            pk_type = int | float
            pk_attr = self.get_pk_attr()
            if self.is_pk_composite() or self.is_string(pk_attr):
                pk_type = str
            self._id_schema[self.obj.__name__] = pk_type
        return self._id_schema[self.obj.__name__]

    @id_schema.setter
    def id_schema(self, value: type):
        self._id_schema[self.obj.__name__] = value

    @property
    def schema(self) -> Type[BaseModel]:
        """
        The pydantic schema for the model. This is the standard schema. If the field is optional, it will be set to None as default.
        """
        if not self._schema:
            self._schema = self.generate_schema(self.list_properties.keys())
        return self._schema

    @schema.setter
    def schema(self, value: Type[BaseModel]):
        self._schema = value

    @property
    def schema_optional(self) -> Type[BaseModel]:
        """
        The pydantic schema for the model. This is the standard schema, but all fields are optional. Useful for POST and PUT requests.
        """
        if not self._schema_optional:
            self._schema_optional = self.generate_schema(
                self.list_properties.keys(), optional=True
            )
        return self._schema_optional

    @schema_optional.setter
    def schema_optional(self, value: Type[BaseModel]):
        self._schema_optional = value

    @property
    def list_columns(self) -> dict[str, Column]:
        if not self._list_columns:
            self._init_properties()
        return self._list_columns

    @list_columns.setter
    def list_columns(self, value: dict[str, Column]):
        self._list_columns = value

    @property
    def list_properties(self) -> dict[str, Column]:
        if not self._list_properties:
            self._init_properties()
        return self._list_properties

    @list_properties.setter
    def list_properties(self, value: dict[str, Column]):
        self._list_properties = value

    @property
    def filters(self) -> dict[str, list[BaseFilter]]:
        if not self._filters:
            self._init_filters()
        return self._filters

    @filters.setter
    def filters(self, value: dict[str, list[BaseFilter]]):
        self._filters = value

    """
    -----------------------------------------
            CONVERSION FUNCTIONS
    -----------------------------------------
    """

    @overload
    def convert_to_result(self, data: Model) -> Tuple[PRIMARY_KEY, Model]: ...
    @overload
    def convert_to_result(
        self, data: List[Model]
    ) -> Tuple[List[PRIMARY_KEY], List[Model]]: ...
    def convert_to_result(self, data: Model | List[Model]):
        """
        Converts the given data to a result tuple.

        Args:
            data (Model | List[Model]): The data to be converted.

        Returns:
            tuple: A tuple containing the primary key(s) and the converted data.

        """
        if isinstance(data, list):
            pks: PRIMARY_KEY = (
                [getattr(item, self.get_pk_attr()) for item in data]
                if not self.is_pk_composite()
                else [
                    [str(getattr(item, key)) for key in self.get_pk_attrs()]
                    for item in data
                ]
            )
        else:
            pks: PRIMARY_KEY = (
                getattr(data, self.get_pk_attr())
                if not self.is_pk_composite()
                else [str(getattr(data, key)) for key in self.get_pk_attrs()]
            )

        return (pks, data)

    """
    ------------------------------
     FUNCTIONS FOR RELATED MODELS
    ------------------------------
    """

    def get_col_default(self, col_name: str) -> Any:
        default = getattr(self.list_columns[col_name], "default", None)
        if default is None:
            return None

        value = getattr(default, "arg", None)
        if value is None:
            return None

        if getattr(default, "is_callable", False):
            return lambda: default.arg(None)

        if not getattr(default, "is_scalar", True):
            return None

        return value

    def get_related_model(self, col_name: str) -> Type[Model]:
        return self.list_properties[col_name].mapper.class_

    def get_related_interface(self, col_name: str, with_fk: bool | None = None):
        return self.__class__(self.get_related_model(col_name), with_fk)

    def get_related_fk(self, model: Type[Model]) -> Optional[str]:
        for col_name in self.list_properties.keys():
            if self.is_relation(col_name):
                if model == self.get_related_model(col_name):
                    return col_name
        return None

    def get_related_fks(self) -> List[str]:
        return [
            self.get_related_fk(model)
            for model in self.list_properties.values()
            if self.is_relation(model)
        ]

    def get_fk_column(self, relationship_name: str) -> str:
        """
        Get the foreign key column for the specified relationship.

        Args:
            relationship_name (str): The name of the relationship.

        Raises:
            Exception: If no foreign key is found for the specified relationship.

        Returns:
            str: The name of the foreign key column.
        """
        # Get the relationship property from the model's mapper
        relationship_prop = class_mapper(self.obj).relationships[relationship_name]

        # Iterate through the columns involved in the relationship
        for local_column, _ in relationship_prop.local_remote_pairs:
            # Check if the local column is the foreign key
            if local_column.foreign_keys:
                return local_column.name

        raise Exception(
            f"No foreign key found for relationship '{relationship_name}' in model '{self.obj.__name__}'."
        )

    def get_info(self, col_name: str):
        if col_name in self.list_properties:
            return self.list_properties[col_name].info
        return {}

    """
    -------------
     GET METHODS
    -------------
    """

    def get_column_list(self) -> List[str]:
        """
        Returns all model's columns on SQLA properties
        """
        return list(self.list_properties.keys())

    def get_user_column_list(self) -> List[str]:
        """
        Returns all model's columns except pk or fk
        """
        return [
            col_name
            for col_name in self.get_column_list()
            if (not self.is_pk(col_name)) and (not self.is_fk(col_name))
        ]

    def get_property_column_list(self) -> List[str]:
        """
        Returns all model's columns that have @property decorator and is public
        """
        self_dict = vars(self.obj)
        return [
            key
            for key in self_dict.keys()
            if self.is_property(key) and not key.startswith("_")
        ]

    def get_search_column_list(self) -> List[str]:
        ret_lst = []
        for col_name in self.get_column_list():
            if not self.is_relation(col_name):
                tmp_prop = self.get_property_first_col(col_name).name
                if (
                    (not self.is_pk(tmp_prop))
                    and (not self.is_fk(tmp_prop))
                    and (not self.is_image(col_name))
                    and (not self.is_file(col_name))
                ):
                    ret_lst.append(col_name)
            else:
                ret_lst.append(col_name)
        return ret_lst

    def get_order_column_list(
        self, list_columns: List[str] = None, depth=0
    ) -> List[str]:
        """
        Get all columns that can be used for ordering

        Args:
            list_columns (List[str], optional): Columns to be used for ordering. Defaults to None.
            depth (int, optional): Depth of the relation. Defaults to 0. Used for recursive calls.

        Returns:
            List[str]: List of columns that can be used for ordering
        """
        ret_lst = []
        list_columns = list_columns or self.get_column_list()

        for col_name in list_columns:
            if "." in col_name:
                col_name, sub_col_name = col_name.split(".")
            else:
                sub_col_name = ""
            if self.is_relation(col_name):
                if (
                    depth > 0
                    or self.is_relation_one_to_many(col_name)
                    or self.is_relation_many_to_many(col_name)
                ):
                    continue
                related_interface = self.get_related_interface(col_name)
                sub_order_columns = related_interface.get_order_column_list(
                    depth=depth + 1
                )
                if sub_col_name:
                    sub_order_columns = [
                        x for x in sub_order_columns if x == sub_col_name
                    ]

                ret_lst.extend(
                    [f"{col_name}.{sub_col}" for sub_col in sub_order_columns]
                )
                continue

            if self.is_property(col_name):
                continue

            if hasattr(self.obj, col_name):
                attribute = getattr(self.obj, col_name)
                if not callable(attribute) or hasattr(attribute, "_col_name"):
                    ret_lst.append(col_name)
            else:
                ret_lst.append(col_name)

        return ret_lst

    def get_file_column_list(self) -> List[str]:
        return [
            i.name
            for i in self.obj.__mapper__.columns
            if isinstance(i.type, FileColumn)
        ]

    def get_image_column_list(self) -> List[str]:
        return [
            i.name
            for i in self.obj.__mapper__.columns
            if isinstance(i.type, ImageColumn)
        ]

    def get_enum_value(self, col_name: str) -> enum.EnumType | list[str]:
        col_type = self.list_columns[col_name].type
        if isinstance(col_type.python_type, enum.EnumType):
            return col_type.python_type
        return col_type.enums

    def get_property_first_col(self, col_name: str) -> ColumnProperty:
        # support for only one col for pk and fk
        return self.list_properties[col_name].columns[0]

    def get_relation_fk(self, col_name: str) -> Column:
        # support for only one col for pk and fk
        return list(self.list_properties[col_name].local_columns)[0]

    """
    -----------------------------------------
         FUNCTIONS for Testing TYPES
    -----------------------------------------
    """

    def is_image(self, col_name: str) -> bool:
        try:
            return isinstance(self.list_columns[col_name].type, ImageColumn)
        except KeyError:
            return False

    def is_file(self, col_name: str) -> bool:
        try:
            return isinstance(self.list_columns[col_name].type, FileColumn)
        except KeyError:
            return False

    def is_string(self, col_name: str) -> bool:
        try:
            return (
                is_sqla_type(self.list_columns[col_name].type, sa_types.String)
                or self.list_columns[col_name].type.__class__ == UUIDType
            )
        except KeyError:
            return False

    def is_text(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Text)
        except KeyError:
            return False

    def is_binary(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.LargeBinary)
        except KeyError:
            return False

    def is_integer(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Integer)
        except KeyError:
            return False

    def is_numeric(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Numeric)
        except KeyError:
            return False

    def is_float(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Float)
        except KeyError:
            return False

    def is_boolean(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Boolean)
        except KeyError:
            return False

    def is_date(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Date)
        except KeyError:
            return False

    def is_datetime(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.DateTime)
        except KeyError:
            return False

    def is_enum(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Enum)
        except KeyError:
            return False

    def is_json(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.JSON)
        except KeyError:
            return False

    def is_jsonb(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, postgresql.JSONB)
        except KeyError:
            return False

    def is_geometry(self, col_name: str) -> bool:
        try:
            from geoalchemy2 import Geometry

            return is_sqla_type(self.list_columns[col_name].type, Geometry)
        except KeyError:
            return False
        except ImportError:
            return False

    def is_relation(self, col_name: str) -> bool:
        try:
            return isinstance(self.list_properties[col_name], RelationshipProperty)
        except KeyError:
            return False

    def is_relation_many_to_one(self, col_name: str) -> bool:
        try:
            if self.is_relation(col_name):
                return self.list_properties[col_name].direction.name == "MANYTOONE"
            return False
        except KeyError:
            return False

    def is_relation_many_to_many(self, col_name: str) -> bool:
        try:
            if self.is_relation(col_name):
                relation = self.list_properties[col_name]
                return relation.direction.name == "MANYTOMANY"
            return False
        except KeyError:
            return False

    def is_relation_many_to_many_special(self, col_name: str) -> bool:
        try:
            if self.is_relation(col_name):
                relation = self.list_properties[col_name]
                return relation.direction.name == "ONETOONE" and relation.uselist
            return False
        except KeyError:
            return False

    def is_relation_one_to_one(self, col_name: str) -> bool:
        try:
            if self.is_relation(col_name):
                relation = self.list_properties[col_name]
                return self.list_properties[col_name].direction.name == "ONETOONE" or (
                    relation.direction.name == "ONETOMANY" and relation.uselist is False
                )
            return False
        except KeyError:
            return False

    def is_relation_one_to_many(self, col_name: str) -> bool:
        try:
            if self.is_relation(col_name):
                relation = self.list_properties[col_name]
                return relation.direction.name == "ONETOMANY" and relation.uselist
            return False
        except KeyError:
            return False

    def is_nullable(self, col_name: str) -> bool:
        if self.is_relation_many_to_one(col_name):
            col = self.get_relation_fk(col_name)
            return col.nullable
        elif self.is_relation_many_to_many(col_name) or self.is_relation_one_to_many(
            col_name
        ):
            return True
        try:
            return self.list_columns[col_name].nullable
        except KeyError:
            return False

    def is_unique(self, col_name: str) -> bool:
        try:
            return self.list_columns[col_name].unique is True
        except KeyError:
            return False

    def is_pk(self, col_name: str) -> bool:
        try:
            return self.list_columns[col_name].primary_key
        except KeyError:
            return False

    def is_pk_composite(self) -> bool:
        return len(self.obj.__mapper__.primary_key) > 1

    def is_fk(self, col_name: str) -> bool:
        try:
            return self.list_columns[col_name].foreign_keys
        except KeyError:
            return False

    def is_property(self, col_name: str) -> bool:
        return hasattr(getattr(self.obj, col_name, None), "fget")

    def is_function(self, col_name: str) -> bool:
        return hasattr(getattr(self.obj, col_name, None), "__call__")

    def get_max_length(self, col_name: str) -> int:
        try:
            if self.is_enum(col_name):
                return -1
            col = self.list_columns[col_name]
            if col.type.length:
                return col.type.length
            else:
                return -1
        except Exception:
            return -1

    def _generate_schema_properties(
        self,
        columns: List[str],
        optional: bool,
        schema_dict: dict[str, Any],
        with_fk: bool,
    ):
        """
        Generate schema properties based on the given columns and options.

        Args:
            columns (List[str]): The list of columns to include in the schema properties.
            optional (bool): Flag indicating whether the properties should be optional.
            schema_dict (dict[str, Any]): The dictionary to store the generated schema properties.
            with_fk (bool): Flag indicating whether to include relationships in the schema properties.

        Returns:
            None
        """
        prop_dict = self.list_properties if with_fk else self.list_columns
        limited_rel_col = {}
        for key in columns:
            # Ignore fk
            if self.is_fk(key):
                continue

            # Check for related models
            sub_key = ""
            if "." in key:
                key, sub_key = key.split(".")

            # Get column from properties
            column = prop_dict.get(key, None)

            # If column is not found, check if it is a property
            if column is None:
                if self.is_property(key):
                    schema_dict[key] = (Any, Field(default=None))
                continue

            params = {}
            type = self.get_type(key, optional)

            if sub_key and key not in columns:
                if not limited_rel_col.get(key):
                    limited_rel_col[key] = []
                limited_rel_col[key].append(sub_key)
                type = self.get_type(key, optional, limited_rel_col[key])

            # Check if it is 'Geometry' type
            try:
                from geoalchemy2 import Geometry

                if type == Geometry:
                    geo_col = self.list_columns[key]
                    type = Annotated[
                        dict[str, Any] | str,
                        BeforeValidator(
                            g.geometry_converter.two_way_converter_generator(
                                geo_col.type.geometry_type
                            )
                        ),
                    ]
            except ImportError:
                pass

            if hasattr(column, "primary_key") and column.primary_key:
                self.id_schema = type
            if self.is_nullable(key) or optional:
                params["default"] = None
                type = type | None
            if self.get_max_length(key) != -1:
                params["max_length"] = self.get_max_length(key)
            schema_dict[key] = (type, Field(**params))
