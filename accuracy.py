import pymongo
import database_details as dbd
import sys


def get_acc(species):
    client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
    database = client[dbd.model_dbname]
    collection = database[species]

    data = collection.find_one()
    model_name = data['name']
    model_acc = data['accuracy']
    return model_name, model_acc


def main():
    len(sys.argv)
    name = sys.argv[1]
    acc = get_acc(name)
    print("[+] Model type:", acc[0], "with AUC:", acc[1])


if __name__ == "__main__":
    main()