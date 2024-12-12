from .base import SimulationChildWrapper
from threedi_api_client.openapi.models import TimedSavedStateUpdate, InitialSavedState
from .base import InitialWrapper


class TimedSavedStateWrapper(SimulationChildWrapper):
    model = TimedSavedStateUpdate
    api_path: str = "create_saved_states_timed"
    scenario_name = "timedsavedstate"


class InitialSavedStateWrapper(InitialWrapper):
    model = InitialSavedState
    api_path: str = "saved_state"
    scenario_name = "initialsavedstate"


WRAPPERS = [TimedSavedStateWrapper, InitialSavedStateWrapper]
