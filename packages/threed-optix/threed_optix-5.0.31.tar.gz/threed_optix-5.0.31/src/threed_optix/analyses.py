import zipfile
import requests
import random
import time
import json
import copy
import os
from typing import List, Dict, Union, Tuple
import pandas as pd
import io
import struct
import shutil
import concurrent.futures

import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from plotly.graph_objs.layout import Colorscale
from functools import reduce

import threed_optix.package_utils.api as au
import threed_optix.package_utils.general as gu
import threed_optix.package_utils.vars as v
import threed_optix as tdo

class RayTable(pd.DataFrame):
    '''
    This is the class that represents the ray table.
    It is a pandas DataFrame with some additional attributes, mainly the setup object.
    '''
    def __init__(self, ray_table_url, maps_url, setup_object):
        '''
        Instanciates a new RayTable object.
        '''

        # Fetch the data from the URL
        df = au._map_ray_table(ray_table_url, maps_url)

        # Call the parent class constructor
        super().__init__(df)

        # Add the setup object as an attribute
        self.attrs['setup'] = setup_object
        return None

    @property
    def setup(self):
        return self.attrs['setup']

class Analysis:

    def __init__(self,
                 surface,
                 resolution: Union[Tuple[int, int], List[int]],
                 rays: Union[dict, int],
                 name: str,
                 version: int = 3,
                 fast: bool=False,
                 ):
        """
        Initializes a new instance of the Analysis class.

        Args:
            surface (Surface): The surface of the analysis.
            resolution (tuple): The resolution of the analysis surface in the form (x, y).
            rays (dict): A dictionary of lasers and the number of rays for each laser.
            name (str): The name of the analysis.
            fast (bool, optional): Not used in practice, Specifies if the analysis is fast or advanced. Defaults to False.

        Returns:
            tdo.Analysis: The created Analysis object.

        Raises:
            AssertionError: If the name or rays are not valid for 'fast' choice.
        """

        def verify(fast, name, rays, surface):
            '''
            Private.
            '''

            errors = []

            if not isinstance(surface, tdo.Surface):
                errors.append(f'surface must be of type Surface, got {surface.__class__.__name__}')

            if fast:
                #Check if the name of the analysis is valid for fast analysis
                if not name in v.FAST_ANALYSIS_NAMES:
                    errors.append(f"Valid names for fast analysis are {v.FAST_ANALYSIS_NAMES}")
                #Check if the number of rays is less than 200
                if not all([num <= 200 for num in rays.values()]):
                    errors.append(f'Number of rays must be less than 200 for fast analysis')
            else:
                #Check if the name of the analysis is valid for advanced analysis
                if name in v.DEPRICATED_ANALYSIS_NAMES:
                    non_polirized_name = name.replace(" Polarized", "")
                    errors.append(f"{name} analysis type name is deprecated. You can use {non_polirized_name} instead to use polarized analysis.")
                elif name not in v.VALID_ANALYSIS_NAMES:
                    errors.append(f"Valid names for advanced analysis are {v.VALID_ANALYSIS_NAMES}")



            #res is 2 floats tuple
            if len(resolution) != 2:
                errors.append(f'Resolution must be a tuple of 2 integers, got len {len(resolution)}')

            #Res in the acceptable range
            if not all([v.ANALYSIS_RES_RANGE[0] < num <= v.ANALYSIS_RES_RANGE[1] for num in resolution]):
                errors.append(f'Resolution must be between {v.ANALYSIS_RES_RANGE[0]} and {v.ANALYSIS_RES_RANGE[1]} for analysis')

            # Rays values are integers
            # Trust me, Don't check for ints, because 1e8 is a float, for example
            if not all([int(num) == num for num in rays.values()]):
                errors.append(f'Number of rays must be an integer')

            # If rays are a dictionary of lasers and number of rays
            if isinstance(rays, dict):
                # Rays keys are LightSource
                if not all([key.__class__.__name__ == 'LightSource' for key in rays.keys()]):
                    errors.append(f'Keys of rays must be of type LightSource')
                # Rays light sources are in the setup
                all_laser_ids_in_rays = self._laser_ids_in_rays(surface._part._setup, rays)
                if not all_laser_ids_in_rays:
                    errors.append('If rays is a dict, all lasers in the setup must be included in the rays dictionary')
                # Rays in the acceptable range
                if not all([v.ANALYSIS_RAYS_RANGE[0] <= num <= v.ANALYSIS_RAYS_RANGE[1] for num in rays.values()]):
                    errors.append(f'Number of rays must be between {v.ANALYSIS_RAYS_RANGE[0]} and {v.ANALYSIS_RAYS_RANGE[1]} for analysis')

            # If rays is an integer, indicating the number of rays for all lasers
            else:
                if v.ANALYSIS_RAYS_RANGE[0] <= rays <= v.ANALYSIS_RAYS_RANGE[1]:
                    errors.append(f'Number of rays must be between {v.ANALYSIS_RAYS_RANGE[0]} and {v.ANALYSIS_RAYS_RANGE[1]} for analysis')

            return errors

        # If rays is an integer, indicating the number of rays for all lasers
        if isinstance(rays, float) or isinstance(rays, int):
            rays = {laser: rays for laser in surface._part._setup.light_sources}

        if isinstance(resolution, (int, float)):
            resolution = (resolution, resolution)

        # Check if the arguments are valid
        errors = verify(fast=fast, name=name, rays=rays, surface = surface)
        if errors:
            raise AssertionError(v.argument_repair_message(errors))

        if not fast and name in (v.VALID_ANALYSIS_NAMES[0], v.VALID_ANALYSIS_NAMES[1], v.VALID_ANALYSIS_NAMES[2]):
            name = f"{name} Polarized"


        self._added = False
        self._urls = []
        self._maps_json = None
        self._fail_message = None
        self._raw_results = {}
        self.results = {}
        self.surface = surface
        self.name = name
        self.rays = rays
        self.resolution = resolution
        self.version = 3
        self.fast = fast

        # No need to generate id anymore, it is being set when added to the surface
        self.id = Analysis._generate_id()


    @classmethod
    def _new(cls, surface, resolution, num_rays, name, type, id):
        '''
        Private.
        Past analysis are stored within the setup.
        When the setup is fetched, the past analysis are created using this method.
        '''
        analysis = object.__new__(cls)
        analysis.surface = surface
        analysis.resolution = list(resolution.values())
        analysis.rays = {surface._part._setup[laser_id]: num for laser_id, num in num_rays.items()}
        analysis.name = name
        analysis.fast = False if type == '1' else True
        analysis.id = id
        analysis._added = True
        analysis._urls = []
        analysis._fail_message = None
        analysis._raw_results = {}
        analysis.results = {}
        return analysis

    def _laser_ids_in_rays(self, setup, rays):
        """
        Validates that all laser IDs in the setup's light sources are included in the rays dictionary.

        Args:
        setup: The setup object containing the light sources.
        rays: The dictionary of rays.
        errors: The list to append error messages to.
        """
        # Extract laser IDs from the light sources in the setup
        laser_ids_in_setup = [laser.id for laser in setup.light_sources]

        laser_ids_in_rays = [laser.id for laser in rays.keys()]

        # Check if all laser IDs are in the rays dictionary
        all_laser_ids_in_rays = all(id in laser_ids_in_rays for id in laser_ids_in_setup)

        return all_laser_ids_in_rays

    @property
    def wls(self):
        '''
        Returns a sorted list of the analysis wavelengths.
        '''
        return self._analysis_wls()

    @classmethod
    def _generate_id(cls):
        '''
        Private
        Generates a unique id for the analysis.
        '''
        int_time = int(time.time())
        enc_36_time = np.base_repr(int_time, 36)
        randint = np.base_repr(random.randint(0, 36**5), 36)[2:5]
        id_ = enc_36_time + randint
        return id_

    def _read_file_old(self, file_path):
        '''
        Private.
        Reads the results of the analysis from a file
        '''

        with open(file_path, 'rb') as f:
            content = f.read().strip()


        header = np.frombuffer(content[:v.HEADER_BYTES], dtype=v.ANALYSIS_HEADER_DTYPES)
        data = np.frombuffer(content[v.HEADER_BYTES:], dtype=v.ANALYSIS_MATRIX_DTYPES)
        return header, data

    def _process_v1_file(self, file_path):
        '''
        Deprecated.
        '''
        file_results = {}
        headers_nums, data = self._read_file_old(file_path)
        headers = gu._process_headers_old(headers_nums)
        wls = self.wls

        if v.DEBUG:
            print(f'Headers: {headers}')
            print(f'Wavelengths: {wls}')
            print(f'Data shape: {data.shape}')

        if headers['data_kind'] not in v.SUPPORTED_DATA_KINDS_NAMES:
            return False

        if data.shape[0] != len(wls)*self.resolution[0]*self.resolution[1]:
            return False

        file_results['metadata'] = headers
        res_x = headers['resolution'][0]
        res_y = headers['resolution'][1]
        data_matrices = data.reshape(len(wls), res_x, res_y)

        if v.DEBUG:
            print(f'Data matrices shape: {data_matrices.shape}')

        file_results['data'] = {}
        for i, wl in enumerate(wls):

            if v.DEBUG:
                print(f'Processing wavelength {wl} nm')

            matrix = data_matrices[i]
            file_results['data'][wl] = matrix

        return file_results

    def _process_old(self, directory):
        '''
        Deprecated.
        '''
        file_results = {}
        for file_name in os.listdir(directory):
            if file_name.endswith('.bin'):
                file_path = f'{directory}/{file_name}'
                file_results[file_name] = self._process_v1_file(file_path)
        return file_results

    def _analysis_wls(self):
        '''
        Private.
        Returns a sorted list of the wavelengths of the analysis
        '''
        analysis_wls = []
        setup = self.surface._part._setup
        laser_objects = [setup[laser.id] for laser in self.rays.keys()]
        for laser in laser_objects:
            wls_dicts = laser.data['light_source']['wavelengths_data']
            wls = [wls_dict['wavelength'] for wls_dict in wls_dicts]
            analysis_wls += wls
        analysis_wls = sorted(list(set(analysis_wls)))
        return analysis_wls

    def _extract_file(self,url, destination):
        ''''
        Private.
        Extracts a zip file from a url to a destination folder
        '''

        # Get the zip file from the url
        response = requests.get(url)

        # If the response is successful, extract the zip file
        if response.status_code == 200:

            # Get the zip file as a BytesIO object
            zip_data = BytesIO(response.content)

            # Read the zip file
            with zipfile.ZipFile(zip_data, 'r') as zip_ref:

                # Extract the zip file to the destination folder
                zip_ref.extractall(destination)

        # Return the file path
        file_name = url.split('/')[-1].replace(f'{self.id}_', '').replace('.zip', '')
        file_path = f'{destination}/{file_name}'
        return file_path

    def _unpack(self):
        '''
        Private.
        Unpacks the results of the analysis to a folder
        '''

        # Get the setup id
        setup = self.surface._part._setup.id

        # Create the destination folder
        destination_path = f'.analysis-files/{setup}/{self.surface.id}/{self.id}'
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        # Extract the files for each one of the urls concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:

            # Submit tasks to the thread pool executor
            future_results = {executor.submit(self._extract_file, url, destination_path): url for url in self._urls}

            # Future is the object name in the python library
            for future in future_results:
                url = future_results[future]

                try:
                    future.result()
                except Exception as e:
                    if v.DEBUG:
                        print(f"An error occured while getting url {url}\n Error: {e}")

        # Return the destination folder
        return destination_path


    ### For version 2 of binary file ###
    def _process_v2_file(self, file_path):
        '''
        This function processes the binary result files of the analysis.
        '''

        # Read the file to get the headers, wls and data
        headers_nums, wls, data = self._read_file2(file_path)

        # Process the headers, and start the file results dictionary
        file_results = self._process_headers(headers_nums)
        file_results_with_wls = self.process_wavelength_data(wls = wls, data = data, file_results = file_results, headers_nums = headers_nums)
        return file_results_with_wls


    ### For version 3 of binary file ###
    def _process_v3_file(self, file_path):
        '''
        This function processes the binary result files of the analysis.
        '''

        # Read the file to get the headers, wls and data
        headers_nums, wls, data = self._read_file3(file_path)

        # Process the headers, and start the file results dictionary
        file_results = self._process_headers(headers_nums)
        file_results_with_wls = self.process_wavelength_data(wls = wls, data = data, file_results = file_results, headers_nums = headers_nums)
        return file_results_with_wls


    def process_wavelength_data(self, wls, data, file_results, headers_nums):
        if v.DEBUG:
            print(f'Headers: {file_results}')
            print(f'Data shape: {data.shape}')

        # Check if the data kind is supported
        if file_results['data_kind'] not in v.SUPPORTED_DATA_KINDS_NAMES:
            if v.DEBUG:
                print(f"Data kind not in the supported kinds: {file_results['data_kind']}")
            return False

        # The data shape should be a matrix of size res_x*res_y for each wavelength. For polarization kind raw, each matrix item has 3 numbers.
        data_shape = (len(wls), self.resolution[0], self.resolution[1], 3) if headers_nums['polarization kind'][0] == 4 else (len(wls), self.resolution[0], self.resolution[1])
        num_items = reduce(lambda x, y: x * y, data_shape)

        # Check if the data shape is correct
        if data.shape[0] != num_items:
            if v.DEBUG:
                print(f"Data shape not correct: {data.shape}, Expected: {data_shape}")
            return False

        # Reshape the long list of numbers to the data matrices
        data_matrices = data.reshape(data_shape)

        if v.DEBUG:
            print(f'Data matrices shape: {data_matrices.shape}')

        # Create a list of results. It's redundant but important since it will be added to a pandas dataframe
        file_results_with_wls = []
        for i, wl in enumerate(wls):
            wl_dict = file_results.copy()
            if v.DEBUG:
                print(f'Processing wavelength {wl} nm')

            # Get the matrix for the current wavelength
            matrix = data_matrices[i]

            # Add the matrix to the results
            wl_dict['data'] = matrix

            # Add the wavelength to the results
            wl_dict['wl'] = wl

            file_results_with_wls.append(wl_dict)

        return file_results_with_wls


    def _process(self, directory):
        '''
        Private.
        Processes the results of the analysis
        '''
        results = []

        # For each results file in the directory, process the file and append the results to a list
        for file_name in os.listdir(directory):
            if file_name.endswith('.bin'):
                file_version = self._check_file_version(f'{directory}/{file_name}')
                self.version = file_version

                if(v.DEBUG):
                    print(f'File Version: {file_version}')

                file_path = f'{directory}/{file_name}'
                if(file_version == 2):
                    file_results = self._process_v2_file(file_path)
                else:
                    file_results = self._process_v3_file(file_path)

                # For now, if the file results are false, we skip it rather then dealing with it.
                if not file_results:
                    continue
                results += file_results

        return results


    def _process_results(self, directory = None, should_delete = True):
        '''
        Private.
        Processes the results of the analysis
        '''
        if directory is None:
            directory = self._unpack()

        if v.DEBUG:
            print(f'Unpacked analysis files to {directory}')
            print(f'Number of files: {len(os.listdir(directory))}')

        version = self._check_file_version(f'{directory}/{os.listdir(directory)[0]}')

        if version == 1:
            self.version = 1
            results = self._process_old(directory)

        elif version == 2 or version == 3:
            results = self._process(directory)

        else:
            raise Exception(f'Version {version} is not supported')

        self._raw_results = results
        if version == 1:
            self.results = gu.reorganize_analysis_results_dict(self._raw_results.values())

        elif version == 2 or version == 3:
            self.results = AnalysisResults(self._raw_results, maps = self._maps_json, analysis_object = self)

        #delete directory and all subdirectories
        if(should_delete):
            shutil.rmtree(directory)

        self.reset()

        #Sort results by source and polarization - for convenience
        try:
            if(not "MULTI_CHANNEL_IMAGE" in self.results['analysis_kind']):
                self.results.sort_values(by = ['spot_target', 'polarization'], axis = 0, inplace = True)
                self.results = self.results.reset_index(drop = True)

        except Exception as e:
            if v.DEBUG:
                print(f"Error: {e}")

        return self.results

    def reset(self):
        self._urls = []
        self._raw_results = {}
        return

    def _check_file_version(self, file_path):
        version_bytes  = v.AnalysisProcessVariables.VERSION_BYTES
        with open(file_path, 'rb') as f:
            # version bytes is the range of the 4 bytes indicating the int32 version number. The first int is the beginning, the second is the end
            f.seek(version_bytes[0])
            version = struct.unpack('i', f.read(version_bytes[1] - version_bytes[0]))[0]

            if v.DEBUG:
                print(f'Version: {version}')

        return version


    ### Read V2 binary file ###
    def _read_file2(self, file_path):

        with open(file_path, 'rb') as f:
            content = f.read().strip()

        header = np.frombuffer(content[:v.AnalysisFile2.HEADER_BYTES], dtype=v.AnalysisFile2.HEADER_DTYPES)
        num_wls = header['num_wavelengths'][0]
        if v.DEBUG:
            print(f'Number of wavelengths: {num_wls}')
            print(f'Header nums: {header}')

        wls = np.frombuffer(content[v.AnalysisFile2.HEADER_BYTES:v.AnalysisFile2.HEADER_BYTES + num_wls*4], dtype=[(f'{wl}i', v.AnalysisFile2.WLS_DTYPE) for wl in range(num_wls)])[0]
        data = np.frombuffer(content[v.AnalysisFile2.HEADER_BYTES + num_wls*4:], dtype=v.AnalysisFile2.DATA_DTYPE)

        if v.DEBUG:
            print(f"Data shape: {data.shape}")

        return header, wls, data


    ### Read V3 binary file ###
    def _read_file3(self, file_path):

        with open(file_path, 'rb') as f:
            content = f.read().strip()

        header = np.frombuffer(content[:v.AnalysisFile3.HEADER_BYTES], dtype=v.AnalysisFile3.HEADER_DTYPES)
        num_wls = header['num_wavelengths'][0]
        if v.DEBUG:
            print(f'Number of wavelengths: {num_wls}')
            print(f'Header nums: {header}')

        wls = np.frombuffer(content[v.AnalysisFile3.HEADER_BYTES:v.AnalysisFile3.HEADER_BYTES + num_wls*4], dtype=[(f'{wl}i', v.AnalysisFile3.WLS_DTYPE) for wl in range(num_wls)])[0]
        data = np.frombuffer(content[v.AnalysisFile3.HEADER_BYTES + num_wls*4:], dtype=v.AnalysisFile3.DATA_DTYPE)

        if v.DEBUG:
            print(f'Data shape: {data.shape}')
            print(f'Wavelengths: {wls}')

        return header, wls, data


    def _process_headers(self, headers):
        '''
        Private.
        Processes the headers of the analysis
        '''
        data_kind_mapping = v.DATA_KINDS_MAPPING
        polarization_mapping = v.POLARIZATION_MAPPING


        analysis_kind = v.ANALYSIS_KIND[headers['analysis kind'][0]]
        data_kind = headers['data kind'][0]
        polarization_kind = headers['polarization kind'][0]
        num_hits = headers['num_hits'][0]
        num_wavelengths = headers['num_wavelengths'][0]
        resolution_x = headers['resolution_x'][0]
        resolution_y = headers['resolution_y'][0]
        resolution = (resolution_x, resolution_y)
        data_kind_value = data_kind_mapping.get(data_kind)
        polarization_kind_value = polarization_mapping.get(polarization_kind)
        spot_target_kind = headers['spot_target_kind'][0]
        spot_target_index = headers['spot_target_index'][0]
        if(self.version == 3):
            number_of_surfaces = headers['number_of_surfaces'][0]

        headers = {
            "analysis_kind": analysis_kind,
            "data_kind": data_kind_value,
            "polarization_kind": polarization_kind_value,
            "num_hits": num_hits,
            "num_wavelengths": num_wavelengths,
            "resolution": resolution,
            'spot_target_kind': spot_target_kind,
            'spot_target_index': spot_target_index,

        }
        try: ## Will work if self.version == 3, else this field is not in header
            headers['number_of_surfaces'] = number_of_surfaces
        except Exception as e:
            if v.DEBUG:
                print(f"Field number of surfaces doesnt exist, check version. Error: {e}")

        return headers

    def __str__(self):
        json_dict = {
            "name": self.name,
            "surface": self.surface.id,
            "rays": {laser.id: num for laser, num in self.rays.items()},
            "resolution": tuple(self.resolution),
        }
        string = json.dumps(json_dict, indent = 4)
        return string

    def __eq__(self, other):
        '''
        Equal analyses are analyses with the same parameters of rays, name, resolution and surface.
        '''
        if not isinstance(other, Analysis):
            return False

        is_rays_equal = self.rays == other.rays
        is_name_equal = self.name == other.name
        is_resolution_x_equal = self.resolution[0] == other.resolution[0]
        is_resolution_y_equal = self.resolution[1] == other.resolution[1]
        is_surface_equal = self.surface.id == other.surface.id

        if is_rays_equal and is_name_equal and is_surface_equal and is_resolution_x_equal and is_resolution_y_equal:
            return True

        return False

    @property
    def data(self):
        return self.results

    def show(self, polarizations: list = None, wavelengths: list = None, figsize: Tuple[int, int] = (20, 20), upscale: bool = False):
        '''
        Shows a static figure of the analysis results.
        Args:
            figsize (tuple): The size of the figure.
            upscale (bool): If True, smoothes the pixels over, if the analysis resolution is lower than the figure resolution.

        Returns:
            None

        Shows:
            A figure of the analysis results.

        Raises:
            Exception: If the analysis was not run yet.
        '''

        raise Exception('This method is not supported yet')

        #3DOptix color scale
        cmap = LinearSegmentedColormap.from_list('custom', v.COLOR_SCALE)

        if not self.results:
            raise Exception('Analysis was not run yet')

        if not polarizations:
            one_wl_data = list(self.results.values())[0]
            polarizations = list(one_wl_data.keys())
        if not wavelengths:
            wavelengths = list(self.results.keys())

        #Check if the analysis was run
        if not self.results:
            raise Exception('Analysis was not run yet')

        #Get the number of polarizations and wavelengths of the analysis- polarizations are the rows and wavelengths are the columns of the presented figure
        num_polarizations = len(self.results)
        num_wavelengths = len(self.wls)
        fig = plt.figure(constrained_layout=True, figsize=figsize)
        subfigs = fig.subfigures(nrows=num_polarizations, ncols=1)

        if num_polarizations == 1:
            subfigs = [subfigs]

        for polarization, subfig in zip(polarizations, subfigs):

            subfig.suptitle(f'Polarization {polarization}')
            axs = subfig.subplots(nrows=1, ncols=num_wavelengths)

            if num_wavelengths == 1:
                axs = [axs]

            for wavelength, ax in zip(wavelengths, axs):
                data = self.results[wavelength][polarization]
                if upscale:
                    dpi = plt.rcParams['figure.dpi']
                    data = gu.upscale(data, figsize[0]*dpi, figsize[1]*dpi)
                ax.imshow(data, cmap=cmap)

                ax.set_title(f'Wavelength {wavelength} nm')

        #Show the figure
        plt.show()
        return None

    def show_interactive(self, polarizations: list = None, wavelengths: list = None, figsize: Tuple[int, int] = (20, 20), upscale: bool = False):
        '''
        Shows an interactive figure of the analysis results.
        Args:
            polarizations (list): The polarizations to present. If None, all polarizations are presented.
            wavelengths (list): The wavelengths to present. If None, all wavelengths are presented.
            height (int): The height of the each figure.
            width (int): The width of each figure.
            upscale (bool): If True, smoothes the pixels over, if the analysis resolution is lower than the figure resolution.
        Returns:
            None

        Shows:
            An interactive figure of the analysis results.

        Raises:
            Exception: If the analysis was not run yet.
        '''

        raise Exception('This method is not supported yet')

        dpi = plt.rcParams['figure.dpi']
        height = figsize[0]*dpi
        width = figsize[1]*dpi

        if not self.results:
            raise Exception('Analysis was not run yet')

        if not polarizations:
            one_wl_data = list(self.results.values())[0]
            polarizations = list(one_wl_data.keys())
        if not wavelengths:
            wavelengths = list(self.results.keys())

        for polarization in polarizations:
            for wavelength in wavelengths:
                data = self.results[wavelength][polarization]
                if upscale:
                    data = gu.upscale(data, height, width)

                fig = px.imshow(data, title=f'Polarization {polarization} Wavelength {wavelength} nm', color_continuous_scale = v.COLOR_SCALE)
                fig.update_layout(height=height, width=width)
                fig.show()

    def copy(self):
        '''
        Copies the analysis to a different analysis object with a different id.
        Returns:
        tdo.Analysis: The copied analysis.
        '''
        copied = copy.deepcopy(self)
        copied.id = Analysis._generate_id()
        copied._added = False
        return copied

class AnalysisResults(pd.DataFrame):

    def __init__(self, data, maps, analysis_object):
        '''
        Private.
        Past analysis are stored within the setup.
        When the setup is fetched, the past analysis are created using this method.
        '''
        df = gu.process_results(data, maps)
        super().__init__(df)
        self.attrs['analysis_id'] = analysis_object.id
        return None
