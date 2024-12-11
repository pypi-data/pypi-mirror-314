import threading
import pickle
import math
import requests
import pandas as pd
import numpy as np
import random
import time
import requests
import zipfile
import os
import copy
import json
import re

from io import BytesIO
from typing import Any, Union, List, Tuple, Dict, Optional

import threed_optix.package_utils.api as au
import threed_optix.package_utils.vars as v
import threed_optix.package_utils.math as mu
import threed_optix.package_utils.general as gu
import threed_optix.analyses as tdo_analyses
import threed_optix.simulations as tdo_simulations
import threed_optix.parts as tdo_parts
import threed_optix.package_utils.vars as v
import threed_optix.package_utils.verifiers as verifiers


class Material:

    @classmethod
    def _new(cls, _api, _data):
        material = cls.__new__(cls)
        material._api = _api
        material._data = _data
        return material

    def __init__(self):
        raise Exception("Material class cannot be instantiated.")

    @property
    def name(self):
        return self._data['name']

    @property
    def id(self):
        return self._data['number_id']

    @property
    def parameters(self):
        return self._data['parameters']

    @property
    def equation(self):
        return v.Materials.EQUATION_TYPE_MAP[self.parameters['type']]

    @property
    def company(self):
        return self.parameters.get('company')

    @property
    def coeffs(self):
        return self.parameters.get('coeffs')

    @property
    def end_lambda(self):
        return self.parameters.get('endLambda')

    @property
    def start_lambda(self):
        return self.parameters.get('startLambda')

    def refractive_index(self, wavelength):

        if 1000*wavelength < self.start_lambda or 1000*wavelength > self.end_lambda:
            raise ValueError(f"Wavelength must be between {self.start_lambda} and {self.end_lambda}")

        if self.equation == v.Materials.SELLEMEIR:
            return Material.calculate_sellmeier(self.coeffs, wavelength)

        if self.equation == v.Materials.CAUCHY:
            return Material.calculate_cauchy(self.coeffs, wavelength)

        if self.equation == v.Materials.CONRADY1:
            return Material.calculate_conrady1(self.coeffs, wavelength)

        if self.equation == v.Materials.CONSTANT:
            return self.coeffs

        if self.equation == v.Materials.MODIFIED_SELLEMEIR:
            return Material.calculate_modified_sellmeier(self.coeffs, wavelength)

        if self.equation == v.Materials.SCHOTT:
            return Material.calculate_schott(self.coeffs, wavelength)

    @staticmethod
    def calculate_sellmeier(coeffs, wavelength):
        wl2 = math.pow(wavelength, 2)
        a = (coeffs['b1'] * wl2) / (wl2 - coeffs['c1'])
        b = (coeffs['b2'] * wl2) / (wl2 - coeffs['c2'])
        c = (coeffs['b3'] * wl2) / (wl2 - coeffs['c3'])
        d = (coeffs['b4'] * wl2) / (wl2 - coeffs['c4'])
        e = (coeffs['b5'] * wl2) / (wl2 - coeffs['c5'])
        f = (coeffs['b6'] * wl2) / (wl2 - coeffs['c6'])
        g = (coeffs['b7'] * wl2) / (wl2 - coeffs['c7'])
        right_side = 1 + a + b + c + d + e + f + g
        refractive_index = math.sqrt(right_side)
        return refractive_index

    @staticmethod
    def calculate_schott(coeffs, wavelength):
        under_sqrt = coeffs['a']\
            + coeffs['b'] * (wavelength ** 2)\
                + coeffs['c'] / (wavelength ** 2)\
                    + coeffs['d'] / (wavelength ** 4)\
                        + coeffs['e'] / (wavelength ** 6)\
                            + coeffs['f'] / (wavelength ** 8)
        return math.sqrt(under_sqrt)

    @staticmethod
    def calculate_cauchy(coeffs, wavelength):
        return Material.calculate_schott(coeffs, wavelength)

    @staticmethod
    def calculate_conrady1(coeffs, wavelength):
        return coeffs['a'] + (coeffs['b']/wavelength) + (coeffs['c']/(wavelength**3.5))

    @staticmethod
    def calculate_modified_sellmeier(coeffs, wavelength):
        under_sqrt = coeffs['a']
        wl2 = wavelength ** 2
        for i in range(1, 8):
            b = coeffs[f'b{i}']
            c = coeffs[f'c{i}']
            under_sqrt += b * wl2 / (wl2 - c)
        return math.sqrt(under_sqrt)

    def describe(self):
        '''
        This function prints the key properties of the material.
        '''
        print(json.dumps({
            'name': self.name,
            'id': self.id,
            'equation': self.equation,
            'company': self.company,
            'end_lambda': self.end_lambda,
            'start_lambda': self.start_lambda
        }, indent=4))

class ThreedOptixAPI:
    """
    Used to manage the communication with the server of 3DOptix.

    Args:
        api_key (str): The API key used for authentication.

    Properties:
        api_key (str): The API key of the user.
        setups (list): The list of setups of the user.
    """


    def __init__(self,
                 api_key: str,
                 verbose: bool = True
                 ):

        # Store the API key
        self.init_error = None
        self.api_key = api_key
        self.setups = None
        self._questions_history = []

        # legacy- not relevat
        self.jobs = []

        # Check if the server is up and the key is valid
        assert self._is_up(), v.SERVER_DOWN_MESSAGE
        assert self._is_key_valid(), v.INVALID_KEY_MESSAGE

        if verbose:
            # Print welcome message
            welcome_thread = threading.Thread(target=au._welcome)
            welcome_thread.start()

        # Fetch setups from the server
        setups_thread = threading.Thread(target=self._initialize_setups)
        setups_thread.start()

        # Wait for both threads to finish
        if verbose:
            welcome_thread.join()

        setups_thread.join()
        if self.init_error is not None:
            #If setups is None, it means that the API key is invalid
            raise self.init_error

    def search_materials(self, material_name):
        # Fetch the material data from the server
        materials_data = au._get_materials(api_key=self.api_key,
                                           material_name=material_name)
        # Create the Material objects
        materials = [Material._new(_api=self, _data=material_data) for material_data in materials_data['materials']]

        return materials

    def create_setup(self,
                     name: str,
                     description: str,
                     labels: List[str],
                     units: str = 'mm',
                     private: bool = True,
                     associated: bool = False,
                     link: str = None,
                     title: str= None,
                     authors: str = None,
                     journal: str = None,
                     abstract: str = None,
                     ):
        '''
        This function creates a new setup with the specified parameters.
        Args:
            name (str): The name of the setup.
            description (str): The description of the setup.
            labels (list): The labels of the setup. enum is in `tdo.SETUP_LABELS`
            units (str): The units of the setup. Default is 'mm'. can be 'mm' or 'inch'
            private (bool): If True, the setup is private. Default is False.
            associated (bool): If True, the setup is associated with a publication. Default is False.
            link (str): The link to the publication. Default is None.
            title (str): The title of the publication. Default is None.
            authors (str): The authors of the publication. Default is None.
            journal (str): The journal of the publication. Default is None.
            abstract (str): The abstract of the publication. Default is None.
        '''


        def verify():
            errors = []

            # Check if the labels are valid
            if not set(labels).issubset(set(v.SETUP_LABELS)):
                errors.append(f"""All labels must one of {', '.join(v.SETUP_LABELS)}""")

            # Check if the units are valid
            if units not in v.SETUP_UNITS:
                errors.append(f"""Units must be one of {', '.join(v.SETUP_UNITS)}""")

            if  not isinstance(name,str) or len(name) == 0:
                errors.append("Name must be a valid non-empty string")

            if not isinstance(description,str) or len(description) == 0:
                errors.append("Description must be a valid non-empty string")

            if len(labels) == 0:
                errors.append("Labels cannot be empty")

            return errors

        # Verify the parameters
        errors = verify()
        # Raise an exception if there are errors
        if len(errors) > 0:
            raise Exception('\n'.join(errors))

        # Organize the data for the API
        data = {
            "details": {
                "setupName": name,
                "labels": labels,
                "generalComments": description,
            },
            "unit": v.CREATE_SETUP_UNITS_MAP[units],
            "permission": 0 if private else 1,
        }

        # Add the associated data if needed
        associated = {
            "isAssociated": associated,
            "link": link,
            "title": title,
            "authors": authors,
            "journal": journal,
            "abstract": abstract,
        }

        for key, value in associated.items():
            if value is not None:
                data['details'][key] = value

        # Create the setup with the API in the database
        response = au._create_setup(data, self.api_key)

        # Get the setup id from the response
        setup_id = response['id']

        # Create the Setup object
        setup = tdo_simulations.Setup._new(_api=self, setup_tuple=(setup_id, name))

        # Add the setup to the setups list
        self.setups.append(setup)
        return setup

    def get(self,
            setup_name: str,
            all: bool = False
            ) -> tdo_simulations.Setup:
        """
        Returns the Setup object with the specified name.
        Args:
            setup_name (str): The name of the setup.
            all (bool): If True, returns all setups with the specified name. else, returns the first one

        Returns:
            Setup (tdo.Setup): The Setup object.
        """

        # If all is True, return all setups with the specified name
        if all:
            setups = []
            for setup in self:
                if setup.name == setup_name:
                    setups.append(setup)
            if len(setups) > 0:
                return setups

        # If all is False, return the first setup with the specified name
        else:
            setup = None
            for s in self.setups:
                if s.name == setup_name:
                    setup = s
                    return setup

        # Raise an exception if the setup is not found
        raise Exception(f"Setup with name {setup_name} not found.")

    def get_setups(self) -> list:
        """
        Returns a list of Setup objects that are associated with the user.

        Returns:
            list: A list of Setup objects.
        """
        return self.setups

    def create_aperture(self,
                        name,
                        inner_dims_x,
                        inner_dims_y,
                        outer_dims_x,
                        outer_dims_y,
                        is_inner_elliptical = True,
                        is_outer_elliptical = True,
                        inner_phase = 0,
                        inner_transmittance = 1,
                        outer_phase = 0,
                        outer_transmittance = 0,
                        check_exist = True,
                        db_id = None
                        ):
        '''
        This function creates a new aperture with the specified parameters.

        Args:
            name (str): The name of the lens.
            inner_dims_x (float): The dims of inner shape. If shape is elliptical (default) it will be treated as x radius, else it will be treated as half width (rectangular aperture).
            inner_dims_y (float): The dims of inner shape. If shape is elliptical (default) it will be treated as y radius, else it will be treated as half height (rectangular aperture).
            outer_dims_x (float): The dims of inner shape. If shape is elliptical (default) it will be treated as x radius, else it will be treated as half width (rectangular aperture).
            outer_dims_y (float): The dims of inner shape. If shape is elliptical (default) it will be treated as y radius, else it will be treated as half height (rectangular aperture).
            is_inner_elliptical (bool, default True): Is the inner shape of the aperture elliptical, if set to False it will be rectangular
            is_outer_elliptical (bool, default True): Is the outer shape of the aperture elliptical, if set to False it will be rectangular
            inner_phase (float, default 0): Inner phase. Expects value in radiance
            inner_transmittance (float, default 1): Inner transmittance
            outer_phase (float, default 0): Outer phase Expects value in radiance
            outer_transmittance (float, default 0): Outer transmittance
            check_exist (bool): If True, checks if the lens already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created lens.
        '''
        type = v.eOpticsTypeNames.APERTURE
        subtype = v.eOpticsSubtypes.Elliptical_Aperture if is_inner_elliptical else v.eOpticsSubtypes.Rectangular_Aperture
        shape = v.eOpticShape.APERTURE
        base_shape = v.eBaseShape.ELLIPTICAL if is_outer_elliptical else v.eBaseShape.RECTANGULAR

        inner_shape = v.eBaseShape.ELLIPTICAL if is_inner_elliptical else v.eBaseShape.RECTANGULAR

        inner_shape_x_key = "radius_x" if is_inner_elliptical else "half_width"
        inner_shape_y_key = "radius_y" if is_inner_elliptical else "half_height"
        outer_shape_x_key = "radius_x" if is_outer_elliptical else "half_width"
        outer_shape_y_key = "radius_y" if is_outer_elliptical else "half_height"

        physical_data = {
            "layers":[
                {
                    "data":{
                        "phase": inner_phase,
                        "transmittance": inner_transmittance
                    },
                    "shape": inner_shape,
                    "geo":{
                        inner_shape_x_key:inner_dims_x,
                        inner_shape_y_key:inner_dims_y
                    }
                },
                {
                    "data":{
                        "phase": outer_phase,
                        "transmittance": outer_transmittance
                    },
                    "shape": base_shape,
                    "geo":{
                        outer_shape_x_key:outer_dims_x,
                        outer_shape_y_key:outer_dims_y
                    }
                }
            ]
        }

        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            geometry={},
            shape=shape,
            name=name,
            coating={},
            check_exist=check_exist,
            db_id=db_id,
            material="",
            physical_data=physical_data
        )


    def create_aspheric_lens(self,
                          name,
                          material,
                          diameter,
                          thickness,
                          r1_x,
                          r1_y,
                          r2_x,
                          r2_y,
                          k1_x = 0,
                          k1_y = 0,
                          k2_x = 0,
                          k2_y = 0,
                          coeffs_front = [],
                          coeffs_back = [],
                          check_exist = True,
                          coating = {},
                          db_id = None):

        '''
        This function creates a new biconic lens with the specified parameters.

        Args:
            name (str): The name of the lens.
            material (str | Material): The material of the lens.
            diameter (float): The diameter of the lens.
            thickness (float): The thickness of the lens.
            r1_x (float): The radius of curvature in the x direction of the first surface.
            r1_y (float): The radius of curvature in the y direction of the first surface.
            r2_x (float): The radius of curvature in the x direction of the second surface.
            r2_y (float): The radius of curvature in the y direction of the second surface.
            k1_x (float): The conic constant in the x direction of the first surface. Default is 0.
            k1_y (float): The conic constant in the y direction of the first surface. Default is 0.
            k2_x (float): The conic constant in the x direction of the second surface. Default is 0.
            k2_y (float): The conic constant in the y direction of the second surface. Default is 0.
            coeffs_front (list): The coefficients of the front surface. Default is [].
            coeffs_back (list): The coefficients of the back surface. Default is [].
            check_exist (bool): If True, checks if the lens already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created lens.
        '''

        type = v.eOpticsTypeNames.LENS
        subtype = v.eOpticsSubtypes.General_Biconic
        shape = v.eOpticShape.CONIC
        base_shape = v.eBaseShape.CIRCULAR

        deformation = {}
        if len(coeffs_front) > 0:
            deformation[v.Surfaces.LENS_FRONT] =  [{
                "type": v.Surfaces.ASPHERE_DEFORMATION,
                "params": {
                    "terms": [[c[0], c[0], c[1]] for c in coeffs_front]
                }
                }
                ]
        if len(coeffs_back) > 0:
            deformation[v.Surfaces.LENS_BACK] = [{
                "type": v.Surfaces.ASPHERE_DEFORMATION,
                "params": {
                    "terms": [[c[0], c[0], c[1]] for c in coeffs_back]
                }
                }
                ]

        # Create the geometry dictionary
        geometry = {
            "diameter": diameter,
            "thickness_center": thickness,
            "r1_x": r1_x,
            "r1_y": r1_y,
            "r2_x": r2_x,
            "r2_y": r2_y,
            "k1_x": k1_x,
            "k1_y": k1_y,
            "k2_x": k2_x,
            "k2_y": k2_y,
            "deformation": deformation
            }

        # Create the lens with the API
        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            geometry=geometry,
            shape=shape,
            name=name,
            coating=coating,
            check_exist=check_exist,
            db_id=db_id,
            material=material
        )


    def create_biconic_lens(self,
                          name,
                          material,
                          diameter,
                          thickness,
                          r1_x,
                          r1_y,
                          r2_x,
                          r2_y,
                          k1_x = 0,
                          k1_y = 0,
                          k2_x = 0,
                          k2_y = 0,
                          check_exist = True,
                          coating = {},
                          db_id = None):

        '''
        This function creates a new biconic lens with the specified parameters.

        Args:
            name (str): The name of the lens.
            material (str | Material): The material of the lens.
            diameter (float): The diameter of the lens.
            thickness (float): The thickness of the lens.
            r1_x (float): The radius of curvature in the x direction of the first surface.
            r1_y (float): The radius of curvature in the y direction of the first surface.
            r2_x (float): The radius of curvature in the x direction of the second surface.
            r2_y (float): The radius of curvature in the y direction of the second surface.
            k1_x (float): The conic constant in the x direction of the first surface. Default is 0.
            k1_y (float): The conic constant in the y direction of the first surface. Default is 0.
            k2_x (float): The conic constant in the x direction of the second surface. Default is 0.
            k2_y (float): The conic constant in the y direction of the second surface. Default is 0.
            check_exist (bool): If True, checks if the lens already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created lens.
        '''

        type = v.eOpticsTypeNames.LENS
        subtype = v.eOpticsSubtypes.General_Biconic
        shape = v.eOpticShape.CONIC
        base_shape = v.eBaseShape.CIRCULAR

        # Create the geometry dictionary
        geometry = {
            "diameter": diameter,
            "thickness_center": thickness,
            "r1_x": r1_x,
            "r1_y": r1_y,
            "r2_x": r2_x,
            "r2_y": r2_y,
            "k1_x": k1_x,
            "k1_y": k1_y,
            "k2_x": k2_x,
            "k2_y": k2_y,
            }

        # Create the lens with the API
        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            geometry=geometry,
            shape=shape,
            name=name,
            coating=coating,
            check_exist=check_exist,
            db_id=db_id,
            material=material
        )

    def create_conic_lens(self,
                          name,
                          material,
                          diameter,
                          thickness,
                          r1,
                          r2,
                          k1 = 0,
                          k2 = 0,
                          check_exist = True,
                          coating = {},
                          db_id = None
                          ):
        '''
        This function creates a new conic lens with the specified parameters.

        Args:
            name (str): The name of the lens.
            material (str | Material): The material of the lens.
            diameter (float): The diameter of the lens.
            thickness (float): The thickness of the lens.
            r1 (float): The radius of curvature of the lens.
            r2 (float): The radius of curvature of the lens.
            k1 (float): The conic constant of the lens. Default is 0.
            k2 (float): The conic constant of the lens. Default is 0.
            check_exist (bool): If True, checks if the lens already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created lens.
        '''

        type = v.eOpticsTypeNames.LENS
        subtype = v.eOpticsSubtypes.General_Conic
        shape = v.eOpticShape.CONIC
        base_shape = v.eBaseShape.CIRCULAR

        # Create the geometry dictionary
        geometry = {
            "diameter": diameter,
            "thickness_center": thickness,
            "r1": r1,
            "r2": r2,
            "k1": k1,
            "k2": k2
            }

        # Create the lens with the API
        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            geometry=geometry,
            shape=shape,
            name=name,
            coating=coating,
            check_exist=check_exist,
            db_id=db_id,
            material=material
        )

    def create_spherical_lens(self,
                          name,
                          material: Union[str, Material],
                          diameter,
                          thickness,
                          r1,
                          r2 = None,
                          check_exist = True,
                          coating = {},
                          db_id = None):
        '''
        This function creates a new spherical lens with the specified parameters.

        Args:
            name (str): The name of the lens.
            material (str | Material): The material of the lens.
            diameter (float): The diameter of the lens.
            thickness (float): The thickness of the lens.
            r1 (float): The radius of curvature of the lens.
            r2 (float): The radius of curvature of the lens. Default is None.
            check_exist (bool): If True, checks if the lens already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created lens.
        '''



        type = v.eOpticsTypeNames.LENS

        ## Check if name is defined
        if(not name or not isinstance(name,str)):
            raise ValueError('Name must be a valid string')

        # Check if the radii are valid
        if r1 == 0 or r2 == 0:
            raise ValueError('Radii cannot be 0. For plano surface, use r1 when r2 is None.')

        # Determine the subtype based on the radii
        if r2 is None:
            # if r2 is None, the lens is plano
            if r1 > 0:
                subtype = v.eOpticsSubtypes.Spherical_Lens_Plano_Convex
            elif r1 < 0:
                subtype = v.eOpticsSubtypes.Spherical_Lens_Plano_Concave

        elif r1 < 0:
            # if r1 is negative, the lens is concave
            if r2 < 0:
                subtype = v.eOpticsSubtypes.Spherical_Lens_Concave_Convex
            elif r2 > 0:
                subtype = v.eOpticsSubtypes.Spherical_Lens_Concave_Concave
        elif r1 > 0:
            # if r1 is positive, the lens is convex
            if r2 < 0:
                subtype = v.eOpticsSubtypes.Spherical_Lens_Convex_Convex
            elif r2 > 0:
                subtype = v.eOpticsSubtypes.Spherical_Lens_Convex_Concave

        shape = v.eOpticShape.SPHERICAL
        base_shape = v.eBaseShape.CIRCULAR

        # Create the geometry dictionary
        geometry = {
            "diameter": diameter,
            "thickness_center": thickness,
            "r1": r1,
            }

        # Add r2 to the geometry dictionary if it is not None
        if r2 is not None:
            geometry["r2"] = r2

        # Create the lens with the API
        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            geometry=geometry,
            shape=shape,
            name=name,
            coating=coating,
            check_exist=check_exist,
            db_id=db_id,
            material=material
        )

    def create_ball_lens(self,
                          name,
                          material,
                          diameter,
                          half = False,
                          check_exist = True,
                          coating = {},
                          db_id = None):
        '''
        Not implemented yet.
        '''

        type = v.eOpticsTypeNames.LENS
        shape = v.eOpticShape.CONIC
        base_shape = v.eBaseShape.CIRCULAR
        subtype = v.eOpticsSubtypes.Half_Ball_Lens if half else v.eOpticsSubtypes.Ball_Lens
        geometry = {
            "diameter": diameter,
            }

        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            geometry=geometry,
            shape=shape,
            name=name,
            coating=coating,
            check_exist=check_exist,
            db_id=db_id,
            material=material
        )

    def create_grating(self,
                       name,
                       material,
                       shape,
                       grooves,
                       order,
                       subtype,
                       orientation_vector,
                       grating_side = 'Front',
                       check_exist = True,
                       coating = {},
                       db_id = None,
                       **kwargs
                       ):
        '''
        This function creates a new grating with the specified parameters.

        Args:
            name (str): The name of the grating.
            material (str | Material): The material of the grating.
            shape (str): The shape of the grating. can be either 'cir' or 'rect'.
            grooves (int): The number of grooves of the grating.
            order (int): The order of the grating.
            subtype (str): The subtype of the grating. enum is in `tdo.GRATING_SUBTYPES`
            orientation_vector (list): The normalized orientation vector of the grating.
            grating_side (str): The side of the grating. can be "Back" or "Front". Default is 'Front'.
            check_exist (bool): If True, checks if the grating already exists. if it exists, it returns it and doesn't create a new one. Default is True.
            coating (dict): The coating of the grating. can be an empty dictionary or a dictionary with surface names as keys and `tdo.Coating` enum as values. Default is {}.
            db_id (str): The database id of the grating. If defined, it will edit the optics in the database. Default is None.
            kwargs (dict): The additional parameters of the grating. For circular grating, 'diameter' and 'thickness' must be provided. For rectangular grating, 'width', 'height', and 'thickness' must be provided. For blazed ruled reflective grating, 'blaze_angle' and 'blaze_wavelength' must be provided.

        Returns:
            str: The database id of the created grating.
        '''

        def verify():

            if v.DEBUG:
                print(f'Kwargs are {kwargs}')
                print(f'Shape is {shape}')
                print(f'Subtype is {subtype}')

            errors = []

            # Check if the subtype is valid
            if subtype not in v.eOpticsSubtypes.GRATING_SUBTYPES:
                errors.append(f"""Subtype must be one of {', '.join(v.eOpticsSubtypes.GRATING_SUBTYPES)}""")

            # Check if the shape is valid
            if shape not in v.eBaseShape.GRATING_SHAPES.keys():
                errors.append(f"""Shape must be one of {', '.join(v.eBaseShape.GRATING_SHAPES.keys())}""")

            if shape == 'cir':
                # Check if the diameter and thickness are provided
                if any([key not in kwargs for key in ['diameter', 'thickness']]):
                    errors.append("For circular grating, diameter and thickness must be provided")
            elif shape == 'rect':
                # Check if the width, height, and thickness are provided
                if any([key not in kwargs for key in ['width', 'height', 'thickness']]):
                    errors.append("For rectangular grating, width, height and thickness must be provided")

            if subtype in [v.eOpticsSubtypes.Blazed_Ruled_Reflective_Grating,
                       v.eOpticsSubtypes.Echelle_Grating,
                       v.eOpticsSubtypes.Transmission_Grating]:
                # Check if the blaze angle and blaze wavelength are provided
                if any([key not in kwargs for key in ['blaze_angle', 'blaze_wavelength']]):
                    errors.append("Blaze angle and blaze wavelength must be provided for the selected subtype")

            # Check if the orientation vector is in length 3
            if len(orientation_vector) != 3:
                errors.append("Orientation vector must have 3 elements")

            # Check if the orientation vector has a length of 1
            if not mu.is_normalized(orientation_vector):
                errors.append("Orientation vector must be normalized")

            # Check if the grating side is valid
            if grating_side not in ['Front', 'Back']:
                errors.append("Grating side must be one of 'front' or 'back'")

            return errors

        # Verify the parameters
        errors = verify()
        if len(errors) > 0:
            raise Exception('\n'.join(errors))

        # Create the geometry dictionary based on the shape
        if shape == 'cir':
            geometry = {
                "diameter": kwargs['diameter'],
                'thickness': kwargs['thickness'],
            }
        elif shape == 'rec':
            geometry = {
                "width": kwargs['width'],
                'height': kwargs['height'],
                'thickness': kwargs['thickness'],
            }


        type = v.eOpticsTypeNames.GRATING
        base_shape = v.eBaseShape.GRATING_SHAPES[shape]
        shape = v.eOpticShape.GRATING

        if subtype in [v.eOpticsSubtypes.Blazed_Ruled_Reflective_Grating,
                       v.eOpticsSubtypes.Echelle_Grating,
                       v.eOpticsSubtypes.Transmission_Grating]:
            physical_data = {
                "blaze_angle": kwargs['blaze_angle'],
                "blaze_wavelength": kwargs['blaze_wavelength'],
            }
        else:
            physical_data = {}

        physical_data['grooves'] = grooves
        physical_data['order'] = order
        physical_data['orientation_vector'] = {'x': orientation_vector[0], 'y': orientation_vector[1], 'z': orientation_vector[2]}
        physical_data['grating_side'] = grating_side

        # Create the grating with the API
        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            geometry=geometry,
            shape=shape,
            name=name,
            coating=coating,
            check_exist=check_exist,
            db_id=db_id,
            material=material,
            physical_data=physical_data
        )

    def create_circular_mirror(self,
                               name,
                               material,
                               diamater,
                               thickness,
                               check_exist = True,
                               coating = {"front": 'ideal_reflector'},
                               db_id = None):
        '''
        This function creats a new circular Metallic Mirror with specified args.

        Args:
            name (str): The name of the mirror.
            material (str | Material): The material of the mirror.
            diameter (float): The diameter of the mirror.
            thickness (float): The thickness of the mirror.
            coating (dict): A dict consisting of the surface and coating type. Default {"front": 'ideal_reflector'}
            check_exist (bool): If True, checks if the mirror already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created mirror.
        '''
        type = v.eOpticsTypeNames.MIRROR
        subtype = v.eOpticsSubtypes.Metallic_Mirror
        base_shape = v.eBaseShape.CIRCULAR
        shape = v.eOpticShape.THIN_LENS

        geometry = {
            "diameter" : diamater,
            "thickness" : thickness,
        }

        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            shape=shape,
            geometry=geometry,
            name=name,
            coating=coating,
            check_exist=check_exist,
            db_id=db_id,
            material=material
        )

    def create_rectangular_mirror(self,
                            name,
                            material,
                            width,
                            height,
                            thickness,
                            check_exist = True,
                            coating = {"front": 'ideal_reflector'},
                            db_id = None):
        '''
        This function creats a new rectangular Metallic Mirror with specified args.

        Args:
            name (str): The name of the mirror.
            material (str | Material): The material of the mirror.
            width (float): The width of the mirror.
            height (float): The height of the mirror.
            thickness (float): The thickness of the mirror.
            coating (dict): A dict consisting of the surface and coating type. Default {"front": 'ideal_reflector'}
            check_exist (bool): If True, checks if the mirror already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created mirror.
        '''
        type = v.eOpticsTypeNames.MIRROR
        subtype = v.eOpticsSubtypes.Metallic_Mirror
        base_shape = v.eBaseShape.RECTANGULAR
        shape = v.eOpticShape.THIN_LENS

        geometry = {
            "width" : width,
            "height": height,
            "thickness" : thickness,
        }

        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            shape=shape,
            geometry=geometry,
            name=name,
            coating=coating,
            check_exist=check_exist,
            db_id=db_id,
            material=material
        )

    def create_roof_prism_mirror(self,
                            name,
                            material,
                            width,
                            height,
                            thickness,
                            check_exist = True,
                            coating = {"front_left" : 'ideal_reflector',
                                       "front_right" : 'ideal_reflector'},
                            db_id = None):
        '''
        This function creats a new rectangular Metallic Mirror with specified args.

        Args:
            name (str): The name of the mirror.
            material (str | Material): The material of the mirror.
            width (float): The width of the mirror.
            height (float): The height of the mirror.
            thickness (float): The thickness of the mirror.
            coating (dict): A dict consisting of the surface and coating type. Default {"front_left" : 'ideal_reflector', "front_right" : 'ideal_reflector'}
            check_exist (bool): If True, checks if the mirror already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created prism.
        '''

        type = v.eOpticsTypeNames.MIRROR
        subtype = v.eOpticsSubtypes.Roof_Prism_Mirror
        base_shape = v.eBaseShape.RECTANGULAR
        shape = v.eOpticShape.ROOF_PRISM_MIRROR

        geometry = {
            "width" : width,
            "height": height,
            "thickness" : thickness,
        }

        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            shape=shape,
            geometry=geometry,
            name=name,
            coating=coating,
            check_exist=check_exist,
            db_id=db_id,
            material=material
        )

    def create_right_angle_prism_mirror(self,
                            name,
                            material,
                            a,
                            b,
                            c,
                            check_exist = True,
                            knife_edge = False,
                            coating = {"hypotenuse" : 'ideal_reflector'},
                            db_id = None):
        '''
        This function creats a new rectangular Metallic Mirror with specified args.

        Args:
            name (str): The name of the prism.
            material (str | Material): The material of the prism.
            a (float): The 'a' param of the prism.
            b (float): The 'b' param of the prism.
            c (float): The 'c' param of the prism.
            coating (dict): A dict consisting of the surface and coating type. Default {"hypotenuse" : 'ideal_reflector'}
            knife_edge (bool): If true, creates a knife edge right angle prism mirror. Default is False
            check_exist (bool): If True, checks if the mirror already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created prism.
        '''

        type = v.eOpticsTypeNames.MIRROR
        subtype = v.eOpticsSubtypes.Right_Angle_Prism_Mirror if not knife_edge else v.eOpticsSubtypes.Knife_Edge_Prism_Mirror
        base_shape = v.eBaseShape.VOLUME
        shape = v.eOpticShape.RIGHT_ANGLE_PRISM

        geometry = {
            "a" : a,
            "b": b,
            "c" : c,
        }

        return self._create_optics(
            type=type,
            subtype=subtype,
            base_shape=base_shape,
            shape=shape,
            geometry=geometry,
            name=name,
            coating=coating,
            check_exist=check_exist,
            db_id=db_id,
            material=material
        )

    def create_off_axis_parabolic_mirror(self,
                            name,
                            material,
                            a,
                            diameter,
                            off_axis_angle,
                            radius_of_curvature,
                            thickness_edge,
                            check_exist = True,
                            coating = {"front" : 'ideal_reflector'},
                            db_id = None):
        '''
        This function creats a new Off Axis Parabolic Mirror with specified args.

        Args:
            name (str): The name of the mirror.
            material (str | Material): The material of the mirror.
            a (float): The 'a' param of the mirror.
            diameter (float): The diameter of the mirror.
            off_axis_angle (float): The off axis angle of the mirror.
            radius_of_curvature (float): The radius of curvature of the mirror.
            thickness_edge (float): Edge thickness of the mirror
            coating (dict): A dict consisting of the surface and coating type. Default {"front" : 'ideal_reflector'}
            check_exist (bool): If True, checks if the mirror already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created mirror.
        '''

        type = v.eOpticsTypeNames.MIRROR
        subtype = v.eOpticsSubtypes.Off_Axis_Parabolic_Mirror
        base_shape = v.eBaseShape.CIRCULAR
        shape = v.eOpticShape.OFF_AXIS_PARABOLIC

        geometry = {"a" : a,
                    "diameter" : diameter,
                    "off_axis_angle": off_axis_angle,
                    "radius_of_curvature": radius_of_curvature,
                    "thickness_edge": thickness_edge}


        return self._create_optics(
        type=type,
        subtype=subtype,
        base_shape=base_shape,
        shape=shape,
        geometry=geometry,
        name=name,
        coating=coating,
        check_exist=check_exist,
        db_id=db_id,
        material=material
    )

    def create_parabolic_mirror(self,
                            name,
                            material,
                            diameter,
                            radius_of_curvature,
                            thickness_edge,
                            check_exist = True,
                            coating = {"front" : 'ideal_reflector'},
                            db_id = None):
        '''
        This function creats a new Off Axis Parabolic Mirror with specified args.

        Args:
            name (str): The name of the mirror.
            material (str | Material): The material of the mirror.
            diameter (float): The diameter of the mirror.
            radius_of_curvature (float): The radius of curvature of the mirror.
            thickness_edge (float): Edge thickness of the mirror
            coating (dict): A dict consisting of the surface and coating type. Default {"front" : 'ideal_reflector'}
            check_exist (bool): If True, checks if the mirror already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created mirror.
        '''

        type = v.eOpticsTypeNames.MIRROR
        subtype = v.eOpticsSubtypes.Parabolic_Mirror_Concave
        base_shape = v.eBaseShape.CIRCULAR
        shape = v.eOpticShape.PARABOLIC

        geometry = {"diameter" : diameter,
                    "radius_of_curvature": radius_of_curvature,
                    "thickness_edge": thickness_edge}


        return self._create_optics(
        type=type,
        subtype=subtype,
        base_shape=base_shape,
        shape=shape,
        geometry=geometry,
        name=name,
        coating=coating,
        check_exist=check_exist,
        db_id=db_id,
        material=material
    )

    def create_cylindrical_mirror(self,
                            name,
                            material,
                            diameter,
                            r1_x,
                            r1_y,
                            thickness_center,
                            check_exist = True,
                            coating = {"front" : 'ideal_reflector'},
                            db_id = None):
        '''
        This function creats a new Off Axis Parabolic Mirror with specified args.

        Args:
            name (str): The name of the mirror.
            material (str | Material): The material of the mirror.
            diameter (float): The diameter of the mirror.
            r1_x (float): The r1_x of the mirror.
            r1_y (float): The r1_y of the mirror.
            thickness_center (float): Center thickness of the mirror
            coating (dict): A dict consisting of the surface and coating type. Default {"front" : 'ideal_reflector'}
            check_exist (bool): If True, checks if the mirror already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created mirror.
        '''
        if np.sign(r1_x) != np.sign(r1_y):
            raise ValueError("Invalid radii! r1_x and r1_y signs must be identical")

        type = v.eOpticsTypeNames.MIRROR
        subtype = v.eOpticsSubtypes.Cylindrical_Mirror_Plano_Concave if (r1_x < 0 and r1_y < 0) else v.eOpticsSubtypes.Cylindrical_Mirror_Plano_Convex
        base_shape = v.eBaseShape.CIRCULAR
        shape = v.eOpticShape.CYLINDRICAL

        geometry = {"diameter" : diameter,
                "r1_x": r1_x,
                "r1_y": r1_y,
                "thickness_center" : thickness_center}

        return self._create_optics(
        type=type,
        subtype=subtype,
        base_shape=base_shape,
        shape=shape,
        geometry=geometry,
        name=name,
        coating=coating,
        check_exist=check_exist,
        db_id=db_id,
        material=material
    )

    def create_curved_mirror(self,
                    name,
                    material,
                    diameter,
                    r1,
                    thickness_center,
                    check_exist = True,
                    coating = {"front" : 'ideal_reflector'},
                    db_id = None):
        '''
        This function creats a new Off Axis Parabolic Mirror with specified args.

        Args:
            name (str): The name of the mirror.
            material (str | Material): The material of the mirror.
            diameter (float): The diameter of the mirror.
            r1 (float): The radius of the mirror.
            thickness_center (float): Center thickness of the mirror
            coating (dict): A dict consisting of the surface and coating type. Default {"front" : 'ideal_reflector'}
            check_exist (bool): If True, checks if the mirror already exists. if it exists, it returns it and doesn't create a new one. Default is True.

        Returns:
            str: The database id of the created mirror.
        '''

        type = v.eOpticsTypeNames.MIRROR
        subtype = v.eOpticsSubtypes.Curved_Mirror_Convex if r1 > 0 else v.eOpticsSubtypes.Curved_Mirror_Concave
        base_shape = v.eBaseShape.CIRCULAR
        shape = v.eOpticShape.SPHERICAL

        geometry = {"diameter" : diameter,
                    "r1": r1,
                    "thickness_center": thickness_center}


        return self._create_optics(
        type=type,
        subtype=subtype,
        base_shape=base_shape,
        shape=shape,
        geometry=geometry,
        name=name,
        coating=coating,
        check_exist=check_exist,
        db_id=db_id,
        material=material
        )

    def create_multiplet(self,
                        name: str,
                        num_surfaces: int,
                        materials:List[str],
                        diameter: float,
                        r_x:List[float],
                        r_y:List[float],
                        thickness:List[float],
                        hole_diameter_front = 0,
                        hole_diameter_back = 0,
                        k_y=[],
                        k_x=[],
                        decenter_x=[],
                        decenter_y=[],
                        coating:Dict = {},
                        coeffs:Dict = {},
                        check_exist = True,
                        db_id = None
                        ):
        """
        This function creates a multiplet lens with specified parameters and returns the created optics database id.

        Parameters:
        -----------
        name : str
            The name of the multiplet.
        num_surfaces : int
            The number of surfaces in the multiplet.
        materials : List[str]
            List of material id's for each element in the multiplet.
        diameter : float
            The diameter of the multiplet.
        r_x : List[float]
            List of x-axis radii of curvature for each surface.
        r_y : List[float]
            List of y-axis radii of curvature for each surface.
        thickness : List[float]
            List of thicknesses for each element.
        hole_diameter_front : float, optional
            Diameter of the hole in the front of the optics (default is 0).
        hole_diameter_back : float, optional
            Diameter of the hole in the back of the optics(default is 0).
        k_y : List[float], optional
            List of y-axis conic constants for each surface (default is No coefficients).
        k_x : List[float], optional
            List of x-axis conic constants for each surface (default is No coefficients).
        decenter_x : List[float], optional
            List of x-axis decenters for each surface (default is No decenter).
        decenter_y : List[float], optional
            List of y-axis decenters for each surface (default is No decenter).
        coating : Dict, optional
            Dictionary specifying coating properties (default is {}).
        coeffs : Dict, optional
            Dictionary of aspheric deformation coefficients for surfaces (default is {}).
            The format for coeffs is {"s1":[[4,0.004],[6,0.0002]]} where each surface you want to add coefficients to is a key in the format "s<surface number>" and value is List[List] where for each sublist sublist[0] is the degree and sublit[1] is the value
        Returns:
        --------
        str
            The db_id of the new multiplet
        """

        hole_diameters = [hole_diameter_front, hole_diameter_back]

        k_x = self._fill_if_empty(k_x, num_surfaces)
        k_y = self._fill_if_empty(k_y, num_surfaces)
        decenter_x = self._fill_if_empty(decenter_x, num_surfaces)
        decenter_y = self._fill_if_empty(decenter_y, num_surfaces)

        verifiers.MultipletVerifiers.validate_multiplet_params(
                                        name=name,
                                        num_surfaces=num_surfaces,
                                        materials=materials,
                                        diameter=diameter,
                                        r_x=r_x,
                                        r_y=r_y,
                                        k_x=k_x,
                                        k_y=k_y,
                                        thickness=thickness,
                                        hole_diameters=hole_diameters,
                                        decenter_x=decenter_x,
                                        decenter_y=decenter_y,
                                        coeffs=coeffs,
                                        coating=coating)

        type = v.eOpticsTypeNames.LENS
        subtype = v.eOpticsSubtypes.Multiplets
        base_shape = v.eBaseShape.CIRCULAR
        shape = v.eOpticShape.MULTIPLET

        multiplet_data={
                "r_x":r_x,
                "r_y": r_y,
                "k_x":k_x,
                "k_y":k_y,
                "ca":[diameter for _ in range(num_surfaces)],
                "t":thickness,
                "hole_diameter":hole_diameters,
                "decenter_x":decenter_x,
                "decenter_y":decenter_y,
            }

        deformation = {}

        if len(coeffs) > 0:
            for surface, params in coeffs.items():
                deformation[surface] =  [{
                    "type": v.Surfaces.ASPHERE_DEFORMATION,
                    "params": {
                        "terms": [[c[0], c[0], c[1]] for c in params]
                    }
                    }
                    ]


        geometry = {
            "diameter": diameter,
            "multipletData":multiplet_data,
            "deformation":deformation
        }

        return self._create_optics(
                type=type,
                subtype=subtype,
                base_shape=base_shape,
                shape=shape,
                geometry=geometry,
                name=name,
                coating=coating,
                check_exist=check_exist,
                db_id=db_id,
                material=materials
            )

    def _fill_if_empty(self, param: Optional[List[float]], target_length: int, fill_value: float = 0.0) -> List[float]:
        return [fill_value for _ in range(target_length)] if not param else param

    def _create_optics(self, type, subtype, base_shape, material, shape, geometry, name, check_exist, db_id, coating, physical_data = None):
        '''
        Private.
        This function is the base function for creating optics.
        It creates the optics with the specified parameters.
        '''

        parameters = {
            "type": type,
            "subType": subtype,
            "materialID": material.id if isinstance(material, Material) else material,
            "baseShape": base_shape,
            "shape": shape,
            "coating": coating,
            "geometry": geometry,
        }

        if physical_data is not None:
            parameters['physical_data'] = physical_data

        optics = {
            "name": name,
            "parameters": parameters
        }

        if db_id is not None:
            optics['number_id'] = db_id

        data = {
            "optics": optics,
            "checlExist": check_exist
        }

        return au._create_part(parameters=data, api_key=self.api_key).get('number_id')

    def ask(self,
            question: str
            ):
        '''
        Not implemented yet.
        This function will call the SDK assistant to answer the question about the SDK
        '''
        try:
            # Update the history with the user question
            self._questions_history.append({"role": "user", "content": question})
            # Ask the question to the assistant
            response = au._ask(self._questions_history[-v.MAX_HISTORY_LEN:], self.api_key)
        except Exception as e:
            # If the request fails, remove the question from the history and raise the exception
            self._questions_history.pop()
            raise e

        # Update the history with the assistant response
        self._questions_history.append({"role": "assistant", "content": response})
        return response

    def feedback(self, feedback: str):
        '''
        Not implemented yet.
        Sending feedback to us about the SDK.
        '''
        raise NotImplementedError("This function is not implemented yet.")

    def _add_part(self, setup_id, type_, db_id = None):
        '''
        Private.
        This is the base function for adding parts to the setup.
        It adds the part with the specified parameters to the setup with the specified id.
        The setup calls this function as a communication bridge.
        '''


        data = {
            "type": type_,
        }
        if db_id is not None and type_ == v.PartType.OPTICS:
            data['number_id'] = db_id

        response = au._add_part(setup_id, data, self.api_key)
        part_id = response['id']
        return part_id

    def _delete_part(self, setup_id, part_id):
        '''
        Private.
        This is the base function for deleting parts from the setup.
        It deletes the part with the specified id from the setup with the specified id.
        The setup calls this function as a communication bridge.
        '''
        return au._delete_part(setup_id, part_id, self.api_key)

    def __contains__(self, item: Union[str, tdo_simulations.Setup]) -> bool:
        """
        Allows checking if a setup id is in the API.

        Args:
            item (tdo.Setup): The setup name, id, or object.

        Returns:
            bool: True if the setup exists, False otherwise.
        """
        contains = False
        if isinstance(item, str):
            for setup in self:
                if setup.id == item:
                    contains = True
                    break
        elif isinstance(item, tdo_simulations.Setup):
            for setup in self:
                if setup.id == item.id:
                    contains = True
                    break
        return contains

    def __len__(self) -> int:
        '''
        Returns the number of setups in the API.
        '''
        return len(self.setups)

    def __iter__(self):
        """
        Iterates over the setups of the API.
        """
        return iter(self.setups)

    def __str__(self) -> str:
        '''
        Prints the API object and the setups it contains.
        '''
        string = f"Client with {len(self)} setups:\n"
        for setup in self:
            string += f"  - {setup.name} ({setup.id})\n"
        return string

    def __getitem__(self, key: str) -> tdo_simulations.Setup:
        """
        Args:
            key (str): The id of the requested setup.
        Returns:
            Setup (tdo.Setup): The requested Setup object.
        """
        # if isinstance(key, int):
        #     return self.setups[key]
        if isinstance(key, str):
            for setup in self:
                if setup.id == key:
                    return setup
            raise KeyError(f"Setup with id {key} not found.")
        raise TypeError(f"Invalid key type {type(key)}. Must be setup id.")

    def _initialize_setups(self):
        '''
        Private.
        Shouldn't be called directly. Initializes the setups property.
        '''
        self.setups = self._get_setups_info()
        if self.setups is not None:
            self.setups = [tdo_simulations.Setup._new(_api=self, setup_tuple=setup) for setup in self.setups]
        return self.setups

    def _get_surface(self, setup_id, surface_id, part_id):
        '''
        Private.
        Shouldn't be called directly. Returns the surface with the specified id.
        '''
        surface_data = au._get_surface(self.api_key, setup_id, surface_id, part_id)
        if surface_data[0] is None:
            raise Exception(f"Surface with id {surface_id} not found.")
        return surface_data[0]

    def _get_setups_info(self) -> list:
        """
        Private.
        Shouldn't be called directly. Returns a list of setups info.
        """
        try:
            data, message = au._get_setups(self.api_key)

            if data is None:
                self.init_error = message

            infos = []
            for info_json in data['setups']:
                infos.append((info_json['id'], info_json['name']))
            return infos
        except Exception as e:
            self.init_error = e
            return None

    def _get_setup_parts(self, setup_id: str) -> list:
        '''
        Private.
        Shouldn't be called directly. Returns a list of parts of the specified setup.
        '''
        parts = au._get_setup(setup_id, self.api_key)
        parts = parts[0]
        return parts

    def _get_part(self, part_id: str, setup_id) -> dict:
        '''
        Private.
        Shouldn't be called directly. Returns a dictionary of the specified part.
        '''
        part = au._get_part(setup_id,part_id,  self.api_key)
        if part[0] is None:
            raise Exception(f"Part with id {part_id} not found.")

        return part[0]

    def _extract_setup_object(self, setup):
        '''
        Private.
        Shouldn't be called directly. Returns the setup object from the specified setup.
        '''
        if isinstance(setup, str):

            if setup in self:
                setup_object = self[setup]
                return setup_object

            elif self.get(setup) is not None:
                setup_object = self.get(setup)
                return setup_object

            else:
                raise Exception(f"Setup with id or name {setup} not found.")

        if isinstance(setup, tdo_simulations.Setup):
            return setup

        if isinstance(setup, int):
            return self.setups[setup]

        raise TypeError(f"Invalid setup type {type(setup)}. Must be Setup object, name, index or id.")

    def _is_up(self) -> bool:
        """
        Calls _healthcheck and returns a boolean indicating if the server is up.

        Returns:
            bool: True if the server is up, False otherwise.
        """
        return au._healthcheck()[0]

    def _is_key_valid(self):
        '''
        Not implemented yet.
        '''
        return True

    def _update_part(self, setup_id: str, part: tdo_parts.Part) -> tuple:
        '''
        Modifies the part's data to the setup with that id.
        Args:
            setup_id (str): The id of the setup.
            part (Part): The part object to update.

        Returns:
            tuple: A tuple of (success, message), where:
                success (bool): True if the part was updated successfully, False otherwise.
                message (str): The message from the server.
        Raises:
            Exception: If the part was not updated successfully.
        '''
        data, message = au._change_part(setup_id, part.id, part._changes, self.api_key)

        if v.DEBUG:
            print(f'Success is: {data}')
            print(f'Message is: {message}')

        if data is None:
            raise Exception(message)
        return (data, message)

    def _run(self,
            setup: tdo_simulations.Setup
            ) -> tdo_analyses.RayTable:
        """
        Propagate the rays in the setup and returns a RayTable object.

        Args:
            setup (tdo.Setup): The setup to run.

        Returns:
            RayTable (tdo.analyses.RayTable): The RayTable object with the results.

        Raises:
            Exception: If the simulation failed.
        """
        setup_object = self._extract_setup_object(setup)

        data, message = au._run_simulation(setup_object.id, self.api_key)

        if data == None:
            raise Exception(message)
        if data['results']['error']['code'] != 0:
            raise Exception(v.SIMULATION_ERROR.format(message = data['results']['error']['message']))

        if data is not None:
            ray_table = data['results']['data']['ray_table']
            maps_url = data['maps_url']
            return tdo_analyses.RayTable(ray_table, maps_url, setup_object)
        else:
            raise Exception(message)

    def _run_async(self, setup: tdo_simulations.Setup):
        '''
        Not implemented yet.
        '''
        setup_object = self._extract_setup_object(setup)
        data, message = au._run_simulation(setup_object.id, self.api_key, is_sync = False)
        if data == None:
            raise Exception(message)
        if data['results']['error']['code'] != 0:
            raise Exception(v.SIMULATION_ERROR.format(message = data['results']['error']['message']))

        if data is not None:
            ray_table = data['results']['data']['ray_table']
            maps_url = data['maps_url']
            return tdo_analyses.RayTable(ray_table, maps_url, setup_object)
        else:
            raise Exception(message)

    def _run_batch_analyses(self,
                  analysis: tdo_analyses.Analysis,
                  configuration_csv_path, parts_id_list, parameters
                  ):
        """
        Run multiple analyses with csv file configuration
        """
        verifiers.BatchAnalysisVerifiers.validate_configurations_csv(configuration_csv_path, parts_id_list)
        verifiers.BatchAnalysisVerifiers.validate_analysis_limits(analysis)
        verifiers.BatchAnalysisVerifiers.validate_and_format_parameters(parameters)

        data,_ = au._run_batch_analyses(setup_id=analysis.surface._part._setup.id,
                                          analysis_id=analysis.id,
                                          configuration_csv_path = configuration_csv_path,
                                          api_key= self.api_key,
                                          parameters = parameters)
        if v.is_new_session == 'True':
            if data['results']['error']['code'] != 0:
                raise Exception(data['results']['error']['message'])
            else:
                return data ## temporary

        if v.is_new_session == 'False':
            return {'status': 'success', 'message': f'Analysis {analysis.id} ran successfully', 'data': data}


    def _run_batch(self,
                  setup: tdo_simulations.Setup,
                  configuration: dict
                  ):
        """
        Not implemented yet.
        """
        response = au._run_batch(setup.id, configuration, self.api_key)
        if response[0] is not None:
            json_ = response[0]
            json_['number_of_changes'] = configuration['number_of_changes']
            json_['simulation_file_prefix'] = configuration['simulation_file_prefix']
            job = tdo_simulations.Job._from_json(response[0], _api = self, _setup = setup)
            job._url = job._url.replace('$', '')
            self.jobs.append(job)
            return job
        else:
            raise Exception(response[1])

    def _run_analysis(self,
                     analysis: tdo_analyses.Analysis,
                     auto_add: bool = False,
                     force: bool = False
                     ) -> bool:
        if auto_add:
            self._add_analysis(analysis, force = force)
        data, _ =  au._run_analysis(setup_id=analysis.surface._part._setup.id, api_key=self.api_key, analysis_id=analysis.id)
        if v.is_new_session == 'True':
            if data['results']['error']['code'] != 0:
                raise Exception(data['results']['error']['message'])

            maps_url = data['maps_url']
            analysis._maps_json = requests.get(maps_url).json()

            if v.DEBUG:
                print(f'Maps json is {analysis._maps_json}')


            analysis_datos = data['results']['data']['analysis']
            analysis._urls = [data['url'] for data in analysis_datos]

            if v.DEBUG:
                print(f'Analysis urls is {analysis._urls}')

            analysis.results = analysis._process_results()

            return copy.deepcopy(analysis.results)

        if v.is_new_session == 'False':
            return {'status': 'success', 'message': f'Analysis {analysis.id} ran successfully', 'data': data}


    def _run_analyses(self,
                     analyses: list,
                     auto_add: bool = False,
                     force:bool = False
                     ):
        '''
        Private.
        '''
        ids = [analysis.id for analysis in analyses]
        setup_id = analyses[0].surface._part._setup.id

        response = {'success': [], 'failed': []}

        if not all([analysis.surface._part._setup.id == setup_id for analysis in analyses]):
            raise Exception(v.ANALYSES_NOT_SAME_SETUP_ERROR)

        if not auto_add and force:
            raise Exception("Force argument can only be used with auto_add argument")

        if auto_add:
            added_successfully = []
            added_failed = []

            for analysis in analyses:
                added = self._add_analysis(analysis, force = force)

                if added:
                    added_successfully.append((analysis, analysis.id))

                else:
                    print(f"Analysis {analysis.id} was failed to be added")
                    added_failed.append((analysis, analysis.id))

            response['added'] = added_successfully
            response['failed'] += added_failed
            ids = [analysis[1] for analysis in added_successfully]

        ran_successfully = []
        ran_failed = []

        if not all([analysis._added for analysis in analyses]):
            not_added = [analysis.id if analysis._added else None for analysis in analyses]
            raise Exception(v.ANALYSES_ADD_ERROR.format(not_added = not_added))

        data, message =  au._run_analyses(setup_id, self.api_key, ids)

        if data == None:
            raise Exception(message)

        for i, analysis in enumerate(analyses):
            is_successful = data['results']['error']['code'] == 0
            ran_successfully.append((analysis, analysis.id))
            if is_successful:
                analysis_datos = data['results']['data']['analysis']
                for data in analysis_datos:
                    url = data['url']
                    analysis._urls.append(url)
                analysis.results = analysis._process_results()
            else:
                ran_failed.append((analysis, analysis.id, data['results']['error']['message']))

        if len(ran_failed) > 0:
            messages = '\n'.join([f'Analysis {failed[1]}: {failed[2]}' for failed in ran_failed])
            raise Exception(v.ANALYSES_RUN_ERROR.format(message = messages))
        return analysis.results

    def _add_analysis(self,
                     analysis: tdo_analyses.Analysis,
                     force = False) -> bool:
        '''
        Adds the specified analysis to the setup.
        Args:
            analysis (tdo.Analysis): The analysis to add.
            force (bool): If True, adds the analysis to the setup even if identical analysis already exists.
            Default is False.
            Each analysis stores its result seperately.
            Filling the same analysis twice will result in larger user's memory resources consumption.
        Returns:
            bool: True if the analysis was added successfully, False otherwise.
        Raises:
            Exception:
                - If the server failed to respond.
                - If the analysis is duplicated and force is False.

        '''
        if analysis.id in [a.id for a in analysis.surface.analyses]:
            analysis._added = True
            return None

        if not force:
            is_duplicated = False
            duplicated = []

            for existing_analysis in analysis.surface.analyses:
                if analysis == existing_analysis:
                    is_duplicated = True
                    duplicated.append(analysis.id)
            if is_duplicated:
                raise Exception(v.ANALYSES_DUPLICATED_ERROR.format(duplicated = ", ".join(duplicated)))

        data = {
                "name": analysis.name,
                "num_rays": {laser.id: num for laser, num in analysis.rays.items()},
                "resolution": {"x": analysis.resolution[0], "y": analysis.resolution[1]},
                "type": 0 if analysis.fast == True else 1,
            }
        part = analysis.surface._part
        response = au._add_analyses(setup_id=part._setup.id,
                                    part_id=part.id,
                                    surface_id=analysis.surface.id,
                                    data=data,
                                    api_key=self.api_key)
        if response[1] == 'Analyses successfully added':
            return response[2]
        raise Exception(response[1])

    def _delete_analysis(self, setup_id, part_id, surface_id, analysis_id):
        '''
        Private.
        '''
        return au._delete_analysis(setup_id=setup_id, part_id=part_id, surface_id=surface_id, analysis_id=analysis_id, api_key=self.api_key)

    def optics_data(self, db_id: Union[str, tdo_parts.Part]):
        '''
        This function returns the optics data from the database.
        Args:
            db_id (str | Part): The database id of the optics or the Part object.

        Returns:
            dict: The optics data.
        '''

        # Get the db_id from the Part object if it is provided
        if isinstance(db_id, tdo_parts.Part):
            db_id = db_id.db_id

        r = au._get_optics_data(db_id = db_id, api_key = self.api_key)
        if r[0] is None:
            raise Exception(r[1])
        data = r[0][db_id]

        # Convert the data from category numbers to strings
        data['parameters']['shape'] = v.eOpticShape.OPTICS_SHAPE_MAP[data['parameters']['shape']]
        data['parameters']['baseShape'] = v.eBaseShape.BASE_SHAPE_MAP[data['parameters']['baseShape']]
        return data

    def _change_cs(self, setup_id, part_id, lcs_id, rcs_id):
        '''
        Private.
        This function changes the coordinate system of the part.
        Used by the Part object, this is a communication bridge.
        Args:
            setup_id (str): The id of the setup.
            part_id (str): The id of the part.
            lcs_id (str): The id of the local coordinate system.
            rcs_id (str): The id of the reference coordinate system.

        Returns:
            tuple: A tuple of (success, message), where:
                data (bool): True if the coordinate system was changed successfully, False otherwise.
                message (str): The message from the server.
        '''

        data = {
            "lcs": lcs_id,
        }
        if rcs_id != v.CoordinateSystems.WORLD:
            data['rcs'] = rcs_id

        return au._change_cs_data(setup_id=setup_id, part_id=part_id, data=data, api_key=self.api_key)

    def _change_scattering(self, setup_id, part_id, surface_id, scattering):
        '''
        This function changes the scattering data of the surface.
        Args:
            setup_id (str): The id of the setup.
            part_id (str): The id of the part.
            surface_id (str): The id of the surface.
            scattering (dict): The scattering data.

        Returns:
            tuple: A tuple of (data, message), where:
                data (bool): True if the scattering data was changed successfully, False otherwise.
                message (str): The message from the server.
        '''
        return au._change_scattering(setup_id=setup_id, part_id=part_id, surface_id=surface_id, data=scattering, api_key=self.api_key)

class Client(ThreedOptixAPI):
    '''
    This is the main class of the SDK.
    It is used to interact with the API and create the setups.
    It wraps ThreedOptixAPI from legacy reasons.
    '''
    def __init__(self, api_key: str, verbose: bool = True):
        super().__init__(api_key, verbose)
