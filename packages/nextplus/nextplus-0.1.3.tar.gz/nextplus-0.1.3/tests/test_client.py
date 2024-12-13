import unittest
from nextplus import NextplusClient
import json

# import dotenv and load
import dotenv
dotenv.load_dotenv()

class TestNextplusClient(unittest.TestCase):

    def test_init_class(self):
        client = NextplusClient()
        self.assertEqual(client.token, None)

    def test_tables_find(self):
        client = NextplusClient()
        tables = client.Tables.find({'where': {'name': 'Machine Status Log'}})
        # Check that tables size is one
        self.assertEqual(len(tables), 1)
        # Check that first element in tables array id equal to 1
        self.assertEqual(tables[0]['id'], '1958dbd0-b9bf-11ee-a4d7-950198b3451e')


    def test_table_find(self):
        client = NextplusClient()
        tableDef = client.Tables.find({'where': {'name': 'Machine Status Log'}})[0]
        print(tableDef['id'])
        table = client.Table(tableDef['id'])
        rows = table.find()
        print(rows)
        self.assertEqual(len(rows),0)

    def test_table_insert(self):
        # Initialize client
        client = NextplusClient()
        # Get table object
        tableDef = client.Tables.find({'where': {'name': 'Machine Status Log'}})[0]
        # Create sample data
        data = {
          "COLUMN_machine-id":"Machine1",
          "COLUMN_status":"idle",
        }
        # Insert data
        table = client.Table(tableDef['id'])
        result = table.insert(data)
        # Check that data was inserted
        self.assertIsNotNone(result['_id'])
        print(f"Record inserted with ID: {result}")
        print(result)
        # Update sample data
        data = {
          "_id": result['_id'],
          "COLUMN_status":"busy"
        }
        updateRes = table.update(data)
        print(json.dumps(updateRes))
        self.assertEqual(updateRes["COLUMN_status"],"busy")
        print(result['_id'])
        table.remove(result['_id'])
        rows = table.find()
        print(json.dumps(rows))
        self.assertEqual(len(rows),0)





if __name__ == '__main__':
    unittest.main()

