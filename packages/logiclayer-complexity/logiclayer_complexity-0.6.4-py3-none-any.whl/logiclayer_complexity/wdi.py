from dataclasses import dataclass, field
from typing import Dict, List

from fastapi import Query
from pydantic import BaseModel, model_validator
from tesseract_olap import DataRequest
from typing_extensions import Annotated, Required, TypedDict


class WdiParameters(BaseModel):
    year: List[int]
    indicator: str
    comparison: str
    value: int
    location: str = ""

    @model_validator(mode="before")
    @classmethod
    def parse_search(cls, content):
        if isinstance(content, str):
            try:
                year, indicator, comparison, value = content.split(":")
            except ValueError:
                year, indicator, value = content.split(":")
                comparison = "gte"
            return {
                "year": year.split(","),
                "indicator": indicator,
                "comparison": comparison,
                "value": value,
            }

        return content


class WdiReferenceSchema(TypedDict, total=False):
    cube: Required[str]
    measure: str
    level_mapper: Dict[str, str]


@dataclass
class WdiReference:
    cube: str
    measure: str = "Measure"
    level_mapper: Dict[str, str] = field(default_factory=dict)

    def build_request(self, params: WdiParameters):
        location = self.level_mapper.get(params.location, params.location)

        return DataRequest.new(
            self.cube,
            {
                "drilldowns": [location],
                "measures": [self.measure],
                "cuts_include": {
                    "Indicator": [params.indicator],
                    "Year": [str(item) for item in params.year],
                },
                "filters": {self.measure: ((params.comparison, params.value),)},
                "sorting": (self.measure, "desc"),
            },
        )

    def get_level(self, name: str):
        return self.level_mapper.get(name, name)


def parse_wdi(
    location: str,
    wdi: Annotated[
        List[str],
        Query(
            description="Applies an additional threshold over the data, using a parameter from the World Bank's WDI database."
        ),
    ] = [],
) -> List[WdiParameters]:
    """WDI dependency.

    Parses the parameters needed for the request done against the WDI cube.
    """

    def parse_singleton(param: str):
        obj = WdiParameters.model_validate(param)
        obj.location = location
        return obj

    return [parse_singleton(param) for token in wdi for param in token.split(",")]
