User Guide

-------Setting up the environment------

To set up the system we will need to configure these 3 things
R and Rstudio
MongoDB
Python


----R and Rstudio----

Prior to download of the application folder we need to do a setup so that the system runs properly, firstly we need to download R studio, to do so follow this link.

https://rstudio.com/products/rstudio/download/

And download Rstudio Desktop which is free. This is the process for windows, for linux or mac it may be slightly different.

From here follow the prompts until you are greeted with the GUI for Rstudio. Keep this open for later.

From here we need to make sure that R can be run from the command line. In most downloads this should be done automatically. To test that it is working type
‘Rscript’
In the command line, if R information is displayed this works correctly. If this is not the case follow this link to set this up.

https://www.datacamp.com/community/tutorials/installing-R-windows-mac-ubuntu


----MongoDB----

Now we want to download the environment for mongodb on the system. We will be installing MongoDB server locally on the system. This link will show you how if you're on windows.

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/

If you are using Linux or Mac follow this link and pick the relevant system instructions

https://docs.mongodb.com/manual/installation/

With this installed make sure you can use mongodb from the command line, in most systems you should be able to just type mongo in the command line and if it displays the mongodb version this means the download has been successful.

Optionally you can install the mongoDB compass graphical user interface, this is shown as part of the process in the demo script. Follow this link to download the GUI.

https://docs.mongodb.com/compass/master/install/

From this link just pick the relevant os and follow the instructions.


----Python----

Installing python is the easiest step in this process to do so just follow this link and pick the latest version.

https://www.python.org/downloads/

Make sure that python will run in the command line, this should be done automatically during download, type
‘Python’
In the terminal, if version information displays the process is successful.

----Environment-----

Now download the sdm.zip file and extract this to the desired directory in the system. First thing you will do is open the extracted folder and locate
‘Setup.R’
Now open this in Rstudio and run the script by highlighting all of the text and pressing CTRL + Enter

The time taken to run this will vary but should be between 2 and 10 minutes.

Next open the terminal and change the directory into the sdm folder. When youre in the sdm folder type…

>python setup.py

Which will install all of the necessary packages on your system. Once this is run the setup is complete and you can follow the demo script for a demo of how this application is used.

-------------Using the Application---------------

Data preprocessed using

>python populate_database.py Monash_sample_VBA.xls

Preprocessing created 4 databases called features, raw_data, training_data and testing_data respectively.

Raw_data corresponds to the original data from xls, training and testing are formatted to work with models, and features represents proper data necessary for formatting new prediction data when the need arises.

The populate_database.py operation takes around about 1.2 minutes on unix machines and between 2.8 and 3.5 minutes on windows.

You will be presented with a screen containing a terminal and a database gui side by side. After each command press the refresh button inside the database gui, it will look list the following. Circled in the top left corner of this image.

Type:

>python list_names.py data

This will provide you with a list of arguments you can use for the build_model operation, You can pick any one of these, in this case our later prediction data corresponds to the first argument, because of this now type...

>python build_model.py Antechinus_agilis

Now press the refresh button inside the gui, you will be presented with a new database called ‘models’ it will look like the following.


Inside it will have a single collection under the name of the argument passed. This means we now have a model. Now to find out what models exist in the database type.

>python list_names.py model

This will list all the existing models in the database, to find out the accuracy and model type of our demo model, write the following command in the terminal.

>python accuracy.py Antechinus_agilis

This will print the model type and accuracy in the terminal. After we have a clear view of what our model looks like we can use it to predict the reliability of new observations. This requires two arguments, the species of which the
observations correspond with and the filename containing all of the unassessed observations. In our case the filename is trial.xls and the species is Antechinus_agilis.

Type the following in the terminal,

>python predict.py Antechinus_agilis trial.xls

This will place a new file in the users downloads folder under the name prediction.xls that contains the input data complete with a new column that shows the reliability score of a given observation.



