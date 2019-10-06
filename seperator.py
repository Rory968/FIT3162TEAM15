# Written by Rory Austin id: 28747194

from errno import EEXIST
import os
import sys
import database_details as dbd

# This is a helper file used to separate a csv file based on a name and create a number of smaller files.
# Used in 'populate_database.py' file.


def separate_types(data_frame):
    '''
    This function takes a data frame and splits it into smaller data frames based on the 'SCIENTIFIC_DISPLAY_NME' of
    the observation.

    :param data_frame: This is a data frame containing observation data for a number of different species.
    :return: list of species names and list of data frames corresponding to each name.
    '''
    try:
        names = data_frame[dbd.splitter].unique()
    except AttributeError:
        print("File must contain attribute 'SCIENTIFIC_DISPLAY_NME', this is necessary for training.")
        sys.exit()
    unique_species = []
    for name in names:
        # !!!Hard coded column name!!!
        df = data_frame[data_frame[dbd.splitter] == name]
        unique_species.append(df)

    return names, unique_species


def export_to_csv(list_of_names, list_of_df, file_path):
    '''
    This function takes a list of names and corresponding data frames and exports
    the data frames to a csv file in a certain file path.

    :param list_of_names: list of species names.
    :param list_of_df: list of species data frames corresponding to list of names.
    :param file_path: the path specified to store the csv files.
    :return: blank.
    '''

    universal_file_path = file_path
    try:
        os.makedirs(universal_file_path)
    except OSError as e:
        if e.errno != EEXIST:
            raise

    for i in range(len(list_of_df)):
        string = os.path.join(universal_file_path,  list_of_names[i] + '.csv')
        list_of_df[i].to_csv(string)

