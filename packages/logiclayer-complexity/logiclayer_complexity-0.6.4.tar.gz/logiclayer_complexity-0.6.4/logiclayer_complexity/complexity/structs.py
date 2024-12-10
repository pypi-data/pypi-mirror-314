from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping, Optional, Tuple

import economic_complexity as ec
import pandas as pd
from typing_extensions import Literal

from logiclayer_complexity.common import df_pivot, series_compare

if TYPE_CHECKING:
    from logiclayer_complexity.rca import RcaParameters, RcaSubnationalParameters


@dataclass
class ComplexityParameters:
    rca_params: "RcaParameters"
    cutoff: float = 1
    iterations: int = 20
    rank: bool = False
    sort_ascending: Optional[bool] = None

    def _calculate(self, rca: pd.Series, kind: Literal["ECI", "PCI"]) -> pd.Series:
        df_rca = rca.unstack()
        eci, pci = ec.complexity(df_rca, cutoff=self.cutoff, iterations=self.iterations)

        if kind == "ECI":
            return eci
        if kind == "PCI":
            return pci

        raise ValueError(
            "Complexity calculation must intend to retrieve 'ECI' or 'PCI'"
        )

    def calculate(self, df: pd.DataFrame, kind: Literal["ECI", "PCI"]) -> pd.DataFrame:
        sort_ascending = self.sort_ascending
        name = f"{self.rca_params.measure} {kind}"

        df_pivot = self.rca_params.pivot(df)

        rca = self.rca_params._calculate(df_pivot)
        cmplx = self._calculate(rca, kind)

        df_cmplx = cmplx.reset_index(name=name)

        col_id: str = df_pivot.index.name if kind == "ECI" else df_pivot.columns.name
        if col_id.endswith(" ID") and col_id[:-3] in df.columns:
            #delete columns that are not needed by endpoints in order to obtain the complete hierarchies in df
            if kind == "ECI":
                df.drop(columns = [self.rca_params.measure, self.rca_params.activity, f"{self.rca_params.activity} ID"], inplace=True)
            else:
                df.drop(columns = [self.rca_params.measure, self.rca_params.location, f"{self.rca_params.location} ID"], inplace=True)

            df_cmplx = df_cmplx.merge(df.drop_duplicates(), on=col_id, how='left')

        if sort_ascending is not None:
            df_cmplx.sort_values(by=name, ascending=sort_ascending, inplace=True)

        if sort_ascending is not None or self.rank:
            df_cmplx[f"{name} Ranking"] = (
                df_cmplx[name].rank(ascending=False, method="max").astype(int)
            )

        return df_cmplx


@dataclass
class ComplexitySubnationalParameters:
    rca_params: "RcaSubnationalParameters"
    eci_threshold: Mapping[str, Tuple[str, int]]
    cutoff: float
    rank: bool = False
    sort_ascending: Optional[bool] = None

    def _calculate(
        self,
        df_subnat: pd.DataFrame,
        df_global: pd.DataFrame,
        name: Literal["ECI", "PCI"],
    ):
        cutoff = self.cutoff
        eci_threshold = self.eci_threshold
        params = self.rca_params.subnat_params

        location = params.location
        location_id = params.location_id
        activity = params.activity
        activity_id = params.activity_id

        complexity_measure = f"{params.measure} {name}"
        rca_measure = f"{params.measure} RCA"

        complexity_dd_id = location_id if name == "ECI" else activity_id

        rca, tbl, df = self.rca_params._calculate_subnat(df_subnat, df_global)

        df_copy = rca.copy()
        df = df_pivot(rca, index=location_id, column=activity_id, value=rca_measure)

        if eci_threshold:
            rcas = df.copy()
            rcas[rcas >= cutoff] = 1
            rcas[rcas < cutoff] = 0

            # Removes small data related with drilldown1
            if location in eci_threshold:
                condition = eci_threshold[location]
                cols = rcas.sum(axis=1)
                cols = list(cols[series_compare(cols, *condition)].index)
                df = df[df.index.isin(cols)]
                df_copy = df_copy[df_copy[location_id].isin(cols)]

            # Removes small data related with drilldown2
            if activity in eci_threshold:
                condition = eci_threshold[activity]
                rows = rcas.sum(axis=0)
                rows = list(rows[series_compare(cols, *condition)].index)
                df = df[rows]
                df_copy = df_copy[df_copy[activity_id].isin(cols)]

        eci, pci = ec.complexity(ec.rca(tbl))
        df_pci = pd.DataFrame(pci).rename(columns={0: complexity_measure}).reset_index()
        df_pci = df_pci.merge(df_copy, on=activity_id)

        results = (
            df_pci[df_pci[rca_measure] >= 1]
            .groupby([complexity_dd_id])
            .mean(numeric_only=True)
            .reset_index()
        )
        results = results[[complexity_dd_id] + [complexity_measure]]

        return results

    def calculate(
        self,
        df_subnat: pd.DataFrame,
        df_global: pd.DataFrame,
        calc: Literal["ECI", "PCI"],
    ) -> pd.DataFrame:
        sort_ascending = self.sort_ascending
        params = self.rca_params.subnat_params

        name = f"{params.measure} {calc}"

        ds = self._calculate(df_subnat, df_global, calc)

        if sort_ascending is not None:
            ds.sort_values(by=name, ascending=sort_ascending, inplace=True)

        if sort_ascending is not None or self.rank:
            ds[f"{calc} Ranking"] = (
                ds[name].rank(ascending=False, method="max").astype(int)
            )

        #delete columns that are not needed by endpoints in order to obtain the complete hierarchies in df
        if calc == "ECI":
            column_id = params.location_id
            df_subnat.drop(columns = [params.activity_id, params.activity, params.measure], inplace=True)
        
        else:
            column_id = params.activity_id
            df_subnat.drop(columns = [params.location_id, params.location, params.measure], inplace=True)
     
        df_cmpx = ds.merge(
            df_subnat.drop_duplicates(), on=column_id, how="inner"
        )
  
        return df_cmpx
