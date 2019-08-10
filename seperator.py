# Written by Rory Austin id: 28747194
from errno import EEXIST
import pandas as pd
import os


def separate_types(data_frame):
    '''
    This function takes a data frame and splits it into smaller data frames based on the 'SCIENTIFIC_DISPLAY_NME' of
    the observation.

    :param data_frame: This is a data frame containing observation data for a number of different species.
    :return: list of species names and list of data frames corresponding to each name.
    '''
    names = data_frame.SCIENTIFIC_DISPLAY_NME.unique()
    unique_species = []
    for name in names:
        # !!!Hard coded column name!!!
        df = data_frame[data_frame['SCIENTIFIC_DISPLAY_NME'] == name]
        unique_species.append(df)

    return names, unique_species


def export_to_csv(list_of_names, list_of_df):
    '''
    This function takes a list of names and corresponding data frames and exports
    the data frames to a csv file in a certain file path.

    :param list_of_names: list of species names
    :param list_of_df: list of species data frames corresponding to list of names.
    :return: blank
    '''

    # !!!Hard coded path!!!
    universal_file_path = r"C:\Users\Owner\Documents\photos\Project data\Species\ "
    try:
        os.makedirs(universal_file_path)
    except OSError as e:
        if e.errno != EEXIST:
            raise

    for i in range(len(list_of_df)):
        print(list_of_names[i])
        string = universal_file_path + list_of_names[i] + '.csv'
        print(string)
        list_of_df[i].to_csv(string)


data = pd.read_csv(r'C:\Users\Owner\Documents\photos\Project data\data.csv')
names, species = separate_types(data)
export_to_csv(names, species)