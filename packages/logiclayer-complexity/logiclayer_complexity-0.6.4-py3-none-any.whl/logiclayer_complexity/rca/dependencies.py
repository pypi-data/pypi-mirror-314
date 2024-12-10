from typing import Dict, List, Optional, Tuple

from fastapi import Depends, Query
from typing_extensions import Annotated

from logiclayer_complexity.dependencies import parse_cuts, parse_threshold

from .structs import RcaHistoricalParameters, RcaParameters, RcaSubnationalParameters


def prepare_rca_params(
    cube: Annotated[
        str,
        Query(
            description="The cube to retrieve the main data",
        ),
    ],
    activity: Annotated[
        str,
        Query(
            description="Productivity categories for the RCA calculation",
        ),
    ],
    location: Annotated[
        str,
        Query(
            description="Geographical categories for the RCA calculation",
        ),
    ],
    measure: Annotated[
        str,
        Query(
            description="Values to use for the RCA calculations",
        ),
    ],
    cuts: Dict[str, Tuple[str, ...]] = Depends(parse_cuts),
    locale: Annotated[
        Optional[str],
        Query(description="Defines the locale variation for the labels in the data"),
    ] = None,
    parents: Annotated[
        bool,
        Query(
            description="Specifies if the response items should include the "
            "parent levels for activity and location."
        ),
    ] = False,
    threshold: Dict[str, Tuple[str, int]] = Depends(parse_threshold),
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
    return RcaParameters(
        cube=cube,
        activity=activity,
        location=location,
        measure=measure,
        cuts=cuts,
        locale=locale,
        parents=parents,
        threshold=threshold,
        rank=rank,
        sort_ascending=ascending,
    )


def prepare_subnatrca_global_params(
    cube: Annotated[
        str,
        Query(
            alias="global_cube",
            description="The cube to retrieve the global data",
        ),
    ],
    activity: Annotated[
        str,
        Query(
            alias="global_activity",
            description="Productivity categories for the RCA calculation",
        ),
    ],
    location: Annotated[
        str,
        Query(
            alias="global_location",
            description="Geographical categories for the RCA calculation",
        ),
    ],
    measure: Annotated[
        str,
        Query(
            alias="global_measure",
            description="Measurement to use for the RCA calculations",
        ),
    ],
    cuts: Annotated[
        List[str],
        Query(
            alias="global_cuts",
            description=(
                "Limits the results returned by the output. Only members of a "
                "dimension matching one of the parameters will be kept in the response."
            ),
        ),
    ] = [],
    locale: Annotated[
        Optional[str],
        Query(description="Locale for the labels in the data"),
    ] = None,
    threshold: Annotated[
        List[str],
        Query(
            alias="global_threshold",
            description="Restricts the data to be used in the calculation, "
            "to rows where the sum of all values through the other dimension "
            "fulfills the condition.",
        ),
    ] = [],
):
    return RcaParameters(
        cube=cube,
        activity=activity,
        location=location,
        measure=measure,
        cuts=parse_cuts(cuts),
        locale=locale,
        threshold=parse_threshold(threshold),
    )


def prepare_subnatrca_subnat_params(
    cube: Annotated[
        str,
        Query(
            alias="subnat_cube",
            description="The cube to retrieve the main data",
        ),
    ],
    activity: Annotated[
        str,
        Query(
            alias="subnat_activity",
            description="Productivity categories for the RCA calculation",
        ),
    ],
    location: Annotated[
        str,
        Query(
            alias="subnat_location",
            description="Geographical categories for the RCA calculation",
        ),
    ],
    measure: Annotated[
        str,
        Query(
            alias="subnat_measure",
            description="Measurement to use for the RCA calculations",
        ),
    ],
    cuts: Annotated[
        List[str],
        Query(
            alias="subnat_cuts",
            description=(
                "Limits the results returned by the output. Only members of a "
                "dimension matching one of the parameters will be kept in the response."
            ),
        ),
    ] = [],
    locale: Annotated[
        Optional[str], Query(description="Locale for the labels in the data")
    ] = None,
    parents: Annotated[
        bool,
        Query(
            description="Specifies if the response items should include the "
            "parent levels for activity and location."
        ),
    ] = False,
    threshold: Annotated[
        List[str],
        Query(
            alias="subnat_threshold",
            description=(
                "Restricts the data to be used in the calculation, to rows where "
                "the sum of all values through the other dimension fulfills the condition."
            ),
        ),
    ] = [],
):
    return RcaParameters(
        cube=cube,
        activity=activity,
        location=location,
        measure=measure,
        cuts=parse_cuts(cuts),
        locale=locale,
        parents=parents,
        threshold=parse_threshold(threshold),
    )


def prepare_subnatrca_params(
    subnat_params: RcaParameters = Depends(prepare_subnatrca_subnat_params),
    global_params: RcaParameters = Depends(prepare_subnatrca_global_params),
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
    return RcaSubnationalParameters(
        global_params=global_params,
        subnat_params=subnat_params,
        rank=rank,
        sort_ascending=ascending,
    )


def prepare_historicalrca_params(
    cube: Annotated[
        str,
        Query(
            description="The cube to retrieve the main data",
        ),
    ],
    activity: Annotated[
        str,
        Query(
            description="Productivity categories for the RCA calculation",
        ),
    ],
    location: Annotated[
        str,
        Query(
            description="Geographical categories for the RCA calculation",
        ),
    ],
    time: Annotated[
        str,
        Query(
            description="Unit of time used for calculations",
        ),
    ],
    measure: Annotated[
        str,
        Query(
            description="Values to use for the RCA calculations",
        ),
    ],
    cuts: Dict[str, Tuple[str, ...]] = Depends(parse_cuts),
    locale: Annotated[
        Optional[str],
        Query(description="Defines the locale variation for the labels in the data"),
    ] = None,
    parents: Annotated[
        bool,
        Query(
            description="Specifies if the response items should include the "
            "parent levels for activity and location."
        ),
    ] = False,
    threshold: Dict[str, Tuple[str, int]] = Depends(parse_threshold),
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
    return RcaHistoricalParameters(
        cube=cube,
        activity=activity,
        location=location,
        measure=measure,
        time=time,
        cuts=cuts,
        locale=locale,
        parents=parents,
        threshold=threshold,
        rank=rank,
        sort_ascending=ascending,
    )
