import operator
from datetime import date, datetime
from typing import Any, Callable, Generic, List, Optional, Self, Type, TypeVar, overload

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    create_model,
    model_validator,
)

from ..model import BasicModel
from ..schemas import PRIMARY_KEY
from .exceptions import (
    ColumnInvalidTypeException,
    ColumnNotExistException,
    ColumnNotSetException,
    GenericColumnException,
    MultipleColumnsException,
    PKMissingException,
    PKMultipleException,
)

__all__ = ["GenericColumn", "GenericModel", "GenericSession"]


class ColumnPlaceholder:
    def __repr__(self) -> str:
        return str(None)


class PKAutoIncrement(ColumnPlaceholder):
    pass


class NoDefault(ColumnPlaceholder):
    pass


T = TypeVar("T")


class GenericProperty(Generic[T]):
    col_type: Type[T]
    primary_key: bool
    auto_increment: bool
    unique: bool
    nullable: bool
    default: T | NoDefault


class PydanticGenericColumn(BaseModel, GenericProperty[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    col_type: T
    primary_key: bool
    auto_increment: bool
    unique: bool
    nullable: bool
    default: T | NoDefault

    @model_validator(mode="after")
    def check_column(self) -> Self:
        if self.primary_key and not isinstance(self.default, NoDefault):
            raise GenericColumnException(
                self, "Primary key columns cannot have a default value"
            )

        if not self.primary_key and self.auto_increment:
            raise GenericColumnException(
                self, "Auto increment can only be set on primary key columns"
            )

        if self.auto_increment and self.col_type != int:
            raise GenericColumnException(
                self, "Primary key with auto increment must be of type int"
            )

        if self.primary_key:
            self.unique = True
            self.nullable = False

        return self


class GenericColumn(GenericProperty[T]):
    """
    A generic column for a generic model. This works similar to a SQLAlchemy column.
    """

    validation_model: BaseModel = None
    _col_name: str = None

    def __init__(
        self,
        col_type: Type[T],
        *,
        primary_key: bool = False,
        auto_increment: bool = False,
        unique: bool = False,
        nullable: bool = True,
        default: T | NoDefault = NoDefault(),
    ):
        """
        GenericColumn constructor. This works similar to a SQLAlchemy column.

        Args:
            col_type (Type[T]): The type of the column.
            primary_key (bool, optional): Whether the column is a primary key. Defaults to False.
            auto_increment (bool, optional): Whether the column is auto incremented. Only works if the column is a primary key. Defaults to False.
            unique (bool, optional): Whether the column is unique. Defaults to False.
            nullable (bool, optional): Whether the column is nullable. Defaults to True.
            default (T | NoDefault, optional): The default value of the column. Will be used if the column is not set by the user. Defaults to NoDefault (no default value).
        """
        model = PydanticGenericColumn(
            col_type=col_type,
            primary_key=primary_key,
            auto_increment=auto_increment,
            unique=unique,
            nullable=nullable,
            default=default,
        )
        self.col_type = model.col_type
        self.primary_key = model.primary_key
        self.auto_increment = model.auto_increment
        self.unique = model.unique
        self.nullable = model.nullable
        self.default = model.default
        # TODO: Handle self.unique

    @overload
    def __get__(
        self, instance: None, owner: Type["GenericModel"]
    ) -> "GenericColumn": ...
    @overload
    def __get__(
        self, instance: "GenericModel", owner: Type["GenericModel"]
    ) -> T | None: ...
    def __get__(self, instance: Optional["GenericModel"], owner: Type["GenericModel"]):
        if not instance:
            return self

        value: T | NoDefault = instance.__dict__.get(f"_{self._col_name}", NoDefault())
        if not isinstance(value, NoDefault):
            return value
        if self.nullable:
            return None
        if self.primary_key and self.auto_increment:
            return PKAutoIncrement()
        return self.default

    def __set__(self, instance: "GenericModel", value: T | NoDefault) -> None:
        try:
            validated = self.validation_model.model_validate({self._col_name: value})
        except ValidationError as e:
            raise ColumnInvalidTypeException(
                instance, f"Invalid type for column {self._col_name}, {str(e)}"
            )
        instance.__dict__[f"_{self._col_name}"] = getattr(validated, self._col_name)

    def __set_name__(self, owner: Type["GenericModel"], name: str) -> None:
        self._col_name = name

        # Create pydantic model for validation
        validation_type = self.col_type
        if self.nullable:
            validation_type = validation_type | None
        if not isinstance(self.default, NoDefault):
            validation_type = validation_type | type(self.default)
            validation_field = Field(default=self.default)
        else:
            validation_field = Field

        self.validation_model = create_model(
            owner.__name__,
            **{name: (validation_type, validation_field)},
        )

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"GenericColumn({self.col_type.__name__}, primary_key={self.primary_key}, auto_increment={self.auto_increment}, unique={self.unique}, nullable={self.nullable}, default={self.default})"


class GenericModel(BasicModel):
    pk: str = None
    properties: dict[str, GenericColumn] = None
    columns: list[str] = None

    def __init_subclass__(cls) -> None:
        self_attr = vars(cls)
        cls.properties = {}
        cls.columns = []
        # Only public attributes
        self_attr = {k: v for k, v in self_attr.items() if not k.startswith("_")}

        for key, value in self_attr.items():
            if isinstance(value, GenericColumn):
                cls.properties[key] = value
                cls.columns.append(key)

                if value.primary_key:
                    if cls.pk and cls.pk != key:
                        raise PKMultipleException(
                            cls.__name__, "Only one primary key is allowed"
                        )
                    cls.pk = key

        if not cls.pk:
            raise PKMissingException(cls.__name__, "Primary key is missing")

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.columns:
                raise ColumnNotExistException(
                    self.__class__.name_, f"Column {key} does not exist"
                )
            setattr(self, key, value)

    def get_col_type(self, col_name: str):
        return self.properties[col_name].col_type

    def is_model_valid(self):
        """
        Check if the model is valid. A model is valid if all the columns are set.

        Raises:
            MultipleColumnsException: If any column is not set.
        """
        errors: list[Exception] = []
        for key in self.columns:
            if isinstance(getattr(self, key), NoDefault):
                errors.append(ColumnNotSetException(self, f"Column {key} is not set"))

        if errors:
            # Rollback to last valid state
            last_valid_data = getattr(self, "_last_valid_state", {})
            self.update(last_valid_data)
            raise MultipleColumnsException(self, errors)

        # Save last valid state
        self._last_valid_state = {key: getattr(self, key) for key in self.columns}

    def __repr__(self):
        return str(self)

    def __str__(self):
        str = self.__class__.__name__ + "=("
        for col in self.columns:
            str += "{0}:{1};".format(col, getattr(self, col))
        str += ")\n"
        return str


class Store(dict[str, list[GenericModel]]):
    def get_models(self, model_cls: Type[T]) -> list[T]:
        return self.get(model_cls.__name__, [])


class GenericSession:
    """
    A generic session for a generic data source. This works similar to a SQLAlchemy session.

    This class can be used as is for a simple in-memory data source.

    But, if you have an external data source, you should override the following methods:

    - **count**: Return the total length of the items after applying all filters and orders.
    - **all**: Return all items after applying all filters and orders.
    - **load_data**: Load data to the session. This will be called when the session is created.
    - **save_data**: Save data to other sources. This will be called when the `add`, `delete`, `add_bulk`, `delete_bulk`, or the FastAPI application is shutting down.
    """

    order_by_cmd: tuple[str, str] | None = None
    filters_cmd: list[
        tuple[Callable[[GenericModel, str, Any], Any | None], str, Any]
    ] = None
    store: Store = None
    store_latest_pk: dict[str, int] = None
    query_class: str = ""
    _offset: int = 0
    _limit: int = 0

    def __init_subclass__(cls) -> None:
        cls.store = Store()
        cls.load_data(cls())

    def __init__(self):
        self._order_by_cmd = None
        self._filters_cmd = []
        self.store_latest_pk = {}
        self.query_class = ""
        self._offset = 0
        self._limit = 0

    def clear(self):
        """
        Deletes the entire store
        """
        self.store = {}
        self.store_latest_pk = {}

    def delete_all(self, model_cls: Type[GenericModel]):
        """
        Deletes all objects of type model_cls
        """
        self.store[model_cls.__name__] = []

    def query(self, model_cls: Type[GenericModel]):
        """
        SQLAlchemy query like method
        """
        self._order_by_cmd = None
        self._filters_cmd = []
        self._offset = 0
        self._limit = 0
        self.query_class = model_cls.__name__
        return self

    def count(self):
        """
        Returns the total length of the items after applying all filters.

        Defaults to `len(self.all())` without any limit and offset.

        Returns:
            int: The total length of the items.
        """
        return len(self.all())

    def all(self):
        """
        Returns all items after applying all filters and orders.

        Returns:
            List[GenericModel]: The items.
        """
        items = []
        if not self._filters_cmd:
            items = self.store.get(self.query_class, [])
        else:
            for item in self.store.get(self.query_class):
                tmp_flag = True
                for filter_cmd in self._filters_cmd:
                    if not filter_cmd[0](item, filter_cmd[1], filter_cmd[2]):
                        tmp_flag = False
                        break
                if tmp_flag:
                    items.append(item)
        if self._order_by_cmd:
            items = self._order_by(items, self._order_by_cmd)
        if self._limit != 0:
            items = items[self._offset : self._offset + self._limit]

        return items

    def get(self, pk: PRIMARY_KEY):
        """
        Returns the object for the key
        Override it for efficiency.
        """
        for item in self.store.get(self.query_class, []):
            # coverts pk value to correct type
            pk = item.properties[item.pk].col_type(pk)
            if getattr(item, item.pk) == pk:
                return item

    def add(self, model: GenericModel, save=True):
        model_cls_name = model.__class__.__name__
        if not self.store.get(model_cls_name):
            self.store[model_cls_name] = []

        pk = getattr(model, model.pk)
        if isinstance(pk, PKAutoIncrement):
            pk = self.store_latest_pk.get(model_cls_name, 0) + 1
            self.store_latest_pk[model_cls_name] = pk
            setattr(model, model.pk, pk)

        model.is_model_valid()
        self.store[model_cls_name].append(model)
        if save:
            self.save_data()

    def add_bulk(self, models: List[GenericModel]):
        for model in models:
            self.add(model, save=False)
        self.save_data()

    def delete(self, item: GenericModel, save=True):
        """
        Delete an item from the session.

        Args:
            item (GenericModel): The item to be deleted.
            save (bool, optional): Whether to save the data after deleting the item. Defaults to True.

        Returns:
            None
        """
        try:
            old_query_class = self.query_class
            self.query_class = item.__class__.__name__
            pk = getattr(item, item.pk)
            item = self.get(pk)
            store = self.store[self.query_class]
            store.remove(item)
            if save:
                self.save_data()
        finally:
            self.query_class = old_query_class

    def delete_bulk(self, items: List[GenericModel]):
        """
        Delete multiple items from the session.

        Args:
            items (List[GenericModel]): The items to be deleted.

        Returns:
            None
        """
        for item in items:
            self.delete(item, save=False)
        self.save_data()

    def scalar(self):
        return 0

    def yield_per(self, _: int):
        """
        Should actually yield results in batches of size **yield_per**. But this is not needed in this case.
        """
        return self.all()

    def commit(self):
        """
        Commit the session. Not needed for generic session.

        Returns:
            None
        """
        pass

    def refresh(self, item):
        """
        Refresh the session. Not needed for generic session.

        Returns:
            None
        """
        pass

    def close(self):
        """
        Close the session. Not needed for generic session.

        Returns:
            None
        """
        pass

    # -----------------------------------------
    #          FUNCTIONS for IMPORT and EXPORT
    # -----------------------------------------

    def load_data(self):
        """
        Override this method to load data to the session. Normally, you would want to use the `add_bulk` method to add data to the session.

        This method will be called only once.
        """
        pass

    def save_data(self):
        """
        Override this method to save data to other sources.

        This method will be called when:
        - The `add` method is called.
        - The `delete` method is called.
        - The `add_bulk` method is called.
        - The `delete_bulk` method is called.
        - The `FastAPI` application is shutting down.
        """
        pass

    # -----------------------------------------
    #           FUNCTIONS for ORDER BY and LIMIT
    # -----------------------------------------

    def order_by(self, order_cmd: str):
        self._order_by_cmd = order_cmd
        return self

    def _order_by(self, data: list[GenericModel], order_cmd: str):
        col_name, direction = order_cmd.split()
        reverse_flag = direction == "desc"
        # patched as suggested by:
        # http://stackoverflow.com/questions/18411560/python-sort-list-with-none-at-the-end
        # and
        # http://stackoverflow.com/questions/5055942/sort-python-list-of-objects-by-date-when-some-are-none

        def col_name_if_not_none(data):
            """
            - sqlite sets to null unfilled fields.
            - sqlalchemy cast this to None
            - this is a killer if the datum is of type datetime.date:
            - it breaks a simple key=operator.attrgetter(col_name)
            approach.

            this function tries to patch the issue
            """
            op = operator.attrgetter(col_name)  # noqa
            missing = getattr(data, col_name) is not None
            return missing, getattr(data, col_name)

        return sorted(data, key=col_name_if_not_none, reverse=reverse_flag)

    def offset(self, offset=0):
        self._offset = offset
        return self

    def limit(self, limit=0):
        self._limit = limit
        return self

    # -----------------------------------------
    #           FUNCTIONS for FILTERS
    # -----------------------------------------

    def starts_with(self, col_name: str, value):
        self._filters_cmd.append((self._starts_with, col_name, value))
        return self

    def _starts_with(self, item: GenericModel, col_name: str, value):
        lw_col = getattr(item, col_name)
        try:
            lw_col = lw_col.lower()
        except Exception:
            return None
        lw_value = value.lower()
        lw_value_list = lw_value.split(" ")

        for lw_item in lw_value_list:
            if not lw_col.startswith(lw_item):
                return None

        return col_name

    def not_starts_with(self, col_name: str, value):
        self._filters_cmd.append((self._not_starts_with, col_name, value))
        return self

    def _not_starts_with(self, item: GenericModel, col_name: str, value):
        lw_col = getattr(item, col_name)
        try:
            lw_col = lw_col.lower()
        except Exception:
            return None
        lw_value = value.lower()
        lw_value_list = lw_value.split(" ")

        for lw_item in lw_value_list:
            if lw_col.startswith(lw_item):
                return None

        return col_name

    def ends_with(self, col_name: str, value):
        self._filters_cmd.append((self._ends_with, col_name, value))
        return self

    def _ends_with(self, item: GenericModel, col_name: str, value):
        lw_col = getattr(item, col_name)
        try:
            lw_col = lw_col.lower()
        except Exception:
            return None
        lw_value = value.lower()
        lw_value_list = lw_value.split(" ")

        for lw_item in lw_value_list:
            if not lw_col.endswith(lw_item):
                return None

        return col_name

    def ends_with(self, col_name: str, value):
        self._filters_cmd.append((self._ends_with, col_name, value))
        return self

    def not_ends_with(self, col_name: str, value):
        self._filters_cmd.append((self._not_ends_with, col_name, value))
        return self

    def _not_ends_with(self, item: GenericModel, col_name: str, value):
        lw_col = getattr(item, col_name)
        try:
            lw_col = lw_col.lower()
        except Exception:
            return None
        lw_value = value.lower()
        lw_value_list = lw_value.split(" ")

        for lw_item in lw_value_list:
            if lw_col.endswith(lw_item):
                return None

        return col_name

    def greater(self, col_name: str, value):
        self._filters_cmd.append((self._greater, col_name, value))
        return self

    def _greater(self, item: GenericModel, col_name: str, value):
        source_value = getattr(item, col_name)

        try:
            # whatever we have to copare it will never match
            if source_value is None:
                return False

            # date has special constructor, tested only on sqlite
            elif isinstance(source_value, date):
                value = datetime.strptime(value, "%Y-%m-%d").date()

            # fallback to native python types
            else:
                value = type(source_value)(value)

            return source_value > value
        except Exception:
            # when everything fails silently report False
            return False

    def greater_equal(self, col_name: str, value):
        self._filters_cmd.append((self._greater_equal, col_name, value))
        return self

    def _greater_equal(self, item: GenericModel, col_name: str, value):
        source_value = getattr(item, col_name)

        try:
            # whatever we have to copare it will never match
            if source_value is None:
                return False

            # date has special constructor, tested only on sqlite
            elif isinstance(source_value, date):
                value = datetime.strptime(value, "%Y-%m-%d").date()

            # fallback to native python types
            else:
                value = type(source_value)(value)

            return source_value >= value
        except Exception:
            # when everything fails silently report False
            return False

    def smaller(self, col_name: str, value):
        self._filters_cmd.append((self._smaller, col_name, value))
        return self

    def _smaller(self, item: GenericModel, col_name: str, value):
        source_value = getattr(item, col_name)

        try:
            # whatever we have to copare it will never match
            if source_value is None:
                return False

            # date has special constructor, tested only on sqlite
            elif isinstance(source_value, date):
                value = datetime.strptime(value, "%Y-%m-%d").date()

            # fallback to native python types
            else:
                value = type(source_value)(value)

            return source_value < value
        except Exception:
            # when everything fails silently report False
            return False

    def smaller_equal(self, col_name: str, value):
        self._filters_cmd.append((self._smaller_equal, col_name, value))
        return self

    def _smaller_equal(self, item: GenericModel, col_name: str, value):
        source_value = getattr(item, col_name)

        try:
            # whatever we have to copare it will never match
            if source_value is None:
                return False

            # date has special constructor, tested only on sqlite
            elif isinstance(source_value, date):
                value = datetime.strptime(value, "%Y-%m-%d").date()

            # fallback to native python types
            else:
                value = type(source_value)(value)

            return source_value <= value
        except Exception:
            # when everything fails silently report False
            return False

    def ilike(self, col_name: str, value):
        self._filters_cmd.append((self._ilike, col_name, value))
        return self

    def _ilike(self, item: GenericModel, col_name: str, value):
        lw_col = getattr(item, col_name)
        try:
            lw_col = lw_col.lower()
        except Exception:
            return None
        lw_value = value.lower()
        lw_value_list = lw_value.split(" ")

        for lw_item in lw_value_list:
            if lw_item not in lw_col:
                return None

        return col_name

    def like(self, col_name: str, value):
        self._filters_cmd.append((self._like, col_name, value))
        return self

    def _like(self, item: GenericModel, col_name: str, value):
        lw_col = getattr(item, col_name)
        lw_value_list = value.split(" ")

        for lw_item in lw_value_list:
            if lw_item not in lw_col:
                return None

        return col_name

    def not_like(self, col_name: str, value):
        self._filters_cmd.append((self._not_like, col_name, value))
        return self

    def _not_like(self, item: GenericModel, col_name: str, value):
        return value not in getattr(item, col_name)

    def equal(self, col_name: str, value):
        self._filters_cmd.append((self._equal, col_name, value))
        return self

    def _equal(self, item: GenericModel, col_name: str, value):
        source_value = getattr(item, col_name)

        try:
            # whatever we have to copare it will never match
            if source_value is None:
                return False

            # date has special constructor, tested only on sqlite
            elif isinstance(source_value, date):
                value = datetime.strptime(value, "%Y-%m-%d").date()

            # fallback to native python types
            else:
                value = type(source_value)(value)

            return source_value == value
        except Exception:
            # when everything fails silently report False
            return False

    def not_equal(self, col_name: str, value):
        self._filters_cmd.append((self._not_equal, col_name, value))
        return self

    def _not_equal(self, item: GenericModel, col_name: str, value):
        return not self._equal(item, col_name, value)

    def in_(self, col_name: str, value):
        self._filters_cmd.append((self._in, col_name, value))
        return self

    def _in(self, item: GenericModel, col_name: str, value):
        return getattr(item, col_name) in value
