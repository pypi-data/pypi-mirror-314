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

"""
Leadscope Python Interface
==========================

Provides access to Leadscope Web Services REST API via Python. \
This is an interface client which requires access to a Leadscope Enterprise server, v2023.0.1 or later.

Available classes
-----------------
:class:`LSEClient`
    REST API client object containing connection details for the Leadscope server
:class:`StructureSet`
    Collection of structures for REST API queries
:class:`StructureSearch`
    Used to search for matching or similar structures from the server database or specific Leadscope projects
:class:`ModelApplication`
    Used to apply Leadscope models
:class:`NitrosamineAssessment`
    Used to used to run N-nitrosamine potency assessments

See the individual classes for detailed documentation.

Server sessions
---------------
Most server requests require an active session to be created via ``LSEClient.start_session``. Such sessions must be closed \
after use using ``LSEClient.end_session``. A preferable option is to use  ``LSEClient.with_session``, which creates a session \
and then closes it at the end, handling any exceptions which may be thrown, all examples will use this method. \
See the documentation for the classes ``LSEClient``, ``StructureSet``, ``StructureSearch``, ``ModelApplication`` and ``NitrosamineAssessment`` \
for a full list of which methods require a session to be open.

Examples
--------
Requesting a list of available statistical models from the Leadscope server::

    from lserest import LSEClient, StructureSet, ModelApplication
    client = LSEClient()

    def example1(c):
        c.list_models()
    
    client.with_session(example1)

Running a model application, specifically the ICH M7 Consensus, on two structures::

    from lserest import LSEClient, StructureSet, ModelApplication
    client = LSEClient()

    def example2(c, molfiles):
        structures = StructureSet(c, molfiles)
        model = ModelApplication(c, structures, consensus_names=['Genetox'])
        model.apply()
        return model
    
    model = client.with_session(example2, ['structure1.mol', 'structure2.mol'])
    
    print(model.consensus_results())
    
Searching the database for similar molecules to a given structure, downloading structural images of each search result
and saving them to a zip archive::

    from lserest import LSEClient, StructureSet, StructureSearch
    import numpy as np
    client = LSEClient()

    def example3(c):
        structures = StructureSet(c, molfile)
        search = StructureSearch(c, structures)
        search.similar(match_pct=70)
        c.save_structure_images(np.unique(search.results()['Structure ID']), 'search_results.zip')
    
    client.with_session(example3, 'structure.mol')

Running an N-nitrosamine potency assessment, on two structures::

    from lserest import LSEClient, StructureSet, NitrosamineAssessment
    client = LSEClient()

    def example4(c):
        structures = StructureSet(c, 'structure1.mol', 'structure2.mol')
        nitro = NitrosamineAssessment(c, structures)
        nitro.apply()
        return nitro
    
    nitro = client.with_session(example4)
    print(nitro.results())

Creating a StructureSet from mol strings::

    mol_string = '<mol string>'
    from lserest import LSEClient, StructureSet, NitrosamineAssessment
    client = LSEClient()
    structures = StructureSet(client)
    structures.mol_strings.append(mol_string)

"""

__all__ = ['LSEClient', 'StructureSet', 'ModelApplication', 'StructureSearch', 'NitrosamineAssessment']

from .lse_client import LSEClient
from .structure_set import StructureSet
from .model_application import ModelApplication
from .structure_search import StructureSearch
from .nitrosamine_assessment import NitrosamineAssessment