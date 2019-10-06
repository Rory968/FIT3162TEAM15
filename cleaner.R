#!/usr/bin/env Rscript
# Written by Rory Austin id: 28747194

#--------------------------------
#Getting point data from database
#--------------------------------
zz <- file("messages.Rout", open="wt")
sink(zz, type="output")
sink(zz, type="message")
library(mongolite)
library(dplyr)
library(sp)
library(caret)
library(usdm)
library(DMwR)
library(stringr)

args <- commandArgs(trailingOnly = TRUE)
name <- str_replace_all(as.character(args), "[\r\n]", "")

# Establishes a connection with the database
require(mongolite)
connection <- mongo(collection = name, db = "raw_data", url = "mongodb://localhost")
points <- connection$find()
connection$disconnect()
points <- data.frame(points)
points <- subset(points, points$RATING_INT != 1)
points <- subset(points, points$RATING_INT != 3)
points <- points[c("LATITUDEDD_NUM", "LONGITUDEDD_NUM", "RATING_INT")]




#----------------
# Get Raster data
#----------------

# Retrieves predictor(raster) values from the worldclim database, [global climate data]
bio <- raster::getData("worldclim", var='bio', res=10)

# Initializes library and looks for colinearity problems in the raster data
v1 <- vifstep(bio)
v2 <- vifcor(bio,th=0.9)

# Removes raster layers with colinearity issues
biom <- exclude(bio, v1, v2)
# Stores used features in the database for future prediction use
features <- data.frame(names(biom))
require(mongolite)
connection <- mongo(collection = name, db = "features", url = "mongodb://localhost")
connection$insert(features)
connection$disconnect()
#-------------------------------------------
# Turn rating value into a factor
points$RATING_INT = as.factor(points$RATING_INT)

# Break set into train and test sets (only oversample test set)
index <- createDataPartition(points$RATING_INT, p = 0.85, list = FALSE)
train_set <- points[index, ]
test_set <- points[-index, ]


train_set <- train_set %>% dplyr::select("LATITUDEDD_NUM", "LONGITUDEDD_NUM", "RATING_INT")
train_set <- na.omit(train_set)
coordinates(train_set)<-~LONGITUDEDD_NUM+LATITUDEDD_NUM
# Plot points on a map
proj4string(train_set) <- projection(raster())
# mapview(train_set)
training <- extract(biom, train_set)
training <- cbind(train_set, training)
train_set <- data.frame(training)

# The below smote declaration will under sample
# smote <- SMOTE(RATING_INT~., data=points)
# Import oversampling library and create oversampled set
smote <- SMOTE(RATING_INT~., train_set, perc.over = 100, k=5, perc.under = 200)
# Convert the oversampled data set to spatial points
smote <- data.frame(smote)
# smote <- SMOTE(RATING_INT~points, smote, perc.over = 1000)
smote <- smote %>% dplyr::select("LATITUDEDD_NUM", "LONGITUDEDD_NUM", "RATING_INT")
smote <- na.omit(smote)
coordinates(smote)<-~LONGITUDEDD_NUM+LATITUDEDD_NUM
# Plot points on a map
proj4string(smote) <- projection(raster())
# mapview(smote)

name

#library(sdm)
# Creates an sdmData object that presents a data set with all three types (presence, absence, environment)
training <- extract(biom, smote)
training <- cbind(smote, training)
training <- data.frame(training)
training <- na.omit(training)
train_connection <- mongo(collection = name, db = "training_data", url = "mongodb://localhost")
train_connection$insert(training)
train_connection$disconnect()
#write.csv(training, file="training.csv")


# Extracts point values from the observational dataframe
test_set <- test_set %>% dplyr::select("LATITUDEDD_NUM", "LONGITUDEDD_NUM", "RATING_INT")
test_set <- na.omit(test_set)
coordinates(test_set)<-~LONGITUDEDD_NUM+LATITUDEDD_NUM
proj4string(test_set) <- projection(raster())
#mapview(test_set)


testing <- extract(biom, test_set)
testing <- cbind(test_set, testing)
testing <- data.frame(testing)
testing <- na.omit(testing)
test_connection <- mongo(collection = name, db = "testing_data", url = "mongodb://localhost")
test_connection$insert(testing)
test_connection$disconnect()
#write.csv(testing, file="testing.csv")

