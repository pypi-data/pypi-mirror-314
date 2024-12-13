import json
from typing import List
from dataclasses import dataclass

@dataclass
class APIResultType:
    method_name:    str
    data:           str
    format:         str

class BaseAPI:
    '''
    Each manufacturer's API offers different methods. In order to
    know which methods are available at execution time, dictionaries
    of available API calls must be offered by the "methods" variable.
    For example:

    >> obj.methods

    [
        {
            'method_name': 'get_user_data',
            'method': self.get_user_data,
            'format': 'json'
        },
        {
            'method_name': 'get_usage_report',
            'method': self.get_usage_report,
            'format': 'csv'
        }
    ]
    
    the "self.methods" class variable must list all the methods which
    retrieve data fom API calls, as well as their return format. Its
    format is as follows:
    [
        {
            'method_name': <method name as string>,
            'method': <pointer to method>,
            'format': <format as string>
        }
        ...
    ]

    the "methods" variable must be instanced within a bound method,
    so that each entry may be properly bound and thus, callable.
    '''
    def methods(self):
        pass

    '''
    The "required_info" variable holds a list of data needed
    for connection. This list contains tuples representing the
    information's name and its type, respectively. For example:

    >> obj.required_info

    [
        ("username", "str"),
        ("password", "str"),
        ("id", "int")
    ]

    After a call to required_info yields this data, the object's
    user knows how to properly call the connect method:

    obj.connect(username="some_username",
                password="some_password",
                id=42)
    '''
    required_info = []


    def connect(self, **kwargs):
        '''
        The "connect" method is responsible for authenticating the API
        and should be implemented accordingly for each specific
        manufacturer. Arguments must be the data required for 
        authentication i.e. credentials or key files. The authentication
        process' result should be stored withing the object, so that
        ideally each object stays authenticated as long as it exists.
        '''
        pass

    def run_with_defaults(self, use_methods = []) -> List[APIResultType]:
        if len(use_methods) == 0:
            use_methods = [method["method_name"] for method in self.methods()]

        filtered_methods = [method for method in self.methods() if method["method_name"] in use_methods]

        for method in filtered_methods:
            rawdata = method['method']()
            api_result = APIResultType(
                method['method_name'],
                self.serialize(rawdata, method['format']),
                method['format']
            )
            yield api_result

    def serialize(self, data: any, input_format: str) -> str:
        if input_format == 'json':
            return json.dumps(data)
        elif input_format == 'list_csv':
            return self.serialize_csv_list(data)
        elif input_format == 'csv':
            return data

    def serialize_csv_list(self, data: List[tuple]) -> str:
        serialized_list = ''
        for pair in data:
            serialized_list += pair[0] + '|#' + pair[1] + '|$'
        return serialized_list.strip('|$')
