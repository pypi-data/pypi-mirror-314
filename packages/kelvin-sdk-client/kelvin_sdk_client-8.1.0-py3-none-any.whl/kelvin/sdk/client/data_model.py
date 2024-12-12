"""
Data Model.
"""

from __future__ import annotations

import json
from collections import ChainMap
from datetime import datetime, timezone
from functools import wraps
from importlib import import_module
from inspect import signature
from types import FunctionType, MethodType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

import structlog
from pydantic.v1 import Extra, ValidationError, validator
from pydantic.v1.main import ModelField
from typing_inspect import get_args, get_origin

from kelvin.sdk.client.serialize import lower

from .base_model import BaseModel, BaseModelMeta
from .deeplist import deeplist
from .error import APIError, ResponseError
from .serialize import is_json
from .utils import file_tuple, instance_classmethod, snake_name

if TYPE_CHECKING:
    from .client import Client

logger = structlog.get_logger(__name__)

T = TypeVar("T")

JSON_CONTENT_TYPES = (
    "application/json",
    "application/x-json-stream",
)
MODELS = "kelvin.sdk.client.model"


def resolve_fields(x: Mapping[str, Any]) -> Dict[str, Any]:
    """Resolve fields from data models."""

    result: Dict[str, Any] = {**x}
    items = [*x.items()]

    for name, value in items:
        if "_" in name and isinstance(value, DataModel):
            head, tail = name.rsplit("_", 1)
            if head != type(value).__name__.lower():
                raise TypeError(f"Unable to get {name!r} from {type(value).__name__!r} object")
            value = result[name] = value[tail]
        if isinstance(value, datetime):
            suffix = "Z" if value.microsecond else ".000000Z"
            result[name] = value.astimezone(timezone.utc).replace(tzinfo=None).isoformat() + suffix

    return result


class DataModelMeta(BaseModelMeta):
    """DataModel metaclass."""

    def __new__(
        metacls: Type[DataModelMeta], name: str, bases: Tuple[Type, ...], __dict__: Dict[str, Any]
    ) -> DataModelMeta:
        cls = cast(DataModelMeta, super().__new__(metacls, name, bases, __dict__))

        # kill unused fields so that they can be used by models
        cls.fields = cls.schema = None  # type: ignore

        return cls

    def __repr__(self) -> str:
        """Pretty representation."""

        methods = "\n".join(
            f"  - {name}: " + x.__doc__.lstrip().split("\n")[0]
            for name, x in (
                (name, getattr(self, name))
                for name in sorted(vars(self))
                if not name.startswith("_")
            )
            if x.__doc__ is not None and isinstance(x, (FunctionType, MethodType))
        )

        return f"{self.__name__}:\n{methods}"

    def __str__(self) -> str:
        """Return str(self)."""

        return f"<class {self.__name__!r}>"


def get_type(name: str) -> Type:
    module_name, type_name = name.rsplit(".", 1)
    return getattr(import_module(f"{MODELS}.{module_name}"), type_name)


class DataModel(BaseModel, metaclass=DataModelMeta):
    """Model base-class."""

    if TYPE_CHECKING:
        fields: Any
        schema: Any

    __slots__ = ("_client",)

    class Config(BaseModel.Config):
        """Model config."""

        extra = Extra.allow

    def __init__(self, client: Optional[Client] = None, **kwargs: Any) -> None:
        """Initialise model."""

        super().__init__(**kwargs)

        object.__setattr__(self, "_client", client)

    @property
    def client(self) -> Optional[Client]:
        """Resource client."""

        if self._client is not None:
            return self._client

        if self._owner is not None:
            return self._owner.client

        return None

    def __getattribute__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_"):
            return super().__getattribute__(name)

        try:
            result = super().__getattribute__(name)
        except AttributeError:
            if "_" in name:
                # fall back to attribute on child field
                head, tail = name.rsplit("_", 1)
                if head in self.__fields__:
                    head = getattr(self, head)
                    try:
                        return getattr(head, tail)
                    except AttributeError:
                        pass
            raise

        return deeplist(result) if isinstance(result, list) else result

    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute."""

        if name.startswith("_"):
            super().__setattr__(name, value)

        try:
            super().__setattr__(name, value)
        except ValueError:
            if "_" in name:
                # fall back to attribute on child field
                head, tail = name.rsplit("_", 1)
                if head in self.__fields__:
                    head = getattr(self, head)
                    try:
                        setattr(head, tail, value)
                    except ValueError:
                        pass
                    else:
                        return
            raise

    @staticmethod
    def translate(
        names: Optional[Mapping[str, str]] = None
    ) -> Callable[[Callable[..., T]], Callable[..., T]]:
        """Translate names and obtain data from object."""

        def outer(f: Callable[..., T]) -> Callable[..., T]:
            positional_args = [
                name
                for name, x in signature(f).parameters.items()
                if name not in {"_client", "_dry_run"} and x.default is x.empty
            ][1:]

            @wraps(f)
            def inner(obj: Any, *args: Any, **kwargs: Any) -> T:
                if isinstance(obj, DataModel):
                    owner_prefix = (
                        snake_name(type(obj._owner).__name__) + "_"
                        if obj._owner is not None
                        else None
                    )
                    for arg_name in positional_args[len(args) :]:
                        if names is not None and arg_name in names:
                            source = names[arg_name]
                            kwargs[arg_name] = obj[source]
                        elif arg_name in obj:
                            kwargs[arg_name] = obj[arg_name]
                        elif owner_prefix is not None and arg_name.startswith(owner_prefix):
                            try:
                                kwargs[arg_name] = obj._owner[arg_name.replace(owner_prefix, "")]
                            except KeyError:
                                pass

                return f(obj, *args, **kwargs)

            return inner

        return outer

    @instance_classmethod
    def _make_request(
        obj: Any,
        client: Optional[Client],
        method: str,
        path: str,
        values: Mapping[str, Any],
        params: Mapping[str, Any],
        files: Mapping[str, Any],
        headers: Mapping[str, Any],
        data: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]],
        body_type: Optional[str],
        array_body: bool,
        result_types: Mapping[str, Optional[Type]],
        stream: bool = False,
        dry_run: bool = False,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make request to API."""

        if isinstance(obj, DataModel):
            if client is None:
                client = obj.client

        if client is None:
            raise ValueError("No client set.")

        # check for fields that need to be dereferenced
        values = resolve_fields(values)
        params = resolve_fields(params)
        files = resolve_fields(files)
        headers = resolve_fields(headers)

        if "{" in path:
            path = path.format_map(values)

        body_data: Any

        if body_type is not None:
            body_type_ = get_type(body_type)

            def prepare(x: Mapping[str, Any]) -> Dict[str, Any]:
                if kwargs:
                    x = ChainMap(kwargs, x)  # type: ignore
                return {
                    k: v
                    for k, v in (
                        (name, x.get(name)) for name in cast(Type[DataModel], body_type_).__fields__
                    )
                    if v is not None
                }

            if array_body:
                if data is None:
                    data = [{}] if kwargs else []
                elif not isinstance(data, Sequence) and all(isinstance(x, Mapping) for x in data):
                    raise ValueError("Data must be a sequence of mappings")

                body_data = [
                    body_type_(**lower(prepare(x))).dict(by_alias=True)
                    for x in cast(Sequence[Mapping[str, Any]], data)
                ]
            else:
                if data is None:
                    data = {}
                elif not isinstance(data, Mapping):
                    raise ValueError("Data must be a mapping")

                if isinstance(obj, DataModel):
                    data = ChainMap(data, obj)  # type: ignore

                body_data = body_type_(**lower(prepare(data))).dict(by_alias=True)
        else:
            body_data = None

        files = {k: file_tuple(v) for k, v in files.items()}

        if dry_run:
            return {
                "path": path,
                "method": method,
                "data": body_data,
                "params": params,
                "files": files,
                "headers": headers,
            }

        response = client.request(
            path, method, body_data, params, files, headers, raise_error=False, stream=stream
        )

        try:
            content_type = response.headers.get("Content-Type", "")
            if content_type == "application/octet-stream":
                return response.iter_content(1024)

            status_code = response.status_code

            result_type = result_types.get(str(status_code), ...)

            if not response.ok:
                if result_type is ...:
                    # try to fill gap with first not "OK" response
                    result_type = next(
                        (
                            v
                            for k, v in sorted(result_types.items())
                            if not 200 <= status_code < 300
                        ),
                        ...,
                    )
                    if result_type is ...:
                        logger.warning("Unknown response code", status_code=status_code)
                        result_type = None
                        if content_type == "application/json" or is_json(response.text):
                            raise APIError(response)
                        response.raise_for_status()

            elif result_type is ...:
                # try to fill gap with first "OK" response
                result_type = next(
                    (v for k, v in sorted(result_types.items()) if 200 <= status_code < 300), ...
                )
                if result_type is ...:
                    logger.warning("Unknown response code", status_code=status_code)
                    result_type = None

            if isinstance(result_type, type):
                if not content_type.startswith(JSON_CONTENT_TYPES):
                    with response:
                        raise ResponseError(
                            f"Unexpected response for {result_type.__name__}",  # type: ignore
                            response,
                        )

                def converter(x: Any) -> Any:
                    return result_type(client=client, **x)  # type: ignore

            elif get_origin(result_type) is list:
                result_type, *_ = get_args(result_type)
                if not content_type.startswith(JSON_CONTENT_TYPES):
                    with response:
                        raise ResponseError(
                            f"Unexpected response for {result_type.__name__}",  # type: ignore
                            response,
                        )

                def converter(x: Any) -> Any:
                    return [result_type(client=client, **v) for v in x]  # type: ignore

            else:
                if not content_type.startswith(JSON_CONTENT_TYPES):
                    with response:
                        return response.text or None

                def converter(x: Any) -> Any:
                    return x

            if not response.ok:
                with response:
                    raise APIError(response, converter)

            if stream:

                def results() -> Iterator[Any]:
                    i = -1
                    errors = []
                    success = False
                    with response:
                        for x in response.iter_lines():
                            if not x:
                                continue
                            i += 0
                            records = json.loads(x)
                            if isinstance(records, dict):
                                records = [records]

                            for record in records:
                                try:
                                    yield converter(record)
                                except ValidationError as e:
                                    errors += [(i, e)]
                                    continue
                                else:
                                    success = True

                        if not errors:
                            return

                        if not success:
                            raise errors[0][1] from None
                        elif errors:
                            summary = "\n".join(f"  {i}: {x}" for i, x in errors)
                            logger.warning(
                                "Skipped items", result_type=result_type, summary=summary
                            )

                results.__qualname__ = "results"

                return results()
            else:
                with response:
                    try:
                        return converter(response.json())
                    except ValidationError as e:
                        raise e from None

        except Exception:
            response.close()
            raise

    @validator("*", pre=True)
    def convert_datetime(cls, value: Any, field: ModelField) -> Any:
        """Correct data-type for datetime values."""

        if not isinstance(value, datetime):
            return value

        field_type = field.type_

        if not isinstance(field_type, type):
            return value

        if issubclass(field_type, str):
            suffix = "Z" if value.microsecond else ".000000Z"
            return value.astimezone(timezone.utc).replace(tzinfo=None).isoformat() + suffix
        elif issubclass(field_type, float):
            return value.timestamp()
        elif issubclass(field_type, int):
            return int(value.timestamp() * 1e9)
        else:
            return value


P = TypeVar("P", bound=DataModel)


class PaginatorDataModel(DataModel, Generic[P]):
    """Paginator data-model."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialise model."""

        super().__init__(**kwargs)

        for x in self.data:
            object.__setattr__(x, "_client", self._client)

    @validator("data", pre=True, check_fields=False)
    def validate_data(cls, v: Sequence[Mapping[str, Any]], field: ModelField) -> List[P]:
        """Validate data field."""

        T = field.type_
        results = []

        for item in v:
            try:
                results += [T(**item)]
            except ValidationError as e:
                logger.warning("Skipped invalid item", name=T.__name__, item=item, error=e)

        return results

    def __getitem__(self, item: Union[str, int]) -> Any:
        """Get item."""

        if isinstance(item, int):
            return self.data[item]

        return super().__getitem__(item)

    def scan(self, path: str, flatten: bool = True, method: str = "GET") -> Iterator[P]:
        """Iterate pages."""

        result = self
        client = self._client

        while True:
            if not result.data:
                return

            if flatten:
                yield from result.data
            else:
                yield result.data

            pagination = result.pagination
            if pagination is None:
                return

            next_page = pagination.next_page
            if next_page is None:
                return

            if "?" in next_page:
                path = next_page
                params = {}
            else:
                page_size = len(result.data)
                params = {"next": next_page, "page_size": page_size}

            with client.request(path, method=method, params=params, data=None) as response:
                result = type(self)(**response.json(), client=client)

    def fetch(self, path: str, method: str = "GET") -> Sequence[P]:
        """Fetch all data."""

        return type(self.data)(self.scan(path, True, method=method))


DataModelBase = DataModel
