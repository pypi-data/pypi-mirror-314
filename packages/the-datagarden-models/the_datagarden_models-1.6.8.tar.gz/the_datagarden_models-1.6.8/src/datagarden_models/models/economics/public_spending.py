from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel

from .base_economics import EconomicsValue


class PublicSpendingByCofogCategoryKeys:
    VALUE = "value"
    SHARE_OF_GDP = "share_of_gdp"


class PublicSpendingByCofogCategoryLegends:
    VALUE_BY_COFOG_CATEGORY = "Public spending by cofog category. In current and/or constant value."
    SHARE_OF_GDP_BY_COFOG_CATEGORY = "Share of GDP by cofog category."


PSBCC = PublicSpendingByCofogCategoryLegends


class PublicSpendingByCofogCategory(DataGardenSubModel):
    value: dict[str, EconomicsValue] = Field(default_factory=dict, description=PSBCC.VALUE_BY_COFOG_CATEGORY)
    share_of_gdp: dict[str, float] = Field(
        default_factory=dict, description=PSBCC.SHARE_OF_GDP_BY_COFOG_CATEGORY
    )


class PublicSpendingLegends:
    BY_COFOG_CATEGORY = "Public spending by cofog category."
    TOTAL = "Total public spending. Incurrent and/or constant value."


PS = PublicSpendingLegends


class PublicSpendingV1(DataGardenSubModel):
    by_cofog_category: PublicSpendingByCofogCategory = Field(
        default_factory=PublicSpendingByCofogCategory,
        description=PS.BY_COFOG_CATEGORY,
    )
    total: EconomicsValue = Field(default_factory=EconomicsValue, description=PS.TOTAL)


class PublicSpendingV1Keys(PublicSpendingByCofogCategoryKeys):
    BY_COFOG_CATEGORY = "by_cofog_category"
    TOTAL = "total"
