import csv
import inspect
import os
import re
import secrets
import sys
import unicodedata
import uuid
from datetime import datetime, timezone
from types import FunctionType
from typing import Any, Awaitable, Callable, Coroutine, Dict, NotRequired, Type, Union

import sqlalchemy.types as sa_types
from fastapi import Depends, UploadFile
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field, create_model
from sqlalchemy import Column
from starlette.concurrency import P, T

__all__ = [
    "ExtenderMixin",
    "SelfDepends",
    "SelfType",
    "Line",
    "generate_report",
    "merge_schema",
    "update_signature",
    "uuid_namegen",
    "secure_filename",
    "ensure_tz_info",
    "validate_utc",
    "smart_run",
    "safe_call",
    "ImportStringError",
    "import_string",
    "is_sqla_type",
    "generate_schema_from_typed_dict",
]

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(10)),
    *(f"LPT{i}" for i in range(10)),
}


class ExtenderMixin:
    """
    A utility class that can be used to extend the attributes of the parent classes.

    When a class inherits from this class, it will take all the non-private attributes of the child class and add them to the parent classes.

    Can also be combined with a class that is a subclass of `Model` from `fastapi_rtk.model` to add new columns when modifying the actual class is not possible.

    ### Example:

    ```python
    class Parent:
        parent_attr = "parent"

    class Child(ExtendingModel, Parent):
        child_attr = "child"

    print(Parent.parent_attr)  # Output: "parent"
    print(Parent.child_attr)  # Output: "child"
    ```
    """

    def __init_subclass__(cls) -> None:
        if ExtenderMixin in cls.__bases__:
            copy_vars = {
                k: v
                for k, v in vars(cls).items()
                if not k == "__module__" and not k == "__doc__"
            }
            cls._extend_parents(**copy_vars)
        return super().__init_subclass__()

    @classmethod
    def _extend_parents(cls, **kwargs):
        for base in cls.__bases__:
            if base is ExtenderMixin:
                continue
            for k, v in kwargs.items():
                setattr(base, k, v)
            if hasattr(base, "_extend_parents"):
                base._extend_parents(**kwargs)


class BaseSelf:
    attr: str | None = None
    ignored_keys: list[str] = None

    def __init__(self) -> None:
        self.ignored_keys = ["attr", "__class__"]

    def __getattribute__(self, name: str) -> Any:
        # Special handling for when name is "ignored_keys" or in self.ignored_keys
        if name == "ignored_keys" or name in self.ignored_keys:
            return super().__getattribute__(name)

        # If attr is not set, set attr to the attribute name
        curr_attr = self.attr
        if curr_attr is None:
            curr_attr = ""
        curr_attr += f".{name}" if curr_attr else name
        self.attr = curr_attr

        return self

    def __call__(self, cls) -> Any:
        split = self.attr.split(".")
        result = None
        for attr in split:
            result = getattr(result or cls, attr)
        return result


class SelfDepends(BaseSelf):
    """
    A class that can be used to create a dependency that depends on the class instance.

    Sometimes you need to create a dependency that requires the class instance to be passed as a parameter when using Depends() from FastAPI. This class can be used to create such dependencies.

    ### Example:

    ```python
        class MyApi:
            @expose("/my_endpoint")
            def my_endpoint(self, permissions: List[str] = SelfDepends().get_current_permissions):
                # Do something
                pass

            def get_current_permissions(self):
                # Do something that requires the class instance, and should returns a function that can be used as a dependency
                pass
    ```

    is equivalent to:

    ```python
        # self. is actually not possible here, that's why we use the string representation of the attribute
        class MyApi:
            @expose("/my_endpoint")
            def my_endpoint(self, permissions: List[str] = Depends(self.get_current_permissions)):
                # Do something
                pass

            def get_current_permissions(self):
                # Do something that requires the class instance, and should returns a function that can be used as a dependency
                pass
    ```
    """

    args = None
    kwargs = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.ignored_keys.append("args")
        self.ignored_keys.append("kwargs")
        self.args = args or ()
        self.kwargs = kwargs or {}

    def __call__(self, cls) -> Any:
        result = super().__call__(cls)
        return Depends(result(*self.args, **self.kwargs))


class SelfType(BaseSelf):
    """
    A class that can be used to create a dependency that depends on the class instance.

    Sometimes you need to create a type that depends on the class instance. This class can be used to create such types.

    ### Example:

    ```python
        class MyApi:
            @expose("/my_endpoint")
            def my_endpoint(self, schema: BaseModel = SelfType().datamodel.obj.schema):
                # Do something
                pass

            @expose("/my_other_endpoint")
            def my_other_endpoint(self, schema: BaseModel = SelfType.with_depends().datamodel.obj.schema):
                # Do something
                pass
    ```

    is equivalent to:

    ```python
        # self. is actually not possible here, that's why we use the string representation of the attribute
        class MyApi:
            @expose("/my_endpoint")
            def my_endpoint(self, schema: self.datamodel.obj.schema):
                # Do something
                pass

            @expose("/my_other_endpoint")
            def my_other_endpoint(self, schema: self.datamodel.obj.schema = Depends()):
                # Do something
                pass
    ```
    """

    depends = False

    def __init__(self, depends: bool = False) -> None:
        super().__init__()
        self.ignored_keys.append("depends")
        self.depends = depends
        self.attr = None

    @classmethod
    def with_depends(cls):
        return cls(depends=True)


class Line(object):
    def __init__(self):
        self._line = None

    def write(self, line):
        self._line = line

    def read(self):
        return self._line


async def generate_report(data, list_columns, label_columns):
    line = Line()
    writer = csv.writer(line, delimiter=",")

    # header
    labels = []
    for key in list_columns:
        labels.append(label_columns[key])

    # rows
    writer.writerow(labels)
    yield line.read()

    async for chunk in data:
        for item in chunk:
            row = []
            for key in list_columns:
                value = getattr(item, key)
                # if value is a function, call it
                if callable(value):
                    try:
                        value = value()
                    except Exception:
                        value = "Error calling function"
                if value is None:
                    value = ""
                row.append(str(value))
            writer.writerow(row)
            yield line.read()


def merge_schema(
    schema: BaseModel,
    fields: Dict[str, tuple[type, Field]],
    only_update=False,
    name: str | None = None,
) -> Type[BaseModel]:
    """
    Replace or add fields to the given schema.

    Args:
        schema (BaseModel): The schema to be updated.
        fields (Dict[str, tuple[type, Field]]): The fields to be added or updated.
        only_update (bool): If True, only update the fields with the same name. Otherwise, add new fields.
        name (str, optional): The name of the new schema. If not given, the schema name will be suffixed with a random hex string. Defaults to None.

    Returns:
        BaseModel: The updated schema.
    """
    name = name or f"{schema.__name__}-{secrets.token_hex(3)}"
    new_fields = dict()
    if only_update:
        for key, value in schema.model_fields.items():
            if key in fields:
                val = fields[key]
                if isinstance(val, tuple):
                    new_fields[key] = val
                else:
                    new_fields[key] = (value.annotation, val)
    else:
        new_fields = fields

    return create_model(
        name,
        **new_fields,
        __base__=schema,
    )


def copy_function(f):
    """Copy a function."""
    return FunctionType(
        f.__code__,
        f.__globals__,
        name=f.__name__,
        argdefs=f.__defaults__,
        closure=f.__closure__,
    )


def update_signature(cls, f):
    """
    Copy a function and update its signature to include the class instance as the first parameter instead of string "self" for FastAPI Route Dependencies.

    It also replaces SelfDepends and SelfType with the actual value.

    Args:
        f (Callable): The function to be updated.
    Returns:
        Callable: The updated function.
    """
    # Get the function's parameters
    old_signature = inspect.signature(f)
    old_parameters = list(old_signature.parameters.values())
    if not old_parameters:
        return f
    old_first_parameter, *old_parameters = old_parameters

    # If the first parameter is self, replace it
    if old_first_parameter.name == "self":
        new_first_parameter = old_first_parameter.replace(default=Depends(lambda: cls))

        new_parameters = [new_first_parameter]
        for parameter in old_parameters:
            parameter = parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
            if isinstance(parameter.default, SelfDepends):
                parameter = parameter.replace(default=parameter.default(cls))
            elif isinstance(parameter.default, SelfType):
                parameter = parameter.replace(
                    annotation=parameter.default(cls),
                    default=(
                        Depends()
                        if parameter.default.depends
                        else inspect.Parameter.empty
                    ),
                )
            new_parameters.append(parameter)

        new_signature = old_signature.replace(parameters=new_parameters)

        # Copy the function to avoid modifying the original
        f = copy_function(f)

        setattr(
            f, "__signature__", new_signature
        )  # Set the new signature to the function

    return f


def uuid_namegen(file_data: UploadFile) -> str:
    """
    Generates a unique filename by combining a UUID and the original filename.

    Args:
        file_data (File): The file data object.

    Returns:
        str: The generated unique filename.
    """
    return str(uuid.uuid1()) + "_sep_" + file_data.filename


def secure_filename(filename: str) -> str:
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.

    On windows systems the function also makes sure that the file is not
    named after one of the special device files.

    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >>> secure_filename('i contain cool \xfcml\xe4uts.txt')
    'i_contain_cool_umlauts.txt'

    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you abort or
    generate a random filename if the function returned an empty one.

    .. versionadded:: 0.5

    :param filename: the filename to secure
    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    for sep in os.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = f"_{filename}"

    return filename


def ensure_tz_info(dt: datetime | str) -> datetime:
    """Ensure that the datetime has a timezone info."""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def validate_utc(dt: datetime) -> datetime:
    """Validate that the datetime is in UTC."""
    if dt.tzinfo.utcoffset(dt) != timezone.utc.utcoffset(dt):
        raise ValueError("Timezone must be UTC")
    return dt


async def smart_run(
    func: Callable[P, Union[T, Awaitable[T]]], *args: P.args, **kwargs: P.kwargs
) -> T:
    """
    A utility function that can run a function either as a coroutine or in a threadpool.

    Args:
        func: The function to be executed.
        *args: Positional arguments to be passed to the function.
        **kwargs: Keyword arguments to be passed to the function.

    Returns:
        The result of the function execution.

    Raises:
        Any exceptions raised by the function.

    """
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return await run_in_threadpool(func, *args, **kwargs)


async def safe_call(coro: Coroutine[Any, Any, T] | T) -> T:
    """
    A utility function that can await a coroutine or return a non-coroutine object.

    Args:
        coro (Any): The function call or coroutine to be awaited.

    Returns:
        The result of the function call or coroutine.
    """
    if isinstance(coro, Coroutine):
        return await coro
    return coro


class ImportStringError(ImportError):
    """
    COPIED FROM WERKZEUG LIBRARY

    Provides information about a failed :func:`import_string` attempt.
    """

    #: String in dotted notation that failed to be imported.
    import_name: str
    #: Wrapped exception.
    exception: BaseException

    def __init__(self, import_name: str, exception: BaseException) -> None:
        self.import_name = import_name
        self.exception = exception
        msg = import_name
        name = ""
        tracked = []
        for part in import_name.replace(":", ".").split("."):
            name = f"{name}.{part}" if name else part
            imported = import_string(name, silent=True)
            if imported:
                tracked.append((name, getattr(imported, "__file__", None)))
            else:
                track = [f"- {n!r} found in {i!r}." for n, i in tracked]
                track.append(f"- {name!r} not found.")
                track_str = "\n".join(track)
                msg = (
                    f"import_string() failed for {import_name!r}. Possible reasons"
                    f" are:\n\n"
                    "- missing __init__.py in a package;\n"
                    "- package or module path not included in sys.path;\n"
                    "- duplicated package or module name taking precedence in"
                    " sys.path;\n"
                    "- missing module, class, function or variable;\n\n"
                    f"Debugged import:\n\n{track_str}\n\n"
                    f"Original exception:\n\n{type(exception).__name__}: {exception}"
                )
                break

        super().__init__(msg)

    def __repr__(self) -> str:
        return f"<{type(self).__name__}({self.import_name!r}, {self.exception!r})>"


def import_string(import_name: str, silent: bool = False) -> Any:
    """
    COPIED FROM WERKZEUG LIBRARY

    Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).

    If `silent` is True the return value will be `None` if the import fails.

    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """
    import_name = import_name.replace(":", ".")
    try:
        try:
            __import__(import_name)
        except ImportError:
            if "." not in import_name:
                raise
        else:
            return sys.modules[import_name]

        module_name, obj_name = import_name.rsplit(".", 1)
        module = __import__(module_name, globals(), locals(), [obj_name])
        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e) from None

    except ImportError as e:
        if not silent:
            raise ImportStringError(import_name, e).with_traceback(
                sys.exc_info()[2]
            ) from None

    return None


def is_sqla_type(col: Column, sa_type: Type[sa_types.TypeEngine]) -> bool:
    """
    Check if the column is an instance of the given SQLAlchemy type.

    Args:
        col (Column): The SQLAlchemy Column to check.
        sa_type (Type[sa_types.TypeEngine]): The SQLAlchemy type to check against.

    Returns:
        bool: True if the column is an instance of the given SQLAlchemy type, False otherwise.
    """
    return (
        isinstance(col, sa_type)
        or isinstance(col, sa_types.TypeDecorator)
        and isinstance(col.impl, sa_type)
    )


def generate_schema_from_typed_dict(typed_dict: type):
    """
    Generate a Pydantic model schema from a TypedDict.
    Args:
        typed_dict (type): A type that is a subclass of dict, typically a TypedDict.
    Returns:
        BaseModel: A Pydantic model generated from the TypedDict.
    Raises:
        TypeError: If the provided typed_dict is not a type or not a subclass of dict.
    """
    if not isinstance(typed_dict, type) or not issubclass(typed_dict, dict):
        raise TypeError("typed_dict must be a type that is a subclass of dict")

    fields = {}
    for key, val in typed_dict.__annotations__.items():
        if getattr(val, "__origin__", None) is NotRequired:
            fields[key] = (val.__args__[0], Field(None))
        else:
            fields[key] = (val, Field(...))
    return create_model(typed_dict.__name__, **fields)
