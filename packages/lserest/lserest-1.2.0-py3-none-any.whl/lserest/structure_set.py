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

from . import LSEClient
import logging

class StructureSet:
    """
    :class:`StructureSet`
    =====================

    The ``StructureSet`` class contains a set of structures to be used within the Leadscope Python Interface \
    and assorted related methods.

    The ``add_smiles`` and ``create_sar_forms`` methods require a server session to be active, a session can be started using ``start_session``, \
    this must be subsequently ended with ``end_session``. In most cases it is preferable to use ``with_session`` \
    which starts and ends the session when done, including in the case of a thrown exception.

    Parameters
    ----------
    client : :class:`lserest.LSEClient`
        An :class:`LSEClient` object containing server connection details
    *molfiles : `str` / `[str]`
        Variable number of structure files in mol/sd format, or a list of files

    Attributes
    ----------
    mol_strings : `[str]`
        List of structures in mol format
    """

    def __init__(self, client:LSEClient, *molfiles:str):
        self._client = client
        self.mol_strings = []
        self.add(*molfiles)
    
    # ---------------------------------------------------------------------------------------------------------------------------------
    # Public API methods:
    # ---------------------------------------------------------------------------------------------------------------------------------
    
    def add(self, *molfiles:str):
        """
        Add any number of molecules to the structure set via mol or sd files. \
        This method is used to add structures from files, if mol strings are to be added directly, \
        use ``this.mol_strings.append(***)``

        Parameters
        ----------
        *molfiles : str / [str]
            Variable number of structure files in mol/sd format, or a list of files
        """
        for molfile in molfiles:
            if type(molfile) is str:
                for mol in self._client.parse_molfile(molfile):
                    self.mol_strings.append(mol['molString'])
            elif type(molfile) is list:
                for mf in molfile:
                    if type(mf) is str:
                        for mol in self._client.parse_molfile(mf):
                            self.mol_strings.append(mol['molString'])
    
    def add_smiles(self, *smiles:str):
        """
        Add any number of structures to the structure set from SMILES strings. \
        This method requires an active session.

        Parameters
        ----------
        *smiles : str
            Variable number of structures as SMILES strings
        
        Returns
        -------
        A one-to-one list of the indices for the corresponding structures into the structure set. \
        If the SMILES string is invalid or another issue occurs, an error message will be displayed and the SMILES string will be skipped, \
        the outputted index in this case will be `None`.
        
        These indices will never change (unless a user manually alters self.mol_strings, which is not indended use).
        """
        if self._client.session_id:
            out_ndx = []
            for smile in smiles:
                try:
                    sf = self._client.submit_post('/structure_util/create_sar_form', { 'smiles': [smile] })[0]
                    if 'error' in sf:
                        logging.error(f' error parsing SMILES string: {sf["error"]}')
                        out_ndx.append(None)
                    elif sf['molString'] in self.mol_strings:
                        logging.warning(f' SMILES string {smile} already exists in structure set')
                        out_ndx.append(self.mol_strings.index(sf['molString']))
                    else:
                        out_ndx.append(len(self.mol_strings))
                        self.mol_strings.append(sf['molString'])
                except Exception as e:
                        logging.error(f' error parsing SMILES string: {e}')
                        out_ndx.append(None)
            return out_ndx
        else:
            logging.error("The method StructureSet.add_smiles requires a session to be opened (see LSEClient.with_session).")
    
    def create_sar_forms(self, overwrite=True):
        """
        Creates SAR-ready structural forms (remove salts, verify not a mixture, etc.).
        
        Returns a structure set of all SAR-ready forms if successful.\
        This will be the current object mutated if `overwrite==True` and a new object otherwise. \
        This method requires an active session.

        Parameters
        ----------
        overwrite: bool
            If true, overwrites existing structure set, if false creates a new one (default: `True`)
        
        Returns:
        --------
        A :class:`lserest.StructureSet`, populated with SAR-ready forms if successful, empty if not
        """
        if self._client.session_id:
            sar_forms = self._client.submit_post('/structure_util/create_sar_form', { 'molfiles': self.mol_strings })
            new_mol_strings = []
            for sf in sar_forms:
                if 'error' in sf:
                    logging.error(f' error creating SAR form: {sf["error"]}')
                    return StructureSet(self._client)
                elif 'sarMolString' in sf:
                    new_mol_strings.append(sf['sarMolString'])
                else:
                    new_mol_strings.append(sf['molString'])
            
            if overwrite:
                self.mol_strings = new_mol_strings
                return self
            else:
                new_structures = StructureSet(self._client)
                new_structures.mol_strings = new_mol_strings
                return new_structures
        else:
            logging.error("The method StructureSet.create_sar_forms requires a session to be opened (see LSEClient.with_session).")