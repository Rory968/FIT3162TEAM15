import database_details as dbd
import pymongo


class TestModel:
    def test_em(self):
        client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
        mydb = client[dbd.model_dbname]
        names = mydb.list_collection_names()
        assert (len(names) > 0, "No models were created.")
