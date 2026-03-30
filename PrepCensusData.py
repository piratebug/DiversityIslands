"""
Date: May 2025
Project: Prep Census Data tool to clean up demographic census .csv's before
running Diversity Index Calculator.

functionality includes...
- remove first row & last row
- remove second column (geographic area name)
- remove all columns that contain "margin of error"
- rename first column header TOTAL_POP
- remove "Estimate!!Total:!!" from all other column headers
- calculate FIPS from GeoID (right 11 digits)
"""
# Imports
import numpy as np
import pandas as pd
# import argparse  # lets you prompt users for arguments, gives error when not supplied
# from pathlib import Path  # makes the input text an actual file path

# Inputs
censusData = pd.read_csv("complexSample.csv") #arcpy.GetParameterAsText(0)  #OR your file path here


# Calculations
def cleanData(censusData):
    try:
        print(censusData) # for testing

        # delete first row
        censusData.drop(0, inplace = True)

        # delete last row
        censusData = censusData.iloc[:-1]
        
        # THERE MUST BE A BETTER WAY

        print(censusData)

        # censusData.to_csv("cleanData.csv") # create new file for data output

    except Exception as issue:
        print("Error occured: ", issue)



if __name__ == "__main__":
    # parser = argparse.ArgumentParser() # lets you prompt users for arguments, gives error when not supplied
    # parser.add_argument("inputFile", type=Path) # makes the input text an actual file path
    # results = parser.parse_args()
    # print(results)
    cleanData(censusData)
