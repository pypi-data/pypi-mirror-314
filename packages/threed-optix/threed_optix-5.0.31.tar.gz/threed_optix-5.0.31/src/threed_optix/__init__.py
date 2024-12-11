from .client import ThreedOptixAPI, Client, Material
from .analyses import Analysis
from .simulations import Setup
from .parts import Part, Surface, LightSource, Detector, GLOBAL
from .utils import *
from . import package_utils
from . import optimize

# Allow users to easily access the enums
from .package_utils.vars import eOpticsSubtypes, Setups, Coating, SETUP_LABELS

__version__ = package_utils.vars.VERSION
GRATING_SUBTYPES = eOpticsSubtypes.GRATING_SUBTYPES
SETUP_LABELS = Setups.SETUP_LABELS

# Enter debug mode, which will print out pretty much every step of the way.
def debug(boolean = None):

    # If the user has specified a boolean, set the debug mode to that value.
    if boolean is not None:
        package_utils.vars.DEBUG = boolean

    # Otherwise, toggle the debug mode.
    else:
        package_utils.vars.DEBUG = not package_utils.vars.DEBUG
