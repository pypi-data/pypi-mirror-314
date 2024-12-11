import glob
import importlib
import os
import pkgutil

from rdflib import RDF, Graph

def find_class_in_modules(class_namespace: str, module_names: list):
    """
    Tries to load a class from a list of modules and checks for a matching class namespace.
    
    :param class_namespace: The full namespace of the class to load (module_name#class_name)
    :param module_names: A list of module names to search in
    :return: The loaded class, or None if not found
    """
    class_name = class_namespace.split('#')[1]

    for module_name in module_names:
        try:
            module = importlib.import_module(module_name)
            the_class = getattr(module, class_name, None)
            if the_class and getattr(the_class, '_oslc_resource_shape', None):
                if the_class._oslc_resource_shape.describes == class_namespace:
                    return the_class
        except (ModuleNotFoundError, AttributeError) as e:
            raise e

    return None


def find_class_file(class_name: str, root_directory: str):
    """
    Searches for a file named <class_name>.py in the given directory and its subdirectories.
    
    :param class_name: The name of the class (used as the filename)
    :param root_directory: The root directory to start searching from
    :return: The full path of the file if found, or None if not found
    """
    file_pattern = f"{class_name}.py"
    
    # Use glob to search for the file in the root_directory and its subdirectories
    for file_path in glob.glob(os.path.join(root_directory, '**', file_pattern), recursive=True):
        return file_path
    
    return None


def load_class_from_file(file_path: str, class_name: str):
    """
    Dynamically loads a class from a given file.
    
    :param file_path: The full path to the .py file
    :param class_name: The name of the class to load from the file
    :return: The loaded class, or None if the class cannot be found
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    cls = getattr(module, class_name, None)
    
    return cls


def create_object_from_class(class_namespace: str):
    """
    Finds the Python class from any installed module containing "oslc" in its name, 
    then instantiates the class dynamically.
    
    :param class_namespace: The namespace of the class to find and instantiate
    :return: An instance of the class, or None if not found
    """

    domain_directory = os.getenv('OSLC4PY_EXTRA_DOMAINS_DIR')
    domains = os.getenv('OSLC4PY_ACTIVE_INSTALLED_DOMAINS')
    
    if not domains or domains == '*':
        oslc_modules = [name for _, name, _ in pkgutil.iter_modules() if 'oslc' in name]
    else:
        oslc_modules = [domain.strip() for domain in domains.split(',')]
    
    cls = find_class_in_modules(class_namespace, oslc_modules)
    if cls:
        return cls()

    class_name = class_namespace.split('#')
    if domain_directory:
        file_path = find_class_file(class_name, domain_directory)
        if file_path:
            cls = load_class_from_file(file_path, class_name)
            if cls:
                return cls()
    return None

def find_rdf_root_class_namespace(rdfxml_string: str):
        """
        Takes an RDF/XML string and returns the root element (subject) if possible.
        The root element is defined as a subject that does not appear as an object
        in any triple in the RDF graph.
        
        :param rdfxml_string: The RDF/XML string to parse
        :return: The URI of the root element, or None if no root is found
        """
        graph = Graph()
        graph.parse(data=rdfxml_string, format="xml")
        
        subjects = set(graph.subjects())
        
        objects = set(graph.objects())
        
        root_candidates = subjects - objects
        for root in root_candidates:
            for _, _, rdf_type in graph.triples((root, RDF.type, None)):
                return rdf_type
        return None