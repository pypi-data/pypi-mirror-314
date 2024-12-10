from typing import Optional

from fastapi import Depends, Query
from typing_extensions import Annotated

from logiclayer_complexity.rca import (
    RcaParameters,
    RcaSubnationalParameters,
    prepare_rca_params,
    prepare_subnatrca_params,
)

from .structs import (
    RelatednessParameters,
    RelatednessSubnationalParameters,
    RelativeRelatednessParameters,
    RelativeRelatednessSubnationalParameters,
)


def prepare_relatedness_params(
    rca_params: "RcaParameters" = Depends(prepare_rca_params),
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
    return RelatednessParameters(
        rca_params=rca_params,
        cutoff=cutoff,
        rank=rank,
        sort_ascending=ascending,
    )


def prepare_relatedness_subnational_params(
    rca_params: RcaSubnationalParameters = Depends(prepare_subnatrca_params),
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
    return RelatednessSubnationalParameters(
        rca_params=rca_params,
        cutoff=cutoff,
        rank=rank,
        sort_ascending=ascending,
    )


def prepare_relative_relatedness_params(
    rca_params: "RcaParameters" = Depends(prepare_rca_params),
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
    return RelativeRelatednessParameters(
        rca_params=rca_params,
        cutoff=cutoff,
        rank=rank,
        sort_ascending=ascending,
    )


def prepare_relative_relatedness_subnational_params(
    rca_params: RcaSubnationalParameters = Depends(prepare_subnatrca_params),
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
    return RelativeRelatednessSubnationalParameters(
        rca_params=rca_params,
        cutoff=cutoff,
        rank=rank,
        sort_ascending=ascending,
    )
