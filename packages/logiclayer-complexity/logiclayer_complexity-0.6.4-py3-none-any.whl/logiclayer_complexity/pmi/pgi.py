from dataclasses import dataclass
from typing import Optional, Set

import economic_complexity as ec
import pandas as pd
from fastapi import Depends, Query
from tesseract_olap import DataRequest, DataRequestParams
from typing_extensions import Annotated

from ..rca import RcaParameters, prepare_rca_params


@dataclass
class PGIParameters:
    rca_params: RcaParameters
    gini_cube: str
    gini_location: str
    gini_measure: str
    cutoff: float = 1
    rank: bool = False
    sort_ascending: Optional[bool] = None

    @property
    def column_name(self):
        return f"{self.rca_params.measure} PGI"

    def build_request(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": [self.gini_location],
            "measures": [self.gini_measure],
            "roles": roles,
        }

        locale = self.rca_params.locale
        if locale is not None:
            params["locale"] = locale

        return DataRequest.new(self.gini_cube, params)

    def _calculate(self, df_pivot: pd.DataFrame, rca: pd.Series, gini: pd.DataFrame):
        df_rca = rca.unstack()

        # prepare gini dataframe
        gini_location = f"{self.gini_location} ID"
        df_gini = gini[[gini_location, self.gini_measure]]
        df_gini.set_index(gini_location, inplace=True)

        df_pgi = ec.pgi(tbl=df_pivot, rcas=df_rca, gini=df_gini, cutoff=self.cutoff)
        return df_pgi["pgi"].rename(self.column_name)

    def calculate(self, df: pd.DataFrame, gini: pd.DataFrame) -> pd.DataFrame:
        sort_ascending = self.sort_ascending
        name = self.column_name
        df_pivot = self.rca_params.pivot(df)

        rca = self.rca_params._calculate(df_pivot)
        pgi = self._calculate(df_pivot, rca, gini)
        df_pgi = pd.DataFrame(pgi, columns=[f"{self.rca_params.measure} PGI"]).reset_index()

        #delete columns that are not needed for the result
        activity_id = self.rca_params.activity_id
        df_labels = df.drop(columns = [self.rca_params.location, self.rca_params.location_id, self.rca_params.measure])
        ds = df_pgi.merge(df_labels.drop_duplicates(), on=activity_id, how="left")

        if sort_ascending is not None:
            ds.sort_values(by=name, ascending=sort_ascending, inplace=True)

        if sort_ascending is not None or self.rank:
            ds[f"{name} Ranking"] = (
                ds[name].rank(ascending=False, method="max").astype(int)
            )

        return ds


def prepare_pgi_params(
    gini_cube: Annotated[
        str,
        Query(
            description="The cube to retrieve the GINI data",
        ),
    ],
    gini_location: Annotated[
        str,
        Query(
            description="Geographical categories for the GINI calculation",
        ),
    ],
    gini_measure: Annotated[
        str,
        Query(
            description="Values to use for the PGI calculations",
        ),
    ],
    rca_params: RcaParameters = Depends(prepare_rca_params),
    ascending: Annotated[
        Optional[bool],
        Query(
            description=(
                "Outputs the results in ascending or descending order. "
                "If not defined, results will be returned sorted by level member."
            ),
        ),
    ] = None,
    cutoff: Annotated[
        float,
        Query(
            description=(
                "The threshold value at which a country's RCA is considered "
                "relevant for an economic activity, for the purpose of calculating "
                "the Complexity Indicators."
            ),
        ),
    ] = 1,
    rank: Annotated[
        bool,
        Query(
            description=(
                "Adds a 'Ranking' column to the data. "
                "This value represents the index in the whole result list, sorted by value."
            ),
        ),
    ] = False,
):
    return PGIParameters(
        rca_params=rca_params,
        gini_cube=gini_cube,
        gini_measure=gini_measure,
        gini_location=gini_location,
        cutoff=cutoff,
        rank=rank,
        sort_ascending=ascending,
    )
