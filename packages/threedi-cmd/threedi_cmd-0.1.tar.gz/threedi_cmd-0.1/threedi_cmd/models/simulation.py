from .base import ModelWrapper
from threedi_api_client.openapi.models import Simulation


class SimulationWrapper(ModelWrapper):
    model = Simulation
    api_path = "simulations"
    scenario_name = "simulation"
