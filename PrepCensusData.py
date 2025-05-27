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

censusData = arcpy.GetParameterAsText(0)  #OR your file path here


def cleanData(censusData):
    try:
        with open(censusData, "r") as censusTable:
            data = censusTable.readlines()

    except Exception as issue:
        print("Error occured: ", issue)

    print(data[0])



if __name__ == "__main__":
    cleanData(censusData)
