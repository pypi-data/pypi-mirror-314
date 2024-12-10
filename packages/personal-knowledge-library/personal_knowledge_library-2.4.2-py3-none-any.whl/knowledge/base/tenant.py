# -*- coding: utf-8 -*-
# Copyright © 2024-present Wacom. All rights reserved.
from typing import List


class TenantConfiguration:
    """
    Tenant configuration
    ====================

    This class represents the configuration of a tenant.
    The configuration includes the following properties:
        - identifier: str
        - ontology_name: str
        - ontology_version: int
        - is_locked: bool
        - name: str
        - rights: List[str]

    Parameters
    ----------
    identifier: str
        Identifier of the tenant
    ontology_name: str
        Name of the ontology
    ontology_version: int
        Version of the ontology
    is_locked: bool
        Flag to indicate if the tenant is locked
    name: str
        name of the tenant
    rights: List[str]
        List of rights
    vector_search_data_properties: List[str]
        List of vector search data properties which are used for vector search in the metadata
    vector_search_object_properties: List[str]
        List of vector search object properties which are used for vector search in the metadata
    content_data_property_name: str
        Name of the content data property which is used for vector search to index documents

    """
    def __init__(self, identifier: str, ontology_name: str, ontology_version: int,
                 is_locked: bool, name: str, rights: List[str],
                 vector_search_data_properties: List[str],
                 vector_search_object_properties: List[str],
                 content_data_property_name: str):
        # Constructor to initialize the properties
        self.__identifier = identifier
        self.__ontology_name = ontology_name
        self.__ontology_version = ontology_version
        self.__is_locked = is_locked
        self.__name = name
        self.__rights = rights
        self.__vector_search_data_properties = vector_search_data_properties
        self.__vector_search_object_properties = vector_search_object_properties
        self.__content_data_property_name = content_data_property_name

    @property
    def identifier(self):
        return self.__identifier

    @property
    def ontology_name(self):
        return self.__ontology_name

    @property
    def ontology_version(self):
        return self.__ontology_version

    @property
    def is_locked(self):
        return self.__is_locked

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def rights(self):
        return self.__rights

    @rights.setter
    def rights(self, value):
        self.__rights = value

    @property
    def vector_search_data_properties(self):
        return self.__vector_search_data_properties

    @vector_search_data_properties.setter
    def vector_search_data_properties(self, value):
        self.__vector_search_data_properties = value

    @property
    def vector_search_object_properties(self):
        return self.__vector_search_object_properties

    @vector_search_object_properties.setter
    def vector_search_object_properties(self, value):
        self.__vector_search_object_properties = value

    @property
    def content_data_property_name(self):
        return self.__content_data_property_name

    @content_data_property_name.setter
    def content_data_property_name(self, value):
        self.__content_data_property_name = value

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            identifier=data_dict.get('id'),
            ontology_name=data_dict.get('ontologyName'),
            ontology_version=data_dict.get('ontologyVersion'),
            is_locked=data_dict.get('isLocked'),
            name=data_dict.get('name'),
            rights=data_dict.get('rights'),
            vector_search_data_properties=data_dict.get('vectorSearchDataProperties'),
            vector_search_object_properties=data_dict.get('vectorSearchObjectProperties'),
            content_data_property_name=data_dict.get('contentDataPropertyName')
        )

    def __repr__(self):
        return (f"TenantConfiguration(identifier='{self.identifier}', ontology_name='{self.ontology_name}', "
                f"ontology_version={self.ontology_version}, is_locked={self.is_locked}, "
                f"name='{self.name}', rights={self.rights}, "
                f"vector_search_data_properties={self.vector_search_data_properties}, "
                f"vector_search_object_properties={self.vector_search_object_properties}, "
                f"content_data_property_name='{self.content_data_property_name}')")
