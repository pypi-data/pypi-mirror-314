from threedi_api_client.openapi.models import Breach
from .base import EventWrapper


class BreachWrapper(EventWrapper):
    model = Breach
    api_path: str = "breaches"
    scenario_name = "breach"


WRAPPERS = [BreachWrapper]
