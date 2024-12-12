from pathlib import Path
from typing import Dict
from threedi_api_client.openapi.models import (
    ConstantRain,
    TimeseriesRain,
    LizardRasterRain,
    LizardTimeseriesRain,
    Upload,
    FileTimeseriesRain,
    FileRasterRain,
    NetCDFRasterRain,
    NetCDFTimeseriesRain,
    ConstantLocalRain,
    TimeseriesLocalRain,
)

from .base import EventWrapper
from .waitfor import WaitForProcessedFileWrapper


class ConstantRainWrapper(EventWrapper):
    model = ConstantRain
    api_path: str = "rain_constant"
    scenario_name = "constantrain"


class LocalConstantRainWrapper(EventWrapper):
    model = ConstantLocalRain
    api_path: str = "rain_local_constant"
    scenario_name = "localrainconstant"


class RainTimeseriesWrapper(EventWrapper):
    model = TimeseriesRain
    api_path: str = "rain_timeseries"
    scenario_name = "timeseriesrain"


class LocalRainTimeseriesWrapper(EventWrapper):
    model = TimeseriesLocalRain
    api_path: str = "rain_local_timeseries"
    scenario_name = "localraintimeseries"


class RainRasterLizardWrapper(EventWrapper):
    model = LizardRasterRain
    api_path: str = "rain_rasters_lizard"
    scenario_name = "rainrasterlizard"


class RainTimeseriesLizardWrapper(EventWrapper):
    model = LizardTimeseriesRain
    api_path: str = "rain_timeseries_lizard"
    scenario_name = "raintimeserieslizard"


class WaitForProcessedTimeseriesFileWrapper(WaitForProcessedFileWrapper):
    model = FileTimeseriesRain
    scenario_name = "waitforraintimeseriesfile"


class WaitForRainTimeseriesNetCDFWrapper(WaitForProcessedTimeseriesFileWrapper):
    model = NetCDFTimeseriesRain
    websocket_model_name = "NetCDFTimeseriesRain"
    scenario_name = "waitforraintimeseriesnetcdf"


class RainTimeseriesNetCDFWrapper(EventWrapper):
    model = Upload
    api_path: str = "rain_timeseries_netcdf"
    scenario_name = "raintimeseriesnetcdf"
    filepath: Path = None

    def initialize_instance(self, data: Dict):
        self.filepath = Path(data.pop("filepath"))
        super().initialize_instance(data)

    @property
    def extra_steps(self):
        data = {
            "file": {"state": "processed", "filename": self.instance.filename},
            "timeout": 30,
        }
        wait_for_validation = WaitForRainTimeseriesNetCDFWrapper(
            data=data, api_client=self._api_client, simulation=self.simulation
        )
        return [wait_for_validation]


class WaitForProcessedRasterFileWrapper(WaitForProcessedFileWrapper):
    model = FileRasterRain
    scenario_name = "waitforrainrasterfile"


class WaitForRainRasterNetCDFWrapper(WaitForProcessedRasterFileWrapper):
    model = NetCDFRasterRain
    websocket_model_name = "NetCDFRasterRain"
    scenario_name = "waitforrainrasternetcdf"


class RainRasterNetCDFWrapper(EventWrapper):
    model = Upload
    api_path: str = "rain_rasters_netcdf"
    scenario_name = "rainrasternetcdf"
    filepath = None

    def initialize_instance(self, data: Dict):
        self.filepath = Path(data.pop("filepath"))
        super().initialize_instance(data)

    @property
    def extra_steps(self):
        data = {
            "file": {"state": "processed", "filename": self.instance.filename},
            "timeout": 30,
        }
        wait_for_validation = WaitForRainRasterNetCDFWrapper(
            data=data, api_client=self._api_client, simulation=self.simulation
        )
        return [wait_for_validation]


WRAPPERS = [
    ConstantRainWrapper,
    RainTimeseriesWrapper,
    RainRasterLizardWrapper,
    RainTimeseriesLizardWrapper,
    RainTimeseriesNetCDFWrapper,
    WaitForRainTimeseriesNetCDFWrapper,
    RainRasterNetCDFWrapper,
    WaitForRainTimeseriesNetCDFWrapper,
    LocalConstantRainWrapper,
    LocalRainTimeseriesWrapper,
]
