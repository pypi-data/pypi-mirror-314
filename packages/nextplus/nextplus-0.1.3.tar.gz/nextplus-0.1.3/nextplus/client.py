import os
import requests
import json
import time
from .tables import Tables
from .table import Table

class NextplusClient:
    def __init__(self, server_url=None, username=None, email=None, password=None, verify_ssl=True):
        self.server_url = server_url or os.getenv('NEXTPLUS_SERVER_URL')
        self.email = email or os.getenv('NEXTPLUS_EMAIL')
        self.username = username or os.getenv('NEXTPLUS_USERNAME')
        self.password = password or os.getenv('NEXTPLUS_PASSWORD')
        self.verify_ssl = verify_ssl
        self.__version__ = '0.1.3'
        self.userAgent = f'Nextplus Python SDK/{self.__version__}'
        self.token = None
        self.token_expiry = None
        if not self.server_url or not self.password or (not self.email and not self.username):
            raise ValueError("Server URL and password are required, along with either username or email. "
                             "These can be provided either as arguments or set as "
                             "environment variables (NEXTPLUS_SERVER_URL, NEXTPLUS_USERNAME, "
                             "NEXTPLUS_EMAIL, and NEXTPLUS_PASSWORD).")
        # Check that valid url is provided with protocol and (http or https) and without trailing slash or any path followed by the hostname / ip address
        if not self.server_url.startswith('http://') and not self.server_url.startswith('https://'):
            raise ValueError("Server URL must start with http:// or https://")
        if self.server_url.endswith('/'):
          raise ValueError("Server URL should not end with '/'")
        if '#' in self.server_url:
          raise ValueError("Server URL should not include #")



    def _validate_token(self):
      """
	      Validate the access token. Refresh if expired.
    	"""
      if not self.token:
        raise ValueError("No token available. Authenticate first.")
      endpoint = "/api/UserModels/current"
      response = self.make_request('GET', endpoint)
      if (response.status_code == 401):
        self._authenticate()

    def _authenticate(self):
        """
        Authenticate with the Nextplus API and store the access token.
        """
        auth_url = f"{self.server_url}/api/UserModels/login?include=user&rememberMe=false"
        auth_data = {
            "forceLogin": True,
            "password": self.password,
            "rememberMe": False
        }
        if (not self.username):
          auth_data["email"] = self.email
        else:
          auth_data["username"] = self.username

        response = requests.post(auth_url, json=auth_data, headers={'User-Agent': self.userAgent}, verify=self.verify_ssl)
        if (response.status_code != 200):
          try:
            print(response.json())
          except Exception:
            print(f'Error authenticating: {response.text}')
        response.raise_for_status()
        self.token = response.json().get('id')
        self.token_expiry = int(time.time()) + int(response.json().get('ttl') - 300)
        if not self.token:
            raise ValueError("Failed to authenticate with Nextplus API")

    def make_request(self, method, endpoint, data=None, params=None):
        """
        Make a request to the Nextplus API.
        """
        if not self.token or int(time.time()) > self.token_expiry:
            self._authenticate()

        url = f"{self.server_url}{endpoint}"
        headers = {'Authorization': self.token, 'User-Agent': self.userAgent}
        if method.lower() == 'get':
            response = requests.get(url, headers=headers, params=params, verify=self.verify_ssl)
        elif method.lower() == 'post':
            response = requests.post(url, headers=headers, json=data, verify=self.verify_ssl)
        elif method.lower() == 'patch':
            response = requests.patch(url, headers=headers, json=data, verify=self.verify_ssl)
        else:
            raise ValueError("Unsupported HTTP method")
        if response.status_code == 401 and endpoint != '/api/UserModels/current':
          self._validate_token()
        if (response.status_code != 200):
          print(json.dumps({"method":method,"endpoint":endpoint,"data":data,"params":params}))
        response.raise_for_status()
        return response.json()

    @property
    def Tables(self):
        """
        Property to access Tables functionality.
        """
        return Tables(self)

    def Table(self, table_id):
        """
        Method to access Table functionality.
        """
        return Table(self, table_id)

