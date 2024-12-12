from .base import SettingsWrapper
from threedi_api_client.openapi.models import (
    PhysicalSettings,
    NumericalSettings,
    TimeStepSettings,
    AggregationSettings,
)


class PhysicalSettingsWrapper(SettingsWrapper):
    model = PhysicalSettings
    api_path: str = "physical"
    scenario_name = "physicalsettings"


class NumercialSettingsWrapper(SettingsWrapper):
    model = NumericalSettings
    api_path: str = "numerical"
    scenario_name = "numericalsettings"


class TimeStepSettingsWrapper(SettingsWrapper):
    model = TimeStepSettings
    api_path: str = "time_step"
    scenario_name = "timestepsettings"


class AggregationSettingsWrapper(SettingsWrapper):
    model = AggregationSettings
    api_path: str = "aggregation"
    scenario_name = "aggregationsettings"


WRAPPERS = [
    PhysicalSettingsWrapper,
    NumercialSettingsWrapper,
    TimeStepSettingsWrapper,
    AggregationSettingsWrapper,
]
