from os import PathLike
import pickle
from typing import Any
import blosc
from .utils import (
    df_to_parquetstream,
    df_to_base64,
    df_to_hex,
    parquetstream_to_df,
    base64_to_df,
    hex_to_df,
)


def blosc_pickle(obj: Any, file: PathLike | None = None):
    pickled = pickle.dumps(obj)
    compressed = blosc.compress(pickled)

    if file is not None:
        with open(file, "wb") as f:
            f.write(compressed)
    return compressed


def blosc_unpickle(data: str | bytes | None = None, file: PathLike | None = None):
    if data is None and file is None:
        raise Exception("Either 'data' or 'file' must be provided, but both were None.")

    if data is None and file is not None:
        with open(file, "rb") as f:
            compressed_pkl = f.read()
    else:
        compressed_pkl = data

    pkled = blosc.decompress(compressed_pkl)
    return pickle.loads(pkled)


__all__ = [
    "df_to_parquetstream",
    "df_to_base64",
    "df_to_hex",
    "parquetstream_to_df",
    "base64_to_df",
    "hex_to_df",
    "blosc_pickle",
    "blosc_unpickle",
]
