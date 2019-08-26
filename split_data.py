# Written by Rory Austin id: 28747194
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import TomekLinks, RandomUnderSampler
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import read_database as read

'''
This file contains all functions and data types relevant to the over-sampling work needed to manipulate the
point data. The block below runs through the process used. All of the functions below this comment block are
used to make that process happen.
'''


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
    # currently only splits into labels and coordinates, doesnt actually creates test set all there though.
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
    pca = PCA(n_components=2)
    x_new = pca.fit_transform(x)
    two_colour = ['#1F77B4', '#FF7F0E']
    two_marker = ['o', 's']
    for l, c, m in zip(np.unique(y), two_colour, two_marker):
        plt.scatter(x_new[y == l, 0],
                    x_new[y == l, 1],
                    c=c, linewidth=0.5, label=l, marker=m)

    plt.title(label)
    plt.legend(loc='upper right')
    plt.show()


def oversampleSMOTE(x, y):
    '''
    This function over-samples the data using SMOTE. This results in a higher
    concentration of minority class points. In our case we will be using occurence data so
    the minority class are the data points that are close to range.

    :param x: data without labels.
    :param y: corresponding labels.
    :return: returns an oversampled numpy array and labels.
    '''
    smote = SMOTE(ratio='minority')
    x_sm, y_sm = smote.fit_sample(x, y)
    # print(x.shape[0], x_sm.shape[0])
    print(x_sm.shape[0] - x.shape[0], 'new synthetic points')
    plot_2d(x_sm, y_sm)
    return x_sm, y_sm


def random_over(x, y):
    '''
    This function over-samples the data randomly, this means creating duplicates.
    Not as effective as SMOTE but is used on the majority class which is more useful
    in terms of occurence data sets.

    :param x: data without labels.
    :param y: corresponding labels.
    :return: returns an oversampled numpy array and labels.
    '''
    ros = RandomOverSampler()
    x_ros, y_ros = ros.fit_sample(x, y)
    # print(x.size, x_ros.size)
    print(x_ros.shape[0] - x.shape[0], 'new random picked points')
    plot_2d(x_ros, y_ros, 'ROS')
    return x_ros, y_ros


def tomek_under(x, y):
    '''
    This function uses tomek links to under-sample the data set,
    Only balances slightly, doesnt really accoutn for the minority class.

    :param x: data without labels.
    :param y: corresponding labels.
    :return: returns an under-sampled numpy array and labels.
    '''
    tl = TomekLinks(return_indices=True, ratio='majority')
    x_tl, y_tl, id_tl = tl.fit_sample(x, y)
    print('Removed Indexses: ', id_tl)
    plot_2d(x_tl, y_tl, 'Tomek Under-sampling')
    return x_tl, y_tl


def random_under(x, y):
    '''
    This function uses random under-sampling to balance the majority
    set with the minority set. This does well to balance but as a result a lot of data is lost.

    :param x: data without labels.
    :param y: corresponding labels.
    :return: returns under-sampled numpy array and labels.
    '''
    rus = RandomUnderSampler(return_indices=True)
    x_rus, y_rus, id_rus = rus.fit_sample(x, y)
    print('Removed indexes: ', id_rus)
    plot_2d(x_rus, y_rus, 'Random under-sampling')
    return x_rus, y_rus



'''
This block of code splits and cleans the data and then oversamples the data and returns the corresponding data and its labels.
There are a number of different methods for doing this, there are SMOTE and Random over-sampling aswell as Tomek-links and 
Random under-sampling.
Currently the random under-sampling is running but all options are there to be commented and uncommented in future.

This currently has base functionality and does not write to the data-base. These features will be added later according to plan.
'''

df = read.read_collection('Species_DB', 'Antechinus_agilis')


rating_header = 'RATING_INT'
points = df[['LATITUDEDD_NUM', 'LONGITUDEDD_NUM', rating_header]]
points = points.dropna()
points[points[rating_header] == 2] = 1
points_x, points_y = create_training_set(points, rating_header)
plot_2d(points_x, points_y, 'Imbalanced dataset (2 PCA components)')


# Split the points into presence and absence points (for data frame)
presence = points[points[rating_header] == 0]
absence = points[points[rating_header] == 1]
pres_x, pres_y = create_training_set(presence, rating_header)
ab_x, ab_y = create_training_set(absence, rating_header)


# sm = oversampleSMOTE(points_x, points_y)[0]
# ros = random_over(points_x, points_y)[0]
# tl = tomek_under(points_x, points_y)[0]
rus = random_under(points_x, points_y)[0]
# print(tl.shape[0], tl.tolist())

