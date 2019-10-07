sdm
---
Written by Rory Austin id: 28747194


Description:

This tool is used for automating the process of species distribution modelling, it is able to create models and use them to predict
the reiability of given species observations in the required format. It provides details on the accuracy of the model and the most useful
features within certain prediction operations.

It also gives the ability ot add new data to the training sets to further the model building, aswell as opertations to reset the database should
it be needed.



Details:

Program runs locally on a setup system.

File for extra data should be in the same format as Monash_sample_VBA.xls given by delwp.
Primarily it needs 'LONGITUDEDD_NUM', 'LATITUDEDD_NUM' and 'RATING_INT' features.

prediction data should have similar format exluding the 'RATING_INT' feature as this will be provided by the model.



Configuration:

A number of things must be installed on the system beforehand,

MongoDB server must be installed locally and a localhost connection must be established.
Rstudio must be downloaded along with R 3.6.1.
Setup.R must be run from within Rstudio to correctly configure R environment.
R path must be configured inside the system environment settings.
Python must be installed on the system.




How to use:

This library has 4 main methods for creating and using species distribution models

Main commands:
To clear database of any tables,
>python    empty_database.py

To populate the database with new data,
>python    populate_database.py    filename.xls

To build a model based on this data (Based on specific species name),
>python    build_model    species_name

To load model and make new predictions,
> python    make_predictions    filename.xls


Other commands:
To load a model and evaluate it,
> python    evaluate_model    species_name

To list all possible arguments at a given time,
> python    list_names    ('model', 'data' or 'help' are the three arguments this module takes, use help for more info.)
