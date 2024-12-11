import threed_optix.analyses as an
import threed_optix.package_utils.math as mu
import threed_optix.package_utils.vars as v
import threed_optix.beams as bm
from typing import Union
import copy
import json
import re

class CoordinateSystem:
    def __init__(self):
        raise TypeError("Cannot directly create an instance of coordinate system.")

    @classmethod
    def _new(cls, id, _data, part):
        cs = object.__new__(cls)
        cs._data = _data
        cs.id = id
        cs._part = part
        return cs

    @property
    def pose(self):
        return self._data['ref_pose']['position'] + self._data['ref_pose']['rotation']

    @property
    def name(self):
        return self._data.get('name', '')

class WorldCS(CoordinateSystem):
    @classmethod
    def _new(cls):
        return super()._new(id = v.CoordinateSystems.WORLD, _data = v.CoordinateSystems.WORLD_DATA, part = None)

GLOBAL = WorldCS._new()

class Surface:
    def __init__(self):
        '''
        Private
        '''
        raise TypeError("Cannot directly create an instance of Surface.")

    @classmethod
    def _new(cls, _part, _data):
        '''
        Private
        '''
        if v.DEBUG:
            print(f'Creating general surface')
        surface = object.__new__(cls)
        surface.name = _data['name']
        surface.id = _data['id']
        surface._part = _part
        surface._analyses = None
        surface._data = None
        return surface

    @property
    def data(self):
        if self._data is None:
            self._data = self._part._get_surface(surface_id = self.id).get(self.id)
        return self._data

    @property
    def analyses(self):
        if self._analyses is None:
            analysis_data = self.data.get('analyses', {})
            self._analyses = [
                an.Analysis._new(surface = self,
                                 id=id,
                                 resolution=analysis['resolution'],
                                 num_rays=analysis.get('num_rays', {laser: v.Analyses.DEFAULT_NUM_RAYS for laser in self._part._setup.light_sources}),
                                 type = analysis['type'],
                                 name = analysis['name'],
                                 )
                for id, analysis in analysis_data.items()
                ]
        return self._analyses

    def __str__(self):
        '''
        Returns a string representation of the surface: name, id, part id, and part label.
        '''
        string = f'Surface with {len(self.analyses)} analyses:\n'
        for analysis in self.analyses:
            string += f'''{analysis.name} ({analysis.id})\n'''
        return string

class DetectorSurface(Surface):

    @classmethod
    def _new(cls, _part, _data):
        if v.DEBUG:
            print(f'Creating detector front')
        surface_obj = super()._new(_part, _data)
        surface_obj.__dict__ = surface_obj.__dict__
        return surface_obj

    def find_analysis(self, name: str, rays: Union[dict, int], resolution: Union[tuple, list], fast: bool = False):

        if isinstance(rays, int):
            rays = {ls: rays for ls in self._part._setup.light_sources}

        wanted_analysis = an.Analysis(surface = self, resolution = resolution, name = name, rays = rays, fast = fast)
        for analysis in self.analyses:
            if analysis == wanted_analysis:
                return analysis
        raise KeyError(f"Analysis with such parameters and name {name} not found in surface.")

    def add_analysis(self, analysis: an.Analysis, force = False):
        data = self._part._setup._api._add_analysis(analysis, force = force)
        analysis._added = True
        analysis.id = data['id']
        self.analyses.append(analysis)
        return

    def delete_analysis(self, analysis: Union[str, an.Analysis]):

        analysis_id = analysis
        if isinstance(analysis, an.Analysis):
            analysis_id = analysis.id

        if not any([(a.id == analysis_id) or (a is analysis) for a in self.analyses]):
            raise Exception(f"Analysis with id {analysis} not found in surface.")

        self._part._setup._api._delete_analysis(analysis_id = analysis_id,
                                              setup_id = self._part._setup.id,
                                              part_id = self._part.id,
                                              surface_id = self.id,
                                              )

        self._analyses = [a for a in self.analyses if a.id != analysis_id]

        return None

class OpticSurface(Surface):
    @classmethod
    def _new(cls, _part, _data):
        '''
        Private
        '''
        surface = object.__new__(cls)
        surface.name = _data['name']
        surface.id = _data['id']
        surface._part = _part
        surface._analyses = None
        surface._data = None
        return surface

    @property
    def scattering(self):
        return self.data['scattering'] if self.data['scattering']['enabled'] else False

    def disable_scattering(self):
        scattering = {
            "enabled": False
        }
        self._part._change_scattering(surface_id = self.id, scattering = scattering)
        self.data['scattering'] = scattering

    def change_scattering(self,
                          transmittance,
                          reflectance,
                          absorption,
                          split_ratio,
                          power_threshold,
                          scatter_model,
                          bsdf = None
                          ):

        parameters = {
            "transmittance": transmittance,
            "reflectance": reflectance,
            "absorption": absorption,
            "numberOfRays": split_ratio,
            "relativePowerThreshold": power_threshold,
            "scatterModel": scatter_model,
        }

        if bsdf is not None:
            parameters['bsdfParams'] = bsdf

        scattering_data = {
            "parameters": parameters
        }

        scattering = {
            "enabled": True,
            "scatteringData": scattering_data
        }
        self._part._change_scattering(surface_id = self.id, scattering = scattering)
        self.data['scattering'] = scattering
        return None

    def lambartian_scattering(self,
                          transmittance = v.Scattering.DEFAULT_TRANS,
                          reflectance = v.Scattering.DEFAULT_REF,
                          absorption = v.Scattering.DEFAULT_ABS,
                          split_ratio = v.Scattering.DEFAULT_NUMBER_OF,
                          power_threshold = v.Scattering.DEFAULT_RELATIVE_POWER,
                          ):

        scatter_model = v.ScatteringModels.LAMBERTIAN
        self.change_scattering(transmittance = transmittance,
                               reflectance = reflectance,
                               absorption = absorption,
                               split_ratio = split_ratio,
                               power_threshold = power_threshold,
                               scatter_model = scatter_model,
                               )

    def abg_scattering(self,
                          transmittance = v.Scattering.DEFAULT_TRANS,
                          reflectance = v.Scattering.DEFAULT_REF,
                          absorption = v.Scattering.DEFAULT_ABS,
                          split_ratio = v.Scattering.DEFAULT_NUMBER_OF,
                          power_threshold = v.Scattering.DEFAULT_RELATIVE_POWER,
                          a = v.Scattering.DEFAULT_A,
                          b  =v.Scattering.DEFAULT_B,
                          g = v.Scattering.DEFAULT_G
                          ):

        scatter_model = v.ScatteringModels.ABG
        bsdf = {
            "a": a,
            "b": b,
            "g": g
        }
        self.change_scattering(transmittance = transmittance,
                               reflectance = reflectance,
                               absorption = absorption,
                               split_ratio = split_ratio,
                               power_threshold = power_threshold,
                               scatter_model = scatter_model,
                               bsdf=bsdf
                               )

    def gaussian_scattering(self,
                          transmittance = v.Scattering.DEFAULT_TRANS,
                          reflectance = v.Scattering.DEFAULT_REF,
                          absorption = v.Scattering.DEFAULT_ABS,
                          split_ratio = v.Scattering.DEFAULT_NUMBER_OF,
                          power_threshold = v.Scattering.DEFAULT_RELATIVE_POWER,
                        sigma_x = v.Scattering.DEFAULT_SIGMAX,
                        sigma_y = v.Scattering.DEFAULT_SIGMAY,
                        azimuth_theta = v.Scattering.DEFAULT_AZIMUTH_THETA
                        ):

        scatter_model = v.ScatteringModels.GAUSSIAN
        bsdf = {
            "sigmaX": sigma_x,
            "sigmaY": sigma_y,
            "azimuth_theta": azimuth_theta
            }

        self.change_scattering(transmittance = transmittance,
                               reflectance = reflectance,
                               absorption = absorption,
                               split_ratio = split_ratio,
                               power_threshold = power_threshold,
                               scatter_model = scatter_model,
                               bsdf=bsdf
                               )

    def cos_scattering(self,
                        transmittance = v.Scattering.DEFAULT_TRANS,
                        reflectance = v.Scattering.DEFAULT_REF,
                        absorption = v.Scattering.DEFAULT_ABS,
                        split_ratio = v.Scattering.DEFAULT_NUMBER_OF,
                        power_threshold = v.Scattering.DEFAULT_RELATIVE_POWER,
                        n = v.Scattering.DEFAULT_N
                        ):

        scatter_model = v.ScatteringModels.COS_NTH
        bsdf = {
            "n": n
            }

        self.change_scattering(transmittance = transmittance,
                               reflectance = reflectance,
                               absorption = absorption,
                               split_ratio = split_ratio,
                               power_threshold = power_threshold,
                               scatter_model = scatter_model,
                               bsdf=bsdf
                               )

class Part:

    def __init__(self):
        '''
        Private
        '''
        raise TypeError("Cannot directly create an instance of Part.")

    @classmethod
    def _new(cls, _setup, id, _data):
        """
        Private
        Creates a new part from the opt_part at the specified index within the setup.

        Args:
            _setup (Setup): The setup object.
            _index (int): The index of the part within the setup.

        Returns:
            Part: The newly created Part object.
        """

        part = object.__new__(cls)
        part._setup = _setup
        part.id = id
        part._data = _data
        part._surfaces = None
        part._changes = {}
        part._errors = []
        part._cs = None
        part._rcs = None
        part._lcs = None
        part.backup_data = None
        part._user_backup = {v.BASE_BACKUP: copy.deepcopy(_data)}
        return part

    def __str__(self) -> str:
        '''
        Returns a string representation of the part: label, id, position, and rotation.
        '''
        string = f'''Part with {len(self.surfaces)} surfaces:\n'''
        for surface in self:
            string += f'''{surface.name} ({surface.id})\n'''
        return string

    def __iter__(self):
        """
        Allows iterating through the surfaces of the part.

        Yields:
            Surface: The next Surface object.
        """
        return iter(self.surfaces)

    def __getitem__(self, key: str):
        """
        Allows getting surfaces by surface id.

        Args:
            key: The id of the surface.

        Returns:
            surface (tdo.Surface): The requested Surface object.

        Raises:
            KeyError: If the surface with the specified id is not found in the part.
            TypeError: If the key is not str.
        """
        # if isinstance(key, int):
        #     return self.surfaces[key]
        if isinstance(key, str):
            for surface in self:
                if surface.id == key:
                    return surface
            raise KeyError(f"Surface with id {key} not found in the part.")
        raise TypeError(f"Invalid key type {type(key)}. Must be surface id.")

    @property
    def data(self):
        '''
        Data is a dictionary containing the part's detailed data.
        '''
        if self._data is None:
            self._data = self._setup._get_part(self.id).get(self.id)
        data = self._data
        return data

    @property
    def cs_data(self):
        return self.data['cs_data']


    @property
    def cs(self):
        if self._cs is None:
            self._cs = [CoordinateSystem._new(id=id, _data=data, part=self) for id, data in self.cs_data['coordinate_systems'].items()]
        return self._cs

    @property
    def lcs(self):
        if self._lcs is None:
            for cs in self.cs:
                if cs.id == self.cs_data['lcs']:
                    self._lcs = cs
        return self._lcs

    @property
    def rcs(self):
        if self._rcs is None:

            if self.cs_data.get('rcs') is None:
                self._rcs = (GLOBAL, None)

            else:
                for part in self._setup:
                    for cs in part.cs:
                        if cs.id == self.cs_data['rcs']:
                            self._rcs = (cs, cs._part)
                            break

                    if self._rcs is not None:
                        break
        return self._rcs

    def change_cs(self, lcs = None, rcs = None):
        if lcs is None and rcs is None:
            raise Exception("At least one of lcs or rcs must be specified.")
        if lcs is None:
            lcs = self.lcs
        if rcs is None:
            rcs = self.rcs[0]

        if isinstance(lcs, CoordinateSystem):
            if lcs not in self.cs:
                raise Exception(f"lcs with id {lcs} not found in part.")
            lcs_id = lcs.id
        elif isinstance(lcs, str):
            if lcs not in [cs.id for cs in self.cs]:
                raise Exception(f"lcs with id {lcs} not found in part.")
            lcs_id = lcs

        if v.DEBUG:
            print(f'RCS type and class: {type(rcs)} {rcs}')

        if isinstance(rcs, CoordinateSystem) or isinstance(rcs, WorldCS):

            ## Takes too much time, Eliav should do it (getting the cs data of each part)
            # if rcs not in [cs for part in self._setup for cs in part.cs] or isinstance(rcs, WorldCS):
            #     raise Exception(f"rcs with id {rcs} not found in setup.")

            rcs_id = rcs.id
        elif isinstance(rcs, str):

            ## Takes too much time, Eliav should do it (getting the cs data of each part)
            # if rcs not in [cs.id for part in self._setup for cs in part.cs] + [WORLD.id]:
            #     raise Exception(f"rcs with id {rcs} not found in setup.")
            rcs_id = rcs

        r = self._setup._change_cs(part_id = self.id, lcs_id = lcs_id, rcs_id = rcs_id)

        if r[0] is None:
            raise Exception(r[1])
        self._lcs = lcs
        self._rcs = (rcs, rcs._part)

        for p in self._setup:
            if p._data is not None:
                if p.rcs[1] == self:
                    if v.DEBUG:
                        print(f'Resetting part {p.id} data')
                    p._data = None
        self._data = None
        return None

    @property
    def material(self):
        '''
        Returns the part's material.
        '''
        return self._parameters['materialID']

    @property
    def surfaces(self):
        '''
        Returns a list of the part's surfaces as tdo.Surface objects.
        '''
        if v.DEBUG:
            print(f'Creating surfaces of part {self.id}')
        if self._surfaces is None:
            self._surfaces = [Surface._new(self, surface) for surface in self.data.get('surfaces', []) if 'name' in surface]
        return self._surfaces

    @surfaces.setter
    def surfaces(self, value):
        raise AttributeError("Cannot set surfaces directly.")

    @material.setter
    def material(self, value):
        raise AttributeError("Cannot set material directly.")

    @data.setter
    def data(self, value):
        raise AttributeError("Cannot set data directly.")

    def _get_surface(self, surface_id):
        return self._setup._get_surface(part_id = self.id, surface_id = surface_id)

    def get(self,
            name: str
            ):
        """
        Returns the surface object with the specified name.

        Args:
            name (str): The name of the surface.

        Returns:
            surface (tdo.Surface): The requested Surface object. If the surface is not found, returns None.
        """
        for surface in self:
            if surface.name == name:
                return surface
        raise KeyError(f"Surface with name {name} not found in the part.")

    def change_pose(self,
                    vector: Union[list, tuple],
                    radians: bool = False
                    ):

        self.backup_data = copy.deepcopy(self.data)
        self._change_pose_data(vector, radians)
        self.sync()

        return self.pose

    def _change_pose_data(self, vector, radians = False):
        '''
        Private.
        '''
        def verify(vector):
            errors = []
            if not isinstance(vector,list) or len(vector) != 6:
                error = f"Pose vector must be a list of length 6, representing position ([:3]) and rotation ([3:]). Got {len(vector)} instead."
                errors.append(error)
            return errors

        self._errors += verify(vector)

        if radians:
            vector[3:] = [mu.rad_to_deg(x) for x in vector[3:]]

        if not self._changes.get('pose'):
            self._changes['pose'] = {}

        self._changes['pose']['rotation'] = vector[3:]
        self._changes['pose']['position'] = vector[:3]

        return None

    @property
    def pose(self):
        '''
        Part's pose is a dictionary containing the part's pose object.
        '''
        return self.data['pose']['position'] + self.data['pose']['rotation']

    @pose.setter
    def pose(self, value):
        raise AttributeError("Cannot set pose directly. Use change_pose() method instead.")

    def change_label(self,
                     label: str):
        '''
        Changes the part's label.
        Args:
            label (str): The part's new label.

        Returns:
            new label (str)
        '''
        self.backup_data = copy.deepcopy(self.data)
        self._change_label_data(label)
        self.sync()
        return self.label

    def _change_label_data(self, label):
        def verify(label):
            return []

        self._errors += verify(label)
        label = str(label)

        self._changes['label'] = label
        return None

    @property
    def label(self):
        '''
        returns the part's label.
        '''
        return self.data['label']

    @label.setter
    def label(self, value):
        raise AttributeError("Cannot set label directly. Use change_label() method instead.")

    def change_config(self, pose: str = None, label: str = None):
        if not self.backup_data:
            self.backup_data = copy.deepcopy(self.data)
        if pose:
            self._change_pose_data(pose)
        if label:
            self._change_label_data(label)

        self.sync()
        return None

    def _change_data(self, data):
        self.backup_data = copy.deepcopy(self.data)
        self._changes = data
        self.sync()
        return self.data

    def sync(self):
        '''
        Private.
        '''
        if self._errors:
            errors = self._errors.copy()
            self.reset()
            raise Exception(v.argument_repair_message(errors))

        r = self._setup._update_part(self)
        if r[0] is None:
            self.reset()
            raise Exception(f"Error updating part: {r[1]}")

        self.backup_data = None
        self.update_data(a = self._data, b = self._changes)

        for part in self._setup:
            if part._data is not None and part != self:
                part._data = None
        return None

    def backup(self, name = v.BASE_BACKUP):
        '''
        Returns a copy of the part, used for backup purposes when changing part's properties.
        '''
        self._user_backup[name] = copy.deepcopy(self.data)
        return None

    def restore(self, name = v.BASE_BACKUP):
        chosen_backup = self._user_backup.get(name)

        if not chosen_backup:
            raise Exception(f"Backup with name {name} not found.")

        self._changes = chosen_backup
        r = self._setup._update_part(self)
        if not r[0]:
            raise Exception(r[1])
        self._data = chosen_backup

        return None

    def del_backup(self, names):
        if isinstance(names, str):
            names = [names]
        for name in names:
            if name in self._user_backup:
                del self._user_backup[name]
            else:
                raise Exception(f"Backup with name {name} not found.")

    def reset(self):
        self._errors = []
        self._data = self.backup_data
        self.backup_data = None
        self._changes = {}
        return None

    def update_data(self, a, b):
        result = a.copy()

        for key, value in b.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.update_data(result[key], value)
            else:
                result[key] = value

        self._data = result
        self._changes = {}

        return result

class Detector(Part):
    '''
    Private
    '''

    def __init__(self):
        raise TypeError("Cannot directly create an instance of Detector.")

    @classmethod
    def _new(cls, _setup, id, _data):
        detector = super()._new(_setup, id, _data)
        detector._setup = _setup
        detector.id = id
        detector._data = _data
        detector._surfaces = None
        detector._changes = {}
        detector._errors = []
        return detector

    def change_size(self, size: Union[list, tuple]):
        self.backup_data = copy.deepcopy(self.data)
        self._change_size_data(size)
        self.sync()
        return self.size

    def _change_size_data(self, size):

        def verify(size):
            errors = []

            if not isinstance(size, (list, tuple)):
                errors.append('Size must be a list or tuple')
            else:
                if not all([isinstance(x, (int, float)) for x in size]):
                    errors.append('Size must be a list of floats or ints.')
                if len(size) != 2:
                    errors.append('Size must be a list of length 2, representing half width and half height.')
                if not all([v.DETECTOR_SIZE_RANGE[0] <= x <= v.DETECTOR_SIZE_RANGE[1] for x in size]):
                    errors.append(f"Half width and half height must be between {v.DETECTOR_SIZE_RANGE[0]} and {v.DETECTOR_SIZE_RANGE[1]}.")


            return errors

        self._errors += verify(size)

        if not self._changes.get('detector_data'):
            self._changes['detector_data'] = {}

        self._changes['detector_data']['size'] = {'half_width': size[0], 'half_height': size[1]}
        return None

    @property
    def surfaces(self):
        '''
        Returns a list of the part's surfaces as tdo.Surface objects.
        '''
        if v.DEBUG:
            print(f'Getting surfaces for detector {self.id}')

        if self._surfaces is None:
            self._surfaces = [
                create_detector_surface(_part = self, _data = surface_data)
                for surface_data in self.data.get('surfaces', [])
                if 'name' in surface_data
                ]
        return self._surfaces


    @property
    def size(self):
        return tuple(self.data['detector_data']['size'].values())

    @size.setter
    def size(self, value):
        raise AttributeError("Cannot set size directly. Use change_size() method instead.")

    def change_opacity(self, opacity: float):
        self.backup_data = copy.deepcopy(self.data)
        self._change_opacity_data(opacity)
        self.sync()
        return self.opacity

    def _change_opacity_data(self, opacity):

        def verify(opacity):
            errors = []
            if not isinstance(opacity, (int, float)):
                errors.append("Opacity must be an int or float, representing opacity.")

            elif opacity < v.DETECTOR_OPACITY_RANGE[0] or opacity > v.DETECTOR_OPACITY_RANGE[1]:
                errors.append("Opacity must be between 0 and 1, representing opacity.")

            return errors

        self._errors += verify(opacity)

        if not self._changes.get('detector_data'):
            self._changes['detector_data'] = {}
        if not self._changes['detector_data'].get('appearance'):
            self._changes['detector_data']['appearance'] = {}
        self._changes['detector_data']['appearance']['opacity'] = opacity
        return None

    @property
    def opacity(self):
        return self.data['detector_data']['appearance']['opacity']

    @opacity.setter
    def opacity(self, value):
        raise AttributeError("Cannot set opacity directly. Use change_opacity() method instead.")

    def change_config(self,
                      pose: str = None,
                      label: str = None,
                      size: Union[list, tuple] = None,
                      opacity: float = None
                      ):
        self.backup_data = copy.deepcopy(self.data)
        if size:
            self._change_size_data(size)
        if opacity:
            self._change_opacity_data(opacity)
        super().change_config(pose, label)
        return None

class LightSource(Part):
    '''
    Private
    '''

    def __init__(self):
        raise TypeError("Cannot directly create an instance of LightSource.")

    @classmethod
    def _new(cls, _setup, id, _data):
        light_source = super()._new(_setup, id, _data)
        light_source._setup = _setup
        light_source.id = id
        light_source._data = _data
        # light_source.beam = bm._create_beam(_part = light_source, _data = _data['light_source'])
        # light_source._data['light_source'] = light_source.beam
        light_source._surfaces = None
        light_source._changes = {}
        light_source._errors = []
        return light_source

    # Wavelengths
    @property
    def wavelengths(self):
        wavelengths = {}
        for wl_dict in self.data['light_source']['wavelengths_data']:
            wavelengths[wl_dict['wavelength']] = wl_dict['weight']

        return wavelengths

    @wavelengths.setter
    def wavelengths(self, value):
        raise AttributeError("Cannot set wavelengths directly. Use change_wavelengths() or add_wavelengths() method instead.")

    def change_wavelengths(self, wavelengths: Union[dict, list]):
        self.backup_data = copy.deepcopy(self.data)
        self._change_wavelengths_data(wavelengths)
        self.sync()
        return self.wavelengths

    def add_wavelengths(self, wavelengths: Union[dict, list]):
        self.backup_data = copy.deepcopy(self.data)
        self._change_wavelengths_data(wavelengths, add = True)
        self.sync()
        return self.wavelengths

    def _change_wavelengths_data(self, wavelengths, add = False):
        def verify(wavelengths):
            errors = []
            if not isinstance(wavelengths, (list, tuple, dict)):
                errors.append('Wavelengths must be a list, tuple or dictionary.')

            elif isinstance(wavelengths, (list, tuple)):
                if not all([isinstance(x, (int, float)) for x in wavelengths]):
                    errors.append('If wavelengths are list or tuple, all wavelengths must be ints or floats, representing wavelengths in nm.')
                elif not all([v.WAVELENGTH_RANGE[0] <= x <= v.WAVELENGTH_RANGE[1] for x in wavelengths]):
                    errors.append(f'If wavelengths are list or tuple, all wavelengths must be between {v.WAVELENGTH_RANGE[0]} and {v.WAVELENGTH_RANGE[1]}.')

            elif isinstance(wavelengths, dict):
                if not all([isinstance(x, (int, float)) for x in wavelengths.keys()]) and all([isinstance(x, (int, float)) for x in wavelengths.values()]):
                    errors.append('If wavelengths are a dictionary, all keys and values must be ints or floats, representing wavelengths in nm.')
                else:
                    if not all([v.WEIGHTS_RANGE[0] <= x <= v.WEIGHTS_RANGE[1] for x in wavelengths.values()]):
                        errors.append('If wavelengths are a dictionary, all weight values must be between 0 and 1, representing the weight of each wavelength.')
                    if not all([v.WAVELENGTH_RANGE[0] <= x <= v.WAVELENGTH_RANGE[1] for x in wavelengths.keys()]):
                        errors.append(f'If wavelengths are a dictionary, all wavelength values must be between {v.WAVELENGTH_RANGE[0]} and {v.WAVELENGTH_RANGE[1]}.')

            return errors


        self._errors += verify(wavelengths)

        wavelengths = self._wavelengths_to_dict(wavelengths)

        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        if not self._changes['light_source'].get('wavelengths_data'):
            self._changes['light_source']['wavelengths_data'] = []

        if add:
            self._changes['light_source']['wavelengths_data'] = self.data['light_source']['wavelengths_data'] + wavelengths
        else:
            self._changes['light_source']['wavelengths_data'] = wavelengths
        return None

    def _wavelengths_to_dict(self, wavelengths):
        if isinstance(wavelengths, list):
            return [{"wavelength": wavelength, 'weight': 1} for wavelength in wavelengths]
        elif isinstance(wavelengths, dict):
            return [{"wavelength": wavelength, 'weight': weight} for wavelength, weight in wavelengths.items()]
        else:
            raise TypeError("Wavelengths must be a list of equal weight wavelengths or a dictionary.")

    # Power
    def change_power(self, new_power: float):
        self.backup_data = copy.deepcopy(self.data)
        self._change_power_data(new_power)
        self.sync()
        return self.power

    def _change_power_data(self, new_power):

        def verify(new_power):
            errors = []
            if not isinstance(new_power, (int, float)):
                errors.append('Power must be an int or float, representing power in Watts.')
            elif new_power < v.POWER_RANGE[0] or new_power > v.POWER_RANGE[1]:
                errors.append(f'Power must be between {v.POWER_RANGE[0]} and {v.POWER_RANGE[1]}')
            return errors

        self._errors += verify(new_power)

        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}

        self._changes['light_source']['power'] = new_power
        return None

    @property
    def power(self):
        return self.data['light_source']['power']

    @power.setter
    def power(self, value):
        raise AttributeError("Cannot set power directly. Use change_power() method instead.")

    def turn_on(self):
        if self.turned_on:
            return
        self.backup_data = copy.deepcopy(self.data)
        self._turn_on_data()
        self.sync()
        return

    def turn_off(self):
        if not self.turned_on:
            return

        self.backup_data = copy.deepcopy(self.data)
        self._turn_off_data()
        self.sync()
        return

    def _turn_on_data(self):
        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        self._changes['light_source']['isActive'] = True
        return None

    def _turn_off_data(self):
        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        self._changes['light_source']['isActive'] = False
        return None

    @property
    def turned_on(self):
        return self.data['light_source']['isActive']

    @turned_on.setter
    def turned_on(self, value):
        raise AttributeError("Cannot set turned_on directly. Use turn_on(), turn_off() methods instead.")

    # Rays direction
    def change_rays_direction(self, azimuth_z, theta = None, phi = None):
        self.backup_data = copy.deepcopy(self.data)
        self._change_rays_direction_data(azimuth_z=azimuth_z, theta=theta, phi=phi)
        self.sync()
        return self.rays_direction

    def _change_rays_direction_data(self, azimuth_z, theta, phi):

        def verify(azimuth_z, theta, phi):

            errors = []

            if azimuth_z is None:
                errors.append('Azimuth_z must be specified.')

            if theta is not None:
                if not isinstance(theta, (int, float)):
                    errors.append('Theta must be an int or float, representing theta in degrees.')
                elif theta < v.THETA_RANGE[0] or theta > v.THETA_RANGE[1]:
                    errors.append(f'Theta must be between {v.THETA_RANGE[0]} and {v.THETA_RANGE[1]}')

            if phi is not None:
                if not isinstance(phi, (int, float)):
                    errors.append('Phi must be an int or float, representing phi in degrees.')
                elif phi < v.PHI_RANGE[0] or phi > v.PHI_RANGE[1]:
                    errors.append(f'Phi must be between {v.PHI_RANGE[0]} and {v.PHI_RANGE[1]}')

            return errors

        self._errors += verify(azimuth_z, theta, phi)

        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        if not self._changes['light_source'].get('angular_information'):
            self._changes['light_source']['angular_information'] = {}

        self._changes['light_source']['angular_information'] =  {"azimuth_z": azimuth_z}
        if theta:
            self._changes['light_source']['angular_information']['theta'] = theta
        if phi:
            self._changes['light_source']['angular_information']['phi'] = phi

        return None

    @property
    def rays_direction(self):
        return self.data['light_source']['angular_information']

    @rays_direction.setter
    def rays_direction(self, value):
        raise AttributeError("Cannot set rays_direction directly. Use change_rays_direction() method instead.")

    # Count
    def change_vis_count(self, new_vis_count: int):
        self.backup_data = copy.deepcopy(self.data)
        self._change_vis_count_data(new_vis_count)
        self.sync()
        return self.data['light_source']['num_of_rays']

    def _change_vis_count_data(self, new_vis_count):

        def verify(new_vis_count):
            errors = []
            if not isinstance(new_vis_count, int):
                errors.append('Vis count must be an int, representing the number of visualization rays.')
            elif new_vis_count < v.LOWER_VIS_COUNT_LIMIT or new_vis_count > v.UPPER_VIS_COUNT_LIMIT:
                errors.append(f'Visualization rays count must be between {v.LOWER_VIS_COUNT_LIMIT} and {v.UPPER_VIS_COUNT_LIMIT}')
            return errors

        self._errors += verify(new_vis_count)

        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        if not self._changes['light_source'].get('num_of_rays'):
            self._changes['light_source']['num_of_rays'] = {}

        self._changes['light_source']['num_of_rays']['count'] = new_vis_count
        return None

    @property
    def vis_count(self):
        return self.data['light_source']['num_of_rays']['count']

    @vis_count.setter
    def vis_count(self, value):
        raise AttributeError("Cannot set vis_count directly. Use change_vis_count() method instead.")

    def change_vis_count_type(self, count_type: str):
        self.backup_data = copy.deepcopy(self.data)
        self._change_vis_count_type_data(count_type)
        self.sync()
        return self.data['light_source']['num_of_rays']

    def _change_vis_count_type_data(self, count_type):
        def verify(count_type):
            errors = []
            if count_type not in v.COUNT_TYPES:
                errors.append(f"Count type must be one of {v.COUNT_TYPES}.")
            return errors

        self._errors += verify(count_type)

        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        if not self._changes['light_source'].get('num_of_rays'):
            self._changes['light_source']['num_of_rays'] = {}

        self._changes['light_source']['num_of_rays']['count_type'] = count_type
        return None

    @property
    def vis_count_type(self):
        return self.data['light_source']['num_of_rays']['count_type']

    @vis_count_type.setter
    def vis_count_type(self, value):
        raise AttributeError("Cannot set count_type directly. Use change_count_type() method instead.")

    def change_count_type(self, count_type: str):
        raise AttributeError("change_count_type is deprecated. Use change_vis_count_type instead.")

    @property
    def count_type(self):
        raise AttributeError("count_type is deprecated. Use vis_count_type instead.")


    # Appearance
    def change_opacity(self, opacity: float):
        self.backup_data = copy.deepcopy(self.data)
        self._change_opacity_data(opacity)
        self.sync()
        return self.data['light_source']['appearance_data']['opacity']

    def _change_opacity_data(self, opacity):

        def verify(opacity):
            errors = []
            if not isinstance(opacity, (int, float)):
                errors.append('Opacity must be an int or float, representing opacity.')
            elif opacity < v.LIGHT_SOURCE_OPACITY_RANGE[0] or opacity > v.LIGHT_SOURCE_OPACITY_RANGE[1]:
                errors.append('Opacity must be between 0 and 1, representing opacity.')
            return errors

        self._errors += verify(opacity)

        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        if not self._changes['light_source'].get('appearance_data'):
            self._changes['light_source']['appearance_data'] = {}

        self._changes['light_source']['appearance_data']['opacity'] = opacity
        return None

    @property
    def opacity(self):
        return self.data['light_source']['appearance_data']['opacity']

    @opacity.setter
    def opacity(self, value):
        raise AttributeError("Cannot set opacity directly. Use change_opacity() method instead.")

    def change_color(self, color: str):
        self.backup_data = copy.deepcopy(self.data)
        self._change_color_data(color)
        self.sync()
        return self.data['light_source']['appearance_data']['color']

    def _change_color_data(self, color):

        def verify(color):
            errors = []
            if not bool(re.match(v.HEX_COLOR_RE, color)):
                errors.append('Color must be a hex color string.')
            return errors

        self._errors += verify(color)

        color = int(color.replace('#', ''), 16)

        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        if not self._changes['light_source'].get('appearance_data'):
            self._changes['light_source']['appearance_data'] = {}

        self._changes['light_source']['appearance_data']['color'] = color
        return None

    @property
    def color(self):
        color_int = self.data['light_source']['appearance_data']['color']
        hex_color = format(color_int, 'x')
        hex_color = hex_color.zfill(6)
        hex_color = '#' + hex_color
        return hex_color


    @color.setter
    def color(self, value):
        raise AttributeError("Cannot set color directly. Use change_color() method instead.")

    # Beam
    def to_gaussian(self, waist_x: float, waist_y: float, waist_position_x: float, waist_position_y: float):
        self.backup_data = copy.deepcopy(self.data)
        self._change_to_gaussian(waist_x, waist_y, waist_position_x, waist_position_y)
        self.sync()
        return self.data['light_source']['gaussian_beam']

    def _change_to_gaussian(self, waist_x, waist_y, waist_position_x, waist_position_y):

        def verify(waist_x, waist_y, waist_position_x, waist_position_y):
            errors = []
            if not all([isinstance(x, (int, float)) for x in [waist_x, waist_y, waist_position_x, waist_position_y]]):
                errors.append('All values must be ints or floats.')
            return errors

        self._errors += verify(waist_x, waist_y, waist_position_x, waist_position_y)

        if self.gaussian_beam:
            del self._data['light_source']['gaussian_beam']
        if self.plane_wave:
            del self._data['light_source']['spatial_information']['plane_wave_data']
        if self.point_source:
            del self._data['light_source']['spatial_information']['point_source_data']


        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        if not self._changes['light_source'].get('gaussian_beam'):
            self._changes['light_source']['gaussian_beam'] = {}

        self._changes['light_source']['source_type'] = v.GAUSSIAN_BEAM
        self._changes['light_source']['gaussian_beam'] = {
            "waist_x": waist_x,
            "waist_y": waist_y,
            "waist_position_x": waist_position_x,
            "waist_position_y": waist_position_y
        }

        return None

    @property
    def gaussian_beam(self):
        if self.data['light_source']['source_type'] == v.GAUSSIAN_BEAM:
            return self.data['light_source']['gaussian_beam']
        else:
            return None

    @gaussian_beam.setter
    def gaussian_beam(self, value):
        raise AttributeError("Cannot set gaussian_beam directly. Use to_gaussian() method instead.")

    def to_point_source(self, density_pattern: str, point_source_data: dict, model_radius: float = None):
        self.backup_data = copy.deepcopy(self.data)
        self._change_to_point_source(density_pattern, point_source_data, model_radius)
        self.sync()
        return self.data['light_source']['spatial_information']

    def _change_to_point_source(self, density_pattern, point_source_data, model_radius =None):

        def verify(density_pattern, model_radius, data):
            errors = []
            if model_radius:
                if model_radius < v.MODEL_RADIUS_RANGE[0] or model_radius > v.MODEL_RADIUS_RANGE[1]:
                    errors.append(f"Model radius must be between {v.MODEL_RADIUS_RANGE[0]} and {v.MODEL_RADIUS_RANGE[1]}")
                if density_pattern not in v.DENSITY_PATTERNS:
                    errors.append(f"Density pattern must be one of {v.DENSITY_PATTERNS}")

            if not isinstance(data, dict):
                errors.append("Point source data must be a dictionary.")
            else:
                type_ = data.get('type')
                if not type_:
                    errors.append("Point source data must have a type entry, representing the divergance type.")
                elif type_ not in v.POINT_SOURCE_TYPES:
                    errors.append(f"Point source type must be one of {v.POINT_SOURCE_TYPES}")

                elif type_ == v.HALF_CONE_ANGLE or type_ == v.HALF_WIDTH_RECT:
                    angle_x = data.get('angle_x')
                    angle_y = data.get('angle_y')

                    if not angle_x:
                        errors.append("Point source data must have an angle_x entry, representing the X-axis opening angle")
                    elif not isinstance(angle_x, (int, float)):
                        errors.append("Angle_x must be an int or float, representing theX-axis opening angle")
                    elif not v.POINT_SOURCE_ANGLE_RANGE[0] <= angle_x <= v.POINT_SOURCE_ANGLE_RANGE[1]:
                        errors.append(f"Angle_x must be between {v.POINT_SOURCE_ANGLE_RANGE[0]} and {v.POINT_SOURCE_ANGLE_RANGE[1]}")

                    if not angle_y:
                        errors.append("Point source data must have an angle_y entry, representing the Y-axis opening angle")
                    elif not isinstance(angle_y, (int, float)):
                        errors.append("Angle_y must be an int or float, representing the Y-axis opening angle")
                    elif not v.POINT_SOURCE_ANGLE_RANGE[0] <= angle_y <= v.POINT_SOURCE_ANGLE_RANGE[1]:
                        errors.append(f"Angle_y must be between {v.POINT_SOURCE_ANGLE_RANGE[0]} and {v.POINT_SOURCE_ANGLE_RANGE[1]}")

                elif type_ == v.HALF_WIDTH_AT_Z:
                    dist_z = data.get('dist_z') #distance to calculate the half_width_x_at_dist and half_width_y_at_dist for
                    half_width_x_at_dist = data.get('half_width_x_at_dist') # the half width on x-axis at dist_z
                    half_width_y_at_dist = data.get('half_width_y_at_dist') # the half width on y-axis at dist_z

                    if not dist_z:
                        errors.append("Point source data must have a dist_z entry, representing the distance to calculate the half_width_x_at_dist and half_width_y_at_dist for")
                    elif not isinstance(dist_z, (int, float)):
                        errors.append("Dist_z must be an int or float, representing the distance to calculate the half_width_x_at_dist and half_width_y_at_dist for")
                    elif not v.POINT_SOURCE_DIST_Z_RANGE[0] <= dist_z <= v.POINT_SOURCE_DIST_Z_RANGE[1]:
                        errors.append(f"Dist_z must be between {v.POINT_SOURCE_DIST_Z_RANGE[0]} and {v.POINT_SOURCE_DIST_Z_RANGE[1]}")

                    if not half_width_x_at_dist:
                        errors.append("Point source data must have a half_width_x_at_dist entry, representing the half width on x-axis at dist_z")
                    elif not isinstance(half_width_x_at_dist, (int, float)):
                        errors.append("Half_width_x_at_dist must be an int or float, representing the half width on x-axis at dist_z")
                    elif not v.POINT_SOURCE_DIST_Z_AT_RANGE[0] <= half_width_x_at_dist <= v.POINT_SOURCE_DIST_Z_AT_RANGE[1]:
                        errors.append(f"Half_width_x_at_dist must be between {v.POINT_SOURCE_DIST_Z_AT_RANGE[0]} and {v.POINT_SOURCE_DIST_Z_AT_RANGE[1]}")

                    if not half_width_y_at_dist:
                        errors.append("Point source data must have a half_width_y_at_dist entry, representing the half width on y-axis at dist_z")
                    elif not isinstance(half_width_y_at_dist, (int, float)):
                        errors.append("Half_width_y_at_dist must be an int or float, representing the half width on y-axis at dist_z")
                    elif not v.POINT_SOURCE_DIST_Z_AT_RANGE[0] <= half_width_y_at_dist <= v.POINT_SOURCE_DIST_Z_AT_RANGE[1]:
                        errors.append(f"Half_width_y_at_dist must be between {v.POINT_SOURCE_DIST_Z_AT_RANGE[0]} and {v.POINT_SOURCE_DIST_Z_AT_RANGE[1]}")

            return errors

        self._errors += verify(density_pattern, model_radius, point_source_data)

        if self.gaussian_beam:
            del self._data['light_source']['gaussian_beam']
        if self.plane_wave:
            del self._data['light_source']['spatial_information']['plane_wave_data']
        if self.point_source:
            del self._data['light_source']['spatial_information']['point_source_data']


        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        if not self._changes['light_source'].get('spatial_information'):
            self._changes['light_source']['spatial_information'] = {}
        if not self._changes['light_source'].get('appearance_data'):
            self._changes['light_source']['appearance_data'] = {}

        self._changes['light_source']['source_type'] = v.POINT_SOURCE
        self._changes['light_source']['spatial_information'] = {
            "density_pattern": density_pattern,
            "point_source_data": point_source_data
        }

        if model_radius:
            self._changes['light_source']['appearance_data']['model_radius'] = model_radius

        return None

    @property
    def point_source(self):
        if self.data['light_source']['source_type'] == v.POINT_SOURCE:
            point_source = copy.deepcopy(self.data['light_source']['spatial_information'])
            model_radius = self.data['light_source']['appearance_data'].get('model_radius')
            if model_radius:
                point_source['model_radius'] = model_radius
            return point_source
        else:
            return None

    @point_source.setter
    def point_source(self, value):
        raise AttributeError("Cannot set point_source directly. Use to_point_source() method instead.")

    def to_plane_wave(self, density_pattern: str, plane_wave_data: dict):
        self.backup_data = copy.deepcopy(self.data)
        self._change_to_plane_wave(density_pattern, plane_wave_data)
        self.sync()

        return self.data['light_source']['spatial_information']

    def _change_to_plane_wave(self, density_pattern, plane_wave_data):

        def verify(density_pattern, plane_wave_data):
            errors = []

            if density_pattern not in v.DENSITY_PATTERNS:
                errors.append(f"Density pattern must be one of {v.DENSITY_PATTERNS}")

            if not isinstance(plane_wave_data, dict):
                errors.append("Plane wave data must be a dictionary.")
            else:
                source_shape = plane_wave_data.get('source_shape') #shape of the rays shooting by the plane wave
                if source_shape not in v.PLANE_WAVE_TYPES:
                    errors.append(f"Source shape must be one of {v.PLANE_WAVE_TYPES}")
                if source_shape == v.RECTANGULAR:
                    width = plane_wave_data.get('width') #Total width of the shape that rays shooting by plane wave source
                    height = plane_wave_data.get('height') #Total height of the shape that rays shooting by plane wave source

                    if not width:
                        errors.append("Plane wave data must have a width entry, representing the total width of the shape that rays shooting by plane wave source")
                    elif not isinstance(width, (int, float)):
                        errors.append("Width must be an int or float, representing the total width of the shape that rays shooting by plane wave source")
                    elif not v.PLANE_WAVE_WIDTH_RANGE[0] <= width <= v.PLANE_WAVE_WIDTH_RANGE[1]:
                        errors.append(f"Width must be between {v.PLANE_WAVE_WIDTH_RANGE[0]} and {v.PLANE_WAVE_WIDTH_RANGE[1]}")

                    if not height:
                        errors.append("Plane wave data must have a height entry, representing the total height of the shape that rays shooting by plane wave source")
                    elif not isinstance(height, (int, float)):
                        errors.append("Height must be an int or float, representing the total height of the shape that rays shooting by plane wave source")
                    elif not v.PLANE_WAVE_HEIGHT_RANGE[0] <= height <= v.PLANE_WAVE_HEIGHT_RANGE[1]:
                        errors.append(f"Height must be between {v.PLANE_WAVE_HEIGHT_RANGE[0]} and {v.PLANE_WAVE_HEIGHT_RANGE[1]}")

                elif source_shape == v.CIRCULAR:
                    radius = plane_wave_data.get('radius')
                    if not radius:
                        errors.append("Plane wave data must have a radius entry, representing the radius of the circle that rays shooting by plane wave source")
                    elif not isinstance(radius, (int, float)):
                        errors.append("Radius must be an int or float, representing the radius of the circle that rays shooting by plane wave source")
                    elif not v.PLANE_WAVE_RADIUS_RANGE[0] <= radius <= v.PLANE_WAVE_RADIUS_RANGE[1]:
                        errors.append(f"Radius must be between {v.PLANE_WAVE_RADIUS_RANGE[0]} and {v.PLANE_WAVE_RADIUS_RANGE[1]}")

                elif source_shape == v.ELLIPTICAL:
                    radius_x = plane_wave_data.get('radius_x')
                    radius_y = plane_wave_data.get('radius_y')
                    if not radius_x:
                        errors.append("Plane wave data must have a radius_x entry, representing the radius of the ellipse on x-axis that rays shooting by plane wave source")
                    elif not isinstance(radius_x, (int, float)):
                        errors.append("Radius_x must be an int or float, representing the radius of the ellipse on x-axis that rays shooting by plane wave source")
                    elif not v.PLANE_WAVE_RADIUS_RANGE[0] <= radius_x <= v.PLANE_WAVE_RADIUS_RANGE[1]:
                        errors.append(f"Radius_x must be between {v.PLANE_WAVE_RADIUS_RANGE[0]} and {v.PLANE_WAVE_RADIUS_RANGE[1]}")

                    if not radius_y:
                        errors.append("Plane wave data must have a radius_y entry, representing the radius of the ellipse on y-axis that rays shooting by plane wave source")
                    elif not isinstance(radius_y, (int, float)):
                        errors.append("Radius_y must be an int or float, representing the radius of the ellipse on y-axis that rays shooting by plane wave source")
                    elif not v.PLANE_WAVE_RADIUS_RANGE[0] <= radius_y <= v.PLANE_WAVE_RADIUS_RANGE[1]:
                        errors.append(f"Radius_y must be between {v.PLANE_WAVE_RADIUS_RANGE[0]} and {v.PLANE_WAVE_RADIUS_RANGE[1]}")

            return errors

        self._errors += verify(density_pattern, plane_wave_data)

        if self.gaussian_beam:
            del self._data['light_source']['gaussian_beam']
        if self.plane_wave:
            del self._data['light_source']['spatial_information']['plane_wave_data']
        if self.point_source:
            del self._data['light_source']['spatial_information']['point_source_data']

        if not self._changes.get('light_source'):
            self._changes['light_source'] = {}
        if not self._changes['light_source'].get('spatial_information'):
            self._changes['light_source']['spatial_information'] = {}


        self._changes['light_source']['source_type'] = v.PLANE_WAVE
        self._changes['light_source']['spatial_information'] = {
            "density_pattern": density_pattern,
            "plane_wave_data": plane_wave_data
        }

        return None

    @property
    def plane_wave(self):
        if self.data['light_source']['source_type'] == v.PLANE_WAVE:
            return self.data['light_source']['spatial_information']
        else:
            return None

    @plane_wave.setter
    def plane_wave(self, value):
        raise AttributeError("Cannot set plane_wave directly. Use to_plane_wave() method instead.")

    @property
    def source_type(self):
        return self.data['light_source']['source_type']

    @source_type.setter
    def source_type(self, value):
        raise AttributeError("Cannot set source_type directly. Use to_plane_wave(), to_gaussian(), or to_point_source() methods instead.")


    def change_config(self,
                      pose: str=None,
                      label: str=None,
                      wavelengths: Union[dict,list] = None,
                      add_wavelengths: Union[dict, list] = None,
                      power: float = None,
                      vis_count: int = None,
                      vis_count_type: str = None,
                      rays_direction: dict = None,
                      opacity: float = None,
                      color: str = None,
                      gaussian_beam: dict = None,
                      point_source: dict = None,
                      plane_wave: dict = None
                      ):

        if wavelengths and add_wavelengths:
            raise ValueError("Only one of wavelengths, add_wavelengths can be defined.")

        if sum([gaussian_beam is not None, point_source is not None, plane_wave is not None]) > 1:
            raise ValueError("Only one of gaussian_beam, point_source, plane_wave can be defined.")

        self.backup_data = copy.deepcopy(self.data)

        if wavelengths:
            self._change_wavelengths_data(wavelengths)
        if add_wavelengths:
            self._change_wavelengths_data(add_wavelengths, add = True)
        if power:
            self._change_power_data(power)
        if vis_count:
            self._change_vis_count_data(vis_count)
        if vis_count_type:
            self._change_vis_count_type_data(vis_count_type)
        if opacity:
            self._change_opacity_data(opacity)
        if color:
            self._change_color_data(color)
        if rays_direction:
            self._change_rays_direction_data(**rays_direction)
        if gaussian_beam:
            self._change_to_gaussian(**gaussian_beam)
        if point_source:
            self._change_to_point_source(**point_source)
        if plane_wave:
            self._change_to_plane_wave(**plane_wave)

        super().change_config(pose, label)
        return None

# create a class called CoordinateSystemPart that's exactly like Part but with a different class name
# You should do that with inheritance and not by copying the code
class CoordinateSystemPart(Part):

    def __init__(self):
        raise TypeError("Cannot directly create an instance of CoordinateSystemPart.")

    @classmethod
    def _new(cls, _setup, id, _data):
        coordinate_system = super(cls, cls)._new(_setup, id, _data)
        return coordinate_system

class Optics(Part):
    def __init__(self):
        raise TypeError("Cannot directly create an instance of Optics.")

    @classmethod
    def _new(cls, _setup, id, _data):
        optics = super()._new(_setup, id, _data)
        optics._setup = _setup
        optics.id = id
        optics._data = _data
        optics._surfaces = None
        optics._optical_data = None
        optics._changes = {}
        optics._errors = []
        return optics

    @property
    def surfaces(self):
        if self._surfaces is None:
            self._surfaces = [OpticSurface._new(self, surface)
                              for surface in self.data.get('surfaces', [])
                              if 'name' in surface
                              ]
        return self._surfaces


    @property
    def db_id(self):
        return self.data.get('number_id', None)

    @property
    def optical_data(self):
        if self._optical_data is None:
            self._optical_data = self._setup._api.optics_data(self.db_id)
        return self._optical_data

    @property
    def physical_data(self):
        return self._parameters.get('physical_data', {})

    @property
    def db_name(self):
        return self.optical_data['name']

    @property
    def _parameters(self):
        return self.optical_data['parameters']

    @property
    def geometry(self):
        return self._parameters['geometry']

    @property
    def brand(self):
        return self._parameters['info']['brand']

    @property
    def base_shape(self):
        return self._parameters['baseShape']

    @property
    def shape(self):
        return self._parameters['shape']

    def _change_scattering(self, surface_id, scattering):
        return self._setup._change_scattering(surface_id=surface_id, scattering=scattering, part_id = self.id)

class CAD(Part):

    def __init__(self):
        raise TypeError("Cannot directly create an instance of CoordinateSystemPart.")

    @classmethod
    def _new(cls, _setup, id, _data):
        cad = super(cls, cls)._new(_setup, id, _data)
        return cad

class BlackBox(Part):

    def __init__(self):
        raise TypeError("Cannot directly create an instance of CoordinateSystemPart.")

    @classmethod
    def _new(cls, _setup, id, _data):
        BlackBox = super(cls, cls)._new(_setup, id, _data)
        return BlackBox

class Group(Part):

    def __init__(self):
        raise TypeError("Cannot directly create an instance of CoordinateSystemPart.")

    @classmethod
    def _new(cls, _setup, id, _data):
        group = super(cls, cls)._new(_setup, id, _data)
        return group

class ParaxialLens(Part):

    def __init__(self):
        raise TypeError("Cannot directly create an instance of CoordinateSystemPart.")

    @classmethod
    def _new(cls, _setup, id, _data):
        ParaxialLens = super(cls, cls)._new(_setup, id, _data)
        return ParaxialLens


def create_detector_surface(_part, _data):
    if v.DEBUG:
        print(f"Creating detector surface with data: {_data}")

    if _data['name'] == v.Surfaces.DETECTOR_FRONT:
        return DetectorSurface._new(_part, _data)

    return Surface._new(_part, _data)

def create_part(_setup, id, type_):
    '''
    Private
    '''
    # part = _setup._get_part(id)
    # _data = part.get(id)
    # if _data.get('detector_data'):
    #     part = Detector._new(_setup, id, _data)
    # elif _data.get('light_source'):
    #     part = LightSource._new(_setup, id, _data)
    # else:
    #     part = Part._new(_setup, id, _data)
    # return part
    type_ = int(type_)

    if v.DEBUG:
        print(f"Creating part with id: {id}, type: {type_}")

    if type_ == v.PartType.OPTICS:
        part = Optics._new(_setup = _setup, id = id, _data= None)

    elif type_ == v.PartType.DETECTOR:
        part = Detector._new(_setup = _setup, id = id, _data= None)

    elif type_ == v.PartType.LIGHT_SOURCE:
        part = LightSource._new(_setup = _setup, id = id, _data= None)

    elif type_ == v.PartType.COORDINATE_SYSTEM:
        part = CoordinateSystemPart._new(_setup = _setup, id = id, _data= None)

    elif type_ == v.PartType.CAD:
        part = CAD._new(_setup = _setup, id = id, _data= None)

    elif type_ == v.PartType.BLACKBOX:
        part = BlackBox._new(_setup = _setup, id = id, _data= None)

    elif type_ == v.PartType.GROUP:
        part = Group._new(_setup = _setup, id = id, _data= None)

    elif type_ == v.PartType.PARAXIAL_LENS:
        part = ParaxialLens._new(_setup = _setup, id = id, _data= None)

    elif type_ == v.PartType.GENERAL:
        part = Part._new(_setup = _setup, id = id, _data= None)

    else:
        part = Part._new(_setup = _setup, id = id, _data= None)

    if v.DEBUG:
        print(f"Part created: {type(part)}")

    return part
