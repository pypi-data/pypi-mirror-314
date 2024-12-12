import requests
import logging
from time import sleep
from typing import List, Dict, Any

class TopomojoException(Exception):
    def __init__(self, status_code, response_message):
        self.status_code = status_code
        self.response_message = response_message
        super().__init__(f"Topomojo API Error - Status Code: {status_code}, Response: {response_message}")

class Topomojo:
    def __init__(self, app_url, api_key, debug:bool=False):
        self.app_url = app_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'accept': 'application/json', 'x-api-key': api_key})
        
        # Setup logger
        self.logger = logging.getLogger(__name__)
        
        if debug:
            self.logger.setLevel(logging.DEBUG)
            # Create console handler and set level to the provided log level
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            # Add formatter to ch
            ch.setFormatter(formatter)

            # Add ch to logger
            self.logger.addHandler(ch)
            self.logger.debug("Topomojo class initialized with logging enabled")
        else:
            self.logger.disabled = True

    ################################## TEMPLATE FUNCTIONS#####################################################################################
    def get_templates(self, WantsAudience=None, WantsPublished=None, WantsParents=None,
                      aud=None, pid=None, sib=None, Term=None,
                      Skip=None, Take=None, Sort=None, Filter=None):
        # Construct the full URL
        full_url = self.app_url + '/api/templates'  # Updated from api_url to app_url

        # Construct the parameters for the request
        params = {
            'WantsAudience': WantsAudience,
            'WantsPublished': WantsPublished,
            'WantsParents': WantsParents,
            'aud': aud,
            'pid': pid,
            'sib': sib,
            'Term': Term,
            'Skip': Skip,
            'Take': Take,
            'Sort': Sort,
            'Filter': Filter,
        }

        self.logger.debug(f"Getting templates with query params: {params}")
        # Make a GET request to the API endpoint with the provided parameters
        response = self.session.get(full_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)

    def update_template(self, changed_template:dict):
        # Construct the full URL for the specific template
        full_url = f"{self.app_url}/api/template"

        # Make a PUT request to the API endpoint with the provided changed_template_json
        self.logger.debug(f"Updating template with content {changed_template}")
        response = self.session.put(full_url, json=changed_template)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return True
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)


    def new_workspace_template(self, template_link_data:dict):
        # Construct the full URL
        full_url = self.app_url + '/api/template'

        self.logger.debug(f"Adding template with data {template_link_data}")

        # Make a POST request to the API endpoint with the provided template_link_data
        response = self.session.post(full_url, json=template_link_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)
        

    def unlink_template(self, template_link_data:dict):
        # Construct the full URL
        full_url = self.app_url + '/api/template/unlink'

        self.logger.debug(f"Unlinking Template {template_link_data}")
        # Make a POST request to the API endpoint with the provided template_link_data
        response = self.session.post(full_url, json=template_link_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)

    def get_template(self, template_id):
        # Construct the full URL
        full_url = f"{self.app_url}/api/vm-template/{template_id}"

        self.logger.debug(f"Getting template {template_id}")

        # Make a GET request to the API endpoint
        response = self.session.get(full_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)
        
    def get_template_detail(self, template_id):
        self.logger.debug(f"Loading template detail for template ID: {template_id}")
        # Construct the full URL
        full_url = f"{self.app_url}/api/template-detail/{template_id}"

        # Make a GET request to the API endpoint
        response = self.session.get(full_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)


    def initialize_template(self, template_id, wait=True):
        # Construct the full URL
        full_url = f"{self.app_url}/api/vm-template/{template_id}"

        self.logger.debug(f"Initializing template {template_id}")

        # Make a PUT request to the API endpoint
        response = self.session.put(full_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # if wait is true, then wait for the disk to be done initializing before returning
            if wait:
                while True: 
                    check = self.get_template(template_id)
                    if check['task']:
                        self.logger.debug(f"Initializing {check['task']['progress']}%")
                        sleep(1)
                    else: 
                        self.logger.debug(f"Done Initializing")
                        break
            # Return the integer response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)

    def deploy_vm_from_template(self, template_id):
        # Construct the full URL
        full_url = f"{self.app_url}/api/vm-template/{template_id}"

        self.logger.debug(f"Deploying VM template {template_id}")

        # Make a POST request to the API endpoint
        response = self.session.post(full_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)


    ################################## WORKSPACE FUNCTIONS#####################################################################################

    def get_workspaces(self, aud: str = None, scope: str = None, doc: int = None,
                    WantsAudience: bool = None, WantsManaged: bool = None,
                    WantsDoc: bool = None, WantsPartialDoc: bool = None,
                    Term: str = None, Skip: int = None, Take: int = None,
                    Sort: str = None, Filter: List[str] = None) -> List[Dict[str, Any]]:
        full_url = f"{self.app_url}/api/workspaces"
        params = {
            "aud": aud,
            "scope": scope,
            "doc": doc,
            "WantsAudience": WantsAudience,
            "WantsManaged": WantsManaged,
            "WantsDoc": WantsDoc,
            "WantsPartialDoc": WantsPartialDoc,
            "Term": Term,
            "Skip": Skip,
            "Take": Take,
            "Sort": Sort,
            "Filter": Filter
        }
        self.logger.debug(f"Calling get_workspaces API with params: {params}")

        response = self.session.get(full_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise TopomojoException(response.status_code, response.text)

    def create_workspace(self, new_workspace_data:dict):
        # Construct the full URL
        full_url = self.app_url + '/api/workspace'

        self.logger.debug(f"Creating workspace {new_workspace_data}")

        # Make a POST request to the API endpoint with the provided new_workspace_data
        response = self.session.post(full_url, json=new_workspace_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)

    def update_workspace(self, workspace_id:str, changed_workspace_data:dict):
        # Construct the full URL for the specific workspace
        full_url = f"{self.app_url}/api/workspace/{workspace_id}"

        self.logger.debug(f"Updating workspace {workspace_id} with content {changed_workspace_data}")

        # Make a PUT request to the API endpoint with the provided changed_workspace_data
        response = self.session.put(full_url, json=changed_workspace_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response (might be empty for successful updates)
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)
        
    def get_workspace_invite(self, workspace_id):
        self.logger.debug(f"Generating invitation code for workspace ID: {workspace_id}")
        # Construct the full URL
        full_url = f"{self.app_url}/api/workspace/{workspace_id}/invite"

        # Make a PUT request to the API endpoint
        response = self.session.put(full_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)
        
    def delete_workspace(self, workspace_id):
        self.logger.debug(f"Deleting workspace with ID: {workspace_id}")
        # Construct the full URL
        full_url = f"{self.app_url}/api/workspace/{workspace_id}"

        # Make a DELETE request to the API endpoint
        response = self.session.delete(full_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            self.logger.debug("Workspace deleted successfully")
            return response
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)
        

    def export_workspace(self, ids: List[str]) -> None:
        self.logger.debug(f"Exporting {len(ids)} workspaces with IDs: {ids}")
        # Construct the full URL
        full_url = f"{self.app_url}/api/admin/export"

        # Make a POST request to the API endpoint with the list of IDs in the body
        response = self.session.post(full_url, json=ids)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            self.logger.debug("Workspaces exported successfully")
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)



    ################################## GAMESPACE FUNCTIONS#####################################################################################

    def get_gamespaces(self, WantsAll:bool=None, WantsActive:bool=None,
                       Term: str=None, Skip:int=None, Take:int=None,
                       Sort:str=None, Filter:list=None):
        
        # Construct the full URL
        full_url = f"{self.app_url}/api/gamespaces"

        # Construct the query parameters
        params = {
            "WantsAll": WantsAll,
            "WantsActive": WantsActive,
            "Term": Term,
            "Skip": Skip,
            "Take": Take,
            "Sort": Sort,
            "Filter": Filter
        }

        self.logger.debug(f"Listing gamespaces with params: {params}")

        # Make a GET request to the API endpoint with the provided query parameters
        response = self.session.get(full_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)

    def stop_gamespace(self, gamespace_id:str):
        self.logger.debug(f"Stopping gamespace {gamespace_id}")
        # Construct the full URL
        full_url = f"{self.app_url}/api/gamespace/{gamespace_id}/stop"

        # Make a POST request to the API endpoint
        response = self.session.post(full_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)

    def complete_gamespace(self, gamespace_id:str):
        self.logger.debug(f"Completing gamespace {gamespace_id}")
        # Construct the full URL
        full_url = f"{self.app_url}/api/gamespace/{gamespace_id}/complete"

        # Make a POST request to the API endpoint
        response = self.session.post(full_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # If the request was not successful, raise a custom exception
            raise TopomojoException(response.status_code, response.text)
