# -*- coding: utf-8 -*-
# Copyright © 2021-24 Wacom. All rights reserved.
from typing import List, Dict, Optional

import requests
from requests import Response

from knowledge.base.tenant import TenantConfiguration
from knowledge.services import DEFAULT_TIMEOUT
from knowledge.services.base import WacomServiceAPIClient, USER_AGENT_HEADER_FLAG, \
    CONTENT_TYPE_HEADER_FLAG, handle_error
from knowledge.services.graph import AUTHORIZATION_HEADER_FLAG


class TenantManagementServiceAPI(WacomServiceAPIClient):
    """
    Tenant Management Service API
    -----------------------------

    Functionality:
        - List all tenants
        - Create tenants

    This is service is used to manage tenants. Only admins can use this service, as it requires the secret key for
    tenant administration.

    Parameters
    ----------
    tenant_token: str
        Tenant Management token
    service_url: str
        URL of the service
    service_endpoint: str
        Base endpoint
    """

    TENANT_ENDPOINT: str = 'tenant'
    USER_DETAILS_ENDPOINT: str = f'{WacomServiceAPIClient.USER_ENDPOINT}/users'

    def __init__(self, tenant_token: str, service_url: str = WacomServiceAPIClient.SERVICE_URL,
                 service_endpoint: str = 'graph/v1'):
        self.__tenant_management_token: str = tenant_token
        super().__init__("TenantManagementServiceAPI", service_url=service_url, service_endpoint=service_endpoint)

    @property
    def tenant_management_token(self) -> str:
        """Tenant Management token."""
        return self.__tenant_management_token

    @tenant_management_token.setter
    def tenant_management_token(self, value: str):
        self.__tenant_management_token = value

    # ------------------------------------------ Tenants handling ------------------------------------------------------

    def create_tenant(self, name: str, create_and_apply_onto: bool = True,
                      rights: Optional[List[str]] = None,
                      vector_search_data_properties: Optional[List[str]] = None,
                      vector_search_object_properties: Optional[List[str]] = None,
                      content_data_property_name: str = "") -> Dict[str, str]:
        """
        Creates a tenant.

        Parameters
        ----------
        name: str -
            Name of the tenant
        create_and_apply_onto: bool
            Creates and applies the ontology.
        rights: List[str]
            List of rights for the tenant. They are encoded in the user token, e.g., "ink-to-text"
        vector_search_data_properties: List[str]
            List of data properties that are automatically added to meta-data of the vector search index documents.
        vector_search_object_properties: List[str]
            List of object properties that are automatically added to meta-data of the vector search index documents.
        content_data_property_name: str
            The data property that is used to indexing its content to the document index.

        Returns
        -------
        tenant_dict: Dict[str, str]
            Newly created tenant structure.
            >>>     {
            >>>       "id": "<Tenant-ID>",
            >>>       "apiKey": "<Tenant-API-Key>",
            >>>       "name": "<Tenant-Name>"
            >>>    }

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f'{self.service_base_url}{TenantManagementServiceAPI.TENANT_ENDPOINT}'
        headers: dict = {
            USER_AGENT_HEADER_FLAG: self.user_agent,
            AUTHORIZATION_HEADER_FLAG: f'Bearer {self.__tenant_management_token}',
            CONTENT_TYPE_HEADER_FLAG: 'application/json'
        }
        payload: dict = {
            "name": name,
            "rights": rights if rights else [],
            "vectorSearchDataProperties": vector_search_data_properties if vector_search_object_properties else [],
            "vectorSearchObjectProperties": vector_search_object_properties if vector_search_object_properties else [],
            "contentDataPropertyName": content_data_property_name
        }
        params: dict = {
            "createAndApplyOnto": create_and_apply_onto
        }
        response: Response = requests.post(url, headers=headers, json=payload, params=params,
                                           timeout=DEFAULT_TIMEOUT,
                                           verify=self.verify_calls)
        if response.ok:
            return response.json()
        raise handle_error("Creation of tenant failed.", response)

    def listing_tenant(self) -> List[TenantConfiguration]:
        """
        Listing all tenants configured for this instance.

        Returns
        -------
        tenants:  List[TenantConfiguration]
            List of tenants

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f'{self.service_base_url}{TenantManagementServiceAPI.TENANT_ENDPOINT}'
        headers: dict = {
            USER_AGENT_HEADER_FLAG: self.user_agent,
            AUTHORIZATION_HEADER_FLAG: f'Bearer {self.__tenant_management_token}'
        }
        response: Response = requests.get(url, headers=headers, data={}, timeout=DEFAULT_TIMEOUT,
                                          verify=self.verify_calls)
        if response.ok:
            return [TenantConfiguration.from_dict(tenant) for tenant in response.json()]
        raise handle_error("Listing of tenant failed.", response)

    def update_tenant_configuration(self, identifier: str, rights: List[str], vector_search_data_properties: List[str],
                                    vector_search_object_properties: List[str], content_data_property_name: str):
        """
        Update the configuration of a tenant.

        Parameters
        ----------
        identifier: str
            Tenant identifier.
        rights: List[str]
            List of rights for the tenant. They are encoded in the user token, e.g., "ink-to-text"
        vector_search_data_properties: List[str]
            List of data properties that are automatically added to meta-data of the vector search index documents.
        vector_search_object_properties: List[str]
            List of object properties that are automatically added to meta-data of the vector search index documents.
        content_data_property_name: str
            The data property that is used to indexing its content to the document index.
        """
        url: str = f'{self.service_base_url}{TenantManagementServiceAPI.TENANT_ENDPOINT}/{identifier}/rights'
        headers: dict = {
            USER_AGENT_HEADER_FLAG: self.user_agent,
            AUTHORIZATION_HEADER_FLAG: f'Bearer {self.__tenant_management_token}',
            CONTENT_TYPE_HEADER_FLAG: 'application/json'
        }
        payload: dict = {
            "rights": rights,
            "vectorSearchDataProperties": vector_search_data_properties,
            "vectorSearchObjectProperties": vector_search_object_properties,
            "contentDataPropertyName": content_data_property_name
        }
        response: Response = requests.patch(url, headers=headers, json=payload, timeout=DEFAULT_TIMEOUT,
                                            verify=self.verify_calls)
        if not response.ok:
            raise handle_error("Creation of tenant failed.", response)
