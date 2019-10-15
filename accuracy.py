# Written by Rory Austin id: 28747194

import pymongo
import database_details as dbd
import sys

# This file when run takes the accuracy for a given species from the models database information and
# prints it inside the console.


def get_acc(species):
    '''
    This function takes a species name as argument and reads its accuracy reading from the database.

    :param species: name of the species.
    :return: returns nothing.
    '''
    try:
        client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
        database = client[dbd.model_dbname]
        collection = database[species]

        data = collection.find_one()
        model_name = data['name']
        model_acc = data['accuracy']
        return model_name, model_acc
    except TypeError:
        print("Model does not exist, type 'list_names model' for possible arguments.\n")
        sys.exit()


def main():
    len(sys.argv)
    try:
        name = sys.argv[1]
    except IndexError:
        print("Must provide argument, use 'list_names model' for a list of arguments")
        return
    acc = get_acc(name)
    print("[+] Model type:", acc[0], "\n    AUC:", acc[1])


if __name__ == "__main__":
    main()