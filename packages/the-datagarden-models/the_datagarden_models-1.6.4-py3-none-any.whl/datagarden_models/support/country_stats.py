from typing import Dict, List

from pydantic import BaseModel, RootModel


class RegionalDataStats(BaseModel):
    count: int
    sources: Dict[str, str]
    to_period: str
    from_period: str
    period_type: List[str]

    @property
    def source_names(self) -> List[str]:
        return list(self.sources.keys())


class RegionData(BaseModel):
    count: int
    region_type: str
    access_level: str
    region_level: int
    with_geojson: int
    regional_data_stats: Dict[str, RegionalDataStats]

    def model_post_init(self, __context) -> None:
        """Convert all keys to lowercase for internal consistency"""
        self.regional_data_stats = {k.lower(): v for k, v in self.regional_data_stats.items()}

    @property
    def regional_data_models(self) -> List[str]:
        return list(self.regional_data_stats.keys())

    def __getattr__(self, attr: str) -> RegionalDataStats:
        if attr in self.regional_data_models:
            return self.regional_data_stats[attr]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")


class CountryStats(RootModel[Dict[str, RegionData]]):
    @property
    def region_types(self) -> List[str]:
        return [region_data.region_type for region_data in self.root.values()]

    def __getattr__(self, attr: str) -> RegionData:
        if attr in self.region_types:
            for region_data in self.root.values():
                if region_data.region_type == attr:
                    return region_data
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")
