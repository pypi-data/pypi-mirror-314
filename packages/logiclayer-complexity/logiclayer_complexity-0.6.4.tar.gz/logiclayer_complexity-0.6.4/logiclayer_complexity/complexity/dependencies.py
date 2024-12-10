from typing import List, Optional

from fastapi import Depends, Query
from typing_extensions import Annotated

from logiclayer_complexity.dependencies import parse_threshold
from logiclayer_complexity.rca import (
    RcaParameters,
    RcaSubnationalParameters,
    prepare_rca_params,
    prepare_subnatrca_params,
)

from .structs import ComplexityParameters, ComplexitySubnationalParameters


def prepare_complexity_params(
    rca_params: RcaParameters = Depends(prepare_rca_params),
    iterations: Annotated[
        int,
        Query(
            description=(
                "The number of iterations used to calculate the Complexity Indicators."
            ),
        ),
    ] = 20,
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
    ascending: Annotated[
        Optional[bool],
        Query(
            description=(
                "Outputs the results in ascending or descending order. "
                "If not defined, results will be returned sorted by level member."
            ),
        ),
    ] = None,
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
    return ComplexityParameters(
        rca_params=rca_params,
        cutoff=cutoff,
        iterations=iterations,
        rank=rank,
        sort_ascending=ascending,
    )


def prepare_complexity_subnational_params(
    rca_params: RcaSubnationalParameters = Depends(prepare_subnatrca_params),
    threshold: Annotated[
        List[str],
        Query(
            alias="threshold_eci",
            description=(
                "Restricts the data to be used in the calculation, to rows where "
                "the sum of all values through the other dimension fulfills the condition."
            ),
        ),
    ] = [],
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
    ascending: Annotated[
        Optional[bool],
        Query(
            description=(
                "Outputs the results in ascending or descending order. "
                "If not defined, results will be returned sorted by level member."
            ),
        ),
    ] = None,
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
    return ComplexitySubnationalParameters(
        rca_params=rca_params,
        eci_threshold=parse_threshold(threshold),
        cutoff=cutoff,
        rank=rank,
        sort_ascending=ascending,
    )
