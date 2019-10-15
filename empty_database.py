# Written by Rory Austin id: 28747194

import pymongo
import sys
import database_details as dbd

# This file when run connects to the database and removes all databases containing species
# information or data.


def remove():
    '''
    This function looks through the database and removes all non essential
    databases found within the client.
    :return: returns nothing.
    '''
    print("[+] Removing non essential databases...")
    client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
    dbs = client.list_database_names()
    critical = ['admin', 'config', 'local']
    for name in dbs:
        if name not in critical:
            client.drop_database(name)
    print("[+] Removal successful.")


def main():
    len(sys.argv)
    remove()


if __name__ == "__main__":
    main()
