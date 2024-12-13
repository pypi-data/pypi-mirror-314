from typing import Optional

import backoff
import urllib3
from google.auth import exceptions as _auth_exceptions
from google.auth.transport.requests import Request as _GoogleRequest
from google.cloud.workflows.executions_v1beta.services.executions import \
    ExecutionsClient
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials

SYNCHRONIZER_NAME = "synchronizer_workflow"
DASHBORD_ORCH_NAME = "dashboard_orch" ## Should be changed to performance_dashboard_orch
GENERAL_DASHBORD_ORCH_NAME = "general_dashboard_orch"
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

class Client(ExecutionsClient):
    def __init__(self, credentials: Optional[Credentials] =None, credentials_for_callback: Optional[Credentials] = None):
        super().__init__(credentials=credentials)
        self._credentials_for_callback = credentials_for_callback


    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ExecutionsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        credentials_for_callback = service_account.Credentials.from_service_account_file(filename, scopes=SCOPES)
        kwargs["credentials_for_callback"] = credentials_for_callback
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @backoff.on_exception(backoff.expo, (ConnectionError, _auth_exceptions.GoogleAuthError), 5)
    def _get_google_open_access_token(self) -> str:
        """ retrieve a token from the service account metadata service """
        credentials = self._credentials_for_callback
        if credentials is None:
            raise ValueError("No credentials provided")
        auth_req = _GoogleRequest()
        credentials.refresh(auth_req)
        return credentials.token


    def get_http_response(self, url: str, method: str = 'GET') -> urllib3.BaseHTTPResponse:
        """ Call a URL with the Google Open Access Token """
        http = urllib3.PoolManager()
        google_token = self._get_google_open_access_token()
        response = http.request(
            method,
            url,
            preload_content=False,
            headers={
                'content-type': 'application/json',
                'Authorization': f'Bearer {google_token}'
            }
        )
        return response
