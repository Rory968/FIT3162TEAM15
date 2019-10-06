import sys
import warnings
import database_details as dbd
import predictions as p
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
import pymongo
import pandas as pd
import models as m
import xlwt


def get_data(client_address, client_name, col_name):
    '''
    This module loads the training and testing data from the database for use later.

    :param client_address: address of the database.
    :param client_name: name of the database.
    :param col_name: name of collection (should be name of species)
    :return: returns tuple of training and testing data.
    '''
    client = pymongo.MongoClient(client_name, client_address)
    db = client['training_data']
    collection = db[col_name]
    cursor = collection.find()
    train_df = pd.DataFrame(list(cursor))
    if train_df.empty:
        print("No data present, type 'list_names data' for possible arguments.")
        sys.exit()
    db = client['testing_data']
    collection = db[col_name]
    cursor = collection.find()
    test_df = pd.DataFrame(list(cursor))
    if test_df.empty:
        print("Data set too small for test data, must get extra for accurate model.")
        sys.exit()
    return train_df, test_df


def model_fit_and_evaluation(name_list, classifier_list, data):
    '''
    This module takes a list of classifiers and their respective names and then trains each of the
    on a training data set, after which it evaluates the model on a testing set and appends its final
    score to the scores list.

    :param name_list: List of model names.
    :param classifier_list: List of classifiers.
    :param data: training and testing data for models.
    :return: Returns their scores in a list.
    '''
    print("[+] Building models...")
    try:
        data[0][dbd.target_variable]
    except KeyError:
        print("Database collection not present, Make sure name is typed correctly.")
        return
    train_data = data[0]
    test_data = data[1]
    train_labels = train_data[dbd.target_variable]
    train_features = train_data.drop(dbd.drop_features, axis=1)._get_numeric_data()
    test_labels = test_data[dbd.target_variable]
    test_features = test_data.drop(dbd.drop_features, axis=1)

    scores = []
    for name, clf in zip(name_list, classifier_list):
        clf.fit(train_features, train_labels)
        pred = clf.predict_proba(test_features)[:, 1]
        try:
            score = metrics.roc_auc_score(test_labels, pred)
        except ValueError:
            print("Only one class present in testing data. More data needed.")
            return
        scores.append(score)
    return scores


def storage(species, scores, name_list, model_list):
    '''
    This module takes trained models and their scores and then finds the highest scoring model
    for a given species. From here it will save the model in the database.

    :param species: species name.
    :param scores: list of scores for classifiers.
    :param name_list: list of names of each classifier.
    :param model_list: list of classifier objects.
    :return: Returns nothing.
    '''
    print("[+] Storing optimal model")
    top3 = sorted(zip(scores, name_list, model_list), reverse=True)[:1]
    for tuple in top3:
        m.save_model(species, tuple[2], tuple[1], tuple[0])
    print("[+] Model saved in database.")


def main():
    # Takes species name as argument in cli and then trains and finds optimal model
    # After this is found it is stored in the database.
    warnings.filterwarnings("ignore")
    len(sys.argv)
    try:
        name = sys.argv[1]
    except IndexError:
        print("Must provide data argument, use 'list_names data' for a list of arguments")
        return
    data = get_data(dbd.client_address, dbd.client_n, name)
    names = ['Gradient_Boosting', 'Random_Forest', 'Neural_Network', 'Adaptive_Boosting', 'Decision_Tree']
    classifiers = [GradientBoostingClassifier(), RandomForestClassifier(n_estimators=10), MLPClassifier(max_iter=1000), AdaBoostClassifier(), DecisionTreeClassifier()]
    scores = model_fit_and_evaluation(names, classifiers, data)
    storage(name, scores, names, classifiers)
    # test_data = data[1]
    # test_labels = test_data[dbd.target_variable]
    # test_features = test_data.drop(dbd.drop_features, axis=1)

    # p.evaluate(name, test_features, test_labels)


if __name__ == "__main__":
    main()

