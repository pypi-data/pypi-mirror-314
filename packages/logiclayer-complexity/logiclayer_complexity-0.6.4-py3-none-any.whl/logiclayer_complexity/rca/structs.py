from dataclasses import dataclass, field
from typing import Dict, Mapping, Optional, Set, Tuple

import economic_complexity as ec
import pandas as pd
from tesseract_olap import DataRequest, DataRequestParams

from logiclayer_complexity.common import df_melt, df_pivot, series_compare


@dataclass
class RcaParameters:
    cube: str
    activity: str
    location: str
    measure: str
    cuts: Mapping[str, Tuple[str, ...]] = field(default_factory=dict)
    locale: Optional[str] = None
    parents: bool = False
    threshold: Mapping[str, Tuple[str, float]] = field(default_factory=dict)
    rank: bool = False
    sort_ascending: Optional[bool] = None

    @property
    def activity_id(self):
        return self.activity + " ID"

    @property
    def location_id(self):
        return self.location + " ID"

    @property
    def column_name(self):
        return f"{self.measure} RCA"

    def build_request(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": (self.location, self.activity),
            "measures": (self.measure,),
            "cuts_include": {**self.cuts},
            "parents": self.parents,
            "roles": roles,
        }

        if self.locale is not None:
            params["locale"] = self.locale

        return DataRequest.new(self.cube, params)

    def apply_threshold(self, df: "pd.DataFrame"):
        """Applies threshold ranges over the provided DataFrame in-place."""
        measure = self.measure

        for level, condition in self.threshold.items():
            column_id = f"{level} ID"
            # From data, group rows by `level` dimension and get the sum of `measure`
            measure_sum = df[[column_id, measure]].groupby(by=[column_id]).sum()
            # Apply threshold condition and get rows that comply
            sum_to_drop = measure_sum.loc[
                series_compare(measure_sum[measure], *condition)
            ]
            # Drop complying rows from summed dataframe (leaving non-complying only)
            measure_sum.drop(sum_to_drop.index, inplace=True)
            # Get indexes of non-complying rows
            data_to_drop = df.loc[df[column_id].isin(measure_sum.index)].index
            # ...and drop them from the original data
            df.drop(data_to_drop, inplace=True)

            del measure_sum, sum_to_drop, data_to_drop

    def pivot(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pivots the Tidy DataFrame to prepare for calculations."""
        location_id = self.location_id
        index = location_id if location_id in df.columns else self.location

        activity_id = self.activity_id
        columns = activity_id if activity_id in df.columns else self.activity

        # pivot the table and remove NAs
        tbl = pd.pivot_table(df, index=index, columns=columns, values=self.measure)
        tbl.dropna(axis=1, how="all", inplace=True)
        tbl.fillna(0, inplace=True)

        return tbl.astype(float)

    def _calculate(self, tbl: "pd.DataFrame") -> pd.Series:
        """Performs the RCA calculation."""
        df_rca = ec.rca(tbl)
        rca = df_rca.stack()
        assert isinstance(rca, pd.Series), "Calculation did not yield a pandas.Series"
        return rca.rename(self.column_name)

    def calculate(self, df: "pd.DataFrame") -> pd.DataFrame:
        """Execute RCA calculations."""
        sort_ascending = self.sort_ascending
        name = self.column_name

        # pivot the data to prepare for calculation
        pivot_tbl = self.pivot(df)
        columns = pivot_tbl.index.name, pivot_tbl.columns.name

        # calculate RCA values
        rca = self._calculate(pivot_tbl)
        ds = df.merge(rca.reset_index(), how="left", on=columns)

        # merge RCA values to input DataFrame
        if sort_ascending is not None:
            ds.sort_values(by=name, ascending=sort_ascending, inplace=True)

        if sort_ascending is not None or self.rank:
            ds[f"{name} Ranking"] = (
                ds[name].rank(ascending=False, method="max").astype(int)
            )

        return ds


@dataclass
class RcaSubnationalParameters:
    subnat_params: RcaParameters
    global_params: RcaParameters
    rank: bool = False
    sort_ascending: Optional[bool] = None

    def _calculate_subnat(self, df_subnat: pd.DataFrame, df_global: pd.DataFrame):
        params_global = self.global_params
        params_subnat = self.subnat_params

        # Prepare Subnational data
        params_subnat.apply_threshold(df_subnat)
        pv_subnat = df_pivot(
            df=df_subnat,
            index=params_subnat.location_id,
            column=params_subnat.activity_id,
            value=params_subnat.measure,
        )

        # Sum activities for each subnat location
        location_sum = pv_subnat.sum(axis=1)

        # Calculates numerator
        rca_numerator = pv_subnat.divide(location_sum, axis=0)

        # Prepare Global data
        params_global.apply_threshold(df_global)
        pv_global = df_pivot(
            df=df_global,
            index=params_global.location_id,
            column=params_global.activity_id,
            value=params_global.measure,
        )

        # Sum locations for each activity globally
        row_sums = pv_global.sum(axis=0)

        # Calculates denominator
        rca_denominator = row_sums / row_sums.sum()  # type: pd.Series

        # Calculates subnational RCA
        tbl_rca = rca_numerator / rca_denominator
        rca_subnat = df_melt(
            tbl_rca,
            index=params_subnat.location_id,
            value=f"{params_subnat.measure} RCA",
        )

        return rca_subnat, pv_global, tbl_rca

    def calculate(self, df_subnat: pd.DataFrame, df_global: pd.DataFrame):
        sort_ascending = self.sort_ascending
        params = self.subnat_params

        name = f"{params.measure} RCA"

        ds, _, _ = self._calculate_subnat(df_subnat, df_global)

        if sort_ascending is not None:
            ds.sort_values(by=name, ascending=sort_ascending, inplace=True)

        if sort_ascending is not None or self.rank:
            ds[f"{name} Ranking"] = (
                ds[name].rank(ascending=False, method="max").astype(int)
            )

        # recover missing labels using InnerJoin against original subnat DF
        df_rca = ds.merge(
            df_subnat,
            on=[params.location_id, params.activity_id],
            how="inner",
        )

        return df_rca


@dataclass
class RcaHistoricalParameters:
    cube: str
    activity: str
    location: str
    time: str
    measure: str
    cutoff: float = 1
    cuts: Dict[str, Tuple[str, ...]] = field(default_factory=dict)
    locale: Optional[str] = None
    parents: bool = False
    rank: bool = False
    sort_ascending: Optional[bool] = None
    threshold: Mapping[str, Tuple[str, float]] = field(default_factory=dict)

    def build_request_a(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": (self.location, self.activity, self.time),
            "measures": (self.measure,),
            "cuts_include": {**self.cuts},
            "parents": self.parents,
            "roles": roles,
        }

        if self.locale is not None:
            params["locale"] = self.locale

        return DataRequest.new(self.cube, params)

    def build_request_b(self, roles: Set[str]) -> DataRequest:
        cuts_copy = self.cuts.copy()
        if self.cuts:
            cuts_copy.pop(self.location, None)

        params: DataRequestParams = {
            "drilldowns": (self.activity, self.time),
            "measures": (self.measure,),
            "cuts_include": {**cuts_copy},
            "roles": roles,
        }

        if self.locale is not None:
            params["locale"] = self.locale

        return DataRequest.new(self.cube, params)

    def build_request_c(self, roles: Set[str]) -> DataRequest:
        cuts_copy = self.cuts.copy()
        if self.cuts:
            cuts_copy.pop(self.activity, None)

        params: DataRequestParams = {
            "drilldowns": (self.location, self.time),
            "measures": (self.measure,),
            "cuts_include": {**cuts_copy},
            "roles": roles,
        }

        if self.locale is not None:
            params["locale"] = self.locale

        return DataRequest.new(self.cube, params)

    def build_request_d(self, roles: Set[str]) -> DataRequest:
        cuts_copy = self.cuts.copy()
        if self.cuts:
            cuts_copy.pop(self.activity, None)
            cuts_copy.pop(self.location, None)

        params: DataRequestParams = {
            "drilldowns": (self.time,),
            "measures": (self.measure,),
            "cuts_include": {**cuts_copy},
            "roles": roles,
        }

        if self.locale is not None:
            params["locale"] = self.locale

        return DataRequest.new(self.cube, params)

    def calculate(
        self,
        df_a: "pd.DataFrame",
        df_b: "pd.DataFrame",
        df_c: "pd.DataFrame",
        df_d: "pd.DataFrame",
    ):
        """Execute RCA calculations."""
        measure = f"{self.measure} RCA"

        df_b.rename(columns={self.measure: f"{self.measure} B"}, inplace=True)
        df_c.rename(columns={self.measure: f"{self.measure} C"}, inplace=True)
        df_d.rename(columns={self.measure: f"{self.measure} D"}, inplace=True)

        common_columns = df_a.columns.intersection(df_b.columns).tolist()
        df_final = df_a.merge(df_b, on=common_columns, how="left")

        common_columns = df_final.columns.intersection(df_c.columns).tolist()
        df_final = df_final.merge(df_c, on=common_columns, how="left")
        df_final = df_final.merge(df_d, on=[self.time], how="left")

        df_final[f"{self.measure} RCA"] = (
            df_final[self.measure] / df_final[f"{self.measure} B"]
        ) / (df_final[f"{self.measure} C"] / df_final[f"{self.measure} D"])
        df_final.drop(
            columns=[f"{self.measure} B", f"{self.measure} C", f"{self.measure} D"],
            inplace=True,
        )

        if self.sort_ascending is not None:
            df_final.sort_values(
                by=measure, ascending=self.sort_ascending, inplace=True
            )

        if self.sort_ascending is not None or self.rank:
            df_final[f"{measure} Ranking"] = (
                df_final[measure].rank(ascending=False, method="max").astype(int)
            )

        return df_final
