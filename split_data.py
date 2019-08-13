# Written by Rory Austin id: 28747194
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import read_database as read


def clean_data(data_frame, split_attr):
    '''
    This function takes a data frame containing the required data set. With it
    the function finds all number types from this frame and makes a new frame containing
    only these columns. Then it will remove all NaN values. This prepares data for a scatter plot.

    :param data_frame: data set needing to be oversampled.
    :param split_attr: the attribute being used to assess reliability of the data set entries.
    :return: returns a cleaned data frame.
    '''
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
    return df


def create_training_set(data, split_attr):
    '''
    This function takes a full cleaned data set and splits the set 80/20 where the 80
    is for training and the 20 is for testing.

    :param data: A data frame containing required data set (preferably cleaned).
    :param split_attr: the attribute being used to assess reliability of the data set entries.
    :return: returns two new data frames corresponding to test and train respectively.
    '''
    y = data[split_attr]
    x = data.drop(split_attr, axis=1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    df = pd.DataFrame(x_train)
    df[split_attr] = y_train
    # df[split_attr].value_counts().plot(kind='bar', title='Count (' + split_attr + ')')
    return x, y


def plot_2d(x, y, label='Classes'):
    '''
    This function takes two data frames corresponding to the training set without labels and
    another containing the labels. It takes them and creates a scatter plot in 2d to visualize the
    type of data set we have (Should be imbalanced).

    :param x: training values without label.
    :param y: training set labels.
    :param label: label for the plot.
    :return: blank.
    '''
    colours = ['#1F77B4', '#FF7F0E', 'g']
    markers = ['o', 's', 'v']
    for l, c, m in zip(np.unique(y), colours, markers):
        plt.scatter(x[y == l, 0],
                    x[y == l, 1 or 3],
                    x[y == l, 2 or 4],
                    c=c, label=l, marker=m)

    plt.title(label)
    plt.legend(loc='upper right')
    plt.show()


data_frame = read.read_collection('Species_DB', 'Antechinus_agilis')
clean = clean_data(data_frame, 'RATING_INT')
# print(data_frame['SCIENTIFIC_DISPLAY_NME'].head())
x, y = create_training_set(clean, 'RATING_INT')
pca = PCA(n_components=3)
x_new = pca.fit_transform(x)
# print(acc, un)
plot_2d(x_new, y, 'Imbalanced dataset (3 PCA components)')