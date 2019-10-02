import pymongo
import sys


def remove():
    print("[+] Removing non essential databases...")
    client = pymongo.MongoClient('localhost', 27017)
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
