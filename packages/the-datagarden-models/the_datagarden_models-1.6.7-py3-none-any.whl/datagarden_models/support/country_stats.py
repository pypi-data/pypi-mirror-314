from collections import defaultdict
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

    @property
    def regional_data_models(self) -> list[str]:
        result = set()
        for region_type in self.region_types:
            region_data = getattr(self, region_type)
            result.update(region_data.regional_data_models)
        return list(result)

    def statistics_for_data_model(self, model_name: str) -> Dict[str, RegionalDataStats]:
        """Get regional statistics for a specific data model.

        Regional statistics include data avaialability statistics for a single data model for all regions.

            Returns:
                Dict[region_type: str, RegionalDataStats]
        """
        if model_name not in self.regional_data_models:
            raise ValueError(f"Data model '{model_name}' not found in regional data models")
        result: dict[str, RegionalDataStats] = defaultdict(RegionalDataStats)
        for region_type in self.region_types:
            region_data = getattr(self, region_type)
            if model_data := region_data.regional_data_stats.get(model_name, None):
                result[region_type] = model_data
        return result

    def region_type_name_for(self, level: int | str) -> str:
        """Get the name of the region type for a given level."""
        region = self.root.get(str(level), None)
        if region:
            return region.region_type
        raise ValueError(f"Region level '{level}' not found in country stats")

    def region_level_for(self, type_name: str) -> str:
        for level, region in self.root.items():
            if region.region_type == type_name:
                return level
        raise ValueError(f"Region type '{type_name}' not found in country stats")
