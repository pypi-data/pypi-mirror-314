import logging
import typing

import numpy as np
import polars as pl

from .. import dstream  # noqa: F401
from .._auxlib._unpack_hex import unpack_hex
from ._impl._check_downstream_version import check_downstream_version
from ._impl._check_expected_columns import check_expected_columns


def _check_df(df: pl.DataFrame) -> None:
    """Create an empty DataFrame with the expected columns for
    unpack_data_packed, handling edge case of empty input."""
    check_downstream_version(df)
    check_expected_columns(
        df,
        expected_columns=[
            "dstream_algo",
            "dstream_S",
            "dstream_T",
            "dstream_storage_hex",
        ],
    )

    if (
        not df.lazy()
        .filter(pl.col("dstream_T") < pl.col("dstream_S"))
        .limit(1)
        .collect()
        .is_empty()
    ):
        raise NotImplementedError("T < S not yet supported")

    if len(df.lazy().select("dstream_algo").unique().limit(2).collect()) > 1:
        raise NotImplementedError("Multiple dstream_algo not yet supported")

    if len(df.lazy().select("dstream_S").unique().limit(2).collect()) > 1:
        raise NotImplementedError("Multiple dstream_S not yet supported")


def _check_bitwidths(df: pl.DataFrame) -> None:
    """Raise NotImplementedError if value bitwidth is not supported."""
    if (
        not df.lazy()
        .filter(pl.col("dstream_value_bitwidth").cast(pl.UInt32) > 64)
        .limit(1)
        .collect()
        .is_empty()
    ):
        raise NotImplementedError("Value bitwidth > 64 not yet supported")
    if (
        not df.lazy()
        .filter(pl.col("dstream_value_bitwidth").cast(pl.UInt32).is_in([2, 3]))
        .limit(1)
        .collect()
        .is_empty()
    ):
        raise NotImplementedError("Value bitwidth 2 and 3 not yet supported")
    if (
        not df.lazy()
        .filter(pl.col("dstream_value_bitwidth").diff() != pl.lit(0))
        .limit(1)
        .collect()
        .is_empty()
    ):
        raise NotImplementedError("Multiple value bitwidths not yet supported")


def _get_value_dtype(value_type: str) -> pl.DataType:
    """Convert value_type string arg to Polars DataType object."""
    value_dtype = {
        "hex": "hex",
        "uint64": pl.UInt64,
        "uint32": pl.UInt32,
        "uint16": pl.UInt16,
        "uint8": pl.UInt8,
    }.get(value_type, None)
    if value_dtype is None:
        raise ValueError("Invalid value_type")
    elif value_dtype == "hex":
        raise NotImplementedError("hex value_type not yet supported")

    return value_dtype


def _make_empty(value_dtype: pl.DataType) -> pl.DataFrame:
    """Create an empty DataFrame with the expected columns for
    unpack_data_packed, handling edge case of empty input."""
    return pl.DataFrame(
        [
            pl.Series(name="dstream_data_id", values=[], dtype=pl.UInt64),
            pl.Series(name="dstream_algo", values=[], dtype=pl.Categorical),
            pl.Series(name="dstream_S", values=[], dtype=pl.UInt32),
            pl.Series(name="dstream_Tbar", values=[], dtype=pl.UInt64),
            pl.Series(name="dstream_T", values=[], dtype=pl.UInt64),
            pl.Series(name="dstream_value", values=[], dtype=value_dtype),
            pl.Series(
                name="dstream_value_bitwidth", values=[], dtype=pl.UInt32
            ),
        ],
    )


def explode_lookup_unpacked(
    df: pl.DataFrame,
    *,
    value_type: typing.Literal["hex", "uint64", "uint32", "uint16", "uint8"],
    result_schema: typing.Literal["coerce", "relax", "shrink"] = "coerce",
) -> pl.DataFrame:
    """Explode downstream-curated data from one-buffer-per-row (with each
    buffer containing multiple data items) to one-data-item-per-row, applying
    downstream lookup to identify origin time `Tbar` of each item.

    Parameters
    ----------
    df : pl.DataFrame
        The input DataFrame containing unpacked data with required columns, one
        row per dstream buffer.

        Required schema:

        - 'dstream_algo' : pl.Categorical
            - Name of downstream curation algorithm used
            - e.g., 'dstream.steady_algo'
        - 'dstream_S' : pl.UInt32
            - Capacity of dstream buffer, in number of data items.
        - 'dstream_T' : pl.UInt64
            - Logical time elapsed (number of elapsed data items in stream).
        - 'dstream_storage_hex' : pl.String
            - Raw dstream buffer binary data, containing packed data items.
            - Represented as a hexadecimal string.

        Optional schema:

        - 'downstream_version' : pl.Categorical
            - Version of downstream library used to curate data items.

        Additional user-defined columns will be forwarded to the output
        DataFrame.

    value_type : {'hex', 'uint64', 'uint32', 'uint16', 'uint8'}
        The desired data type for the 'dstream_value' column in the output
        DataFrame.

        Note that 'hex' is not yet supported.

    result_schema : Literal['coerce', 'relax', 'shrink'], default 'coerce'
        How should dtypes in the output DataFrame be handled?
        - 'coerce' : cast all columns to output schema.
        - 'relax' : keep all columns as-is.
        - 'shrink' : cast columns to smallest possible types.

    Returns
    -------
    pl.DataFrame
        A DataFrame with exploded data and extracted values, one row per data
        item from the input dstream buffers.

        Output schema:

        - 'dstream_data_id' : pl.UInt64
            - Row index identifier of dstream buffer that data item is from.
        - 'dstream_Tbar' : pl.UInt64
            - Logical position of data item in stream (number of prior data
              items).
        - 'dstream_T' : pl.UInt64
            - Logical time elapsed (number of elapsed data items in stream).
        - 'dstream_value' : pl.String or specified numeric type
            - Data item content, format depends on 'value_type' argument.
        - 'dstream_value_bitwidth' : pl.UInt32
            - Size of 'dstream_value' in bits.

        User-defined columns are NOT forwarded from the unpacked dataframe. To
        include additional columns, join the output DataFrame with the original
        input DataFrame.

    Raises
    ------
    NotImplementedError
        - If 'dstream_value_bitwidth' is greater than 64 or equal to 2 or 3.
        - If 'dstream_value_bitwidth' is not consistent across all data items.
        - If 'dstream_S' is not consistent across all dstream buffers.
        - If buffers aren't filled (i.e., 'dstream_T' < 'dstream_S').
        - If multiple dstream algorithms are present in the input DataFrame.
        - If 'value_type' is 'hex'.
    ValeError
        If any of the required columns are missing from the input DataFrame.

    See Also
    --------
    unpack_data_packed :
        Preproccessing step, converts data with downstream buffer and counter
        serialized into a single hexadecimal string into input format for this
        function.
    """
    _check_df(df)
    value_dtype = _get_value_dtype(value_type)

    if df.lazy().limit(1).collect().is_empty():
        return _make_empty(value_dtype)

    dstream_S = df.lazy().select("dstream_S").limit(1).collect().item()
    dstream_algo = df.lazy().select("dstream_algo").limit(1).collect().item()
    dstream_algo = eval(dstream_algo)
    num_records = df.lazy().select(pl.len()).collect().item()
    num_items = num_records * dstream_S

    logging.info("begin explode_lookup_unpacked")
    logging.info(" - prepping data...")

    df = (
        df.with_columns(
            pl.coalesce(
                pl.col("^dstream_data_id$"),
                pl.arange(num_records, dtype=pl.UInt64),
            ).alias("dstream_data_id"),
        )
        .select(["dstream_data_id", "dstream_storage_hex", "dstream_T"])
        .select(pl.all())
        .sort("dstream_T")
    )

    df = df.with_columns(
        dstream_value_bitwidth=np.right_shift(
            pl.col("dstream_storage_hex").str.len_bytes() * 4,
            int(dstream_S).bit_length() - 1,
        ),
    )

    _check_bitwidths(df)

    logging.info(" - exploding dataframe...")

    df_long = df.drop("dstream_storage_hex").select(
        pl.all().gather(np.repeat(np.arange(num_records), dstream_S)),
    )

    logging.info(" - unpacking hex strings...")

    concat_hex = (
        df.lazy()
        .select(pl.col("dstream_storage_hex").str.join(""))
        .collect()
        .item()
    )

    df_long = df_long.with_columns(
        dstream_value=pl.Series(
            unpack_hex(concat_hex, num_items), dtype=value_dtype
        ),
    )

    logging.info(" - looking up ingest times...")

    lookup_op = dstream_algo.lookup_ingest_times_batched
    dstream_T = df.lazy().select("dstream_T").collect().to_numpy().ravel()
    df_long = (
        df_long.with_columns(
            dstream_Tbar=pl.Series(
                name="dstream_Tbar",
                values=lookup_op(dstream_S, dstream_T).ravel(),
            ),
        )
        .lazy()
        .collect()
    )

    logging.info(" - finalizing result schema")
    try:
        df_long = {
            "coerce": lambda df: df.cast(
                {
                    "dstream_data_id": pl.UInt64,
                    "dstream_Tbar": pl.UInt64,
                    "dstream_T": pl.UInt64,
                    "dstream_value": value_dtype,
                    "dstream_value_bitwidth": pl.UInt32,
                },
            ),
            "relax": lambda df: df,
            "shrink": lambda df: df.select(pl.all().shrink_dtype()),
        }[result_schema](df_long)
    except KeyError:
        raise ValueError(f"Invalid arg {result_schema} for result_schema")

    logging.info("explode_lookup_unpacked complete")
    return df_long
