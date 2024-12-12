from .actions import ActionWrapper
from .simulation import SimulationWrapper
from . import waitfor
from . import savedstate
from . import rain
from . import lateral
from . import sources_sinks
from . import wind
from . import breach
from . import rasteredit
from . import initial_waterlevels
from . import structure_control
from . import boundary_conditions
from . import leakage
from . import settings
from . import revision
from . import postprocessing

# Define a list of WRAPPERS
# A wrapper is an object that 'wraps' a certain
# resource of the openapi by automatically mapping
# all of it's openapi client methods.

# For every step in a scenario a wrapper is generated

WRAPPERS = (
    [
        ActionWrapper,
        SimulationWrapper,
    ]
    + rain.WRAPPERS
    + savedstate.WRAPPERS
    + waitfor.WRAPPERS
    + lateral.WRAPPERS
    + sources_sinks.WRAPPERS
    + wind.WRAPPERS
    + breach.WRAPPERS
    + rasteredit.WRAPPERS
    + initial_waterlevels.WRAPPERS
    + structure_control.WRAPPERS
    + boundary_conditions.WRAPPERS
    + leakage.WRAPPERS
    + settings.WRAPPERS
    + revision.WRAPPERS
    + postprocessing.WRAPPERS
)
