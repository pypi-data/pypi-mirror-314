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

from . import LSEClient, StructureSet
from ._util import print_progress, DataFrameBuilder, check_task_error

import logging

class ModelApplication:
    """
    :class:`ModelApplication`
    =========================

    The ModelApplication class is used to apply statistical models and consensuses via the Leadscope Python Interface.

    The ``apply`` method requires a server session to be active, a session can be started using ``start_session``, \
    this must be subsequently ended with ``end_session``. In most cases it is preferable to use ``with_session`` \
    which starts and ends the session when done, including in the case of a thrown exception.


    Parameters
    ----------
    client : :class:`lserest.LSEClient`
        An :class:`LSEClient` object containing server connection details
    structures : :class:`lserest.StructureSet`
        A :class:`StructureSet` containing the structures to apply the models to
    consensus_names : `[str]`
        A list of consensuses to run, can be listed via `LSEClient.list_consensuses()` (default: `[]`)
    model_ids : `[int]` / `[str]`
        A list of model IDs for models to run, can be listed via `LSEClient.list_models()` (default: `[]`)
    product_names : `[str]`
        A list of Leadscope product names for models to run, can be listed via `LSEClient.list_models()` (default: `[]`)
    exclude_images : `bool`
        Don't return images from the server (default: `True`)
    image_size : `int`
        The size (square) in pixels for images if returned (default: 50)
    progress_callback : `callable`
        A progress reporting function (optional: prints to console if not specified)
    
    Attributes
    ----------
    json_results : JSON
        Results for the models and consensuses which have been run, populated by ``apply``
    """

    def __init__(self, client:LSEClient, structures:StructureSet, consensus_names:list=[], model_ids:list=[], product_names:list=[],
                 exclude_images:bool=True, image_size:int=50):

        self._client = client
        self.structures = structures

        self.consensus_names = consensus_names
        self.model_ids = model_ids
        self.product_names = product_names
        self.exclude_images = exclude_images
        self.image_size = image_size
        
        self.json_results = None
    
    # ---------------------------------------------------------------------------------------------------------------------------------
    # Public API methods:
    # ---------------------------------------------------------------------------------------------------------------------------------
    
    def apply(self, progress_callback=print_progress):
        """
        Apply one or more models, including consensus results if relevant. \
        This method requires an active session.

        This is a long task, the parameter `progress_callback` can be set to use a custom progress reporting function.

        This saves the returned JSON to `self.json_results`, consensus and model results can then also be obtained via \
        `consensus_results() and `model_results()`.

        Warning: if `apply()` is re-run, the results are overwritten, not appended to.

        Parameters
        ----------
        progress_callback : callable
            A progress reporting function (optional: prints to console if not specified)
        """
        if self._client.session_id:
            self._client.submit_post('/modelApplication/start', {
                'molfiles': self.structures.mol_strings,
                'leadscopeProductNames': self.product_names,
                'modelInfoIds': self.model_ids,
                'consensusNames': self.consensus_names,
                'excludeImages': self.exclude_images,
                'imageSize': self.image_size
            })

            state = self._client.wait_for_task(progress_callback)
            if state['complete']: self.json_results = self._client.submit_get('/modelApplication/results')
            else: check_task_error(state)
        else:
            logging.error("The method ModelApplication.apply requires a session to be opened (see LSEClient.with_session).")
    
    def model_results(self):
        """
        Gets model results for the models which have been run, must have first called `apply()`.

        Returns
        -------
        A :class:`pandas.DataFrame` of model results
        """
        model_data = DataFrameBuilder(len(self.json_results))
        for i, app_result in enumerate(self.json_results):
            model_data.add_name(i, app_result['name'])
            for model in app_result['results']:
                if 'prediction' in model:
                    if 'call' in model['prediction']:
                        model_data.add_result(i, model['prediction']['call'], f"{model['name']} Call")
                    if 'positiveProbability' in model['prediction']:
                        model_data.add_result(i, model['prediction']['positiveProbability'], f"{model['name']} Probability")
                    if 'prediction' in model['prediction']:
                        model_data.add_result(i, model['prediction']['prediction'], f"{model['name']} Prediction")
                    if 'referenceExperimentalValue' in model['prediction']:
                        model_data.add_result(i, model['prediction']['referenceExperimentalValue'], f"{model['name']} Ref. Expt. Value")
                    if 'matchingPositiveAlerts' in model['prediction']:
                        model_data.add_result(i, ', '.join(model['prediction']['matchingPositiveAlerts']), f"{model['name']} Matching Positive Alerts")

        return model_data.df()
    

    def consensus_results(self):
        """
        Gets consensus results for the consensuses which have been run, must have first called `apply()`.

        Returns
        -------
        A :class:`pandas.DataFrame` of consensus results
        """
        consensus_data = DataFrameBuilder(len(self.json_results))
        for i, app_result in enumerate(self.json_results):
            consensus_data.add_name(i, app_result['name'])
            for consensus in app_result['consensusResults']:
                if 'result' in consensus:
                    consensus_data.add_result(i, consensus['result'], f"{consensus['name']} Result")
                if 'explanation' in consensus:
                    consensus_data.add_result(i, consensus['explanation'], f"{consensus['name']} Explanation")
            
        return consensus_data.df()
    
    # ---------------------------------------------------------------------------------------------------------------------------------
    # Internal methods
    # ---------------------------------------------------------------------------------------------------------------------------------
    
    def _apply(self, progress_callback, client:LSEClient):
        client.submit_post('/modelApplication/start', {
            'molfiles': self.structures.mol_strings,
            'leadscopeProductNames': self.product_names,
            'modelInfoIds': self.model_ids,
            'consensusNames': self.consensus_names,
            'excludeImages': self.exclude_images,
            'imageSize': self.image_size
        })

        state = client.wait_for_task(progress_callback)
        if state['complete']: self.json_results = client.submit_get('/modelApplication/results')
        else: check_task_error(state)



        