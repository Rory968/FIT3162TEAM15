import pickle
import pymongo
import time
import database_details as dbd


def save_model(species, model, model_name, acc):
    pickled_model = pickle.dumps(model)
    client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
    database = client[dbd.model_dbname]
    collection = database[species]

    info = collection.insert_one({model_name: pickled_model, 'name': model_name, 'created_time': time.time(), 'accuracy': acc})
    print(info.inserted_id, 'Saved successfully with this id')
    details = {'inserted_id': info.inserted_id, 'model_name': model_name, 'created_time': time.time()}
    return details


def load_model(species):
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

