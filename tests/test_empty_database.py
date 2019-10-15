import database_details as dbd
import pymongo


class TestEmpty:
    def test_em(self):
        client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
        mydb = client[dbd.name]
        names = mydb.list_collection_names()
        assert (len(names) == 0, "Data is still present.")
