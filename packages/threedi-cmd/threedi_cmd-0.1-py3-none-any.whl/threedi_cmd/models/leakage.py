from pathlib import Path
from .base import EventWrapper
from typing import Dict
from threedi_api_client.openapi.models import (
    ConstantLeakage,
    TimeseriesLeakage,
    FileTimeseriesLeakage,
    FileRasterLeakage,
    NetCDFRasterLeakage,
    NetCDFTimeseriesLeakage,
    Upload,
)

from .waitfor import WaitForProcessedFileWrapper


class ConstantLeakageWrapper(EventWrapper):
    model = ConstantLeakage
    api_path: str = "leakage_constant"
    scenario_name = "constantleakage"


class LeakageTimeseriesWrapper(EventWrapper):
    model = TimeseriesLeakage
    api_path: str = "leakage_timeseries"
    scenario_name = "timeseriesleakage"


class WaitForLeakageTimeseriesFileWrapper(WaitForProcessedFileWrapper):
    model = FileTimeseriesLeakage
    scenario_name = "waitforleakagetimeseriesfile"


class WaitForLeakageTimeseriesNetCDFWrapper(WaitForLeakageTimeseriesFileWrapper):
    model = NetCDFTimeseriesLeakage
    websocket_model_name = "NetCDFTimeseriesLeakage"
    scenario_name = "waitforleakagetimeseriesnetcdf"


class LeakageTimeseriesNetCDFWrapper(EventWrapper):
    model = Upload
    api_path: str = "leakage_timeseries_netcdf"
    scenario_name = "leakagetimeseriesnetcdf"
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
        wait_for_validation = WaitForLeakageTimeseriesNetCDFWrapper(
            data=data, api_client=self._api_client, simulation=self.simulation
        )
        return [wait_for_validation]


class WaitForLeakageRasterFileWrapper(WaitForProcessedFileWrapper):
    model = FileRasterLeakage
    scenario_name = "waitforleakagerasterfile"


class WaitForLeakageRasterNetCDFWrapper(WaitForLeakageRasterFileWrapper):
    model = NetCDFRasterLeakage
    websocket_model_name = "NetCDFRasterLeakage"
    scenario_name = "waitforleakagerasternetcdf"


class LeakageRasterNetCDFWrapper(EventWrapper):
    model = Upload
    api_path: str = "leakage_rasters_netcdf"
    scenario_name = "leakagerasternetcdf"
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
        wait_for_validation = WaitForLeakageRasterNetCDFWrapper(
            data=data, api_client=self._api_client, simulation=self.simulation
        )
        return [wait_for_validation]


WRAPPERS = [
    ConstantLeakageWrapper,
    LeakageTimeseriesWrapper,
    LeakageTimeseriesNetCDFWrapper,
    WaitForLeakageTimeseriesNetCDFWrapper,
    LeakageRasterNetCDFWrapper,
    WaitForLeakageTimeseriesNetCDFWrapper,
]
