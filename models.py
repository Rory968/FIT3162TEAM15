# Written by Rory Austin id: 28747194

import pickle
import pymongo
import time
import database_details as dbd

# This file is a helper file for a number of the modelling functions. It provides
# methods to save and load the model from the database.


def save_model(species, model, model_name, acc):
    '''
    This function takes a given model and its corresponding data and stores it in the
    database.

    :param species: name of the species it corresponds to.
    :param model: the model object itself
    :param model_name: the name of the model object eg. type of model
    :param acc: the accuracy reading of the model.
    :return: returns the details of the storage transaction.
    '''
    pickled_model = pickle.dumps(model)
    client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
    database = client[dbd.model_dbname]
    collection = database[species]

    info = collection.insert_one({model_name: pickled_model, 'name': model_name, 'created_time': time.time(), 'accuracy': acc})
    print(info.inserted_id, 'Saved successfully with this id')
    details = {'inserted_id': info.inserted_id, 'model_name': model_name, 'created_time': time.time()}
    return details


def load_model(species):
    '''
    This function takes a species name and loads the pre trained model currently stored in the database that corresponds
    to that name.

    :param species: the name of the species.
    :return: returns the model object.
    '''
    json = {}
    client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
    database = client[dbd.model_dbname]
    collection = database[species]

    data = collection.find_one()
    model_name = data['name']

    data = collection.find({'name': model_name})
    for i in data:
        json = i
    pickled_model = json[model_name]
    return pickle.loads(pickled_model)

