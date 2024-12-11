from oslc4py_client.annotation_types.CreationFactory import CreationFactory
from oslc4py_client.annotation_types.Dialog import Dialog
from typing import List

from oslc4py_client.annotation_types.Occurs import Occurs
from oslc4py_client.annotation_types.Representation import Representation
from oslc4py_client.annotation_types.ValueType import ValueType


def oslc_allowed_value(value: str):
    def decorator(func):
        func._oslc_allowed_value = value
        return func
    return decorator

def oslc_allowed_values(values: List[str]):
    def decorator(func):
        func._oslc_allowed_values = values
        return func
    return decorator

def oslc_creation_factory(factory: CreationFactory):
    def decorator(func):
        func._oslc_creation_factory = factory
        return func
    return decorator

def oslc_default_value(value: str):
    def decorator(func):
        func._oslc_default_value = value
        return func
    return decorator

def oslc_description(description: str):
    def decorator(func):
        func._oslc_description = description
        return func
    return decorator

def oslc_dialog(dialog: Dialog):
    def decorator(func):
        func._oslc_dialog = dialog
        return func
    return decorator

def oslc_dialogs(dialogs: List[Dialog]):
    def decorator(func):
        func._oslc_dialogs = dialogs
        return func
    return decorator

def oslc_hidden(hidden: bool):
    def decorator(func):
        func._oslc_hidden = hidden
        return func
    return decorator

def oslc_max_size(max_size: int):
    def decorator(func):
        func._oslc_max_size = max_size
        return func
    return decorator

def oslc_member_property(property: bool):
    def decorator(func):
        func._oslc_member_property = property
        return func
    return decorator

def oslc_name(name: str):
    def decorator(func):
        func._oslc_name = name
        return func
    return decorator

def oslc_namespace(namespace: str):
    def decorator(func):
        func._oslc_namespace = namespace
        return func
    return decorator

def oslc_namespace_definition(namespace_uri: str, prefix: str):
    def decorator(func):
        func._oslc_namespace_definition = type('', (), {})()
        func._oslc_namespace_definition.namespace_uri = namespace_uri
        func._oslc_namespace_definition.prefix = prefix
        return func
    return decorator

def oslc_not_query_result(not_query_result: bool):
    def decorator(func):
        func._oslc_not_query_result = not_query_result
        return func
    return decorator

def oslc_occurs(occurs: Occurs):
    def decorator(func):
        func._oslc_occurs = occurs
        return func
    return decorator

def oslc_property_definition(property_definition: str):
    def decorator(func):
        func._oslc_property_definition = property_definition
        return func
    return decorator

def oslc_query_capability(title: str, label: str = "", resourceShape: str = "", resourceTypes: list = [], usages: list = []):
    def decorator(func):
        func._oslc_query_capability = type('', (), {})()
        func._oslc_query_capability.title = title
        func._oslc_query_capability.label = label
        func._oslc_query_capability.resourceShape = resourceShape
        func._oslc_query_capability.resourceTypes = resourceTypes
        func._oslc_query_capability.usages = usages
        return func
    return decorator

def oslc_range(range: List[str]):
    def decorator(func):
        func._oslc_range = range
        return func
    return decorator

def oslc_rdf_collection_type(collectionType: str, namespaceURI: str):
    def decorator(func):
        func._oslc_rdf_collection_type = type('', (), {})()
        func._oslc_rdf_collection_type.collectionType = collectionType
        func._oslc_rdf_collection_type.namespaceURI = namespaceURI
        return func
    return decorator

def oslc_read_only(read_only: bool):
    def decorator(func):
        func._oslc_read_only = read_only
        return func
    return decorator

def oslc_representation(representation: Representation):
    def decorator(func):
        func._oslc_representation = representation
        return func
    return decorator

def oslc_resource_shape(describes, title:str):
    def decorator(func):
        func._oslc_resource_shape = type('', (), {})() 
        func._oslc_resource_shape.describes = describes
        func._oslc_resource_shape.title = title
        return func
    return decorator

def oslc_schema(schema):
    def decorator(func):
        func._oslc_schema = schema
        return func
    return decorator

def oslc_service(service: str):
    def decorator(func):
        func._oslc_service = service
        return func
    return decorator

def oslc_title(title:str):
    def decorator(func):
        func._oslc_title = title
        return func
    return decorator

def oslc_value_shape(value_shape:str):
    def decorator(func):
        func._oslc_value_shape = value_shape
        return func
    return decorator

def oslc_value_type(value_type: ValueType):
    def decorator(func):
        func._oslc_value_type = value_type
        return func
    return decorator