import os
import tempfile
import logging
import requests
import time
from oslc4py_client.OSLCResource import OSLCResource
from oslc4py_client.helpers import create_object_from_class, find_rdf_root_class_namespace

class OSLCPythonClient:
    def __init__(self, root_url, port, accepted_responses=None, transient_responses=None):
        self.base_url = f"{root_url}:{port}"
        self.accepted_responses = accepted_responses if accepted_responses is not None else [200, 201]
        self.transient_responses = transient_responses if transient_responses is not None else [404]
        temp_dir = tempfile.gettempdir()
        log_file = os.path.join(temp_dir, 'oslc4py_client.log')

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)

            ch = logging.StreamHandler()
            ch.setLevel(logging.ERROR)

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

        self.logger.debug(f"OSLCPythonClient initialized with base_url: {self.base_url}")

    def post(self, endpoint: str, resource: OSLCResource, expected_outcome: OSLCResource = None,
             accepted_responses=None, transient_responses=None):
        url = f"{self.base_url}/{endpoint}"
        rdf_data = resource.serialize() 
        headers = {'Content-Type': 'application/rdf+xml'}
        self.logger.debug(f"Sending POST request to {url}")
        response = requests.post(url, data=rdf_data, headers=headers)
        self.logger.debug(f"Received response with status code {response.status_code} for POST request to {url}")
        return self.__process_response(
            response, 
            expected_outcome, 
            accepted_responses or self.accepted_responses, 
            transient_responses or self.transient_responses
        )

    def get(self, endpoint: str, expected_outcome: OSLCResource = None, 
            accepted_responses=None, transient_responses=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {'Accept': 'application/rdf+xml'}
        self.logger.debug(f"Sending GET request to {url}")
        response = requests.get(url, headers=headers)
        self.logger.debug(f"Received response with status code {response.status_code} for GET request to {url}")
        return self.__process_response(
            response, 
            expected_outcome, 
            accepted_responses or self.accepted_responses, 
            transient_responses or self.transient_responses
        )

    def __process_response(self, response, expected_outcome: OSLCResource, accepted_responses, transient_responses):
        if response.status_code in transient_responses:
            self.logger.warning(f"Received transient response {response.status_code} for URL {response.url}")
            return None
        if response.status_code not in accepted_responses:
            self.logger.error(f"Failed to process request to {response.url}. Status code: {response.status_code}")
            raise Exception(f"""Failed to process request. Status code: {response.status_code} \nResponse body: {response.text}""" )
        
        self.logger.debug(f"Processing response from {response.url}")
        
        if expected_outcome is None:
            class_namespace = find_rdf_root_class_namespace(response.text)
            obj = create_object_from_class(class_namespace)
            if obj:
                obj.deserialize(response.text)
                self.logger.debug(f"Deserialized response into object of type {type(obj).__name__}")
                return obj
            else:
                self.logger.error(f"Could not find class for {class_namespace}")
                raise Exception("Could not find class for ", class_namespace)
        else:
            expected_outcome.deserialize(response.text)
            self.logger.debug(f"Deserialized response into expected outcome of type {type(expected_outcome).__name__}")
            return expected_outcome
        
    def __default_status_check(self, resource):
        result = 'complete' in next(iter(resource.state)).lower()
        return result
    
    def poll(self, endpoint: str, expected_outcome: OSLCResource = None, condition: callable = None, 
             interval: int = 10, retries: int = 5, accepted_responses=None, transient_responses=None):
        accepted_responses = accepted_responses or self.accepted_responses
        transient_responses = transient_responses or self.transient_responses

        for attempt in range(retries):
            self.logger.info(f"Polling attempt {attempt + 1}/{retries} for endpoint {endpoint}...")

            response = self.get(endpoint, expected_outcome, accepted_responses, transient_responses)
            if response is None:
                continue
            if condition:
                if condition(response):
                    self.logger.info("Condition met. Resource found.")
                    return response
            else:
                if self.__default_status_check(response):
                    self.logger.info("Condition met. Resource found.")
                    return response
            self.logger.info(f"Condition not met. Retrying in {interval} seconds...")
            time.sleep(interval)
        self.logger.error(f"Polling failed for endpoint {endpoint}. Resource not found after max retries.")
        raise Exception("Polling failed. Resource not found after max retries.")
    
    def get_resource(self, endpoint, expected_resource = None, max_repeats=3, 
                                       wait_time_between_repeats=5, accepted_responses=None,
                                       transient_responses=None):
        accepted_responses = accepted_responses or self.accepted_responses
        transient_responses = transient_responses or self.transient_responses

        repeats = 0
        while repeats < max_repeats:
            self.logger.info(f"Attempt {repeats + 1}/{max_repeats} to get resource from endpoint {endpoint}")
            response = self.get(endpoint, expected_resource, accepted_responses, transient_responses)
            if response is None:
                self.logger.warning(f"Resource not found at endpoint {endpoint}. Retrying in {wait_time_between_repeats} seconds...")
                time.sleep(wait_time_between_repeats)
                repeats += 1
            else:
                self.logger.info(f"Resource obtained from endpoint {endpoint}")
                return response
        self.logger.error(f"Max retries reached for endpoint {endpoint}. Resource not found.")
        raise Exception("Max retries reached")