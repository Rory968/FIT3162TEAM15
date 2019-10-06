#!/usr/bin/env Rscript
# Written by Rory Austin id: 28747194

#--------------------------------
#Getting point data from database
#--------------------------------
zz <- file("messages.Rout", open="wt")
sink(zz, type="message")
sink(zz, type="output")
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
connection <- mongo(collection = name, db = "temp", url = "mongodb://localhost")
points <- connection$find()
connection$disconnect()
points <- data.frame(points)
points <- points[c("LATITUDEDD_NUM", "LONGITUDEDD_NUM")]
#----------------
# Get Raster data
#----------------

# Retrieves predictor(raster) values from the worldclim database, [global climate data]
require(raster)
cwd <- getwd()
path <- paste(cwd, 'wc10', sep = '/')
hdr <- list.files(path=path, pattern='\\.bil$', full.names = TRUE)
bio <- stack(hdr)
# Initializes library and looks for raster layers corresponding to training data
connection <- mongo(collection = name, db = "features", url = "mongodb://localhost")
features <- connection$find()
connection$disconnect()
features <- as.character(unlist(features))
biom <- raster::dropLayer(bio, features)

#-------------------------------------------

points <- points %>% dplyr::select("LATITUDEDD_NUM", "LONGITUDEDD_NUM")
coordinates(points)<-~LONGITUDEDD_NUM+LATITUDEDD_NUM
predictor <- extract(biom, points)
points <- data.frame(points)
predictor <- cbind(points, predictor)
testing <- data.frame(predictor)
#testing
# predictor <- na.omit(testing)
test_connection <- mongo(collection = name, db = "backlog", url = "mongodb://localhost")
test_connection$insert(testing)
test_connection$disconnect()