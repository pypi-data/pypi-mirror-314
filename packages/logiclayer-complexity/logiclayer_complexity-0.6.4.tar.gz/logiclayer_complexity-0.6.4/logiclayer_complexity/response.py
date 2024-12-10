import os
import tempfile as tmp
from enum import Enum
from hashlib import md5
from typing import Dict, Optional, Tuple

import orjson
import pandas as pd
from fastapi import HTTPException, Response
from fastapi.responses import FileResponse, PlainTextResponse
from starlette.background import BackgroundTask

from .structs import TopkIntent


class ResponseFormat(str, Enum):
    csv = "csv"
    excel = "xlsx"
    jsonarrays = "jsonarrays"
    jsonrecords = "jsonrecords"
    parquet = "parquet"
    tsv = "tsv"

    def __str__(self) -> str:
        return self.value

    def serialize(
        self,
        df: pd.DataFrame,
        aliases: Dict[str, str],
        filters: Dict[str, Tuple[str, ...]],
        topk: Optional["TopkIntent"] = None,
    ):
        # filter which members will be sent in the response
        for key, values in filters.items():
            column_id = f"{key} ID"
            dropping = df.loc[~df[column_id].isin(values)].index
            df.drop(dropping, inplace=True)
            del dropping

        # apply aliases requested by the user
        df.rename(columns=aliases, inplace=True)

        # apply topk parameter
        if topk:
            if topk.order == "desc":
                applyfn = lambda x: x.nlargest(topk.amount, topk.measure)
            else:
                applyfn = lambda x: x.nsmallest(topk.amount, topk.measure)
            df = df.groupby(topk.level, group_keys=False).apply(applyfn)

        return data_response(df, self)


MIMETYPES = {
    ResponseFormat.csv: "text/csv",
    ResponseFormat.excel: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ResponseFormat.jsonarrays: "application/json",
    ResponseFormat.jsonrecords: "application/json",
    ResponseFormat.parquet: "application/vnd.apache.parquet",
    ResponseFormat.tsv: "text/tab-separated-values",
}
TEMPDIR = os.getenv("TESSERACT_TEMPDIR", os.getcwd())


def data_response(
    df: pd.DataFrame,
    extension: ResponseFormat,
) -> Response:
    columns = tuple(df.columns)

    headers = {
        "X-Tesseract-Columns": ",".join(columns),
        "X-Tesseract-QueryRows": str(len(df.index)),
    }
    kwargs = {"headers": headers, "media_type": MIMETYPES[extension]}

    if extension is ResponseFormat.csv:
        content = df.to_csv(sep=",", index=False)
        return PlainTextResponse(content, **kwargs)

    elif extension is ResponseFormat.tsv:
        content = df.to_csv(sep="\t", index=False)
        return PlainTextResponse(content, **kwargs)

    elif extension is ResponseFormat.jsonarrays:
        res = df.to_dict("tight")
        target = {"columns": columns, "data": res["data"]}
        content = orjson.dumps(target)
        return PlainTextResponse(content, **kwargs)

    elif extension is ResponseFormat.jsonrecords:
        target = {"columns": columns, "data": df.to_dict("records")}
        content = orjson.dumps(target)
        return PlainTextResponse(content, **kwargs)

    elif extension is ResponseFormat.excel:
        with tmp.NamedTemporaryFile(
            delete=False, dir=TEMPDIR, suffix=f".{extension}"
        ) as tmp_file:
            df.to_excel(tmp_file.name, engine="xlsxwriter")

        kwargs["filename"] = f"data_{shorthash(','.join(columns))}.{extension}"
        kwargs["background"] = BackgroundTask(os.unlink, tmp_file.name)
        return FileResponse(tmp_file.name, **kwargs)

    elif extension is ResponseFormat.parquet:
        with tmp.NamedTemporaryFile(
            delete=False, dir=TEMPDIR, suffix=f".{extension}"
        ) as tmp_file:
            df.to_parquet(tmp_file.name)

        kwargs["filename"] = f"data_{shorthash(','.join(columns))}.{extension}"
        kwargs["background"] = BackgroundTask(os.unlink, tmp_file.name)
        return FileResponse(tmp_file.name, **kwargs)

    raise HTTPException(406, f"Requested format is not supported: {extension}")


def shorthash(string: str) -> str:
    return str(md5(string.encode("utf-8")).hexdigest())[:8]
