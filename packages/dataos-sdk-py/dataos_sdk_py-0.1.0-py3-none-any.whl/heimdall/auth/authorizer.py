import logging

from typing import Dict, Tuple
from requests import HTTPError

from heimdall.auth.policy_enforcement_provider import PolicyEnforcementProvider
from heimdall.heimdall_client import HeimdallClient
from heimdall.models.authorization_request import AuthorizationRequest, PepContext, AuthorizationRequestBatch
from heimdall.models.authorization_response import AuthorizationResponse, Error, AuthorizationResponseBatch, \
    AuthResponseSingle


class AuthorizationError(Exception):
    def __init__(self, status_code, message):
        super().__init__(f"Authorization failed: HTTP {status_code} - {message}")
        self.status_code = status_code

class Authorizer:
    def __init__(self, pep: PolicyEnforcementProvider, client: HeimdallClient, user_agent: str):
        """
        Handles authorization using the Heimdall client's authorization API.

        :param pep: The policy enforcement provider.
        :type pep: PolicyEnforcementProvider
        :param client: The Heimdall client.
        :type client: HeimdallClient
        :param user_agent: The user agent associated with the authorization requests.
        :type user_agent: str
        """
        self.pep = pep
        self.client = client
        self.user_agent = user_agent

    def authorize(self, token: str, correlation_id: str) -> AuthorizationResponse:
        """
        Authorizes an access token using the Heimdall client's authorization API.

        :param token: The access token to authorize.
        :type token: str
        :param correlation_id: The correlation ID for the authorization request.
        :type correlation_id: str
        :return: An AuthorizationResponse object containing the result of the authorization request.
        :rtype: AuthorizationResponse
        """
        auth_request = AuthorizationRequest(token)
        try:
            return self.client.authorize_api.authorize(auth_request, correlation_id).execute()
        except HTTPError as http_error:
            error_message = str(http_error)
            return AuthorizationResponse(
                allow=False,
                valid=False,
                error=Error(http_error.response.status_code, f"Authorization failed: {error_message}")
            )

    def authorize_atom(self, token: str, atom_id: str, variable_values: Dict[str, str] = None,
                       correlation_id: str = ""):
        """
        Authorizes an access token for a specific atom using the Heimdall client's authorization API.

        :param token: The access token to authorize.
        :type token: str
        :param atom_id: The ID of the atom to authorize the token for.
        :type atom_id: str
        :param variable_values: A map of variable names to values used to resolve the atom's inputs.
        :type variable_values: Dict[str, str]
        :param correlation_id: The correlation ID for the authorization request.
        :type correlation_id: str
        :return: An AuthorizationResponse object containing the result of the authorization request.
        :rtype: AuthorizationResponse
        """
        if not token:
            return AuthorizationResponse(
                allow=False,
                valid=False,
                error=Error(400, "token is empty")
            )
        atom = self.pep.get_atom(atom_id, variable_values)
        if not atom:
            return AuthorizationResponse(
                allow=False,
                valid=False,
                error=Error(400, f"atom not found with id {atom_id}")
            )
        auth_request = AuthorizationRequest(token, atom.to_auth_context(), PepContext(self.user_agent, atom_id))
        try:
            return self.client.authorize_api.authorize(auth_request, correlation_id).execute()
        except HTTPError as http_error:
            error_message = str(http_error)
            return AuthorizationResponse(
                allow=False,
                valid=False,
                error=Error(http_error.response.status_code, f"Authorization failed: {error_message}")
            )

    def authorize_batch(self, token: str, batch: Dict[str, Tuple[str, Dict[str, str]]], correlation_id: str = ""):
        """
        Authorizes a token for a batch of atoms and returns the AuthorizationResponseBatch.

        :param token: The token to authorize.
        :type token: str
        :param batch: A map of atom IDs to tuples of atom ID, variable values, and correlation ID.
        :type batch: Dict[str, Tuple[str, Dict[str, str], str]]
        :param correlation_id: The correlation ID to include in the authorization request.
        :type correlation_id: str
        :return: The AuthorizationResponseBatch for the given token and batch of atoms.
        :rtype: AuthorizationResponseBatch
        """
        if not token:
            return AuthorizationResponseBatch(results={"request": AuthResponseSingle(
                allow=False,
                valid=False,
                error=Error(400, "token is empty")
            )})
        contexts = {}
        for req_key, (atom_id, variable_values) in batch.items():
            atom = self.pep.get_atom(atom_id, variable_values)
            if not atom:
                return AuthorizationResponseBatch(results={req_key: AuthResponseSingle(
                    allow=False,
                    valid=False,
                    error=Error(400, f"atom not found with id {atom_id}")
                )})
            contexts[req_key] = atom.to_auth_context()
        auth_request = AuthorizationRequestBatch(token, contexts)
        try:
            return self.client.authorize_api.authorize_batch(auth_request, correlation_id).execute()
        except HTTPError as http_error:
            error_message = str(http_error)
            raise AuthorizationError(http_error.response.status_code,
                                     f"batch authorization failed, error={error_message}")
