# Written by Rory Austin id:28747194
import os
import sys
import pymongo
import pandas as pd
import spreadsheet_to_csv as stc
import seperator as sep
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector
import subprocess

# This script takes an excel workbook file and converts it into a csv file in order to populate a MongoDB database.
# It will split the data in the csv by scientific display name and create a number of collections based on these names.


def create_dict(dir):
    ''' This function takes a csv file path and reads this file into the pandas data frame,
    From here is turns the data frame into a dictionary to be input into the MongoDB collection.

    :param file: File path containing the csv file that has the data in it
    :return: Returns the data from the csv stored in a dictionary format
    '''
    files = []
    names = []
    for file in os.listdir(dir):
        if file.endswith('.csv'):
                names.append(file[:-4])
                f = open(os.path.join(dir, file))
                data_frame = pd.read_csv(f)
                files.append(data_frame.to_dict('records'))
    return names, files


def clean_names(list_names):
    '''
    This function takes a list of species names and cleans the names so that they are suitable
    format for collection titles.

    :param list_names: list of species names held in file.
    :return: cleaned list of names
    '''
    for i in range(len(list_names)):
        list_names[i] = list_names[i].lstrip(' ').replace(' ', '_').replace('.', '')

    return list_names


def populate(list_names, list_df):
    '''
    This function takes a list of species names and a list of their corresponding dataframes and
    populates a MongoDB database with a number of collections corresponding to each species.

    :param list_names: list of species names contained in file.
    :param list_df: list of data frames containing data for each species by name.
    :return: blank
    '''
    client = pymongo.MongoClient('localhost', 27017)
    mydb = client['raw_data']
    for i in range(len(list_names)):
        collection = mydb[list_names[i]]
        collection.insert_many(list_df[i])
        client.close()
    print("[+] Population complete")
    return


def find_path(name):
    print("[+] Searching for " + name)
    for root, dirs, files in os.walk("C:\\"):

        if name in files:
            print("[+] Found at " + os.path.join(root, name))
            return os.path.join(root, name)


def r_script_setup(names):
    package_names = ['mongolite', 'caret', 'DMwR', 'dplyr', 'usdm', 'sp', 'mapview']
    if all(rpackages.isinstalled(x) for x in package_names):
        have_package = True
    else:
        have_package = False
    if not have_package:
        utils = rpackages.importr('utils')
        utils.chooseCRANmirror(ind=1)
        to_install = [x for x in package_names if not rpackages.isinstalled(x)]
        if len(to_install) > 0:
            utils.install_packages(StrVector(to_install))
    base = rpackages.importr('base')


# This block establishes the file paths and transfers the xls file to the csv file.
# Create a folder in the Documents\photos path called Project data and download the xls in there.
len(sys.argv)
file = sys.argv[1]
filepath = find_path(file)
cwd = os.getcwd()

#print(filepath, cwd)
xls_file_path = filepath
csv_file_path = r'C:\Users\Owner\Documents\photos\Project data\data.csv'
directory = os.path.join("C:\\Users\\Owner\\Documents\\photos\\Project data\\Species\\")
stc.csv_from_xls(xls_file_path, csv_file_path)


# This block takes the initial csv and makes a directory with smaller csv files for each species.
data = pd.read_csv(csv_file_path)
names, species = sep.separate_types(data)
sep.export_to_csv(names, species, directory)


# This block takes the newly created csv file and populates the MongoDB database with it.
sample_data_names, sample_data_dict = create_dict(directory)
clean_names = clean_names(sample_data_names)
#print(clean_names, len(sample_data_dict))
populate(clean_names, sample_data_dict)




