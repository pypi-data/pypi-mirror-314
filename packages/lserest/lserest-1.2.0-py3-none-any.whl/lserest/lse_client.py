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

import requests
import time
import logging
import tomli

from http.client import HTTPConnection
from zipfile import ZipFile
import pandas as pd

from ._util import print_hierarchy, check_error, extract_json, lookup_recursive

class LSEClient:
    """
    :class:`LSEClient`
    ==================

    The LSEClient class is the basic Python client for access to the Leadscope Web Services.
    
    The package is designed to be used with the "public API methods", listed below, and the \
    additional classes: ``StructureSet``, ``StructureSearch``, ``ModelApplication`` and ``NitrosamineAssessment``. \
    However if desired, direct GET and POST requests can be sent via the \
    "direct REST API access methods".

    Most methods require a server session to be active, a session can be started using ``start_session``, \
    this must be subsequently ended with ``end_session``. In most cases it is preferable to use ``with_session`` \
    which starts and ends the session when done, including in the case of a thrown exception.

    Parameters
    ----------
    root_url : `str`
        (Optional) root URL for server, if not specified, the LSEClient looks for `config.toml` \
            in the current directory or specified location
    username : `str`
        (Optional) username for server, if not specified, the LSEClient looks for `config.toml` \
            in the current directory or specified location
    password : `str`
        (Optional) password for server, if not specified, the LSEClient looks for `config.toml` \
            in the current directory or specified location
    company : `str`
        (Optional) company name for server, if not specified, the LSEClient looks for `config.toml` \
            in the current directory or specified location
    config_file : `str`
        Location of `config.toml` file instead of setting above parameters (default: `config.toml`)
    

    Attributes
    -----------------
    session_id : `str`
        Session ID when an active session is open
    """

    def __init__(self, root_url:str=None, username:str=None, password:str=None, company:str=None, config_file='config.toml'):

        self.session_id = None
        
        self._debugging_enabled = False

        if not (root_url and username and password and company):
            with open(config_file, "rb") as f: server = tomli.load(f)['server']

        self.__root_url = root_url if root_url else server['root_url']
        self.__username = username if username else server['username']
        self.__password = password if password else server['password']
        self.__company = company if company else server['company']

        self.test_connection()

    # ---------------------------------------------------------------------------------------------------------------------------------
    # Server control methods
    # ---------------------------------------------------------------------------------------------------------------------------------

    def with_session(self, func:callable, enable_logging=False, **kwargs):
        """
        Starts a session, evaluates `func(self)`, and then ends the session, even if an error occurs.
        
        Parameters
        ----------
        func : callable
            A function with one parameter (this :class:`LSEClient`) to execute within the session
        enable_logging : bool
            True iff low level debugging should be enabled throughout the session
        **kwargs 
            Additional arguments to pass to func (these must all be provided as keyword arguments)
        
        Returns
        -------
        The result of `func(this)`
        """
        if enable_logging:
            self.debug_requests_on()
        try:
            result = None
            self.start_session()
            try:
                result = func(self,**kwargs)
            except BaseException:
                logging.exception("Exception thrown during REST session")
            finally:
                self.end_session()
        finally:
            if enable_logging:
                self.debug_requests_off()
            return result

    def start_session(self):
        """
        Starts a session and returns the ID that should be used for further requests.\
        Be certain to call `end_session()` when complete (even when an error occurs).\
        Consider using `with_session()` instead, which automatically closes the session.
        
        Returns
        -------
        The `str` identifier for the session
        """
        result_json = self.submit_post('/sessions', {
            'user': self.__username,
            'password': self.__password,
            'company': self.__company
        })
        self.session_id = result_json['lseSessionId']
        return self.session_id

    def end_session(self):
        """Ends the current session."""
        requests.delete(self.__root_url + "/sessions", headers=self._json_headers())
        self.session_id = None
        return True

    def check_session(self):
        """
        Retrieves details about the current session if available.
        
        Returns
        -------
        The decoded JSON session dict object
        """
        return self.submit_get('/sessions')
    
    def update_password(self, new_password:str):
        """
        Updates the password of the user in the current session to new_password and also internally\
        updates this client object to use the new password for future sessions. \
        This method requires an active session.

        Parameters
        ----------
        new_password : str
            The new password to be used by the user in the current session

        Returns
        -------
        True on success
        """
        if self.session_id:
            result_json = self.submit_post('/sessions/updatePassword', {
                'user': self.__username,
                'password': new_password,
                'company': self.__company
            })

            if result_json['success']: self.__password = new_password

            return result_json['success']
        else:
            logging.error("The method LSEClient.update_password requires a session to be opened (see LSEClient.with_session).")
    
    # ---------------------------------------------------------------------------------------------------------------------------------
    # Public API methods:
    # ---------------------------------------------------------------------------------------------------------------------------------

    def list_properties(self, structure_ids:list=None, verbose=False):
        """
        List the available properties to the console. Property details are given in the following format:
             └> propertyId: propertyName

        This method requires an active session.
        
        Parameters
        ----------
        structure_ids : [int] / [str]
            Optional list of structure IDs to limit to properties which have values for
        verbose : bool
            If set to true, `list_properties()` returns the full JSON response
        """
        if self.session_id:
            if type(structure_ids) != type(None):
                return self._list_hierarchy('/properties/hierarchyWithValues',
                                    structure_ids=[int(id) for id in structure_ids], verbose=verbose)
            else:
                return self._list_hierarchy('/properties', verbose=verbose)
        else:
            logging.error("The method LSEClient.list_properties requires a session to be opened (see LSEClient.with_session).")
    
    def lookup_property_id(self, property_path:list):
        """
        Find the ID of a specified property, if the property does not exist, returns `None`. \
        This method requires an active session.
        
        Parameters
        ----------
        property_path : list
            The full path for the property within the database, this must exactly match the hierarchy names
            (e.g. ['Published Models', 'Genetox Suite*', 'Gene Mutation', 'Microbial In Vitro', 'Bacterial Mutation'])

        Returns
        -------
        The ID for the specified property if it exists, `None` if not
        """
        if self.session_id:
            hierarchy = self.submit_get('/properties')
            return lookup_recursive(hierarchy, property_path)
        else:
            logging.error("The method LSEClient.lookup_property_id requires a session to be opened (see LSEClient.with_session).")
    
    def list_text_properties(self, structure_ids:list=None, verbose=False):
        """
        List the available text properties to the console. Property details are given in the following format:
             └> propertyId: propertyName

        This method requires an active session.
        
        Parameters
        ----------
        structure_ids : [int] / [str]
            Optional list of structure IDs to limit to properties which have values for
        verbose : bool
            If set to true, `list_text_properties()` returns the full JSON response
        """
        if self.session_id:
            if type(structure_ids) != type(None):
                return self._list_hierarchy('/text_properties/hierarchyWithValues',
                                    structure_ids=[int(id) for id in structure_ids], verbose=verbose)
            else:
                return self._list_hierarchy('/text_properties', verbose=verbose)
        else:
            logging.error("The method LSEClient.list_text_properties requires a session to be opened (see LSEClient.with_session).")
    
    def lookup_text_property_id(self, property_path:list):
        """
        Find the ID of a specified text property, if the property does not exist, returns `None`. \
        This method requires an active session.
        
        Parameters
        ----------
        property_path : list
            The full path for the property within the database, this must exactly match the hierarchy names
            (e.g. ['Published Models', 'Genetox Expert Alerts Suite', 'Gene Mutation', 'Microbial In Vitro', 'Bacterial Mutation Call'])

        Returns
        -------
        The ID for the specified textproperty if it exists, `None` if not
        """
        if self.session_id:
            hierarchy = self.submit_get('/text_properties')
            return lookup_recursive(hierarchy, property_path)
        else:
            logging.error("The method LSEClient.lookup_text_property_id requires a session to be opened (see LSEClient.with_session).")

    def list_models(self, verbose=False):
        """
        List the available models to the console. Model details are given in the following format:
             └> <[(key)LeadscopeProductName]> (key)modelId: (non-key)name

        This method requires an active session.
        
        Parameters
        ----------
        verbose : bool
            If set to true, `list_models()` returns the full JSON response
        """
        if self.session_id:
            return self._list_hierarchy('/modelApplication', print_item=self._print_model, verbose=verbose)
        else:
            logging.error("The method LSEClient.list_models requires a session to be opened (see LSEClient.with_session).")

    def list_consensuses(self, verbose=False):
        """
        List the available consensuses to the console. Consensus details are given in the following format:
             └> [(key)consensusName] (non-key)name

        This method requires an active session.
        
        Parameters
        ----------
        verbose : bool
            If set to true, `list_consensuses()` returns the full JSON response
        """
        if self.session_id:
            return self._list_hierarchy('/modelApplication/consensusHierarchy', verbose=verbose,
                                print_folder=lambda h, ind: print(f"{ind}{h['displayName']}:"),
                                print_item=lambda h, ind: print(f"{ind}[{h['keyName']}] {h['displayName']}")
            )
        else:
            logging.error("The method LSEClient.list_consensuses requires a session to be opened (see LSEClient.with_session).")
    
    def get_property_values(self, property_ids:list, structure_ids:list):
        """
        Gets the values of specified properties for a set of structures. \
        This method requires an active session.

        Parameters
        ----------
        property_ids : [int] / [str]
            A list of property IDs to list values of
        structure_ids : [int] / [str]
            A list of structure IDs to list property values of
        
        Returns
        -------
        A :class:`pandas.DataFrame` populated with property values.\
        If no value exists for a certain structure, the corresponding cell will contain `None`.
        """
        if self.session_id:
            property_values = self.submit_post('/properties/values', {
                'propertyIds': [int(id) for id in property_ids],
                'structureIds': [int(id) for id in structure_ids]
            })
            n_structs = len(structure_ids)
            structure_ids = [int(sid) for sid in structure_ids]
            data = {'Structure ID': structure_ids}
            for property in property_values:
                property_column = [None] * n_structs
                for value in property['values']:
                    property_column[structure_ids.index(value['structureId'])] = value['value']
                data[property['propertyName']] = property_column
                
            return pd.DataFrame(data)
        else:
            logging.error("The method LSEClient.get_property_values requires a session to be opened (see LSEClient.with_session).")
    
    def get_text_property_values(self, text_property_ids:list, structure_ids:list):
        """
        Gets the values of specified text properties for a set of structures. \
        This method requires an active session.

        Parameters
        ----------
        text_property_ids : [int] / [str]
            A list of text property IDs to list values of
        structure_ids : [int] / [str]
            A list of structure IDs to list property values of
        
        Returns
        -------
        A :class:`pandas.DataFrame` populated with text property values.\
        If no value exists for a certain structure, the corresponding cell will contain `None`.
        """
        if self.session_id:
            text_property_values = self.submit_post('/text_properties/values', {
                'propertyIds': [int(id) for id in text_property_ids],
                'structureIds': [int(id) for id in structure_ids]
            })
            n_structs = len(structure_ids)
            structure_ids = [int(sid) for sid in structure_ids]
            data = {'Structure ID': structure_ids}
            for property in text_property_values:
                property_column = [None] * n_structs
                for value in property['values']:
                    property_column[structure_ids.index(value['structureId'])] = value['value']
                data[property['propertyName']] = property_column

            return pd.DataFrame(data)
        else:
            logging.error("The method LSEClient.get_text_property_values requires a session to be opened (see LSEClient.with_session).")

    def get_structure_images(self, structure_ids:list, size=300, zip:str=None):
        """
        Return a collection of structure images as raw byte data. \
        Also saves images to zip archive if parameter `zip` is specified. \
        This method requires an active session.
        
        Parameters
        ----------
        structure_ids : [int] / [str]
            A list of structure IDs to collect images from
        size : int
            The size in pixels (square) to render the structure in (default: 300)
        zip : str
            File path for created zip archive (optional)
        
        Returns
        -------
            A :class:`pandas.DataFrame` populated with structure images as raw data (PNG format)
        """
        if self.session_id:
            images = []
            for id in structure_ids:
                try: image = self.submit_get(f'/structures/{id}/image?size={size}', return_type='bytes')
                except RuntimeError:
                    images.append(None)
                    logging.warning(f' Structure {id} not found')
                else: images.append(image)
            
            images = pd.DataFrame({'Structure ID': structure_ids, 'Image': images})

            if zip:
                try:
                    with ZipFile(zip, 'w') as zip_file:
                        for _, struct in images.iterrows():
                            if struct['Image']:
                                zip_file.writestr(f"structure_{struct['Structure ID']}.png", struct['Image'])
                except: logging.exception(f"Failed writing images to zip archive at {zip}")
            
            return images
        else:
            logging.error("The method LSEClient.get_structure_images requires a session to be opened (see LSEClient.with_session).")
    
    def get_study_summaries(self, structure_ids:list):
        """
        Gets study summaries for a set of structures. \
        This method requires an active session.

        Parameters
        ----------
        structure_ids : [int] / [str]
            A list of structure IDs to get summaries for
        
        Returns
        -------
        JSON response from server. The study summary for a the i-th structure can be converted to a :class:`pandas.DataFrame` via::
            pandas.DataFrame(results[i]['studySummaries'])
        where `results` is the output of `get_study_summaries`.
        """
        if self.session_id:
            ids_string = ','.join([str(sid) for sid in structure_ids])
            return self.submit_get(f'/structures/study_summaries?ids={ids_string}')
        else:
            logging.error("The method LSEClient.get_study_summaries requires a session to be opened (see LSEClient.with_session).")

    def get_toxml(self, structure_ids:list, zip:str=None):
        """
        Gets all ToxML content for a collection of structures by structure ID. \
        Also saves images to zip archive if parameter `zip` is specified. \
        This method requires an active session.

        Parameters
        ----------
        structure_ids : [int] / [str]
            A list of structure IDs to get ToxML content for
        zip : str
            File path for created zip archive (optional)
        
        Returns
        -------
        List of XML responses from server
        """
        if self.session_id:
            results = []
            for id in structure_ids:
                try: toxml = self.submit_get(f'/structures/{id}/content', return_type='bytes')
                except RuntimeError:
                    results.append(None)
                    logging.warning(f' Structure {id} not found')
                else: results.append({'structure_id': id, 'toxml': toxml})

            if zip:
                try:
                    with ZipFile(zip, 'w') as zip_file:
                        for toxml in results:
                            if toxml:
                                zip_file.writestr(f"toxml_{toxml['structure_id']}.xml", toxml['toxml'])
                except: logging.exception(f"Failed writing ToxML content to zip archive at {zip}")

            return results
        else:
            logging.error("The method LSEClient.get_toxml requires a session to be opened (see LSEClient.with_session).")
    
    def get_compound_info(self, structure_ids:list):
        """
        Gets higher level compound info for a collection of structures by structure ID. \
        This method requires an active session.

        Parameters
        ----------
        structure_ids : [int] / [str]
            A list of structure IDs to get compound info for
        
        Returns
        -------
        JSON response from server.
        """
        if self.session_id:
            results = []
            for id in structure_ids:
                try: compound_info = self.submit_get(f'/structures/{id}/compound_info')
                except RuntimeError:
                    results.append(None)
                    logging.warning(f' Structure {id} not found')
                else: results.append({'structure_id': id, 'compound_info': compound_info})

            return results
        else:
            logging.error("The method LSEClient.get_compound_info requires a session to be opened (see LSEClient.with_session).")

    # ---------------------------------------------------------------------------------------------------------------------------------
    # Direct REST API access methods:
    # ---------------------------------------------------------------------------------------------------------------------------------

    def submit_get(self, relative_url:str, json=None, return_type='json'):
        """
        Submits a GET request to the server at the relative url, optionally with JSON body content. \
        Checks the result for an error and throws a RuntimeError if found. \
        If an unknown return_type is specified, 'bytes' is used and a warning is printed to the log. \
        This method will usually require an active session.
        
        Parameters
        ----------
        relative_url : str
            The relative url for the request; e.g. '/sessions/task'
        json : dict, list, str, etc.
            (Optional) JSON object being submitted
        return_type : str
            The return type for the request ['json', 'string', 'bytes'] (default: json) 
        
        Returns
        -------
        The object returned from the server [dict, list, string, etc.]
        """
        response = requests.get(self.__root_url + relative_url, headers=self._json_headers(), json=json)
        if return_type == 'json': return extract_json(response)
        else: check_error(response, True)
        if return_type == 'string': return response.text
        elif return_type != 'bytes': logging.warning(f' Unknown return_type specified: {return_type}, raw response returned.')
        return response.content

    def submit_post(self, relative_url:str, json=None, return_type='json'):
        """
        Submits a POST request to the server at the relative url, optionally with JSON body content. \
        Checks the result for an error and throws a RuntimeError if found. \
        If an unknown return_type is specified, 'bytes' is used and a warning is printed to the log. \
        This method will usually require an active session.
        
        Parameters
        ----------
        relative_url : str
            the relative url for the request; e.g. '/sessions'
        json : dict, list, string, etc.
            (Optional) JSON object being submitted
        return_type : str
            The return type for the request ['json', 'string', 'bytes'] (default: json) 
        
        Returns
        -------
        The object returned from the server [dict, array, string, etc.]
        """
        response = None
        response = requests.post(self.__root_url + relative_url, headers=self._json_headers(), json=json)
        if return_type == 'json': return extract_json(response)
        else: check_error(response, True)
        if return_type == 'string': return response.text
        elif return_type != 'bytes': logging.warning(f' Unknown return_type specified: {return_type}, raw response returned.')
        return response.content
    
    def test_connection(self):
        """
        Tries to starts a session, confirms whether successful, and then ends the session, even if an error occurs.\
        If an error occurs, throws a verbose error.
        """
        root_url = self.__root_url.split("://")
        scheme = root_url[0]
        hostport = root_url[1].split("/")[0]

        try:
            requests.request('HEAD', f"{scheme}://{hostport}")
        except requests.exceptions.Timeout:
            logging.exception(f"Connection timeout from {scheme}://{hostport}.")
        except requests.exceptions.ConnectionError:
            logging.exception(f"Error connecting to {scheme}://{hostport}. Check the URL and port")
        else:
            try:
                self.start_session()
                self.check_session()
            except RuntimeError as e:
                logging.exception("Exception thrown creating REST session. Check username, password and company name fields.")
            except BaseException:
                logging.exception("Exception thrown creating REST session")
            finally:
                self.end_session()

    def check_task(self):
        """
        Returns the state of any currently running task.
        
        Returns
        -------
        The decoded JSON task state dict object
        """
        return self.submit_get('/sessions/task')

    def cancel_task(self):
        """Cancels the currently running task."""
        requests.delete(self.__root_url + "/sessions/task", headers=self._json_headers())

    def wait_for_task(self, progress_callback=None):
        """
        Checks the current task, and while running continues to check the task,\
        passing the state to progress_callback if given.
        
        Parameters
        ----------
        progress_callback : callable
            A progress reporting function, optional
        
        Returns
        -------
        The final decoded JSON task state dict object
        """
        state = self.check_task()
        while state['running']:
            if progress_callback is not None:
                progress_callback(state)
            time.sleep(2)
            state = self.check_task()
        return state

    def parse_molfile(self, molfile_path:str):
        """
        Parses the given molfile.
        
        Parameters
        ----------
        molfile_path : str
            Path to a mol or sd file
        
        Returns
        -------
        The list of dict parsed molfiles and errors
        """
        response = requests.post(self.__root_url + '/structure_util/parse_molfile',
            headers=self._multipart_headers(),
            files={'molfile': open(molfile_path, 'rb')})
        result_json = extract_json(response)
        return result_json

    def get_from_hierarchy_by_name(self, hierarchy, name):
        '''Get from hierarchy by name.'''
        results = {}
        if hierarchy.get('name') == name and 'id' in hierarchy:
            results[hierarchy['id']] = name
        if 'children' in hierarchy:
            for child in hierarchy['children']:
                child_results = self.get_from_hierarchy_by_name(child, name)
                results.update(child_results)
        return results

    def debug_requests_on(self):
        '''Switches on logging of the requests module.'''
        HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        self._debugging_enabled = True

    def debug_requests_off(self):
        '''Switches off logging of the requests module.'''
        HTTPConnection.debuglevel = 0
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.WARNING)
        root_logger.handlers = []
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)
        requests_log.propagate = False
        self._debugging_enabled = False
    
    # ---------------------------------------------------------------------------------------------------------------------------------
    # Internal methods
    # ---------------------------------------------------------------------------------------------------------------------------------

    def _json_headers(self):
        """
        Creates the headers for a json request. Includes the LSE session id if available.
        
        Returns
        -------
        The headers dict
        """
        if self.session_id is not None:
            return {'Content-Type': 'application/json', 'lseSessionId': self.session_id}
        else:
            return {'Content-Type': 'application/json'}

    def _multipart_headers(self):
        """
        Creates the headers for a multi-part request (i.e. no Content-Type header since requests will generate it).\
        Includes the LSE session id if available
        
        Returns
        -------
        The headers dict
        """
        if self.session_id is not None:
            return {'lseSessionId': self.session_id}
        else:
            return {}
    
    def _print_model(self, hierarchy, indent_str):
        try: print(f"{indent_str}[{hierarchy['leadscopeProductName']}] {hierarchy['id']}: {hierarchy['name']}")
        except: print(f"{indent_str}{hierarchy['id']}: {hierarchy['name']}")
    
    def _list_hierarchy(self, get_string, structure_ids=None, print_folder:callable=lambda h, ind: print(f"{ind}{h['name']}:"),
                    print_item:callable=lambda h, ind: print(f"{ind}{h['id']}: {h['name']}"), verbose=False):
        """
        List a given hierarchy.
            
        Parameters
        ----------
        client : lserest.LSEClient
            An LSEClient object
        get_string : str
            The REST GET request string (not including the root_url)
        print_folder : callable
            The function for printing folder details
        print_item : callable
            The function for printing item details
        """
        if structure_ids: hierarchy = self.submit_post(get_string, { 'structureIds': structure_ids })
        else: hierarchy = self.submit_get(get_string)
        print_hierarchy(hierarchy, print_folder=print_folder, print_item=print_item)
        if verbose: return hierarchy
