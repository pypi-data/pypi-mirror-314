from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel


class EconomicMetaDataKeys:
    UNIT = "unit"
    CURRENCY = "currency"
    REFERENCE_YEAR = "reference_year"


class EconomicMetaDataLegends:
    UNIT = "units of measure."
    CURRENCY = "currency of measure."
    REFERENCE_YEAR = "reference year for the data."


K = EconomicMetaDataLegends


class EconomicsMetaData(DataGardenSubModel):
    unit: int = Field(default=1, description=K.UNIT)
    currency: str = Field(default="EUR", description=K.CURRENCY)
    reference_year: Optional[str] = Field(default=None, description=K.REFERENCE_YEAR)

    class Meta:
        exclude_fields_in_has_values_check = ["unit", "reference_year", "currency"]


class EconomicBaseKeys:
    VALUE_CURRENT = "value_current"  # value at current prices
    VALUE_CONSTANT = "value_constant"  # value at constant prices


class EconomicBaseLegends:
    VALUE_CURRENT = "value at current prices, ie exact price at the time of the data collection."
    VALUE_CONSTANT = "value at constant prices, ie value adjusted for inflation related to a reference year."


L = EconomicBaseLegends


class EconomicsValue(DataGardenSubModel):
    value_current: Optional[float] = Field(default=None, description=L.VALUE_CURRENT)
    value_constant: Optional[float] = Field(default=None, description=L.VALUE_CONSTANT)
