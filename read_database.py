# Written by Rory Austin id: 28747194
import pymongo
import pandas as pd
import database_details as dbd

# This is a helper file that reads from a populated MongoDB database


def read_collection(db_name, collection_name):
    '''
    This function connects to a database populated with data and reads the data into a
    pandas data frame for later computation.

    :param db_name: name of database to connect to.
    :param collection_name: name of required collection.
    :return: returns a pandas data frame containing the required collection data.
    '''
    # !!!Hard coded connection variable!!!
    client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
    db = client[db_name]
    test_col = db[collection_name]
    df = pd.DataFrame(list(test_col.find()))
    return df

