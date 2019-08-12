import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import read_database as read


def clean_data(data_frame, split_attr):
    cols = list(data_frame.select_dtypes(include=['float64', 'int64']).columns)
    df = data_frame[cols]
    av = []
    for name in cols:
        av.append(df[name].count()/len(df))
    safe = []
    for i in range(len(av)):
        if av[i] == 1 or cols[i] == split_attr:
            safe.append(cols[i])

    df = df[safe]
    df = df.dropna()
    print(df)
    return df


def create_training_set(data, split_attr):
    # ADD DOCSTRING
    y = data[split_attr]
    x = data.drop(split_attr, axis=1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    df = pd.DataFrame(x_train)
    df[split_attr] = y_train
    df[split_attr].value_counts().plot(kind='bar', title='Count (' + split_attr + ')')
    print(df[split_attr].value_counts())
    return x, y


def plot_2d(x, y, label='Classes'):
    # ADD DOCSTRING
    colours = ['#1F77B4', '#FF7F0E']
    markers = ['o', 's']
    for l, c, m in zip(np.unique(y), colours, markers):
        plt.scatter(x[y == l, 0],
                    x[y == l, 1 or 2],
                    c=c, label=l, marker=m)

    plt.title(label)
    plt.legend(loc='upper right')
    plt.show()


data_frame = read.read_collection('Species_DB', 'Antechinus_agilis')
clean = clean_data(data_frame, 'RATING_INT')
# print(data_frame['SCIENTIFIC_DISPLAY_NME'].head())
x, y = create_training_set(clean, 'RATING_INT')
pca = PCA(n_components=2)
x_new = pca.fit_transform(x)
plot_2d(x_new, y, 'Imbalanced dataset (3 PCA components')