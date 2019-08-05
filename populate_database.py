# Written by Rory Austin id:28747194

import pymongo
import pandas as pd
import spreadsheet_to_csv as stc


# This block is establishing a connection to the server that the database is kept in.
# MongoDB database is being used for scalability and flexibility.
print("[+] Establishing server connection")
client = pymongo.MongoClient('localhost', 27017)
mydb = client['database']
collection = mydb['data_sample_collection']


def create_dict(file):
    ''' This function takes a csv file path and reads this file into the pandas dataframe,
    From here is turns the dataframe into a dictionary to be input into the MongoDB collection.

    :param file: File path containing the csv file that has the data in it
    :return: Returns the data from the csv stored in a dictionary format
    '''
    print("[+] Opening CSV")
    f = open(file)
    data_frame = pd.read_csv(f)
    return data_frame.to_dict('records')


# This block establishes the file paths and transfers the xls file to the csv file.
# Create a folder in the Documents\photos path called Project data and download the xls in there.
xls_file_path = r'C:\Users\Owner\Documents\photos\Project data\Monash_sample_VBA.xls'
csv_file_path = r'C:\Users\Owner\Documents\photos\Project data\data.csv'
stc.csv_from_xls(xls_file_path, csv_file_path)
# This block takes the newly created csv file and populates the MongoDB database with it.
sample_data_dict = create_dict(csv_file_path)
print("[+] Importing to database collection...")
collection.insert_many(sample_data_dict)
print("[+] Process completed successfully.")
client.close()
