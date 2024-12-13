from typing import Literal, Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel

from .base_economics import EconomicsValue


########## Start Model defenition #########
class AddedValueByEconomicActivityKeys:
    CLASSIFICATION_TYPE = "classification_type"
    AS_PERCENTAGE = "as_percentage_of_gdp"


class AddedValueByEconomicActivityLegends:
    CLASSIFICATION_TYPE = "Formal classification type of the added value."
    AS_PERCENTAGE = "Added value for catagery As percentage of GDP."


AVC = AddedValueByEconomicActivityLegends


class AddedValueByEconomicActivity(DataGardenSubModel):
    classification_type: Optional[Literal["ISICV3", "ISICV4", "NAICS2017", "NACE2"]] = Field(
        default=None, description=AVC.CLASSIFICATION_TYPE
    )
    as_percentage_of_gdp: dict[str, float] = Field(default_factory=dict, description=AVC.AS_PERCENTAGE)


########## Start Model defenition #########
class ValueAddedKeys:
    UNITS = "units"
    TOTAL = "total"
    BY_NACE_ACTIVITY = "by_nace_activity"
    BY_ECONOMIC_ACTIVITY = "by_economic_activity"


class ValueAddedLegends:
    TOTAL = "Total value added in given units."
    UNITS = "Currency and units."
    BY_NACE_ACTIVITY = (
        "By NACE economic activity. See also "
        "https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Statistical_classification_of_economic_activities_in_the_European_Community_(NACE)"
    )
    BY_ECONOMIC_ACTIVITY = "By activity value category based upon either NACE or ISIC or NAICS."


LV = ValueAddedLegends


class ValueAdded(DataGardenSubModel):
    total: EconomicsValue = Field(default_factory=EconomicsValue, description=LV.TOTAL)
    by_economic_activity: AddedValueByEconomicActivity = Field(
        default_factory=AddedValueByEconomicActivity,
        description=LV.BY_ECONOMIC_ACTIVITY,
    )


class GDPV1Legends:
    TOTAL_GDP = "Total annual GDP at current and/or constant value for the region."
    GDP_PER_INHABITANT = "GDP per inhabitant current and/or constant value."
    VALUE_ADDED = "Economic value added as percentage of GDP for the region."
    YOY_GROWTH = "Growth versus previous year in percent."
    YOY_GROWTH_PER_CAPITA = "Growth versus previous year in percent per capita."


L = GDPV1Legends


class GDP(DataGardenSubModel):
    total_gdp: EconomicsValue = Field(default_factory=EconomicsValue, description=L.TOTAL_GDP)
    gdp_per_inhabitant: EconomicsValue = Field(
        default_factory=EconomicsValue, description=L.GDP_PER_INHABITANT
    )
    value_added: ValueAdded = Field(default_factory=ValueAdded, description=L.VALUE_ADDED)
    yoy_growth: Optional[float] = Field(default=None, description=L.YOY_GROWTH)
    yoy_growth_per_capita: Optional[float] = Field(default=None, description=L.YOY_GROWTH_PER_CAPITA)


class GDPV1Keys(ValueAddedKeys, AddedValueByEconomicActivityKeys):
    TOTAL_GDP = "total_gdp"
    GDP_PER_INHABITANT = "gdp_per_inhabitant"
    VALUE_ADDED = "value_added"
    GDP_AT_CONSTANT_PRICES = "gdp_at_constant_prices"
    YOY_GROWTH = "yoy_growth"
    YOY_GROWTH_PER_CAPITA = "yoy_growth_per_capita"
