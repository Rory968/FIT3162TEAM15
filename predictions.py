import models as m
from sklearn import metrics


def evaluate(species, test_data, test_labels):
    model = m.load_model(species)
    pred = model.predict_proba(test_data)[:, 1]
    score = metrics.roc_auc_score(test_labels, pred)
    print('AUC:', score)

