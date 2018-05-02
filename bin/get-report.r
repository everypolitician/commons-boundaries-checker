#!/usr/bin/env Rscript

# The following packages must be installed for this to work locally:
# rgdal, gdalUtils and cleangeo
# To do this start R locally and run:
# > install.packages("rgdal")
# > install.packages("gdalUtils")
# > install.packages("cleangeo")


args = commandArgs(trailingOnly=TRUE)

# FIXME: give a more helpful error if there are != 1 arguments
shapefile <- args[1]

suppressMessages(require('rgdal'))
suppressMessages(require('gdalUtils'))
suppressMessages(require('cleangeo'))

sp <- readOGR(shapefile)
report <- clgeo_CollectionReport(sp)
summary <- clgeo_SummaryReport(report)

all.valid <- all(report$valid)

if (!all.valid) {
   print(report)
   quit(status=1)
} else {
	print(summary)
}
