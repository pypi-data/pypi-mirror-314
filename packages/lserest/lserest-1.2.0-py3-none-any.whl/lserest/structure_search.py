# Copyright 2024 Leadscope, Inc.; Instem LSS Ltd.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import pandas as pd

from ._util import print_progress, check_task_error
from . import LSEClient, StructureSet

class StructureSearch:
    """
    :class:`StructureSearch`
    ========================

    The ``StructureSearch`` class is used to search for matching or similar structures from the server database or
    specific Leadscope projects.

    The ``similar``, ``exact``, ``substructure``, ``family`` and ``by_names``, methods require a server session to be active, \
    a session can be started using ``start_session``, \
    this must be subsequently ended with ``end_session``. In most cases it is preferable to use ``with_session`` \
    which starts and ends the session when done, including in the case of a thrown exception.

    Parameters
    ----------
    client : :class:`lserest.LSEClient`
        An :class:`LSEClient` object containing server connection details
    structures : :class:`lserest.StructureSet`
        A :class:`StructureSet` containing the structures to search based on
    max_results : `int`
        Maximum number of results to return, ordered by similarity if limit reached (default: 1000)

    Attributes
    ----------
    json_results : JSON
        Search results, populated by ``similar``, ``exact``, `.`substructure``, ``family`` or ``by_names``
    """

    def __init__(self, client:LSEClient, structures:StructureSet=None, max_results=1000):

        self._client = client
        self.structures = structures
        self.max_results = max_results

        self.json_results = None

        self._type = None
        self._match_pct = None
        self._names = None
    
    # ---------------------------------------------------------------------------------------------------------------------------------
    # Public API methods:
    # ---------------------------------------------------------------------------------------------------------------------------------
    
    def similar(self, match_pct=30, progress_callback=print_progress):
        """
        Search for similar structures via Tanimoto index. The score is based on features - 100 % similarity does not mean an\
        exact match and a structure with no features will not be matched with anything, even exact matches. \
        This method requires an active session.

        This is a long task, the parameter `progress_callback` can be set to use a custom progress reporting function.

        This saves the returned JSON to `self.json_results`. Formatted results can then also be obtained with `results()`.
        
        Warning: if another search is run, the results are overwritten.

        Parameters
        ----------
        match_pct : int
            Minimum percentage similarity to be considered a match (default: 30 %)
        progress_callback : callable
            A progress reporting function (optional: prints to console if not specified)
        """
        if self._client.session_id:
            self._apply('Similarity', progress_callback, match_pct=match_pct)
        else:
            logging.error("The method StructureSearch.similar requires a session to be opened (see LSEClient.with_session).")
    
    def substructure(self, progress_callback=print_progress):
        """
        Search for substructures. \
        This method requires an active session.

        This is a long task, the parameter `progress_callback` can be set to use a custom progress reporting function.

        This saves search results to self.results. Warning: if another search is run, the results are overwritten.

        Parameters
        ----------
        progress_callback : callable
            A progress reporting function (optional: prints to console if not specified)
        """
        if self._client.session_id:
            self._apply('Substructure', progress_callback)
        else:
            logging.error("The method StructureSearch.substructure requires a session to be opened (see LSEClient.with_session).")
    
    def exact(self, progress_callback=print_progress):
        """
        Search for exact matches. \
        This method requires an active session.

        This is a long task, the parameter `progress_callback` can be set to use a custom progress reporting function.

        This saves search results to self.results. Warning: if another search is run, the results are overwritten.

        Parameters
        ----------
        progress_callback : callable
            A progress reporting function (optional: prints to console if not specified)
        """
        if self._client.session_id:
            self._apply('Exact', progress_callback)
        else:
            logging.error("The method StructureSearch.exact requires a session to be opened (see LSEClient.with_session).")
    
    def family(self, progress_callback=print_progress):
        """
        Search for family matches. \
        This method requires an active session.

        This is a long task, the parameter progress_callback can be set to use a custom progress reporting function.

        This saves search results to self.results. Warning: if another search is run, the results are overwritten.

        Parameters
        ----------
        progress_callback : callable
            A progress reporting function (optional: prints to console if not specified)
        """
        if self._client.session_id:
            self._apply('Family', progress_callback)
        else:
            logging.error("The method StructureSearch.family requires a session to be opened (see LSEClient.with_session).")
    
    def by_names(self, names:list, progress_callback=print_progress):
        """
        Search by structure name. This method does not use `self.structures`. \
        This method requires an active session.

        This is a long task, the parameter progress_callback can be set to use a custom progress reporting function.

        This saves search results to self.results. Warning: if another search is run, the results are overwritten.

        Parameters
        ----------
        names : [int] / [str]
            A list of structure names to search for
        progress_callback : callable
            A progress reporting function (optional: prints to console if not specified)
        """
        if self._client.session_id:
            self._names = names
            self._apply('names', progress_callback)
        else:
            logging.error("The method StructureSearch.by_names requires a session to be opened (see LSEClient.with_session).")

    def results(self):
        """
        Presents search results as a :class:`pandas.DataFrame`.

        Returns
        -------
        A :class:`pandas.DataFrame` of the search results
        """
        if self._type == None: return None
        elif self._type == "Similarity":
            search_data = {'Structure ID': [], 'Structure Name': [], 'Match': [], 'Similarity': []}
            for result in self.json_results['resultElements']:
                try:
                    for hit in result['hitTerms']:
                        split_hit = hit.split('(')
                        match = split_hit[0].strip()
                        similarity = float(split_hit[1].strip().strip(')'))
                        
                        if similarity*100 >= self._match_pct:
                            search_data['Structure ID'].append(result['structureId'])
                            search_data['Structure Name'].append(result['structureName'])
                            search_data['Match'].append(match)
                            search_data['Similarity'].append(similarity)
                except (KeyError, IndexError):
                    logging.warning("JSON issue in StructureSearch results")
        else:
            search_data = {'Structure ID': [], 'Structure Name': [], 'Match': []}
            for result in self.json_results['resultElements']:
                try:
                    for hit in result['hitTerms']:
                        search_data['Structure ID'].append(result['structureId'])
                        search_data['Structure Name'].append(result['structureName'])
                        search_data['Match'].append(hit)
                except (KeyError, IndexError):
                    logging.warning(" JSON issue in StructureSearch results")
        
        return pd.DataFrame(search_data)
    
    # ---------------------------------------------------------------------------------------------------------------------------------
    # Internal methods
    # ---------------------------------------------------------------------------------------------------------------------------------

    def _apply(self, type:str, progress_callback, match_pct=30):
        if type == 'names':
            self._client.submit_post('/structureSearch/ids', {
                'databaseID': True,
                'ids': self._names,
                'maxReturnCount': self.max_results
            })
        else:
            self._client.submit_post('/structureSearch/structure', {
                'type': type,
                'matchPercentage': match_pct,
                'maxReturnCount': self.max_results,
                'molfiles': self.structures.mol_strings
            })

        state = self._client.wait_for_task(progress_callback)
        if state['complete']:
            app_results = self._client.submit_get('/structureSearch/results')
            self._type = type
            self._match_pct = match_pct
            self.json_results = app_results
        else:
            check_task_error(state)