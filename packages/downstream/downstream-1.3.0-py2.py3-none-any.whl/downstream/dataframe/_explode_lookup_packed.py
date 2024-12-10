import typing

import polars as pl

from ._explode_lookup_unpacked import explode_lookup_unpacked
from ._unpack_data_packed import unpack_data_packed


def explode_lookup_packed(
    df: pl.DataFrame,
    *,
    value_type: typing.Literal["hex", "uint64", "uint32", "uint16", "uint8"],
    result_schema: typing.Literal["coerce", "relax", "shrink"] = "coerce",
) -> pl.DataFrame:
    """Explode downstream-curated data from hexidecimal serialization of
    downstream buffers and counters to one-data-item-per-row, applying
    downstream lookup to identify origin time `Tbar` of each item."""
    df = unpack_data_packed(df, result_schema=result_schema)
    return explode_lookup_unpacked(
        df, result_schema=result_schema, value_type=value_type
    )
