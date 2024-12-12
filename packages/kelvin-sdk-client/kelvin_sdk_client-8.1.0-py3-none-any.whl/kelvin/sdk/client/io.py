"""IO functions."""

from __future__ import annotations

from datetime import tzinfo
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Union, overload

from pandas import DataFrame, MultiIndex, concat, json_normalize, to_datetime
from typing_extensions import Literal
from tzlocal import get_localzone

from .utils import chunks, inflate, map_chunks

STORAGE_FIELDS = {"resource", "source", "timestamp", "type"}
DATA = [
    "payload",
]
INDEX = [
    "resource",
    "timestamp",
]
DEFAULT_TZ = str(get_localzone())

ExpandType = Literal["column", "index"]


def parse_resource(resource: str) -> Dict[str, str]:
    """Parse KRN resource string."""

    try:
        scheme, nid, nss = resource.split(":", 2)
    except IndexError:
        raise ValueError(f"Invalid resource {resource!r}")

    if scheme != "krn":
        raise ValueError(f"Invalid resource scheme {scheme!r}")

    result: Dict[str, str] = {"nid": nid}

    # Asset Datastream
    if nid == "ad":
        try:
            asset_name, datastream_name = nss.split("/", 1)
        except IndexError:
            raise ValueError(f"Invalid resource string {nss!r} for resource {nid!r}")
        result["asset_name"] = asset_name
        result["datastream_name"] = datastream_name
    else:
        raise ValueError(f"Unsupported resource namespace {nid!r}")

    return result


def _convert_timeseries(
    x: Iterable[Mapping[str, Any]],
    tz: Union[tzinfo, str],
    expand_resource: Optional[ExpandType] = "index",
) -> DataFrame:
    """Convert timeseries into dataframe."""

    data = DataFrame.from_records(x)
    if data.empty:
        return DataFrame(
            {name: [] for name in DATA},
            index=MultiIndex.from_tuples([], names=INDEX),
        )

    data["timestamp"] = to_datetime(data.timestamp, utc=True).dt.tz_convert(tz)
    data.set_index(INDEX, inplace=True)

    if expand_resource is None:
        return data

    data = data.reset_index("resource")
    resource = json_normalize(data.pop("resource").apply(parse_resource))  # type: ignore
    resource.index = data.index
    data = concat([resource, data], axis=1)

    if expand_resource == "column":
        return data
    elif expand_resource == "index":
        return data.set_index([*resource.columns], append=True)
    else:
        raise ValueError(f"Unknown expansion-type {expand_resource!r}")

    return data


@overload
def timeseries_to_dataframe(
    x: Iterable[Mapping[str, Any]],
    chunk_size: Literal[None] = None,
    tz: Union[tzinfo, str] = DEFAULT_TZ,
    expand_resource: Optional[ExpandType] = "index",
) -> DataFrame:
    ...


@overload
def timeseries_to_dataframe(
    x: Iterable[Mapping[str, Any]],
    chunk_size: int,
    tz: Union[tzinfo, str] = DEFAULT_TZ,
    expand_resource: Optional[ExpandType] = "index",
) -> Iterator[DataFrame]:
    ...


def timeseries_to_dataframe(
    x: Iterable[Mapping[str, Any]],
    chunk_size: Optional[int] = None,
    tz: Union[tzinfo, str] = DEFAULT_TZ,
    expand_resource: Optional[ExpandType] = "index",
) -> Union[DataFrame, Iterator[DataFrame]]:
    """Convert timeseries into dataframe, optionally in chunks."""

    if chunk_size is None:
        return _convert_timeseries(x, tz=tz, expand_resource=expand_resource)

    return map_chunks(chunk_size, _convert_timeseries, x, tz=tz, expand_resource=expand_resource)


def _convert_dataframe(x: DataFrame) -> List[Dict[str, Any]]:
    """Convert dataframe into timeseries."""

    x = x.reset_index()

    missing = STORAGE_FIELDS - {*x}
    if missing:
        raise ValueError(f"Missing fields: {', '.join(sorted(missing))}")

    columns = {*x} - STORAGE_FIELDS

    if not columns:
        raise ValueError("No columns found")

    if "payload" in columns:
        extra = columns - {"payload"}
        if extra:
            raise ValueError(f"Unexpected columns: {', '.join(sorted(extra))}")

    elif "field" in columns and "value" in columns:
        extra = columns - {"field", "value"}
        if extra:
            raise ValueError(f"Unexpected columns: {', '.join(sorted(extra))}")
        x = (
            x.groupby([*STORAGE_FIELDS])[["field", "value"]]
            .apply(lambda x: inflate(x.itertuples(index=False)))
            .reset_index(name="payload")
        )

    else:
        x["payload"] = [inflate(v.items()) for v in x[columns].to_dict(orient="records")]
        x = x.drop(columns=columns)

    x["timestamp"] = x.timestamp.astype(int)

    return x.to_dict(orient="records")


def dataframe_to_timeseries(
    x: DataFrame, chunk_size: Optional[int] = None
) -> Union[List[Dict[str, Any]], Iterator[List[Dict[str, Any]]]]:
    """Convert dataframe into timeseries, optionally in chunks."""

    if chunk_size is None:
        return _convert_dataframe(x)

    return (_convert_dataframe(chunk) for chunk in chunks(x, chunk_size))
