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
import numpy as np
import pandas as pd


# Test Inputs
##inputTable = 'sample.csv'
##totalPopulation = 'Total'
##totalPopDivList = ['White', 'Black', 'Native', 'Asian', 'Other']


# Calculations
def calculateDivIndex(inputTable, totalPopulation, totalPopDivList):

    # Prep totalPopDivList because the multiple value Fields data arrives as "input;input"
    # rather than a list of strings such as ["input","input"]
    # Remove single quotes then split by semicolon
    totalPopDivList = totalPopDivList.replace("'","")
    totalPopDivList = totalPopDivList.split(";")
    
    data = pd.read_csv(inputTable)
    totalDivDivList = []
    forRemoval = []
    sumData = 0.0

    arcpy.AddMessage("Test")

    try:
        for div in totalPopDivList:
            divPerc = div + " Perc" # population percentages
            divLog = div + " Log"   # natural logs of percentages
            divDiv = div + " Div"   # diversification (percentages * natural logs)
            
            # Create columns for and calculate percentages for each diversity column
            data[divPerc] = data[div] / data[totalPopulation]
            forRemoval.append(data[divPerc])
            arcpy.AddMessage('Calculating diversity percentages...')
            
            # Create columns for and calculate natural log of each diversity percentage
            data[divLog] = np.log(data[divPerc])
            forRemoval.append(data[divLog])
            arcpy.AddMessage('Calculating natural logs...')
            
            # Errors with inf/-inf when log encounters '0' in divPerc, replaces infs with 0
            data[divLog].replace([np.inf, -np.inf], 0, inplace = True)
            
            # Multiply each population percentage by its Natural Log
            data[divDiv] = data[divPerc] * data[divLog]
            arcpy.AddMessage('Calculating diversification...')
            
            # Create list of diversifictions to iterate through later
            totalDivDivList.append(data[divDiv])

        # Calculate the inverse sum of all the diversifications (divDiv)
        for div in totalDivDivList:
            sumData = sumData + div
            
            # Inverse of the sum becomes the Diversity Index
            data['Diversity Index'] = -sumData
            arcpy.AddMessage('Calculating diversity index...')

        # Clean up columns
        for div in totalPopDivList:
            divPerc = div + " Perc" # population percentages
            divLog = div + " Log"   # natural logs of percentages
            divDiv = div + " Div"   # diversification (percentages * natural logs)

            del data[divPerc]
            del data[divLog]
            del data[divDiv]
        arcpy.AddMessage('Cleaning up data...')


        data.to_csv(inputTable)

    except Exception as issue:
        print("Error occured: ", issue)
        






if __name__ == "__main__":
    inputTable = arcpy.GetParameterAsText(0)         # table user will be working with
    totalPopulation = arcpy.GetParameterAsText(1)    # user input field
    totalPopDivList = arcpy.GetParameterAsText(2)  # user input multiple columns
    
    calculateDivIndex(inputTable, totalPopulation, totalPopDivList)



