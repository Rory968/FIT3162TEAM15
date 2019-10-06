import pymongo
import database_details as dbd
import sys


def list_names(arg):
    '''
    This function takes an argument from the command line and displays
    the names and information relevant to the given argument. The model argument will
    print all names of models that are currently stores in the database, the data argument will
    do the same thing but for raw data.
    :param arg: type of list needed.
    :return: returns nothing.
    '''
    if arg == 'help':
        print("List model names with 'list_names model'.")
        print("List current data with 'list_names data'.")
    elif arg == 'data':
        client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
        names = client[dbd.name].list_collection_names()
        if len(names) > 0:
            for name in names:
                print(name)
        else:
            print("No current data is present.")
    elif arg == 'model':
        client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
        names = client[dbd.model_dbname].list_collection_names()
        if len(names) > 0:
            for name in names:
                print(name)
        else:
            print("No current models are trained.")
    else:
        print("Given argument does not exist, use 'list_names help' for possible arguments.")


def main():
    len(sys.argv)
    try:
        arg = sys.argv[1]
    except IndexError:
        print("Must provide argument, use 'list_names help' for more details.")
        return
    list_names(arg)


if __name__ == "__main__":
    main()