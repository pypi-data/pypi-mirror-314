import json
import logging
import re
from typing import List, Optional
from pydantic import BaseModel, Field

from heimdall.models.authorization_atom import AuthorizationAtom


# Define the data class for AuthorizationAtom

# Define the data class for PolicyEnforcementProvider
class PolicyEnforcementProvider(BaseModel):
    version: str
    id: str
    name: str
    description: str
    authorization_atoms: List[AuthorizationAtom] = Field(default_factory=list)

    # Regular expression pattern to find variables in strings
    variable_pattern = re.compile(r'\$\{(.+?)\}')

    def __init__(self, version: str, id: str, name: str, description: str, atoms: List['AuthorizationAtom'] = None):
        """
        Represents a policy enforcement provider.

        :param version: The version of the policy enforcement provider.
        :type version: str
        :param id: The unique identifier of the policy enforcement provider.
        :type id: str
        :param name: The name of the policy enforcement provider.
        :type name: str
        :param description: The description of the policy enforcement provider.
        :type description: str
        :param atoms: The list of authorization atoms for this policy enforcement provider, defaults to None.
        :type atoms: List['AuthorizationAtom'], optional
        """
        self.version = version
        self.id = id
        self.name = name
        self.description = description
        self.atoms = atoms
    # Method to add an AuthorizationAtom to the PolicyEnforcementProvider
    def add_atom(self, atom: AuthorizationAtom):
        """
        Adds an authorization atom to this policy enforcement provider.

        :param atom: The authorization atom to add.
        :type atom: AuthorizationAtom
        """
        variables = self.find_variables(atom.tags)
        variables.extend(self.find_variables(atom.paths))
        atom.variables = list(set(variables))
        i = next((i for i, a in enumerate(self.authorization_atoms) if a.id == atom.id), -1)
        if i == -1:
            self.authorization_atoms.append(atom)
        else:
            self.authorization_atoms.insert(i, atom)

    # Method to export the PolicyEnforcementProvider to a file
    def export(self, file_path: str):
        """
        Exports this policy enforcement provider to a file.

        :param file: The path to the file to write to.
        :type file: str
        """
        with open(file_path, 'w') as file:
            json.dump(self.dict(), file)

    # Method to get an AuthorizationAtom from the PolicyEnforcementProvider
    def get_atom(self, atom_id: str, variables: dict) -> Optional[AuthorizationAtom]:
        """
        Gets an authorization atom from this policy enforcement provider.

        :param atom_id: The ID of the authorization atom to get.
        :type atom_id: str
        :param variables: The map of variable names to values used to resolve the atom's inputs, defaults to None.
        :type variables: Dict[str, str], optional
        :return: The authorization atom with the specified ID and variable values, or None if no such atom exists
                 or if any required variable values are missing.
        :rtype: AuthorizationAtom or None
        """
        orig = next((a for a in self.authorization_atoms if a.id == atom_id), None)
        if orig:
            aa = orig.copy()
            if aa.has_variables():
                if not variables:
                    logging.log(f"Authorization atom {atom_id} has variables and no values were provided")
                    return None
                for v in aa.variables:
                    value = variables.get(v)
                    if value is None or value == "":
                        logging.log(f"Authorization atom {atom_id} has variable {v} and no value was provided")
                        return None
                aa.paths = self.replace_variables(variables, aa.paths)
                aa.tags = self.replace_variables(variables, aa.tags)
            return aa
        return None

    # Method to replace variables in strings with their corresponding values from a dictionary
    def replace_variables(self, variables: dict, strings: List[str]) -> List[str]:
        """
        Replaces variables in the given list of strings with their corresponding values from the given map of variables.

        :param variables: The map of variables to replace in the strings.
        :type variables: Dict[str, str]
        :param strings: The list of strings in which to replace the variables.
        :type strings: List[str]
        :return: The list of strings with variables replaced by their corresponding values from the map of variables.
        :rtype: List[str]
        """
        if not strings:
            return []
        new_strings = []
        if not variables:
            new_strings.extend(strings)
        else:
            for string in strings:
                def repl(match):
                    return variables.get(match.group(1), match.group(0))
                new_string = self.variable_pattern.sub(repl, string)
                new_strings.append(new_string)
        return new_strings

    # Method to find variables in a list of strings and return them in a list
    def find_variables(self, strings: List[str]) -> List[str]:
        """
       Finds variables in the given list of strings and returns them in a list.

       :param strings: The list of strings in which to find variables.
       :type strings: List[str]
       :return: The list of variables found in the strings.
       :rtype: List[str]
       """
        variables = []
        if strings:
            for string in strings:
                variables.extend(match.group(1) for match in self.variable_pattern.finditer(string))
        return variables
