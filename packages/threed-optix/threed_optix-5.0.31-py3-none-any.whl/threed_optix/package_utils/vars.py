import numpy as np
import re

DEBUG = False
BASE_BACKUP = 'DEFAULT'
VALID_RESPONSE_CODES = [200, 201, 202, 204]
# Take the version of the package
VERSION = "5.0.31"


#Base API URL
API_URL = "https://api.3doptix.com/v1"

is_new_session = 'True' #0 for origin that is a human user
class Surfaces:
    DETECTOR_FRONT = 'front'
    DETECTOR_BACK = 'back'
    LENS_FRONT = 'front'
    LENS_BACK = 'back'
    ASPHERE_DEFORMATION = 'ASPHERE'

class Analyses:
    DEFAULT_NUM_RAYS = 30
    BATCH_ANALYSIS_RAY_LIMIT = 10e6
    BATCH_ANALYSIS_RESOLUTION_LIMIT = 1000
    BATCH_ANALYSIS_PARAMETERS_KEYS = ["polarization", "has_total", "has_coherence_groups"]
    POLARIZTION_FILTERS = ["X","Y","Z","NONE"]

class Endpoints:
    GET_MATERIALS_ENDPOINT = 'material/name/{material_name}'
    GET_SURFACE_DATA = 'setups/{setup_id}/parts/{part_id}/surfaces/{surface_id}'
    DELETE_ANALYSIS = 'setups/{setup_id}/parts/{part_id}/surfaces/{surface_id}/analyses/{analysis_id}'
    GET_OPTICS_DATA = 'optics/{number_id}'
    CHANGE_CS = 'setups/{setup_id}/parts/{part_id}/cs_data'
    SCATTERING = 'setups/{setup_id}/parts/{part_id}/surfaces/{surface_id}/scattering'

class AddParts:
    VALID_PART_ARGUMENTS = ['pose', 'label']
    VALID_OPTICS_ARGUMENTS = VALID_PART_ARGUMENTS
    VALID_DETECTOR_ARGUMENTS = ['size', 'opacity'] + VALID_PART_ARGUMENTS
    VALID_LIGHT_SOURCE_ARGUMENTS = ['wavelengths', 'add_wavelengths', 'power', 'vis_count', 'vis_count_type', 'rays_direction', 'opacity', 'color', 'gaussian_beam', 'point_source', 'plane_wave'] + VALID_PART_ARGUMENTS


#GET endpoints
GET_SETUPS_ENDPOINT = 'setups'
GET_SETUP_ENDPOINT = 'setups/{setup_id}'
GET_PART_ENDPOINT = 'setups/{setup_id}/parts/{part_id}'
MAX_HISTORY_LEN = 5

# DELETE endpoints
DELETE_PART_ENDPOINT = 'setups/{setup_id}/parts/{part_id}'

#PUT endpoints
# PUT_BATCH_CHANGES_ENDPOINT = "setups/{setup_id}/batch_changes"
PUT_SIMULATION_ENDPOINT = 'setups/{setup_id}/simulation'
PUT_PART_ENDPOINT = 'setups/{setup_id}/parts/{part_id}'

#POST endpoints
POST_ADD_ANALYSIS_ENDPOINT = "setups/{setup_id}/parts/{part_id}/surfaces/{surface_id}/analyses"
POST_CREATE_OPTICS_ENDPOINT = "optics"
POST_CREATE_SETUP_ENDPOINT = 'setups'
POST_ADD_PART_ENDPOINT = 'setups/{setup_id}/parts'

#Snellius version: must be compatible
SNELLIUS_VERSION = "2.2.23"
GPU_TYPE = "g4"

#Messages and warnings
SET_API_URL_WARNING = "Are you sure you want to change the API URL? This is internal option and should not be used by users."
SERVER_DOWN_MESSAGE = "The server is down. Please try again later."
WELCOME_MESSAGE = f"Welcome to 3DOptix! 🌈 You are now being connected to the 3DOptix API. Let's start!"
GETTING_PARTS_MESSAGE = f"We are retrieving the setup information. This needs to be done only once. Please wait."

# Setups
SETUP_LABELS = ["General",
                "Microscopy",
                "Telescopy" ,
                "Spectroscopy" ,
                "Imaging" ,
                "Non-linear optics" ,
                "Fiber" ,
                "Illumination" ,
                "Light sources" ,
                "Laser Optics" ,
                "Diffractive Optics"
]

INCH = 'in'
MM = 'mm'
SETUP_UNITS = [MM, INCH]
CREATE_SETUP_UNITS_MAP = {
    INCH: 0,
    MM: 1,
}

class PartType:
    DETECTOR = 9
    LIGHT_SOURCE = 8
    OPTICS = 2
    COORDINATE_SYSTEM = 7
    GENERAL = 0,
    PARAXIAL_LENS = 1,
    CAD = 3,
    GROUP = 5,
    BLACKBOX = 6,
    PART_TYPES = [OPTICS, LIGHT_SOURCE, DETECTOR, COORDINATE_SYSTEM]

## Analysis process variables, exported to mitigate duplications
class AnalysisProcessVariables:
    VERSION_BYTES = [16, 20]

    SPOT_TARGET_KINDS = {
            0: 'Source',
            1: 'Group',
            2: 'Total',
            3: 'None',
        }
    WLS_DTYPE = np.float32
    DATA_DTYPE = np.float32


# Analysis for V2 snellius file
class AnalysisFile2:
    VERSION_BYTES = AnalysisProcessVariables.VERSION_BYTES
    HEADER_DTYPES = [
       ('magic number', np.int32), #0:4
        ('analysis kind', np.int32), #4:8
        ('data kind', np.int32), #8:12
        ('polarization kind', np.int32), #12:16
        ('version', np.int32), #16:20
        ('num_hits', np.int64), #20:28
        ('num_wavelengths', np.int32), #28:32
        ('resolution_x', np.int32), #32:36
        ('resolution_y', np.int32), #36:40
        ('spot_target_kind', np.int32), #40:44
        ('spot_target_index', np.int32), #44:48
        ('detector_width', np.float32), #48:52
        ('detector_height', np.float32), #52:56
    ]
    HEADER_BYTES = 56
    SPOT_TARGET_KINDS = AnalysisProcessVariables.SPOT_TARGET_KINDS

    WLS_DTYPE = AnalysisProcessVariables.WLS_DTYPE
    DATA_DTYPE = AnalysisProcessVariables.DATA_DTYPE

# Analysis for V3 snellius file
class AnalysisFile3:
    VERSION_BYTES = AnalysisProcessVariables.VERSION_BYTES
    HEADER_DTYPES = [
        ('magic number', np.int32), #0:4
        ('analysis kind', np.int32), #4:8
        ('data kind', np.int32), #8:12
        ('polarization kind', np.int32), #12:16
        ('version', np.int32), #16:20
        ('num_hits', np.int64), #20:28
        ('num_wavelengths', np.int32), #28:32
        ('resolution_x', np.int32), #32:36
        ('resolution_y', np.int32), #36:40
        ('spot_target_kind', np.int32), #40:44
        ('spot_target_index', np.int32), #44:48
        ('detector_width', np.float32), #48:52
        ('detector_height', np.float32), #52:56
        ('number_of_surfaces', np.int32),#56:60
    ]
    HEADER_BYTES = 60
    SPOT_TARGET_KINDS = AnalysisProcessVariables.SPOT_TARGET_KINDS

    WLS_DTYPE = AnalysisProcessVariables.WLS_DTYPE
    DATA_DTYPE = AnalysisProcessVariables.DATA_DTYPE



## Analysis file decoding format
ANALYSIS_HEADER_DTYPES = np.dtype([
        ('magic number', np.int32), #0:4
        ('analysis kind', np.int32), #4:8
        ('data kind', np.int32), #8:12
        ('polarization kind', np.int32), #12:16
        ('version', np.int32), #16:20
        ('num_hits', np.int64), #20:28
        ('num_wavelengths', np.int32), #28:32
        ('resolution_x', np.int32), #32:36
        ('resolution_y', np.int32), #36:40
    ])
# ANALYSIS_MATRIX_DTYPES = np.dtype(np.float32).newbyteorder('<')
ANALYSIS_MATRIX_DTYPES = np.float32
HEADER_BYTES = 40
DATA_KINDS_MAPPING = {
    -1: 'INVALID_SPOT_DATA_KIND',
    0: 'SPOT_INCOHERENT_IRRADIANCE_S',
    1: 'SPOT_INCOHERENT_IRRADIANCE_P',
    2: 'SPOT_COHERENT_IRRADIANCE_S',
    3: 'SPOT_COHERENT_IRRADIANCE_P',
    4: 'SPOT_COHERENT_PHASE_S',
    5: 'SPOT_COHERENT_PHASE_P',
    6: 'SPOT_INCOHERENT_IRRADIANCE',
    7: 'SPOT_COHERENT_IRRADIANCE',
    8: 'SPOT_COHERENT_PHASE',
    9: 'SPOT_FIELD',
    10: 'SPOT_MTF',
    11: 'SPOT_WAVEFRONT'
}

ANALYSIS_KIND = {
    0 : 'RAY_TABLE',
    1 : 'SPOT',
    2 : 'RAY_SEARCH',
    3 : 'TIME_DOMAIN',
    4 : 'MULTI_CHANNEL_IMAGE'
}

SUPPORTED_DATA_KINDS_NAMES = [
    'SPOT_INCOHERENT_IRRADIANCE_S',
    'SPOT_INCOHERENT_IRRADIANCE_P',
    'SPOT_COHERENT_IRRADIANCE_S',
    'SPOT_COHERENT_IRRADIANCE_P',
    'SPOT_COHERENT_PHASE_S',
    'SPOT_COHERENT_PHASE_P',
    'SPOT_INCOHERENT_IRRADIANCE',
    'SPOT_COHERENT_IRRADIANCE',
    'SPOT_COHERENT_PHASE',
]

POLARIZATION_MAPPING = {
    0: 'NONE_POLARIZATION',
    1: 'X_POLARIZATION',
    2: 'Y_POLARIZATION',
    3: 'Z_POLARIZATION',
    4: 'RAW_POLARIZATION',
}

## Valid names
FAST_ANALYSIS_NAMES = [
    "Spot (Incoherent Irradiance)",
    "Spot (Incoherent Irradiance) Through Focus",
    "Grid Distortion",
    "Distortion & Field Curvature",
    "OPD (Optical Path Difference)",
    "Ray Abberations (TRA and LRA)",
    "Polarization Map"
]

DEPRICATED_ANALYSIS_NAMES =  [

    "Spot (Coherent Irradiance) Polarized",
    "Coherent Phase Polarized",
    "Spot (Incoherent Irradiance) Polarized"
]
VALID_ANALYSIS_NAMES =  [
    "Spot (Incoherent Irradiance)",
    "Spot (Coherent Irradiance)",
    "Coherent Phase",
    "Spot (Coherent Irradiance) Huygens",
    "Coherent Phase Huygens",
    "Spot (Coherent Irradiance) Fresnel",
    "Coherent Phase Fresnel",
    "Spot (Coherent Irradiance) Polarized",
    "Coherent Phase Polarized",
    "Spot (Incoherent Irradiance) Polarized",
    "Spectral Collection Analysis"
]
VALID_RESPONSE_CODESANALYSIS_NAMES =  [
    "Spot (Incoherent Irradiance)",
    "Spot (Coherent Irradiance)",
    "Coherent Phase",
    "Spot (Coherent Irradiance) Huygens",
    "Coherent Phase Huygens",
    "Spot (Coherent Irradiance) Fresnel",
    "Coherent Phase Fresnel"
]

## results color scale (as in GUI)
COLOR_SCALE = [
    [0.0, '#0000FF'],
    [0.25, '#00FF00'],
    [0.5, 'yellow'],
    [0.75, 'orange'],
    [1.0, '#FF0000']
]

# Errors
## simulation errors
SIMULATION_ERROR = """Simulation failed (server side).\n Error message: "{message}"."""

## Analyses errors
ANALYSES_ADD_ERROR = "Analyses {not_added} were not added. Please add them first"
ANALYSES_NOT_SAME_SETUP_ERROR = f"Analyses must be from the same setup."
ANALYSIS_RUN_ERROR = """Analyses failed (server side).\n Error message: "{message}"."""
ANALYSES_DUPLICATED_ERROR = """Analyses with ids {duplicated} are duplicated.\nYou can use the existing analyses with the same parameters or force this action by setting 'force' argument to True"""
ANALYSES_RUN_ERROR = """Analysis failed (server side).\n Error message: "{message}"."""

#Arguments
def argument_repair_message(errors):
    return "Invalid arguments. Errors:\n" + "\n".join(errors)

# Analysis
ANALYSIS_RES_RANGE = [0, 10000]
ANALYSIS_RAYS_RANGE = [1, 1e9]

# Quick Focus
class eQuickFocus():
    QUICK_FOCUS_RADIUS = 5
    MAX_DISTANCE_TRACING = 300
    NUM_SEGMENTS = 15
    X_VAL_IDX = 0
    Y_VAL_IDX = 1
    RAY_DATA_IDX = 1

# Detector Data
## size
DETECTOR_SIZE_RANGE = [0.0001, 200]
DETECTOR_OPACITY_RANGE = [0, 1]
#Light source data
##Beam kinds
GAUSSIAN_BEAM = "GAUSSIAN_BEAM"
POINT_SOURCE = "POINT_SOURCE"
PLANE_WAVE = "PLANE_WAVE"
BEAM_KINDS = [POINT_SOURCE, GAUSSIAN_BEAM, PLANE_WAVE]

## Density patterns
XY_GRID = "XY_GRID"
CONCENTRIC_CIRCLES = "CONCENTRIC_CIRCLES"
RANDOM = "RANDOM"
DENSITY_PATTERNS = [XY_GRID, CONCENTRIC_CIRCLES, RANDOM]

## Count type
TOTAL = "TOTAL"
PER_WAVELENGTH = "PER_WAVELENGTH"
LOWER_VIS_COUNT_LIMIT = 1
UPPER_VIS_COUNT_LIMIT = 200
COUNT_TYPES = [TOTAL, PER_WAVELENGTH]

## Plane wave
RECTANGULAR = "RECTANGULAR"
CIRCULAR = "CIRCULAR"
ELLIPTICAL = "ELLIPTICAL"
PLANE_WAVE_TYPES = [RECTANGULAR, CIRCULAR, ELLIPTICAL]

## Appearance
HEX_COLOR_RE = r'#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})'
LIGHT_SOURCE_OPACITY_RANGE = [0, 1]
MODEL_RADIUS_RANGE = [1, 10]
## Angular Information
AZIMUTH_Z_RANGE = [-90, 90]
THETA_RANGE = [-180, 180]
PHI_RANGE = [0,180]

## Power
POWER_RANGE = [0, 1e6]

## Point Source
HALF_CONE_ANGLE = "HALF_CONE_ANGLE"
HALF_WIDTH_RECT = "HALF_WIDTH_RECT"
HALF_WIDTH_AT_Z = "HALF_WIDTH_AT_Z"
POINT_SOURCE_TYPES = [HALF_CONE_ANGLE, HALF_WIDTH_RECT, HALF_WIDTH_AT_Z]
PLANE_WAVE_WIDTH_RANGE = [0.0001, 1e5]
PLANE_WAVE_HEIGHT_RANGE = [0.0001, 1e5]
PLANE_WAVE_RADIUS_RANGE = [0.0001, 1e2]
POINT_SOURCE_ANGLE_RANGE = [0.001, 180]
POINT_SOURCE_DIST_Z_RANGE = [0.0001, 9007199254740991]
POINT_SOURCE_DIST_Z_AT_RANGE = [0.0001, 9007199254740991]


## Wavelegnth
WAVELENGTH_RANGE = [140, 20000]
WEIGHTS_RANGE = [1e-5, 1]

# Create Optics
METALLIC_MIRROR = "Metallic Mirror"
DIELECTRIC_MIRROR = "Dielectric Mirror"
DICHROIC_MIRROR = "Dichroic Mirror"
CURVED_MIRROR_CONCAVE = "Curved Mirror (Concave)"
CURVED_MIRROR_CONVEX = "Curved Mirror (Convex)"
CYLINDRICAL_MIRROR_PLANO_CONVEX = "Cylindrical Mirror (Plano-Convex)"
CYLINDRICAL_MIRROR_PLANO_CONCAVE = "Cylindrical Mirror (Plano-Concave)"
PARABOLIC_MIRROR_CONCAVE = "Parabolic Mirror (Concave)"
OFF_AXIS_PARABOLIC_MIRROR = "Off-Axis Parabolic Mirror"
D_SHAPED_MIRROR = "D-Shaped Mirror"
KNIFE_EDGE_PRISM_MIRROR = "Knife-Edge Prism Mirror"
RIGHT_ANGLE_PRISM_MIRROR = "Right-Angle Prism Mirror"
ROOF_PRISM_MIRROR = "Roof Prism Mirror"
ELLIPSOIDAL = "Ellipsoidal"
KNIFE_EDGE_PRISM = "Knife-Edge Prism"
RIGHT_ANGLE_PRISM = "Right-Angle Prism"
EQUIANGULAR_PRISM = "Equilateral Prism"
DOVE_PRISM = "Dove Prism"
WEDGE_PRISM = "Wedge Prism"
PELLIN_BROCA_PRISM = "Pellin Broca Prism"
PENTA_PRISM = "Penta Prism"
AXICON_PRISM = "Axicon Prism"
RHOMBIC_PRISM = "Rhombic Prism"
MULTIPLETS = "Multiplets"
SPHERICAL_LENS_PLANO_CONVEX = "Spherical Lens (Plano-Convex)"
SPHERICAL_LENS_PLANO_CONCAVE = "Spherical Lens (Plano-Concave)"
SPHERICAL_LENS_CONVEX_CONVEX = "Spherical Lens (Convex-Convex)"
SPHERICAL_LENS_CONCAVE_CONCAVE = "Spherical Lens (Concave-Concave)"
SPHERICAL_LENS_CONCAVE_CONVEX = "Spherical Lens (Concave-Convex)"
SPHERICAL_LENS_CONVEX_CONCAVE = "Spherical Lens (Convex-Concave)"
CYLINDRICAL_LENS_PLANO_CONVEX = "Cylindrical Lens (Plano-Convex)"
CYLINDRICAL_LENS_PLANO_CONCAVE = "Cylindrical Lens (Plano-Concave)"
BALL_LENS = "Ball Lens"
HALF_BALL_LENS = "Half Ball Lens"
OFF_AXIS_PARABOLIC_LENS = "Off-Axis Parabolic Lens"
ASPHERIC_LENS = "Aspheric Lens"
ODD_ASPHERE = "Odd Asphere"
PARAXIAL_LENS = "Paraxial lens"
GENERAL_CONIC = "General Conic"
GENERAL_BICONIC = "General Biconic"
LONGPASS_FILTER = "Longpass Filter"
SHORTPASS_FILTER = "Shortpass Filter"
BANDPASS_FILTER = "Bandpass Filter"
DICHROIC_FILTER = "Dichroic Filter"
NOTCH_FILTER = "Notch Filter"
CALIBRATION_FILTER = "Calibration Filter"
SPECTRAL_SHAPE_FILTER = "Spectral Shape Filter"
LASER_LINE_FILTER = "Laser-line Filter"
COLOR_GLASS = "Color Glass"
NEUTRAL_DENSITY_FILTER = "Neutral Density Filter"
HOT_COLD_MIRROR = "Hot/Cold Mirror"
THIN_BS = "Thin BS"
CUBE_BS = "Cube BS"
CUBE_BS_POLARIZED = "Cube BS Polarizing"

THIN_LENS_TYPE = 0,
D_SHAPED_TYPE = 1,
ODD_ASPHERE_TYPE = 2,
CONIC_TYPE = 3,
SPHERICAL_TYPE = 4,
CYLINDRICAL_TYPE = 5,
ELLIPSOIDAL_TYPE = 6,
PARABOLIC_TYPE = 7,
ASPHERIC_TYPE = 8,
HALF_BALL_LENS_TYPE = 9,
BALL_LENS_TYPE = 10,
OFF_AXIS_PARABOLIC_TYPE = 11,
ROOF_PRISM_MIRROR_TYPE = 12,
BS_CUBE_TYPE = 13,
RIGHT_ANGLE_PRISM_TYPE = 14,
EQUAL_PRISM_TYPE = 15,
WEDGE_TYPE = 16,
PENTA_PRISM_TYPE = 17,
DISPERSION_PRISM_TYPE = 18,
PELLIN_BROCA_PRISM_TYPE = 19,
DOVE_PRISM_TYPE = 20,
AXICON_PRISM_TYPE = 21,
RHOMBIC_PRISM_TYPE = 22,
XY_POLYNOMIAL_TYPE = 23,
ODD_POLYNOMIAL_TYPE = 24,
QCON_ASPHERE_TYPE = 25,
Y_TOROID_TYPE = 26,
X_TOROID_TYPE = 27,
GRATING_TYPE = 28,
MULTIPLET_TYPE = 29,
PARAXIAL_LENS_TYPE = 30,
ZERNIKE_TYPE = 31,
MASK_TYPE = 32,
APERTURE_TYPE = 33

class Setups:
    SETUP_LABELS = ["General",
                    "Microscopy",
                    "Telescopy" ,
                    "Spectroscopy" ,
                    "Imaging" ,
                    "Non-linear optics" ,
                    "Fiber" ,
                    "Illumination" ,
                    "Light sources" ,
                    "Laser Optics" ,
                    "Diffractive Optics"
    ]

class Materials:
    SELLEMEIR = "Sellmeier"
    MODIFIED_SELLEMEIR = "Modified Sellmeier"
    CAUCHY = "Cauchy"
    SCHOTT = "Schott"
    CONRADY1 = "Conrady1"
    CONSTANT = "Constant"
    EQUATION_TYPE_MAP = {
        0: CONSTANT,
        1: SELLEMEIR,
        2: MODIFIED_SELLEMEIR,
        3: CAUCHY,
        6: SCHOTT,
        8: CONRADY1,
    }

class eOpticsTypeNames:
    MIRROR = "Mirror"
    LENS = "Lens"
    FILTER = "Filter"
    BEAM_SPLITTER = "Beam Splitter"
    PRISM = "Prism"
    GRATING = "Grating"
    WINDOW = "Window"
    NON_LINEAR_OPTICS = "Nonlinear Optics (Coming soon)"
    OBJECTIVE = "Objective (Coming soon)"
    POLARIZER = "Polarizer (Coming soon)"
    WAVE_PLATE = "Wave Plate (Coming soon)"
    APERTURE = "Aperture"
    MASK = "Mask"
    POLARIZING_ELEMENT = "Polarizing Element"

class eOpticsSubtypes:
    Metallic_Mirror = "Metallic Mirror"
    Dielectric_Mirror = "Dielectric Mirror"
    Dichroic_Mirror = "Dichroic Mirror"
    Curved_Mirror_Concave = "Curved Mirror (Concave)"
    Curved_Mirror_Convex = "Curved Mirror (Convex)"
    Cylindrical_Mirror_Plano_Convex = "Cylindrical Mirror (Plano-Convex)"
    Cylindrical_Mirror_Plano_Concave = "Cylindrical Mirror (Plano-Concave)"
    Parabolic_Mirror_Concave = "Parabolic Mirror (Concave)"
    Off_Axis_Parabolic_Mirror = "Off-Axis Parabolic Mirror"
    D_Shaped_Mirror = "D-Shaped Mirror"
    Knife_Edge_Prism_Mirror = "Knife-Edge Prism Mirror"
    Right_Angle_Prism_Mirror = "Right-Angle Prism Mirror"
    Roof_Prism_Mirror = "Roof Prism Mirror"
    Ellipsoidal = "Ellipsoidal"
    Knife_Edge_Prism = "Knife-Edge Prism"
    Right_Angle_Prism = "Right-Angle Prism"
    Equilateral_Prism = "Equilateral Prism"
    Dove_Prism = "Dove Prism"
    Wedge_Prism = "Wedge Prism"
    Pellin_Broca_Prism = "Pellin Broca Prism"
    Penta_Prism = "Penta Prism"
    Axicon_Prism = "Axicon Prism"
    Rhombic_Prism = "Rhombic Prism"
    Multiplets = "Multiplets"
    Spherical_Lens_Plano_Convex = "Spherical Lens (Plano-Convex)"
    Spherical_Lens_Plano_Concave = "Spherical Lens (Plano-Concave)"
    Spherical_Lens_Convex_Convex = "Spherical Lens (Convex-Convex)"
    Spherical_Lens_Concave_Concave = "Spherical Lens (Concave-Concave)"
    Spherical_Lens_Concave_Convex = "Spherical Lens (Concave-Convex)"
    Spherical_Lens_Convex_Concave = "Spherical Lens (Convex-Concave)"
    Cylindrical_Lens_Plano_Convex = "Cylindrical Lens (Plano-Convex)"
    Cylindrical_Lens_Plano_Concave = "Cylindrical Lens (Plano-Concave)"
    Ball_Lens = "Ball Lens"
    Half_Ball_Lens = "Half Ball Lens"
    Off_Axis_Parabolic_Lens = "Off-Axis Parabolic Lens"
    Aspheric_Lens = "Aspheric Lens"
    Odd_Asphere = "Odd Asphere"
    Paraxial_Lens = "Paraxial lens"
    General_Conic = "General Conic"
    General_Biconic = "General Biconic"
    Longpass_Filter = "Longpass Filter"
    Shortpass_Filter = "Shortpass Filter"
    Bandpass_Filter = "Bandpass Filter"
    Dichroic_Filter = "Dichroic Filter"
    Notch_Filter = "Notch Filter"
    Calibration_Filter = "Calibration Filter"
    Spectral_Shape_Filter = "Spectral Shape Filter"
    Laser_Line_Filter = "Laser-line Filter"
    Color_Glass = "Color Glass"
    Neutral_Density_Filter = "Neutral Density Filter"
    Hot_Cold_Mirror = "Hot/Cold Mirror"
    Thin_BS = "Thin BS"
    Cube_BS = "Cube BS"
    Cube_BS_POLARIZED = "Cube BS Polarizing"
    Blazed_Ruled_Reflective_Grating = "Blazed Ruled Reflective Grating"
    Reflective_Grating = "Reflective Grating"
    Echelle_Grating = "Echelle Grating"
    Transmission_Grating = "Transmission Grating"
    Flat_Window = "Flat Window"
    Wedge_Window = "Wedge Window"
    Curved_Window_Plano_Convex = "Curved Window (Plano-Convex)"
    Curved_Window_Plano_Concave = "Curved Window (Plano-Concave)"
    Elliptical_Aperture = "Elliptical Aperture"
    Rectangular_Aperture = "Rectangular Aperture"
    Aperture_Image_Upload = "Aperture Image Upload"
    Ideal_Polarizer = "Ideal Polarizer"
    Ideal_Waveplate = "Ideal Waveplate"
    GRATING_SUBTYPES = [Blazed_Ruled_Reflective_Grating, Reflective_Grating, Echelle_Grating, Transmission_Grating]

class eBaseShape:
    CIRCULAR = 0
    RECTANGULAR = 1
    VOLUME = 2
    ELLIPTICAL = 3
    BASE_SHAPE_MAP = {0: 'Circular', 1: 'Rectangular', 2: 'Volume', 3: 'Elliptical'}
    GRATING_SHAPES = {'cir': CIRCULAR, 'rec': RECTANGULAR}

class eOpticShape:
    THIN_LENS = 0
    D_SHAPED = 1
    ODD_ASPHERE = 2
    CONIC = 3
    SPHERICAL = 4
    CYLINDRICAL = 5
    ELLIPSOIDAL = 6
    PARABOLIC = 7
    ASPHERIC = 8
    HALF_BALL_LENS = 9
    BALL_LENS = 10
    OFF_AXIS_PARABOLIC = 11
    ROOF_PRISM_MIRROR = 12
    BS_CUBE = 13
    RIGHT_ANGLE_PRISM = 14
    EQUAL_PRISM = 15
    WEDGE = 16
    PENTA_PRISM = 17
    DISPERSION_PRISM = 18
    PELLIN_BROCA_PRISM = 19
    DOVE_PRISM = 20
    AXICON_PRISM = 21
    RHOMBIC_PRISM = 22
    XY_POLYNOMIAL = 23
    ODD_POLYNOMIAL = 24
    QCON_ASPHERE = 25
    Y_TOROID = 26
    X_TOROID = 27
    GRATING = 28
    MULTIPLET = 29
    PARAXIAL_LENS = 30
    ZERNIKE = 31
    MASK = 32
    APERTURE = 33
    OPTICS_SHAPE_MAP = {
        0: 'Thin Lens',
        1: 'D-Shaped',
        2: 'Odd Asphere',
        3: 'General Conic',
        4: 'Spherical',
        5: 'Cylindrical',
        6: 'Ellipsoidal',
        7: 'Parabolic',
        8: 'Aspheric',
        9: 'Half Ball Lens',
        10: 'Ball Lens',
        11: 'Off-Axis Parabolic',
        12: 'Roof Prism Mirror',
        13: 'Cube BS',
        14: 'Right Angle Prism',
        15: 'Equilateral Prism',
        16: 'Wedge Prism',
        17: 'Penta Prism',
        18: 'Dispersion Prism',
        19: 'Pellin Broca Prism',
        20: 'Dove Prism',
        21: 'Axicon Prism',
        22: 'Rhombic Prism',
        23: 'XY Polynomial',
        24: 'Odd Polynomial',
        25: 'Qcon Asphere',
        26: 'Y Toroid',
        27: 'X Toroid',
        28: 'Grating',
        29: 'Multiplet',
        30: 'Paraxial Lens',
        31: 'Zernike',
        32: 'Mask',
        33: 'Aperture'
    }

class APIMessages:
    PART_MODIFIED = 'Part Modified'

class CoordinateSystems:
    WORLD = 0
    WORLD_DATA = {'ref_pose': {'position': [0, 0, 0], 'rotation': [0, 0, 0]}, 'name': 'Global'}

class ScatteringModels:
    LAMBERTIAN = "LAMBERTIAN"
    GAUSSIAN = "GAUSSIAN"
    COS_NTH = "COS_NTH"
    ABG = "ABG"
class Scattering:
    DEFAULT_TRANS = 1
    DEFAULT_ABS = 0
    DEFAULT_REF = 0
    DEFAULT_RELATIVE_POWER = 0.00001
    DEFAULT_NUMBER_OF = 10
    DEFAULT_SIGMAX = 10
    DEFAULT_SIGMAY = 10
    DEFAULT_AZIMUTH_THETA = 0
    DEFAULT_N = 1.5
    DEFAULT_A = 1
    DEFAULT_B = 2
    DEFAULT_G = 2

class Coating:
    TotalAbsorber = 'absorbing'
    IdealReflector = 'ideal_reflector'
    TR_50_50 = 'np_beam_splitter_50_50'
    TR_70_30 = 'np_beam_splitter_70_30'
    TR_30_70 = 'np_beam_splitter_30_70'
    IdealBBAR = 'ideal_broadband_ar'
    COATINGS_TYPES = [TotalAbsorber, IdealReflector, TR_50_50, TR_70_30, TR_30_70, IdealBBAR]
