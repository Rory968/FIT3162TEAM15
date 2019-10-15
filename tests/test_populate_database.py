import database_details as dbd
import pymongo


class TestPop:
    def test_raw(self):
        client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
        mydb = client[dbd.name]
        names = mydb.list_collection_names()
        assert (len(names) > 0, "No data placed in database.")

    def test_train(self):
        client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
        mydb = client[dbd.train_name]
        names = mydb.list_collection_names()
        assert (len(names) > 0, "No training data created.")

    def test_test(self):
        client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
        mydb = client[dbd.train_name]
        names = mydb.list_collection_names()
        assert(len(names) > 0, "No testing data created.")
