import requests
from colorama import init, Fore, Style
import time
import json
import math
import numpy as np
from threed_optix.package_utils import vars as v
import pandas as pd
import threed_optix.package_utils.math as mu
import copy
import os

def verify_response(response):
    '''
    This function checkes if the response is valid.
    '''

    #If the response status code is not in the valid response codes, raise an exception.
    if int(response.status_code) not in v.VALID_RESPONSE_CODES:
        raise Exception(f'Error: {response.status_code} - {response.text}')
    return None


#General Purpose
def _healthcheck():
    """
    Checks if the server is up and well.
    """
    url = f'{v.API_URL}/healthcheck'

    r = requests.get(url)
    verify_response(r)
    r = r.json()
    return (r['status'] == 'SUCCESS', r['message'])

def _get(
    endpoint: str,
    api_key: str,
    #payload: dict = {}
    ):
    """
    Sends a GET request to the endpoint with the API key.

    Args:
        endpoint (str): The endpoint to send the request to.
        api_key (str): The API key.

    Returns:
        tuple: The data and message from the response.
    """

    url = f'{v.API_URL}/{endpoint}'
    headers = {'X-API-KEY': api_key,
               'Content-Type': 'application/json',
               "sdk-version": v.VERSION,
               'is_new_session': v.is_new_session}

    if v.DEBUG:
        print(f'GET {url}')
        print(f'Headers: {headers}')

    r = requests.get(url, headers=headers)
    verify_response(r)
    r = r.json()

    if v.DEBUG:
        print(f'Response: {r}')

    # Return the data if the status is SUCCESS, otherwise return None, and the message.
    return (r['data'] if 'status' in r and r['status'] == 'SUCCESS' else None, r['message'])

def _put(endpoint: str, api_key: str, json_data: dict = None):
    """
    Sends a PUT request to the endpoint.

    Args:
        endpoint (str): The endpoint to send the request to.
        json_data (dict): The JSON payload for the request.
        api_key (str): The API key.

    Returns:
        tuple: The data and message from the response.
    """
    url = f'{v.API_URL}/{endpoint}'
    headers = {'X-API-KEY': api_key,
               'Content-Type': 'application/json',
               "sdk-version": v.VERSION,
                'is_new_session': v.is_new_session}

    if v.DEBUG:
        print(f'PUT {url}')
        print(f'Headers: {headers}')
        print(f'Payload: {json_data}')

    r = requests.put(url, headers=headers, json=json_data)
    verify_response(r)
    r = r.json()

    if v.DEBUG:
        print(f'Response: {r}')

    # Return the data if the status is SUCCESS, otherwise return None, and the message.
    return (r['data'] if 'status' in r and r['status'] == 'SUCCESS' else None, r['message'])

def _put_batch(endpoint, api_key, data, configuration_csv_path):
    url = f'{v.API_URL}/{endpoint}'
    headers = {'X-API-KEY': api_key,
               "sdk-version": v.VERSION,
                'is_new_session': v.is_new_session}
    with open(configuration_csv_path, 'rb') as file:
        files = [('synthetic_data_csv', (os.path.basename(configuration_csv_path), file, 'text/csv'))]
        if v.DEBUG:
            print(f'PUT {url}')
            print(f'Headers: {headers}')
            print(f'Payload: {data}')
            print(f'File: {file}')

        r = requests.put(url, headers=headers, data=data,files=files)
        verify_response(r)
        r = r.json()

        if v.DEBUG:
            print(f'Response: {r}')

        return (r['data'] if 'status' in r and r['status'] == 'SUCCESS' else None, r['message'])

def _set(endpoint, data, api_key):
    '''
    Sends a POST request to the endpoint with the data and the API key.
    tbh, I don't know why it's seperated from the _post function.

    Args:
        endpoint (str): The endpoint to send the request to.
        data (dict): The data to send.
        api_key (str): The API key.

    Returns:
        tuple: The data and message from the response.
    '''
    url = f'{v.API_URL}/{endpoint}'
    headers = {'X-API-KEY': api_key,
               'Content-Type': 'application/json',
               "sdk-version": v.VERSION,
                'is_new_session': v.is_new_session}


    if v.DEBUG:
        print(f'SET {url}')
        print(f'Headers: {headers}')
        print(f'Payload: {data}')


    r = requests.post(url, headers=headers, json=data)

    verify_response(r)
    r = r.json()

    if v.DEBUG:
        print(f'Response: {r}')

    return ('status' in r and r['status'] == 'SUCCESS', r['message'])

def _post(endpoint, data, api_key):
    '''
    Sends a POST request to the endpoint with the data and the API key.

    Args:
        endpoint (str): The endpoint to send the request to.
        data (dict): The data to send.
        api_key (str): The API key.

    Returns:
        tuple: The status, message, and data from the response.
    '''
    url = f'{v.API_URL}/{endpoint}'
    headers = {'X-API-KEY': api_key,
               'Content-Type': 'application/json',
               "sdk-version": v.VERSION,
                'is_new_session': v.is_new_session}


    if v.DEBUG:
        print(f'POST {url}')
        print(f'Headers: {headers}')
        print(f'Payload: {data}')

    r = requests.post(url, headers=headers, json=data)
    verify_response(r)
    r = r.json()

    if v.DEBUG:
        print(f'Response: {r}')

    return ('status' in r and r['status'] == 'SUCCESS', r['message'], r.get('data', None))

def _delete(endpoint, api_key):
    '''
    Sends a DELETE request to the endpoint with the API key.

    Args:
        endpoint (str): The endpoint to send the request to.
        api_key (str): The API key.

    Returns:
        tuple: The status and message from the response.
    '''
    url = f'{v.API_URL}/{endpoint}'
    headers = {'X-API-KEY': api_key,
               'Content-Type': 'application/json',
               "sdk-version": v.VERSION,
                'is_new_session': v.is_new_session}

    if v.DEBUG:
        print(f'DELETE {url}')
        print(f'Headers: {headers}')

    r = requests.delete(url, headers=headers)
    verify_response(r)
    r = r.json()

    if v.DEBUG:
        print(f'Response: {r}')

    return ('status' in r and r['status'] == 'SUCCESS', r['message'])

def _create_setup(parameters, api_key):
    '''
    This function accesses the API create setup endpoint.
    '''
    endpoint = v.POST_CREATE_SETUP_ENDPOINT
    response = _post(endpoint, parameters, api_key)
    if not response[0]:
        raise Exception(response[1])
    return response[2]

def _delete_part(setup_id, part_id, api_key):
    '''
    This function accesses the API delete part endpoint.
    '''
    endpoint = v.DELETE_PART_ENDPOINT.format(setup_id=setup_id, part_id=part_id)
    return _delete(endpoint, api_key)

def _add_part(setup_id, data, api_key):
    '''
    This function accesses the API add part endpoint.
    '''
    endpoint = v.POST_ADD_PART_ENDPOINT.format(setup_id=setup_id)
    response = _post(endpoint,data,api_key)
    if not response[0]:
        raise Exception(response[1])
    return response[2]

def _get_setups(api_key: str):
    """
    Returns the list of setup names and ids of the user.

    Args:
        api_key (str): The API key.

    Returns:
        list: A list of setup names and ids.
    """
    endpoint = v.GET_SETUPS_ENDPOINT
    response = _get(endpoint, api_key)

    return response

def _get_setup(
    setup_id: str,
    api_key: str
    ):
    """
    Returns the opt file for the specified setup id.

    Args:
        setup_id (str): The setup id.
        api_key (str): The API key.

    Returns:
        str: The opt file content.
    """

    endpoint = v.GET_SETUP_ENDPOINT.format(setup_id=setup_id)

    return _get(endpoint, api_key)

def _get_surface(api_key, setup_id, surface_id, part_id):
    '''
    This function fetches the information of a surface.
    '''
    endpoint = v.Endpoints.GET_SURFACE_DATA.format(setup_id=setup_id, surface_id=surface_id, part_id=part_id)
    return _get(endpoint, api_key)

def _create_part(parameters, api_key):
    '''
    This function accesses the API create part endpoint.
    '''
    endpoint = v.POST_CREATE_OPTICS_ENDPOINT
    response = _post(endpoint, parameters, api_key)
    if not response[0]:
        raise Exception(response[1])
    return response[2]

def _get_part(setup_id: str, part_id: str, api_key: str):
    '''
    This function fetches the information of a part.
    '''
    endpoint = v.GET_PART_ENDPOINT.format(setup_id=setup_id, part_id=part_id)
    part =  _get(endpoint, api_key)
    return part

def _change_part(setup_id, part_id, data, api_key):
    '''
    This function accesses the API change part endpoint.
    '''

    # Copy the data to avoid changing the original data.
    data_copy = copy.deepcopy(data)

    # Convert the rotation to radians.
    if data.get('pose'):
        data_copy['pose']['rotation'] =[mu.deg_to_rad(x) for x in data_copy['pose']['rotation']]
    endpoint = v.PUT_PART_ENDPOINT.format(setup_id=setup_id, part_id=part_id)
    r = _put(endpoint=endpoint, api_key=api_key, json_data=data_copy)
    return r

def _delete_analysis(setup_id, part_id, surface_id,analysis_id, api_key):
    '''
    This function accesses the API delete analysis endpoint.
    '''
    endpoint = v.Endpoints.DELETE_ANALYSIS.format(setup_id=setup_id,
                                                 part_id=part_id,
                                                 analysis_id=analysis_id,
                                                 surface_id = surface_id)
    return _delete(endpoint, api_key)

def _run_async(setup_id, api_key):
    '''
    Not suppoerted anymore.
    '''
    endpoint =  v.PUT_SIMULATION_ENDPOINT.format(setup_id=setup_id)
    json_data = {
        "gpu_type": v.GPU_TYPE,
    }
    r = _put(endpoint = endpoint, json_data=json_data, api_key= api_key)
    return r

def _run_batch_analyses(setup_id, api_key, analysis_id, configuration_csv_path, parameters):

    endpoint = v.PUT_SIMULATION_ENDPOINT.format(setup_id=setup_id)
    data = {
        "gpu_type": v.GPU_TYPE,
        "is_sync": True,
        "analysis_id": analysis_id,
        "parameters":json.dumps(parameters) ## It has to be a json object else API rejects it
    }

    return _put_batch(endpoint=endpoint, api_key=api_key, configuration_csv_path=configuration_csv_path,data=data)

def _run_batch(
    setup_id: str,
    configuration: dict,
    api_key: str):
    """
    Not supported anymore.
    Puts the batch run request.

    Args:
        setup_id (str): The setup id.
        configuration (dict): The batch configuration.
        api_key (str): The API key.
    """
    endpoint = v.PUT_BATCH_CHANGES_ENDPOINT.format(setup_id=setup_id)
    return _put(endpoint = endpoint, api_key= api_key, json_data = configuration)

def _run_simulation(setup_id, api_key, is_sync = True):
    '''
    This function accesses the API run simulation endpoint for propagation.
    '''
    endpoint =  v.PUT_SIMULATION_ENDPOINT.format(setup_id=setup_id)
    json_data = {
        "gpu_type": v.GPU_TYPE,
        "is_sync": is_sync,
    }
    r = _put(endpoint = endpoint, json_data=json_data, api_key= api_key)
    return r

def _add_analyses(setup_id, part_id, surface_id, data, api_key):
    '''
    This function accesses the API add analysis endpoint.
    '''
    endpoint = v.POST_ADD_ANALYSIS_ENDPOINT.format(setup_id=setup_id, part_id=part_id, surface_id = surface_id)
    return _post(endpoint = endpoint,data=data, api_key = api_key)

def _run_analysis(setup_id: str, api_key: str, analysis_id: str):
    '''
    This function accesses the API run simulation endpoint to run an analysis.
    '''
    endpoint = v.PUT_SIMULATION_ENDPOINT.format(setup_id=setup_id)

    json_data = {
        "gpu_type": v.GPU_TYPE,
        "is_sync": True,
        "analysis_id": analysis_id,
    }

    return _put(endpoint = endpoint, json_data = json_data, api_key = api_key)

def _change_scattering(setup_id, part_id, surface_id, data, api_key):
    '''
    This function accesses the API change scattering endpoint.
    '''
    endpoint = v.Endpoints.SCATTERING.format(setup_id=setup_id, part_id=part_id, surface_id=surface_id)
    return _put(endpoint=endpoint, api_key=api_key, json_data=data)

def _get_optics_data(api_key, db_id):
    '''
    This function fetches the optics data.
    '''
    endpoint = v.Endpoints.GET_OPTICS_DATA.format(number_id=db_id)
    return _get(endpoint, api_key)

def _change_cs_data(setup_id, part_id, data, api_key):
    '''
    This function accesses the API change cs endpoint.
    '''
    endpoint = v.Endpoints.CHANGE_CS.format(setup_id=setup_id, part_id=part_id)
    return _put(endpoint=endpoint, api_key=api_key, json_data=data)

def _ask(conversation, api_key):
    '''
    Not implemented yet.
    This function accesses the API ask endpoint.
    It allows the user to ask questions to the SDK Assistant
    '''
    endpoint = v.GET_ANSWER_ENDPOINT
    headers = {'X-API-KEY': api_key}
    params = {'threed_optix_key': api_key, "conversation": json.dumps(conversation)}
    r = requests.get(endpoint, headers=headers, params=params)
    verify_response(r)
    r = r.json()
    return r['answer']

def _set_api_url(url, are_you_sure=False):
    '''
    Private.
    This function sets the API URL.
    It should be used internally to switch the API URL to dev or release.
    '''

    if not are_you_sure:
        raise Exception(v.SET_API_URL_WARNING)

    print(v.SET_API_URL_WARNING)
    print('Previous API URL was', v.API_URL)
    print('Setting API URL to', url)
    v.API_URL = url

def _get_materials(api_key, material_name):
    '''
    This function fetches the materials data based on the material name.
    '''
    endpoint = v.Endpoints.GET_MATERIALS_ENDPOINT.format(material_name=material_name)
    data, message = _get(endpoint, api_key)
    if data is None:
        raise Exception(message)
    return data

def _set_ask_url(url, are_you_sure=False):
    '''
    Not implemented yet.
    This function sets the ASK URL.
    It should be used internally to switch the ASK URL to dev or release.
    '''
    if not are_you_sure:
        raise Exception(v.SET_API_URL_WARNING)

    print(v.SET_API_URL_WARNING)
    print('Previous ASK URL was', v.ASK_URL)
    print('Setting ASK URL to', url)
    v.ASK_URL = url

def _welcome():
    '''
    Private.
    This is the function that prints the welcome message, when the client object is created.
    '''
    init(autoreset=True)
    color = Fore.WHITE
    print('******************')
    for i, char in enumerate(v.WELCOME_MESSAGE):
        print(f"{color}{char}", end="")
        time.sleep(0.01)  # Adjust the delay for the desired speed

    print(Style.RESET_ALL)  # Reset the style after the rainbow effect
    print('******************')

def _print_getting_parts():
    '''
    Deprecated.
    This function used to print a message when we fetched the parts information of the setup.
    It is no longer needed since we are not fetching the parts information all at once anymore.
    '''
    init(autoreset=True)
    color = Fore.WHITE
    print('******************')
    for i, char in enumerate(v.GETTING_PARTS_MESSAGE):
        print(f"{color}{char}", end="")
        time.sleep(0.01)  # Adjust the delay for the desired speed

    print(Style.RESET_ALL)  # Reset the style after the rainbow effect
    print('******************')

def _map_ray_table(rays_url, maps_url):
    '''
    This function creates a pandas dataframe from the rays data and maps the indices to the actual values.
    Args:
        rays_url (str): The URL to the rays data, recieved from the simulation results.
        maps_url (str): The URL to the maps data, recieved from the simulation results.

    Returns:
        pandas.DataFrame: The rays data with the indices mapped to actual values.
    '''

    # Fetch the rays data and the maps data.
    rays_df = pd.read_csv(rays_url)

    # This is probably useless, but I'm documenting when I don't have time to examine changes.
    rays_df = rays_df.copy()

    # Fetch the maps data.
    maps_json = requests.get(maps_url).json()

    # Set the index to the idx column.
    rays_df.set_index('idx', inplace=True)

    # Map the indices to the actual values.
    rays_df = rays_df.apply(lambda row: _map_ray_row(row, maps_json, rays_df), axis=1)

    rays_df.drop(['hit_surface_idx', 'wavelength_idx', 'source_idx'], inplace=True, axis=1)

    return rays_df

def _map_ray_row(row, map, ray_df):
    '''
    This is a helper function to map the indices to the actual values in the rays data per each row of the ray dataframe.
    '''
    # Map the surface thr ray originated from
    row['origin_surface'] = map['surfaces'][int(ray_df.iloc[int(row['parent_idx'])]['hit_surface_idx'])] if (row['parent_idx'] != -1 and ray_df.iloc[int(row['parent_idx'])]['hit_surface_idx'] != -1) else -1

    # Map the surface from indices to the actual id.
    row['surface'] = map['surfaces'][int(row['hit_surface_idx'])] if row['hit_surface_idx'] != -1 else -1

    # Map the wavelength from indices to the actual value.
    row['wavelength'] = map['wavelengths'][int(row['wavelength_idx'])]

    # Map the light source from indices to the actual light source id.
    row['light_source'] = map['sources'][int(row['source_idx'])]

    return row
