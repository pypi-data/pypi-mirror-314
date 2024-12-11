from datetime import datetime
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF
import inspect
from oslc4py_client.annotation_types.Occurs import Occurs
from oslc4py_client.annotation_types.ValueType import ValueType
from oslc4py_client.Link import Link
from oslc4py_client.helpers import create_object_from_class

class OSLCResource:
    def __init__(self, **kwargs):
        self.namespaces = {}
        self.uri = None
        self.warnings = []  
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def serialize(self, root_uri=None):
        graph = Graph()
        for prefix, uri in self.namespaces.items():
            graph.bind(prefix, Namespace(uri))
        root_node = URIRef(root_uri) if root_uri else URIRef(self.uri) if self.uri else BNode()
        self.serialize_inner(graph, root_node)

        return graph.serialize(format='pretty-xml', encoding='utf-8').decode('utf-8')

    def serialize_inner(self, graph, node):
        class_type = self.__class__

        graph.add((node, RDF.type, URIRef(self._oslc_namespace + class_type.__name__)))

        for name, obj in inspect.getmembers(class_type):
            if isinstance(obj, property):
                if hasattr(obj.fget, '_oslc_name'):
                    value = getattr(self, name)
                    occurs = getattr(obj.fget, '_oslc_occurs', Occurs.ZERO_OR_ONE)
                    if (value is None or value == set()) and occurs in [Occurs.EXACTLY_ONE, Occurs.ONE_OR_MANY]:
                        self.warnings.append(f"Property '{name}' is required but has no value during serialization.")
                        continue  # Skip adding this property since it has no value
                    if value is not None and value != set():
                        predicate = URIRef(obj.fget._oslc_property_definition)
                        if isinstance(value, list) or isinstance(value, set):
                            for item in value:
                                self._add_to_graph(graph, node, predicate, item, obj)
                        else:
                            self._add_to_graph(graph, node, predicate, value, obj)
                else:
                    raise Exception(f"oslc_name property not set, can't serialize value")
        return graph

    def _add_to_graph(self, graph, node, predicate, value, obj):
        if isinstance(value, OSLCResource):
            child_node = BNode()
            graph.add((node, predicate, child_node))
            value.serialize_inner(graph, child_node)
        elif hasattr(obj.fget, '_oslc_value_type') and obj.fget._oslc_value_type == ValueType.RESOURCE:
            if isinstance(value, Link):
                value = value.value 
            graph.add((node, predicate, URIRef(value)))
        else:
            graph.add((node, predicate, Literal(value)))

    def deserialize(self, rdfxml_string):
        graph = Graph()
        graph.parse(data=rdfxml_string, format='xml')

        for prefix, namespace in graph.namespaces():
            self.namespaces[prefix] = namespace

        target_class_uri = URIRef(f"{self._oslc_namespace}{self._oslc_name}")
        for s in set(graph.subjects(RDF.type, target_class_uri)):
            self.uri = s
            self.deserialize_inner(graph, s)

    def deserialize_inner(self, graph, node):
        class_type = self.__class__
        if isinstance(node, URIRef):
            self.uri = node
        for name, obj in inspect.getmembers(class_type):
            if isinstance(obj, property) and hasattr(obj.fget, '_oslc_name'):
                predicate = URIRef(obj.fget._oslc_property_definition)
                values = list(graph.objects(subject=node, predicate=predicate))
                occurs = getattr(obj.fget, '_oslc_occurs', Occurs.ZERO_OR_ONE)
                # Handle single or optional occurrence
                if occurs in [Occurs.EXACTLY_ONE, Occurs.ZERO_OR_ONE]:
                    if values:
                        value = values[0]
                        try:
                            value = self.deserialize_value(value, obj, graph)
                            setattr(self, name, value)
                        except Exception as e:
                            self.warnings.append(f"Failed to deserialize property '{name}': {e}")
                    elif occurs == Occurs.EXACTLY_ONE:
                        self.warnings.append(f"Property '{name}' is required but missing during deserialization.")
                # Handle multiple occurrences
                elif occurs in [Occurs.ZERO_OR_MANY, Occurs.ONE_OR_MANY]:
                    if values:
                        value_list = []
                        for v in values:
                            try:
                                value = self.deserialize_value(v, obj, graph)
                                value_list.append(value)
                            except Exception as e:
                                self.warnings.append(f"Failed to deserialize property '{name}': {e}")
                        setattr(self, name, value_list)
                    elif occurs == Occurs.ONE_OR_MANY:
                        self.warnings.append(f"Property '{name}' is required but missing during deserialization.")

    def deserialize_value(self, value, obj, graph):
        if hasattr(obj.fget, '_oslc_value_type'):
            value_type = obj.fget._oslc_value_type
            try:
                if value_type == ValueType.DATETIME:
                    value = datetime.fromisoformat(str(value))
                elif value_type == ValueType.RESOURCE:
                    value = str(value)
                elif value_type == ValueType.LOCALRESOURCE:
                    range_uri = obj.fget._oslc_range
                    nested_instance = create_object_from_class(range_uri)
                    if nested_instance is not None:
                        nested_instance.deserialize_inner(graph, value)
                        value = nested_instance
                else:
                    value = str(value)
            except Exception as e:
                self.warnings.append(f"Error converting value '{value}' for property '{obj.fget._oslc_name}': {e}")
                raise e
        return value
