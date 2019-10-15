# Written by Rory Austin id: 28747194

import models as m
from sklearn import datasets
from sklearn import metrics
import os
import sys
from pathlib import Path
import pandas as pd
import database_details as dbd
import pymongo
import subprocess


# This is a helper file for the predict file, this contains the majority of the
# prediction logic, evaluate is unused and acts as a backup for accuracy.
# prep_data converts given data into same format as training data for predictions
# replace data is used when the data already exists and just needs to be overwritten in the database
# predict preps and makes predictions on the data, it then saves these to a file called 'predictions.xls'


def evaluate(species, test_data, test_labels):
    '''
    Small function to evaluate the accuracy of a function should the original method disappear.
    :param species: name of the species.
    :param test_data: untampered training data.
    :param test_labels: labels for corresponding data.
    :return: returns nothing.
    '''
    model = m.load_model(species)
    pred = model.predict_proba(test_data)[:, 1]
    score = metrics.roc_auc_score(test_labels, pred)
    print('AUC:', score)


def find_path(name):
    '''
    Small function to find given directories or files within a system.
    :param name: name of directory or file.
    :return: returns the path as a string.
    '''
    print("[+] Searching for " + name)
    for root, dirs, files in os.walk(str(Path.home())):

        if name in files:
            return os.path.join(root, name)
        if name in dirs:
            return os.path.join(root, name)


def prep_data(species, data_path):
    '''
    This function takes a path to a file of data and prepares this data
    by transforming it into the same format as the data from the training
    phase.
    :param species: name of the species.
    :param data_path: path to the file containing the raw data.
    :return: returns a data frame containing prepped data.
    '''
    cwd = os.getcwd()
    script_path = find_path("prep_prediction_data.R")
    data = pd.read_excel(data_path)
    data.to_csv(os.path.join(cwd, 'temp.csv'))
    client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
    db = client['temp']
    collection = db[species]
    collection.insert_many(data.to_dict('records'))
    command = "Rscript"
    cmd = [command, script_path, species]
    subprocess.call(cmd)
    client.drop_database('temp')
    db = client[dbd.backlog_dbname]
    collection = db[species]
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))
    client.drop_database(dbd.backlog_dbname)
    client.close()
    return df


def replace_data(species, data):
    '''
    Small function to switch data in a collection inside the database, is not used.
    :param species: name of the species.
    :param data: corresponding data.
    :return: returns nothing.
    '''
    client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
    db = client[dbd.backlog_dbname]
    db.drop_collection(species)
    collection = db[species]
    collection.insert_many(data)


def predict(species, data_name):
    '''
    This function uses the name of the species along with observational data that has not been rated yet
    It takes this data and puts it through a trained model in order to provide automted predictions on the
    reliability of the observation.
    :param species: name of the species.
    :param data_name: name of the file containing the raw data.
    :return: returns nothing.
    '''
    raw = find_path(data_name)
    data = prep_data(species, raw)
    try:
        data = data.drop(['_id', 'bio4', 'bio10'], axis=1)
    except KeyError:
        data = data.drop('_id', axis=1)
    cols = [dbd.long, dbd.lat]
    data = data[[c for c in data if c not in cols] + [c for c in cols if c in data]]
    data.insert(0, 'Unnamed: 0', range(0, 0+len(data)))
    data.fillna(data.mean(), inplace=True)
    model = m.load_model(species)
    predictions = model.predict(data)
    raw = pd.read_excel(raw)
    raw.insert(len(raw.columns), dbd.target_variable, predictions)
    importance = model.feature_importances_
    largest = max(list(importance))
    index = list(importance).index(largest)
    print("[+] Best feature in prediction", list(raw)[index], "with importance value of", largest)
    cwd = os.getcwd()
    try:
        os.mkdir(os.path.join(cwd, 'Predictions'))
    except FileExistsError:
        cwd = cwd
    csv_file_path = Path(os.path.join(cwd, 'Predictions', species+'_last_predictions.csv'))
    raw.to_csv(csv_file_path)
    downpath = find_path('Downloads')
    raw.to_excel(downpath+'/predictions.xls')
    print("[+] Predictions complete, check downloads folder.")





