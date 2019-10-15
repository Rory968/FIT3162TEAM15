# Written by Rory Austin id: 28747194

import predictions as p
import os
import sys


# This file when run takes a file that is present in the system and associates it with
# a species name the user passes through the command line, when it is run it will fetch the
# model for the specified species and prep the data for predictions, it will then make
# these predictions and save them to a new file called 'predictions.xls' in the downloads folder
# of the system.

def predict(species, data_name):
    '''
    This function makes use of the predictions file to predict the
    reliability of a given set of observations using a pre trained model.
    :param species:
    :param data_name:
    :return:
    '''
    p.predict(species, data_name)
    cwd = os.getcwd()
    os.remove(os.path.join(cwd, 'temp.csv'))


def main():
    len(sys.argv)
    try:
        species = sys.argv[1]
    except IndexError:
        print("Must provide model argument, use 'list_names model' for a list of arguments.")
        return
    try:
        data_name = sys.argv[2]
    except IndexError:
        print("Must provide data file name for predictions.")
        return
    if data_name.endswith('.xls'):
        predict(species, data_name)
    else:
        print("Prediction data must be in .xls format.")


if __name__ == "__main__":
    main()
