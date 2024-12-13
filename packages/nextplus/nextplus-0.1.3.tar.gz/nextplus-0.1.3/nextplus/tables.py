import json
class Tables:
    def __init__(self, client):
        """
        Initialize with an instance of NextplusClient.
        """
        self.client = client

    def find(self, filter=None):
        """
        Fetch a list of all tables with optional filtering.
        """
        endpoint = '/api/Tables'
        params = {'filter': json.dumps(filter)} if filter else None
        return self.client.make_request('GET', endpoint, params=params)
