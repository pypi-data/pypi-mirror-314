import json
class Table:
    def __init__(self, client, table_id):
        if not client:
            raise ValueError("A NextplusClient instance is required")
        if not table_id:
            raise ValueError("Table ID is required")

        self.client = client
        self.table_id = table_id

    def find(self, filter=None):
      if filter is not None and not isinstance(filter, dict):
          raise ValueError("Filter must be a dictionary")

      # Initialize the filter if it's None
      if filter is None:
          filter = {}

      # Add 'deletedAt' condition if 'deleted' is not True and 'where' clause exists
      if filter.get("deleted") is not True:
          filter.setdefault("where", {})["deletedAt"] = None

      endpoint = f'/api/Tables/getTableList/{self.table_id}'
      params = {'filter': json.dumps(filter)}
      return self.client.make_request('GET', endpoint, params=params)


    def insert(self, record):
        if not isinstance(record, dict) or not record:
            raise ValueError("Record must be a non-empty dictionary")

        endpoint = '/api/Tables/createNewRecord'
        data = {
            "record": record,
            "tableId": self.table_id
        }
        return self.client.make_request('POST', endpoint, data=data)

    def update(self, record):
        if not isinstance(record, dict) or not record:
            raise ValueError("Record must be a non-empty dictionary")
        if "_id" not in record:
            raise ValueError("Record must contain an '_id' field for update")

        endpoint = '/api/Tables/updateRecord'
        data = {
            "record": record,
            "tableId": self.table_id
        }
        return self.client.make_request('POST', endpoint, data=data)

    def remove(self, record_id):
        if not record_id:
            raise ValueError("Record ID is required for removal")

        endpoint = '/api/Tables/removeRecord'
        data = {
            "tableId": self.table_id,
            "recordId": record_id
        }
        return self.client.make_request('POST', endpoint, data=data)

    # Additional methods for other operations can be added here
