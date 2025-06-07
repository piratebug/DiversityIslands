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
import arcpy
import pandas as pd


# Set workspace as a user specified parameter
ws = #arcpy.GetParameterAsText(0) # or your filepath here, for testing
arcpy.env.workspace = ws


# Inputs
#inputTable = arcpy.GetParameterAsText(1) #table user will be working with
#totalPopluation = arcpy.GetParameterAsText(2) #user input field
#totalPopDivList = arcpy.GetParameterAsText(3) #user input multiple columns
inputTable = 'sample.csv'
totalPopulation = 'Total'
totalPopDivList = ['White', 'Black', 'Native', 'Asian', 'Other']


# Calculations
def calculateDivIndex(inputTable, totalPopulation, totalPopDivList):
    data = pd.read_csv(inputTable)

    for div in totalPopDivList:
        divPerc = div + " Perc"
        data[divPerc] = data[div] / data[totalPopulation]
    

    print(data.head())


    
## Figure out how to code natural logarithm
## Repeat column creation on natural log, multiplying percentges, and inverse sum
## Don't forget the try / excepts


if __name__ == "__main__":
    inputTable = 'sample.csv'

    calculateDivIndex(inputTable, totalPopulation, totalPopDivList)



