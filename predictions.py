import models as m
import spreadsheet_to_csv as stc
from sklearn import metrics
import os
from pathlib import Path
import pandas as pd
import database_details as dbd
import pymongo
import subprocess


def evaluate(species, test_data, test_labels):
    model = m.load_model(species)
    pred = model.predict_proba(test_data)[:, 1]
    score = metrics.roc_auc_score(test_labels, pred)
    print('AUC:', score)


def find_path(name):
    print(name)
    print("[+] Searching for " + name)
    for root, dirs, files in os.walk(Path("C:/")):

        if name in files:
            # print("[+] Found at " + os.path.join(root, name))
            return os.path.join(root, name)


def prep_data(species, data_name):
    script_path = Path('C:/Users/Owner/Documents/Travel_package/prep_predict_data.R')
    filepath = find_path(data_name)
    csv_file_path = Path('C:/Users/Owner/Documents/photos/Project data/predictors.csv')
    # stc.csv_from_xls(filepath, csv_file_path)
    data = pd.read_csv(filepath)
    print(data)
    client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
    db = client['temp']
    collection = db[species]
    collection.insert_many(data)
    command = "Rscript"
    cmd = [command, script_path, species]
    subprocess.call(cmd)
    client.drop_database('temp')
    db = client[dbd.backlog_dbname]
    collection = db[species]
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))
    return df


def replace_data(species, data):
    client = pymongo.MongoClient(dbd.client_n, dbd.client_address)
    db = client[dbd.backlog_dbname]
    db.drop_collection(species)
    collection = db[species]
    collection.insert_many(data)


def predict(species, data_name):
    data = prep_data(species, data_name)
    data = data.fillna(0, inplace=True)
    model = m.load_model(species)
    predictions = model.predict(data)
    data[dbd.target_variable] = predictions
    replace_data(species, data)





