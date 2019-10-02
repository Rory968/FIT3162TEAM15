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
from xlwt import Workbook


def get_data(client_address, client_name, col_name):
    client = pymongo.MongoClient(client_name, client_address)
    db = client['training_data']
    collection = db[col_name]
    cursor = collection.find()
    train_df = pd.DataFrame(list(cursor))
    db = client['testing_data']
    collection = db[col_name]
    cursor = collection.find()
    test_df = pd.DataFrame(list(cursor))
    return train_df, test_df


def model_fit_and_evaluation(name_list, classifier_list, data):
    print("[+] Building models...")
    try:
        data[0][dbd.target_variable]
    except KeyError:
        print("\nDatabase collection not present, Make sure name is typed correctly.")
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
            print("\nOnly one class present in testing data. More data needed.")
            return
        scores.append(score)
    return scores


def storage(species, scores, name_list, model_list):
    print("[+] Storing optimal model")
    top3 = sorted(zip(scores, name_list, model_list), reverse=True)[:1]
    for tuple in top3:
        m.save_model(species, tuple[2], tuple[1])
    print("[+] Model saved in database.")


def main():
    warnings.filterwarnings("ignore")
    len(sys.argv)
    name = sys.argv[1]
    data = get_data(dbd.client_address, dbd.client_n, name)
    names = ['Gradient_Boosting', 'Random_Forest', 'Neural_Network', 'Adaptive_Boosting', 'Decision_Tree']
    classifiers = [GradientBoostingClassifier(), RandomForestClassifier(n_estimators=10), MLPClassifier(max_iter=1000), AdaBoostClassifier(), DecisionTreeClassifier()]
    scores = model_fit_and_evaluation(names, classifiers, data)
    storage(name, scores, names, classifiers)
    test_data = data[1]
    test_labels = test_data[dbd.target_variable]
    test_features = test_data.drop(dbd.drop_features, axis=1)
    p.evaluate(name, test_features, test_labels)
    test_features.to_csv('test.csv')

    p.predict(name, 'test.csv')


if __name__ == "__main__":
    main()

