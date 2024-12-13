from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel

from .base_demographics import AgeGender


class MortalityV1Legends:
    DEATHS_BY_AGE = "Death count per year. " "In number of individuals per age or age group."
    MORTALITY_BY_AGE = "Mortality before age or within age group per 1000 of live births."
    TOTAL_DEATHS = "Total number of deaths in a year. " "In number of individuals."
    INFANT_DEATHS = "Number of infant deaths under age 1. " "In number of individuals."
    INFANT_DEATH_RATE = "Infant death rate per 1000 live births."
    TOTAL_MALE_DEATHS = "Total number of male deaths in a year. " "In number of individuals."
    TOTAL_FEMALE_DEATHS = "Total number of female deaths in a year. " "In number of individuals."
    DEATH_RATE = "Death rate per 1000 persons. "


L = MortalityV1Legends


class Mortality(DataGardenSubModel):
    deaths_by_age: AgeGender = Field(default_factory=AgeGender, description=L.DEATHS_BY_AGE)
    mortality_by_age: AgeGender = Field(default_factory=AgeGender, description=L.MORTALITY_BY_AGE)
    total_deaths: Optional[float] = Field(default=None, description=L.TOTAL_DEATHS)
    total_male_deaths: Optional[float] = Field(default=None, description=L.TOTAL_MALE_DEATHS)
    total_female_deaths: Optional[float] = Field(default=None, description=L.TOTAL_FEMALE_DEATHS)
    death_rate: Optional[float] = Field(default=None, description=L.DEATH_RATE)
    infant_deaths: Optional[float] = Field(default=None, description=L.INFANT_DEATHS)
    infant_death_rate: Optional[float] = Field(default=None, description=L.INFANT_DEATH_RATE)


class MortalityV1Keys:
    DEATHS_BY_AGE = "deaths_by_age"
    MORTALITY_BY_AGE = "mortality_by_age"
    TOTAL_DEATHS = "total_deaths"
    INFANT_DEATHS = "infant_deaths"
    INFANT_DEATH_RATE = "infant_death_rate"
    TOTAL_MALE_DEATHS = "total_male_deaths"
    TOTAL_FEMALE_DEATHS = "total_female_deaths"
    DEATH_RATE = "death_rate"
