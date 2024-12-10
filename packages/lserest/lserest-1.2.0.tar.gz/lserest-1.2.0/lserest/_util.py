# Copyright 2023 Leadscope, Inc.; Instem LSS Ltd.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
from json.decoder import JSONDecodeError

"""Utility classes and methods for lserest package"""

def print_hierarchy(hierarchy, indent=0, 
                    print_folder:callable=lambda h, ind: print(f"{ind}{h['name']}:"),
                    print_item:callable=lambda h, ind: print(f"{ind}{h['id']}: {h['name']}")):
    """
    Recursively print a given hierarchy (to console by default).
        
    Parameters
    ----------
    hierarchy : dict
        The current node in the hierarchy
    indent : int
        The hierarchy depth of the current folder/item
    print_folder  :callable
        The function for printing folder details
    print_item : callable
        The function for printing item details
    """
    indent_str = '' if indent == 0 else '    '*(indent-1) + ' └> '
    if hierarchy['type'] == 'FOLDER':
        print_folder(hierarchy, indent_str)
        for child in hierarchy['children']: print_hierarchy(child, indent+1, print_folder, print_item)
    else: 
        print_item(hierarchy, indent_str)

def lookup_recursive(hierarchy, path):
    if not path: return None
    for node in hierarchy['children']:
        if node['name'] == path[0]:
            if node['type'] == 'FOLDER': return lookup_recursive(node, path[1:])
            elif len(path) == 1: return node['id']
            else: return None


def print_progress(state):
    """Display the progress of a task."""
    try: print(rf'Working ( {state["statusMessage"]} ) - {state["percentComplete"]} % complete')
    except: pass

class DataFrameBuilder:
    def __init__(self, n_rows):
        self._data = {'Name': [None]*n_rows}
        self.n_rows = n_rows
    
    def add_name(self, i, name):
        self._data['Name'][i] = name
    
    def add_result(self, i, datum, field_name):
        try: self._data[field_name][i] = datum
        except KeyError:
            self._data[field_name] = [None] * self.n_rows
            self._data[field_name][i] = datum
    
    def df(self):
        return pd.DataFrame(self._data)
    
# -------------------------------------------------------------------------------------------------------------------------------------
# Server response utility functions
# -------------------------------------------------------------------------------------------------------------------------------------


def extract_json(response):
    """
    Attempts to extract a decoded json object from the response, but only if the status code is 200 (successful)
    Raises a RuntimeError with the text of the response if the status code is anything else
        
    Parameters
    ----------
    response :
        A requests response object
    
    Returns:
    --------
        A decoded json object (dict, array, string, etc.)
    """
    if response.status_code == 200:
        json = response.json()
        check_error(json)
        return json
    else:
        raise RuntimeError("Error from server: " + response.text)

def check_task_error(json):
    """
    Checks a state object for an error raises an appropriate error if found
        
    Parameters
    ----------
    json : dict, list, string, etc.
        The decoded json response for a task state request (dict, array, string, etc.)
    """
    if 'error' in json and json['error'] is not None:
        check_error(json['error'])

def check_error(response, non_json=False):
    """
    Checks the result of a request to determine if an error has occurred.\
    If so, it Raises a RuntimeError containing the detailed message and stack trace from the server.\
    If not, returns with None.
        
    Parameters
    ----------
    json : dict, list, string, etc.
        The decoded json response from a server request
    non_json : bool
        If the supplied response has not been converted to json yet
    """
    if non_json:
        try: json = response.json()
        except JSONDecodeError: return None
    else: json = response
    if 'exception' in json and json['exception'] is not None:
        message = 'Exception from server: '
        if 'message' in json['exception']:
            message += json['exception']['message']
        if 'stackTrace' in json:
            message += '\n' + json['stackTrace']
        raise RuntimeError(message)