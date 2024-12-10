from dataclasses import dataclass
from typing import Optional, Set

import economic_complexity as ec
import pandas as pd
from fastapi import Depends, Query
from tesseract_olap import DataRequest, DataRequestParams
from typing_extensions import Annotated

from ..rca import RcaParameters, prepare_rca_params


@dataclass
class PEIIParameters:
    rca_params: RcaParameters
    emissions_cube: str
    emissions_measure: str
    emissions_location: str
    cutoff: float = 1
    rank: bool = False
    sort_ascending: Optional[bool] = None

    @property
    def column_name(self):
        return f"{self.rca_params.measure} PEII"

    def build_request(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": [self.emissions_location],
            "measures": [self.emissions_measure],
            "roles": roles,
        }

        locale = self.rca_params.locale
        if locale is not None:
            params["locale"] = locale

        return DataRequest.new(self.emissions_cube, params)

    def _calculate(
        self, df_pivot: pd.DataFrame, rca: pd.Series, emissions: pd.DataFrame
    ) -> pd.Series:
        df_rca = rca.unstack()

        # prepare emissions dataframe
        emissions_location = f"{self.emissions_location} ID"
        df_emissions = emissions[[emissions_location, self.emissions_measure]]
        df_emissions.set_index(emissions_location, inplace=True)

        df_peii = ec.peii(
            tbl=df_pivot, rcas=df_rca, emissions=df_emissions, cutoff=self.cutoff
        )
        return df_peii["peii"].rename(self.column_name)

    def calculate(self, df: pd.DataFrame, emissions: pd.DataFrame) -> pd.DataFrame:
        sort_ascending = self.sort_ascending
        name = self.column_name

        df_pivot = self.rca_params.pivot(df)

        rca = self.rca_params._calculate(df_pivot)
        peii = self._calculate(df_pivot, rca, emissions)
        df_peii = pd.DataFrame(peii, columns=[f"{self.rca_params.measure} PEII"]).reset_index()

        #delete columns that are not needed for the result
        activity_id = self.rca_params.activity_id
        df_labels = df.drop(columns = [self.rca_params.location, self.rca_params.location_id, self.rca_params.measure])

        ds = df_peii.merge(df_labels.drop_duplicates(), on=activity_id, how="left")

        if sort_ascending is not None:
            ds.sort_values(by=name, ascending=sort_ascending, inplace=True)

        if sort_ascending is not None or self.rank:
            ds[f"{name} Ranking"] = (
                ds[name].rank(ascending=False, method="max").astype(int)
            )

        return ds


def prepare_peii_params(
    emissions_cube: Annotated[
        str,
        Query(
            description="The cube to retrieve the Emissions data",
        ),
    ],
    emissions_measure: Annotated[
        str,
        Query(
            description="Values to use for the PEII calculations",
        ),
    ],
    emissions_location: Annotated[
        str,
        Query(
            description="Geographical categories for the emission calculation",
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
    return PEIIParameters(
        rca_params=rca_params,
        emissions_cube=emissions_cube,
        emissions_measure=emissions_measure,
        emissions_location=emissions_location,
        cutoff=cutoff,
        rank=rank,
        sort_ascending=ascending,
    )
