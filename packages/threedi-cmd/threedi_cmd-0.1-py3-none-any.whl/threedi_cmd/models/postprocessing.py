from .base import LizardPostprocessingWrapper
from threedi_api_client.openapi.models import (
    BasicPostProcessing,
    DamagePostProcessing,
    ArrivalTimePostProcessing
)


class LizardBasicPostprocessingWrapper(LizardPostprocessingWrapper):
    model = BasicPostProcessing
    api_path: str = "basic"
    scenario_name = "lizardbasicpostprocessing"


class LizardDamagePostprocessingWrapper(LizardPostprocessingWrapper):
    model = DamagePostProcessing
    api_path: str = "damage"
    scenario_name = "lizarddamagepostprocessing"


class LizardArrivalPostprocessingWrapper(LizardPostprocessingWrapper):
    model = ArrivalTimePostProcessing
    api_path: str = "arrival"
    scenario_name = "lizardarrivalpostprocessing"


WRAPPERS = [
    LizardBasicPostprocessingWrapper,
    LizardDamagePostprocessingWrapper,
    LizardArrivalPostprocessingWrapper
]
