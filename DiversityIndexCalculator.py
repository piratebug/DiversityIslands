"""
Date: May 2025
Project: Diversity Index Calculator Tool for GIS Programming Class
This program will take a series of spreadsheets from the census and use the fields
to calculate a diversity index for the respective area.

Final tool should look something like...
Table: [user input]
Overall Population: [user input field]
Diveristy Populations: [multiple user input fields]


and will function something like...
-for each Diversity Population input:
--calculate percent of overall population
--calculate natural logarithm 
--multiply percentage of population by natural log
--calculate inverse sum for each category (race, age, gender)
"""
# Imports
import pandas as pd
import arcpy

# Set workspace as a user specified parameter
ws =  arcpy.GetParameterAsText(0) # or your filepath here, for testing
arcpy.env.workspace = ws

# Inputs
inputTable = 'sample.csv' #table user will be working with
#totalPopulation = #user input field
#totalPopDiversity = [] #multiple user input columns

# Calculations
def calculateDivIndex(inputTable):
    with open(inputTable, 'r') as table:
        data = table.readlines()
    print(data)
    table.close()

## Refresh on how to use pandas to create a dataframe from a csv, select columns
## Refresh howto create new column - create new column to store div population percentages
## Figure out how to code natural logarithm
## Repeat column creation on natural log, multiplying percentges, and inverse sum
## Don't forget the try / excepts


if __name__ == "__main__":
    inputTable = 'sample.csv'

    calculateDivIndex(inputTable)



