import logging
from pathlib import Path
from typing import Callable, List, Type

import threedi_api_client.openapi.models as models
import yaml

logger = logging.getLogger(__name__)


class Organisation:
    fields = "{{ organisation_uuid }}"


class ThreediModel:
    fields = {
        "schematisation_id": "{{ schematisation_id }}",
        "revision_id": "{{ revision_id }}",
        "auto_update": True,
    }


class Simulation:
    fields = {
        "threedimodel": ThreediModel,
        "organisation": Organisation,
        "name": "{{ simulation_name }}",
        "start_datetime": "{{ datetime_now }}",
        "duration": "{{ duration }}",
    }


def reference_uuid_environment_converter(config: dict, **kwargs: dict) -> dict:
    """Return environment corrected configuration"""
    assert (
        "reference_uuid" in config
    ), f"Reference UUID not found in configuration: {config}"

    if isinstance(config["reference_uuid"], str):
        # Reference UUID is already a string, no need to resolve
        return config

    assert isinstance(config["reference_uuid"], dict), (
        f"Attempting to resolve reference UUID from environment "
        f"but config is not a dict: {config}"
    )

    environment = kwargs.get("environment", "production")
    config["reference_uuid"] = config["reference_uuid"][environment]
    return config


scenario_mapping: dict[str, Type[Organisation | ThreediModel | Simulation]] = {
    "organisation": Organisation,
    "simulation": Simulation,
    "threedimodel": ThreediModel,
}


class YamlEvent:
    """Simulation step as defined in the yaml file"""

    def __init__(self, model: models, converters: List[Callable] = []):
        self.model = model
        self.converters = converters

    def convert_yaml_to_openapi(self, yaml_config: dict, **kwargs: str) -> dict:
        for converter in self.converters:
            yaml_config = converter(yaml_config, **kwargs)

        return self._convert(yaml_config)

    def _convert(self, yaml_config: dict) -> dict:
        # Create placeholders for all required values and fill values if they are present
        # in the attribute_map
        openapi_spec = {}
        for key in self.model.required_fields:
            if key in yaml_config:
                openapi_spec[key] = yaml_config[key]
            else:
                openapi_spec[key] = "{{ " + key + " }}"

        for key, value in yaml_config.items():
            if key in self.model.attribute_map:
                openapi_spec[key] = value

        return openapi_spec


event_mapping = {
    "breach": YamlEvent(models.Breach),
    "constantlateral": YamlEvent(models.ConstantLateral),
    "constantrain": YamlEvent(models.ConstantRain),
    "filelateral": YamlEvent(models.FileLateral),
    "leakagerasterlocal": YamlEvent(models.FileRasterLeakage),
    "localrainconstant": YamlEvent(models.ConstantLocalRain),
    "localraintimeseries": YamlEvent(models.TimeseriesLocalRain),
    "rainrasterlizard": YamlEvent(
        models.LizardRasterRain, [reference_uuid_environment_converter]
    ),
    "raintimeserieslizard": YamlEvent(
        models.LizardTimeseriesRain, [reference_uuid_environment_converter]
    ),
    # rasteredit
    "timeseriesboundary": YamlEvent(models.BoundaryCondition),
    # "timeseriesinflow": YamlEvent(models.TimeseriesInflow),
    "timeserieslateral": YamlEvent(models.TimeseriesLateral),
    "timeseriesleakage": YamlEvent(models.TimeseriesLeakage),
    "timeseriesrain": YamlEvent(models.TimeseriesRain),
    "timeseriessourcessinks": YamlEvent(models.TimeseriesSourcesSinks),
    # saved_state
    # initial saved state
    "timeserieswind": YamlEvent(models.TimeseriesWind),
    # "winddragcoefficients": YamlEvent(models.WindDragCoefficients),
}


class YamlConverter:
    """Converts a yaml for a 3Di simulation to a format that can be used by the API"""

    def __init__(self, environment: str = "production"):
        self.environment: str = environment

    def convert_yaml(self, yaml_file: Path) -> None:
        with open(yaml_file, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        meta = {}
        if "meta" in data:
            meta = data["meta"]

        scenario = {}
        scenario["steps"] = self._get_events(data["scenario"]["steps"])
        del data["scenario"]["steps"]

        for key, values in data["scenario"].items():
            if key in scenario_mapping:
                model = scenario_mapping[key]
                params = self._extract_scenario(model, values)
                scenario[key] = params
            else:
                logger.warning(f"Could not map unknown scenario: {key}")

        test_name = yaml_file.stem
        with open(yaml_file.parent / f"{test_name}_converted.yaml", "w") as f:
            yaml.dump({"meta": meta, "scenario": scenario}, f)

    def fill_yaml(
        self, yaml_file: Path, schematisation_id: int, revision_id: int
    ) -> None:
        with open(yaml_file, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        data["scenario"]["simulation"]["threedimodel"]["schematisation_id"] = (
            schematisation_id
        )
        data["scenario"]["simulation"]["threedimodel"]["revision_id"] = revision_id

        with open(yaml_file, "w") as f:
            yaml.dump(data, f)

    def _extract_scenario(
        self, model: Type[Organisation | ThreediModel | Simulation], values: dict
    ) -> dict | str:
        # Recursivlely extract fields from scenario models
        if isinstance(model.fields, str):
            return model.fields

        params = {}
        for key, v in model.fields.items():
            if key in scenario_mapping:
                params[key] = self._extract_scenario(scenario_mapping[key], {})
            elif key in values:
                params[key] = values[key]
            else:
                params[key] = v

        return params

    def _get_events(self, steps: List[dict]) -> List[dict]:
        events = []
        for step in steps:
            key = list(step.keys())[0]
            if key in event_mapping:
                event: YamlEvent = event_mapping[key]
                config = event.convert_yaml_to_openapi(
                    step[key], **{"environment": self.environment}
                )
                events += [{key: config}]

        events += [{"action": {"name": "start", "waitfor_timeout": 1800}}]
        events += [{"waitforstatus": {"name": "finished", "timeout": 1800}}]
        return events
