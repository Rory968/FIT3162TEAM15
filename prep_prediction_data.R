#!/usr/bin/env Rscript
# Written by Rory Austin id: 28747194

#--------------------------------
#Getting point data from database
#--------------------------------
zz <- file("messages.Rout", open="wt")
sink(zz, type="message")
library(mongolite)
library(stringr)

args <- commandArgs(trailingOnly = TRUE)
name <- str_replace_all(as.character(args), "[\r\n]", "")
# Establishes a connection with the database
require(mongolite)
connection <- mongo(collection = name, db = "temp", url = "mongodb://localhost")
points <- connection$find()
connection$disconnect()
points <- data.frame(points)
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
#-------------------------------------------


predictor <- extract(biom, points)
predictor <- cbind(points, predictor)
testing <- data.frame(predictor)
# predictor <- na.omit(testing)
test_connection <- mongo(collection = name, db = "backlog", url = "mongodb://localhost")
test_connection$insert(testing)
test_connection$disconnect()