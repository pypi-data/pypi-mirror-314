import logging
import ibm_aigov_facts_client._wrappers.requests as requests


from ..utils.client_errors import *
from typing import BinaryIO, Dict, List, Any, Sequence

from ibm_aigov_facts_client.client import fact_trace

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator, CloudPakForDataAuthenticator
from ibm_aigov_facts_client.utils.constants import *
from ibm_aigov_facts_client.utils.config import *



_logger = logging.getLogger(__name__)


class Utils:

    def __init__(self, facts_client: 'fact_trace.FactsClientAdapter'):
        self._is_cp4d = facts_client._is_cp4d
        self._facts_client = facts_client
        if self._is_cp4d:
            self._cpd_configs = facts_client.cp4d_configs
            self._cp4d_version = facts_client._cp4d_version
  


    def get_cloud_object_storage_instances(self) -> List[Dict]:
        """
        Retrieves a list of cloud object storage instances.

        This method queries and returns information about all cloud object storage instances available in IBM Cloud.

        .. warning::
            **Note:**
            This method is applicable only in IBM Cloud and is not available in the Watsonx Governance platform.

        Returns:
            List[Dict]: A list of dictionaries, where each dictionary represents a cloud object storage instance
                        with the following keys:
                        
                        - Name: The name of the cloud object storage instance.
                        - GUID: The globally unique identifier (GUID) of the instance.
                        - Created ID: The identifier of the creation event.
                        - Creator Name: The name of the creator of the instance.


        Example:
            >>> storage_instances = obj.get_cloud_object_storage_instances()
            >>> for instance in storage_instances:
            >>>     print(instance['Name'], instance['GUID'])
        
        """
        
        if self._is_cp4d:
            raise ClientError("This method is not allowed in the on-prem environment")
        try:
            # Send the GET request
            _ENV = get_env()
            resource_url = RESOURCES_URL_MAPPING_NEW.get(_ENV)
            if not resource_url:
                raise ValueError("Resource URL for environment is not defined")
            
            response = requests.get(resource_url, headers=self._get_headers())
            
            # Check the status code
            if response.status_code == 200:
                data = response.json() 
                instances = []
                for resource in data.get('resources', []):
                    resource_id = resource.get('id', '')
                    if ':cloud-object-storage' in resource_id:
                        name = resource.get('name', 'Not Available')
                        guid = resource.get('guid', 'Not Available')
                        created_id = resource.get('created_by', 'Not Available')
                        creator_name = self._fetch_user_name(created_id)
                        
                        instances.append({
                            'Name': name,
                            'GUID': guid,
                            'Created ID': created_id,
                            'Creator Name': creator_name
                        })
                
                return instances
            else:
                _logger.error(f"Failed to fetch data. Status code: {response.status_code}")
                return []

        except Exception as e:
            _logger.error(f"An error occurred while fetching cloud object storage instances: {e}")
            return []
    

        # utils============================

    def _get_headers(self):
        token = self._facts_client._authenticator.token_manager.get_token() if (isinstance(self._facts_client._authenticator, IAMAuthenticator) or (
            isinstance(self._facts_client.authenticator, CloudPakForDataAuthenticator))) else self._facts_client.authenticator.bearer_token
        iam_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % token
        }
        return iam_headers
    
    def _fetch_user_name(self, user_id: str) -> str:
        try:
            user_profile_url = self._retrieve_user_profile_url(user_id)
            response = requests.get(user_profile_url, headers=self._get_headers())

            if response.status_code == 200:
                user_data = response.json()
                user_names = [
                    resource['entity'].get('name', 'N/A')
                    for resource in user_data.get('resources', [])
                    if resource.get('entity', {}).get('iam_id') == user_id
                ] or ['N/A']
                return user_names[0]
            else:
                _logger.error(f"Failed to fetch user profile for user ID '{user_id}'. "
                              f"Status code: {response.status_code}")
                return 'N/A'
        except Exception as e:
            _logger.error(f"An error occurred while fetching user profile: {e}")
            return 'N/A'
    
    def _retrieve_user_profile_url(self, external_model_admin: str) -> str:
        if self._is_cp4d:
            url = self._cpd_configs['url'] + \
                '/v2/user_profiles?q=iam_id%20IN%20'+external_model_admin
        else:
            if get_env() == 'dev':
                url = dev_config['DEFAULT_DEV_SERVICE_URL'] + \
                    '/v2/user_profiles?q=iam_id%20IN%20'+external_model_admin
            elif get_env() == 'test':
                url = test_config['DEFAULT_TEST_SERVICE_URL'] + \
                    '/v2/user_profiles?q=iam_id%20IN%20'+external_model_admin
            else:
                url = prod_config['DEFAULT_SERVICE_URL'] + \
                    '/v2/user_profiles?q=iam_id%20IN%20'+external_model_admin

        return url