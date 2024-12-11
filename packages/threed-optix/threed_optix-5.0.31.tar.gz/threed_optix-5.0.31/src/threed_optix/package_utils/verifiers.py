from typeguard import typechecked
from typing import List,Dict
import re
import pandas as pd
from threed_optix.analyses import Analysis
import threed_optix.package_utils.vars as v

class MultipletVerifiers:

    @staticmethod
    @typechecked
    def validate_multiplet_params(
                        name: str,
                        num_surfaces: int,
                        materials:List[str],
                        diameter: float,
                        r_x:List[float],
                        r_y:List[float],
                        thickness:List[float],
                        hole_diameters: List[float],
                        k_y: List[float],
                        k_x: List[float],
                        decenter_x: List[float],
                        decenter_y: List[float],
                        coeffs:Dict,
                        coating: Dict):

        if(num_surfaces < 3):
            raise ValueError(f"Invalid number of surfaces!"
                            f"The minimal number of surfaces is 3, input is {num_surfaces}")

        param_length_checks = {
        "r_x": num_surfaces,
        "r_y": num_surfaces,
        "thickness": num_surfaces - 1,
        "hole_diameters": 2,
        "k_y": num_surfaces,
        "k_x": num_surfaces,
        "decenter_x": num_surfaces,
        "decenter_y": num_surfaces,
        "materials":num_surfaces-1
        }

        # Validate lists
        for param_name, expected_length in param_length_checks.items():
            MultipletVerifiers.check_params_length(locals()[param_name], expected_length, param_name)

        MultipletVerifiers.validate_dict_keys(coeffs, num_surfaces)
        MultipletVerifiers.validate_dict_keys(coating,num_surfaces)

        return

    @staticmethod
    def check_params_length(param, target_length, param_name):
        if len(param) != target_length:
            raise ValueError(
                f"Invalid list length for '{param_name}'! "
                f"Expected {target_length}, got {len(param)}."
            )
        return

    @staticmethod
    def validate_dict_keys(surfaces_dict, num_surfaces):
        if not surfaces_dict:
            return

        pattern = re.compile(r"^s(\d+)$")  # Matches keys in the format s<number>
        for key in surfaces_dict:
            match = pattern.match(key)
            if match:
                number = int(match.group(1))  # Extract the number from the key
                if number > num_surfaces:
                    raise ValueError(
                        f"Invalid key '{key}' in coeffs! The number ({number}) exceeds num_surfaces ({num_surfaces})."
                    )
            else:
                raise ValueError(
                    f"Invalid key '{key}' in coeffs! Keys must match the pattern 's<number>'."
            )

        return

class BatchAnalysisVerifiers:

    @staticmethod
    def validate_configurations_csv(configurations_csv_path, parts_id_list):
        all_id = set(parts_id_list)
        config_df = pd.read_csv(configurations_csv_path)

        for part_id in config_df.columns:
            if part_id not in all_id:
                raise NameError(f"Part id '{part_id}' exists in csv columns but does not exist in setup. Please make sure that all csv columns are a valid part.id of a part in this setup")

        pattern = re.compile(r"""
        ^([XYZABG]-?\d+(\.\d+)?)+$  # Matches one or more valid components
        """, re.VERBOSE)

        # Apply regex validation to all cells
        is_valid = config_df.map(lambda x: bool(pattern.match(str(x))) if isinstance(x, str) else False)

        # Identify invalid cells
        invalid_cells = config_df[~is_valid]
        if not is_valid.all().all():
            # Raise an error with the locations of invalid cells
            invalid_locations = list(zip(*(~is_valid.to_numpy()).nonzero()))
            raise ValueError(
                f"Invalid cells found at rows and columns: {invalid_locations}\nInvalid values:\n{invalid_cells.dropna(how='all')}"
            )

        return

    @staticmethod
    def validate_analysis_limits(analysis: Analysis):
        for num_rays in analysis.rays.values():
            if num_rays > v.Analyses.BATCH_ANALYSIS_RAY_LIMIT:
                raise ValueError(f"Number of rays in analysis exceeds the limit, the limit is {v.Analyses.BATCH_ANALYSIS_RAY_LIMIT} rays")

        if analysis.resolution[0] > v.Analyses.BATCH_ANALYSIS_RESOLUTION_LIMIT or analysis.resolution[1] > v.Analyses.BATCH_ANALYSIS_RESOLUTION_LIMIT:
            raise ValueError(f"Detector resolutions exceeds the limit, the limit is ({(v.Analyses.BATCH_ANALYSIS_RESOLUTION_LIMIT,v.Analyses.BATCH_ANALYSIS_RESOLUTION_LIMIT)}")

        return

    @staticmethod
    @typechecked
    def validate_and_format_parameters(parameters: Dict):
        if parameters == {}:
            return

        for key in parameters.keys():
            if key not in v.Analyses.BATCH_ANALYSIS_PARAMETERS_KEYS:
                raise KeyError(f"Invalid key in parametes! Valid keys are: {v.Analyses.BATCH_ANALYSIS_PARAMETERS_KEYS}")

        if(polarizations := parameters.get(v.Analyses.BATCH_ANALYSIS_PARAMETERS_KEYS[0], False)):

            if not isinstance(polarizations,list):
                raise ValueError(f"Invalid input as polarization, polarization should be a list")

            for pol in polarizations:
                if pol not in v.Analyses.POLARIZTION_FILTERS or len(polarizations) > 4:
                    raise ValueError(f"Invalid polarization filter! Availvable filters are: {v.Analyses.POLARIZTION_FILTERS}")

            parameters['polarization'] = {"polarization_kind": polarizations,
                                          "has_mapping": False} ## False is defalut for now, can change if you wish

        coherence = {}
        if(has_total := parameters.get(v.Analyses.BATCH_ANALYSIS_PARAMETERS_KEYS[1])) is not None:
            GeneralVerifiers.validate_bool(has_total,v.Analyses.BATCH_ANALYSIS_PARAMETERS_KEYS[1])

            coherence['has_total'] = has_total
            parameters.pop(v.Analyses.BATCH_ANALYSIS_PARAMETERS_KEYS[1])

        if(has_coherence_groups := parameters.get(v.Analyses.BATCH_ANALYSIS_PARAMETERS_KEYS[2])) is not None:
            GeneralVerifiers.validate_bool(has_coherence_groups,v.Analyses.BATCH_ANALYSIS_PARAMETERS_KEYS[2])

            coherence['has_coherence_groups'] = has_coherence_groups
            parameters.pop(v.Analyses.BATCH_ANALYSIS_PARAMETERS_KEYS[2])

        if len(coherence.keys()) > 0:
            parameters['coherence'] = coherence

        if v.DEBUG:
            print(f"parameters: {parameters}")

        return

class GeneralVerifiers:

    @staticmethod
    def validate_bool(val, key):
        if not isinstance(val, bool):
                raise ValueError(f"Invalid value for {key}, Value should be boolean")
