import os
import pickle
import time
import random
import requests
import zipfile
import dill
import copy
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from typing import List, Dict

from typing import Union
from io import BytesIO

import numpy as np
import pandas as pd

import threed_optix.package_utils.math as mu
import threed_optix.package_utils.general as gu
import threed_optix.package_utils.api as au
import threed_optix.package_utils.vars as v
import threed_optix.analyses as tdo_analyses
import threed_optix.parts as tdo_parts
from typing import Dict
from typeguard import typechecked

class Setup(object):
    """
    Used to manage the simulation setup and its parts.

    Properties:
        name (str): The name of the setup.
        id (str): The id of the setup.
        _api (ThreedOptixAPI): The pointer to the API that created it.
        parts (list): The list of part objects (or classes that inherit from Part).
    """

    def __init__(self):
        '''
        Private
        '''
        raise TypeError("Cannot directly create an instance of Setup.")

    @classmethod
    def _new(cls, _api, setup_tuple: tuple):
        """
        Private.
        Creates a setup with API pointer, id, and name only.

        Args:
            _api (ThreedOptixAPI): The API pointer.
            info_json (dict): Information JSON.

        Returns:
            Setup: The newly created Setup object.
        """
        setup = object.__new__(cls)
        setup.id = setup_tuple[0]
        setup.name = setup_tuple[1]
        setup._api = _api
        setup._opt = None
        setup._parts = None
        setup._user_backup = {v.BASE_BACKUP: None}
        return setup

    def __len__(self) -> int:
        """
        Returns the number of parts that the setup has.

        Returns:
            int: The number of parts in the setup.
        """
        return len(self.parts)

    def __iter__(self):
        """
        Iterates through the parts of the setup.
        """
        return iter(self.parts)

    def __contains__(self, part: Union[tdo_parts.Part, str]) -> bool:
        """
        Allows checking if a part is in the setup.

        Args:
            part (tdo.Part): The part to check.

        Returns:
            bool: True if the part is in the setup, False otherwise.

        Raises:
            TypeError: If the part is not a Part object or a part id.
        """

        if not isinstance(part, (tdo_parts.Part, str)):
            raise TypeError(f"Invalid part type {type(part)}. Must be Part or part id.")

        if isinstance(part, tdo_parts.Part):
            for p in self:
                if p.id == part.id:
                    return True

        if isinstance(part, str):
            for p in self:
                if p.id == part:
                    return True

        return False

    def __getitem__(self, key: str):
        """
        Getting parts by index.

        Args:
            key (str): The id of the part.

        Returns:
            Part (tdo.Part): The requested Part object.

        Raises:
            TypeError: If the key is not an int or a str.
            KeyError: If the key is a str and the part is not found.
        """
        # if isinstance(key, int):
        #     return self.parts[key]
        if isinstance(key, str):
            for part in self:
                if part.id == key:
                    return part
            raise KeyError(f"Part with id {key} not found in the setup.")
        raise TypeError(f"Invalid key type {type(key)}. Must be part index or id.")

    def __str__(self):
        '''
        Returns a string representation of the setup and its parts ids and labels.
        '''
        string = f"Setup {self.name} ({self.id}) with {len(self)} parts:\n"
        for part in self:
            string += f"  - {part.label} ({part.id})\n"
        return string

    @property
    def parts(self):
        """
        Property to access the list of part objects of the setup.
        Returns:
            list: The list of Part objects.
        """
        if self._parts is None:
            self._get_parts()
            self._user_backup[v.BASE_BACKUP] = {part.id: copy.deepcopy(part._data) for part in self}

        return self._parts

    def _retrieve_parts(self):
        try:
            setup_data = self._api._get_setup_parts(self.id)
            parts = setup_data.get(self.id).get('parts')

            self._parts = [tdo_parts.create_part(_setup=self, id=part['id']) for part in parts]
        except Exception as e:
            self.retrieving_parts_error = e

    def _get_parts(self):

        def create_part(id, type_):
            try:
                part = tdo_parts.create_part(_setup=self, id=id, type_ = type_)
                self._parts.append(part)
            except Exception as e:
                self._part_creation_errors.append(e)
            return None

        self._parts = []

        setup_data = self._api._get_setup_parts(self.id)
        parts = setup_data.get(self.id).get('parts')
        self._part_creation_errors = []

        for part in parts:
                create_part(id=part['id'], type_ = part['type'])

        if len(self._part_creation_errors) > 0:
            raise self._part_creation_errors[0]

        if v.DEBUG:
            print(f"Parts retrieved: {len(self._parts)}")

        return None

    def _get_part(self, part_id):
        '''
        Private.
        '''
        part = self._api._get_part(part_id, self.id)
        return part

    def _get_surface(self, part_id, surface_id):
        return self._api._get_surface(setup_id = self.id, part_id=part_id, surface_id=surface_id)

    def add_analysis(self, analysis, force = False):
        analysis.surface.add_analysis(analysis, force = force)
        return

    def delete_analysis(self, analysis: Union[str, tdo_analyses.Analysis]):
        analysis.surface.delete_analysis(analysis)
        return


    def get(self,
            part_label: str,
            all: bool = False):
        """
        Returns the part object with the specified label.

        Args:
            part_label (str): The label of the part.
            all (bool): If True, returns a list of all parts with the specified label.

        Returns:
            Part (tdo.Part): The requested Part object if found, None otherwise.
        """
        if all:
            parts = []
            for part in self:
                if part.label == part_label:
                    parts.append(part)
            return parts

        for part in self:
            if part.label == part_label:
                return part

        raise KeyError(f"Part with label {part_label} not found in the setup.")

    def at(self, location: tuple):
        """
        Private.
        Returns the closest part object to the specified location in the global coordinate system.

        Args:
            location (tuple): The global coordinates (x, y, z) of the location.

        Returns:
            Part: The closest Part object.
        """

        distances = []

        for part in self:
            distance = mu._3d_distance(location, part._pose._position)
            distances.append(distance)

        min_value = min(distances)
        min_index = distances.index(min_value)
        min_part = self[min_index]
        return min_part

    def save(self, file_path: str):
        """
        Saves the object to a re-creatable pickle file with 'dill' package.

        Args:
            file_path (str): The path to save the pickle file.
        """
        with open(file_path, 'wb') as f:
            dill.dump(self, f)

    @classmethod
    def load(cls, file_path: str, api):
        """
        Loads the object from the pickle\dill file path.

        Args:
            file_path (str): The path to the dill file.
            api (tdo.ThreedOptixAPI): The API instance.

        Returns:
         setup (tdo.Setup): The loaded Setup object.
        """
        with open(file_path, 'rb') as f:
            setup = dill.load(f)
        if api is not None:
            setup._api = api
        return setup

    def plot(self):
        """
        Private.
        Plots the setup to visualize its configuration.
        """
        raise NotImplementedError("This method is not implemented yet.")

    def restore(self, name = v.BASE_BACKUP):
        threads = []
        for part in self:
            thread = threading.Thread(target=part.restore, kwargs={'name': name})
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return None

    def _update_part(self, part: tdo_parts.Part):
        '''
        Private
        '''
        return self._api._update_part(self.id, part)


    def backup(self, name = v.BASE_BACKUP):
        for part in self:
            part.backup(name = name)
        return None

    @property
    def light_sources(self):
        '''
        Returns a list of all lasers in the setup.
        '''
        lasers = []
        for part in self:
            if isinstance(part, tdo_parts.LightSource):
                lasers.append(part)
        return lasers

    @property
    def detectors(self):
        '''
        Returns a list of all detectors in the setup.
        '''
        detectors = []
        for part in self:
            if isinstance(part, tdo_parts.Detector):
                detectors.append(part)
        return detectors

    @property
    def optics(self):
        '''
        Returns a list of all optics in the setup.
        '''
        optics = []
        for part in self:
            if isinstance(part, tdo_parts.Part) \
                and not isinstance(part, tdo_parts.LightSource) \
                    and not isinstance(part, tdo_parts.Detector):
                optics.append(part)
        return optics

    def run(self, analysis:tdo_analyses.Analysis = None, configurations_csv_path: str = None, parameters: Dict = {}):
        '''
        Function used to run an analysis.

        Args:
            analysis (tdo_analyses.Analysis, default None): Analysis object which you want to run. If no argumet is enterd a ray table will be returned with initial ray count as defined in the GUI.
            configurations_csv_path (str CSV file path, default None): Path to a csv file where each line is a configuration for an analysis iteration. Guide for creating such file is in our website.
            paramaters (Dict, default None): Filters for what analysis parameters you want to calculate, used to filter out unwanted parametes of anlysis when running analysis ***WITH CSV FILE ONLY***.

        'parameters' keys:
            polarization (list) -> ["X","Y","Z","NONE"] | Can use one or more to select what kind of polarization you want to calculate.
            has_total (bool, default True) -> True/False | true means you will recieve results for all light sources combined in addition for results for each lightsource
            has_coherence_groups (bool, default True) -> True/False | true means you will recieve results for coherence groups in adittion to lightsources.

            Returns:
                Results dataframe for analysis
                Raytable for no analysis
                Dict with links to analysis results for analysis + csv file
        '''
        if analysis is None:
            return self._api._run(self.id)

        if not isinstance(analysis, tdo_analyses.Analysis):
            raise Exception

        if configurations_csv_path != None:
            return self._api._run_batch_analyses(analysis, configurations_csv_path,[part.id for part in self.parts], parameters)

        results = self._api._run_analysis(analysis)
        return results


    def _download_file(self, url, file_path):
        """
        Downloads a ZIP file from a URL, extracts its contents, and saves the extracted files in the specified directory.
        """
        try:
            # Download the file
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for bad status codes

            # Create the directory for the destination folder if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save the ZIP file to the given file path
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            if v.DEBUG:
                print(f"Download URL: {url}")
                print(f"Downloaded ZIP file: {file_path}")

            # Check if the downloaded file is a ZIP file
            if zipfile.is_zipfile(file_path):
                # Extract the ZIP file contents to the directory
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    # Extract all the contents of the zip file to the destination folder
                    zip_ref.extractall(os.path.dirname(file_path))

                # Optionally, remove the ZIP file after extraction
                os.remove(file_path)

        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")
        except zipfile.BadZipFile as e:
            print(f"Failed to extract {file_path}: {e}")

    def download_analysis_files(self, data: Dict, setups_to_download_range: List[int] = None, target_dir="results"):
        """
        Downloads all analysis and maps_url files concurrently from the provided dictionary to a specified directory.

        Args:
            data (dict): The input dictionary containing file information.
            target_dir (str): The directory where files will be stored. Defaults to 'results' in the current directory.
            setups_to_download_range (list default None): List of length 2, to indicate which setup results you want to download. for example [0, 9] to download the results for the 10 first setups. If no range is entered function will download all setups files.

        Returns:
            Directory path where files are downloaded to, if you entered a path input it will return the same path, else the default path.
        """
        # Ensure the target directory exists
        os.makedirs(target_dir, exist_ok=True)
        download_tasks = []

        # Prepare download tasks
        setups = data.get('results', {}).get('data', {}).get('setups', [])
        setups.sort(key = lambda setup: setup['setup_num'])

        if setups_to_download_range is None:
            setups_to_download_range = [0, len(setups) - 1]

        setups = setups[setups_to_download_range[0]:setups_to_download_range[1] + 1] ## Use only wanted setups.

        for setup in setups:
            setup_num = setup.get('setup_num', 'unknown_setup')
            setup_dir = os.path.join(target_dir, setup_num)
            os.makedirs(setup_dir, exist_ok=True)

            # Add analysis files to download tasks
            for analysis in setup.get('analysis', []):
                file_name = analysis.get('name', 'unnamed_file')
                file_url = analysis.get('url')
                if file_url:
                    file_path = os.path.join(setup_dir, file_name)
                    download_tasks.append((file_url, file_path))

        # Add maps_url file to download tasks
        maps_url = data.get('maps_url')
        if maps_url:
            maps_file_name = "maps_url.json"
            maps_file_path = os.path.join(target_dir, maps_file_name)
            download_tasks.append((maps_url, maps_file_path))

        if v.DEBUG:
                print(f"Files to download: {len(download_tasks)}")

        # Download files concurrently
        start_time = time.time()
        max_threads = 5
        with ThreadPoolExecutor(max_threads) as executor:
            futures = [executor.submit(self._download_file, url, path) for url, path in download_tasks]
            for future in futures:
                future.result()  # Wait for all downloads to complete

        if(v.DEBUG):
            print(f"Time to download files: {time.time() - start_time}")

        return target_dir

    def proccess_analysis_files(self, analysis: tdo_analyses.Analysis, setup_dir_path, maps_json_path):
        try:
            with open(maps_json_path, 'r') as json_file:
                analysis._maps_json = json.load(json_file)
        except FileNotFoundError:
            print(f"Error: Path '{maps_json_path}' is invalid!! Please make sure you didnt delete/rename the file and gave the right path as input")
            raise FileNotFoundError

        return analysis._process_results(directory=setup_dir_path, should_delete=False)


    def delete_part(self, part: tdo_parts.Part):
        '''
        Deletes the part from the setup.
        '''
        self._api._delete_part(self.id, part.id)
        self._parts = [p for p in self.parts if p.id != part.id]

        if isinstance(part, tdo_parts.LightSource):
            for part in self:

                if part._surfaces is None:
                    continue

                for surface in part.surfaces:

                    if surface._analyses is None:
                        continue

                    for analysis in surface.analyses:
                        # if the laser id in the analysis rays attribute as key, delete the entry
                        if part.id in analysis.rays:
                            del analysis.rays[part.id]

        return

    def add_optics(self, db_id, **kwargs):
        if not all([key in v.AddParts.VALID_OPTICS_ARGUMENTS for key in kwargs.keys()]):
            raise Exception(f'Invalid arguments for optics. Valid arguments are {v.AddParts.VALID_OPTICS_ARGUMENTS}')
        return self._add_part(type_ = v.PartType.OPTICS, db_id = db_id, **kwargs)

    def add_light_source(self, **kwargs):
        if not all([key in v.AddParts.VALID_LIGHT_SOURCE_ARGUMENTS for key in kwargs.keys()]):
            raise Exception(f'Invalid arguments for light source. Valid arguments are {v.AddParts.VALID_LIGHT_SOURCE_ARGUMENTS}')
        return self._add_part(type_ = v.PartType.LIGHT_SOURCE, **kwargs)

    def add_detector(self, **kwargs):
        if not all([key in v.AddParts.VALID_DETECTOR_ARGUMENTS for key in kwargs.keys()]):
            raise Exception(f'Invalid arguments for detector. Valid arguments are {v.AddParts.VALID_DETECTOR_ARGUMENTS}')
        return self._add_part(type_ = v.PartType.DETECTOR, **kwargs)

    def _add_part(self, type_, db_id=None, **kwargs):


        part_id = self._api._add_part(setup_id=self.id,
                                      type_=type_,
                                      db_id=db_id
                                      )

        part = tdo_parts.create_part(_setup=self,
                                     id=part_id,
                                     type_ = type_
                                     )
        if self._parts is not None:
            self.parts.append(part)

        if kwargs != {}:
            try:
                part.change_config(**kwargs)
            except Exception as e:
                self.delete_part(part)
                raise e
        return part

    def _change_cs(self, part_id, lcs_id, rcs_id):
        return self._api._change_cs(setup_id = self.id, part_id = part_id, lcs_id = lcs_id, rcs_id = rcs_id)

    def _change_scattering(self, part_id, surface_id, scattering):
        return self._api._change_scattering(setup_id = self.id, part_id = part_id, surface_id = surface_id, scattering = scattering)

class Job:
    """
    Private.
    Contains information about a batch job.

    Attributes:
        _api (ThreedOptixAPI): The API pointer.
        _setup (Setup): The setup pointer.
        __base_url (str): The base URL for results.
        _prefix (str): The prefix of the results.
        __num_changes (int): Number of requested changes.
    """

    ##Magic methods and constructors
    def __init__(self):
        raise TypeError("Cannot directly create an instance of Job.")

    @classmethod
    def _from_json(cls, json_: dict, _api, _setup):
        """
        Creates the Job instance from the response JSON.

        Args:
            json (dict): The JSON response.

        Returns:
            Job: The created Job instance.
        """
        job = object.__new__(cls)
        job._url = json_['url'].replace('$', '')
        job._setup = _setup
        job._api = _api
        job._prefix = json_['simulation_file_prefix']
        job._num_changes = json_['number_of_changes']
        job.results = [tdo_analyses.RayTable(job._url.format(index = index), _setup) for index in range(job._num_changes)]
        return job

    def __str__(self):
        string = f'Job with {self._num_changes} changes and prefix {self._prefix} at {self._url}.\nBased on setup {self._setup.name} ({self._setup.id})'
        return string

    def __getitem__(self, index):
        """
        Gets the URL of the analysis at the specified location.

        Args:
            index: The index of the analysis.

        Returns:
            str: The URL of the analysis.
        """
        return self.results[index]

    def __len__(self) -> int:
        """
        Returns the number of changes.

        Returns:
            int: The number of changes.
        """
        return self._num_changes

    def __iter__(self):
        """
        Allows iterations over the URLs.

        Yields:
            str: The next URL.
        """
        return iter(self.results)

    ##Main 'Public' Methods
    def pull(self, index, filepath, **kwargs):
        """
        Gets the results of the analysis at the specified index.

        Args:
            index: The index of the analysis.

        Returns:
            dict: The results of the analysis.
        """
        result = self[index]
        result.to_csv(filepath, **kwargs)

    def status(self):
        """
        Returns a status report of the job.

        Returns:
            str: The status report.
        """
        raise NotImplementedError("This method is not implemented yet.")
