"""
Last Updated: 13 April 2026
Project: Prep Census Data tool to clean up demographic census .csv's before
running Diversity Index Calculator.

functionality includes...

- determine if RACE or AGE/GENDER dataset submitted

For RACE dataset:
X remove first row & last row
X remove second column (geographic area name)
X remove all columns that contain "margin of error"
X rename first column header TotalPop
X remove "Estimate!!Total:!!" from all other column headers
X remove "Two or more races:!!" from all other column headers
X calculate FIPS from GeoID (right 11 digits)
X creates "Total AAPI" column (sum of Asian & Native Hawaiian and Pacific Islander)
X creates "Total Multiracial" column (sum of all "Two or more" cateogries)

For AGE/GENDER dataset:
X remove first row & last row
X remove second column (geographic area name)
X remove all columns that contain "margin of error"
X remove final column
X rename first column header TotalPop
X remove "Estimate!!Total:!!" from all other column headers
X simplify column headers
X calculate FIPS from GeoID (convert to numeric)
X create new columns, grouping ages by decades
X remove excess columns

Next task: add user functionality
"""
# Imports
import pandas as pd
import tkinter as tk
from tkinter import filedialog
# import argparse  # lets you prompt users for arguments, gives error when not supplied
# from pathlib import Path  # makes the input text an actual file path

# Inputs
## create root window
root = tk.Tk()
root.withdraw()

## bring in the file
inputFile = filedialog.askopenfilename()

censusData = pd.read_csv(inputFile) #arcpy.GetParameterAsText(0)  #OR your file path here


# Calculations
def cleanData(censusData):
    # create an IF check to determine if it's a Race or Age/Gender file, direct to correct function
    # cleanRaceData(censusData)
    cleanAgeGenderData(censusData)
    # pass 

def cleanRaceData(censusData):
    try:
        print(censusData[:5]) # for testing

        # set headers to the the contents of the first row, then delete first row
        censusData.columns = censusData.iloc[0]
        censusData.drop(0, inplace = True)


        # delete last row
        censusData = censusData.iloc[:-1]
        
        # remove second column
        censusData = censusData.drop(['Geographic Area Name'], axis=1)

        # remove last column (a rogue NaN)  ***NEED TO WRITE A TEST FOR THIS, NOT SURE WHY IT SHOWS UP***
        censusData = censusData.iloc[:,:-1]

        # delete all columns containing 'margin of error' 
        marginsOfError = [col for col in censusData.columns if "Margin of Error" in col]
        censusData.drop(censusData[marginsOfError], axis=1, inplace = True)

        # rename first column header TotalPop
        censusData = censusData.rename(columns={"Estimate!!Total:": "TotalPop"})

        # strip "Estimate!!Total:!!" from other column headers
        for col in censusData.columns:
            if "Estimate!!Total:!!" in col:
                newCol = col.removeprefix("Estimate!!Total:!!")
                censusData = censusData.rename(columns={col: newCol})
                
        # further simplify column headers - remove "Two or more races:!!"
        for col in censusData.columns:
            if "Two or more races:!!" in col:
                newCol = col.removeprefix("Two or more races:!!")
                censusData = censusData.rename(columns={col: newCol})
     
        # create FIPS from GEOID (Geography column) by removing first 9 characters
        fips = [geoid[9:] for geoid in censusData.Geography]
        censusData["FIPS"] = fips
        # move it to the front
        last_col = censusData.iloc[:, -1]
        censusData = pd.concat([last_col, censusData.iloc[:, :-1]], axis=1)

        # remove Geography column
        censusData = censusData.drop(['Geography'], axis=1)

        # simplify column names
        censusData = censusData.rename(columns={
            "White alone": "White_Alone",
            "Black or African American alone": "Black_AA_Alone",
            "American Indian and Alaska Native alone": "AIAN_Alone",
            "Asian alone": "Asian_Alone",
            "Native Hawaiian and Other Pacific Islander alone": "NHPI_Alone",
            "Some other race alone": "Other_Alone",
            "Two or more races:": "Two_Plus",
            "Two races including Some other race": "Two_Incl_Other",
            "Two races excluding Some other race, and three or more races": "Two_Excl_Other_Three_Plus"
        })

        # convert all columns from strings to numbers
        censusData = censusData.apply(pd.to_numeric)

        # create AAPI column by summing Asian & Native Hawaiian and Pacific Islander columns
        censusData["AAPI"] = censusData["Asian_Alone"] + censusData["NHPI_Alone"]

        # relocate AAPI to a spot that makes sense
        col = censusData.pop("AAPI")
        censusData.insert(7, "AAPI", col)

        # create multiracial column from all two or more columns
        censusData["Total_Multiracial"] = censusData["Two_Plus"] + censusData["Two_Incl_Other"] + censusData["Two_Excl_Other_Three_Plus"]

        # print(list(censusData.columns))
        # print(censusData.iloc[:5, 3:])

        # export refined data to new .csv
        censusData.to_csv("cleanRaceData.csv")

    except Exception as issue:
        print("Oops! An error occured: ", issue)

def cleanAgeGenderData(censusData):
    try:
        print(censusData[:5]) # for testing

        # set headers to the the contents of the first row, then delete first row
        censusData.columns = censusData.iloc[0]
        censusData.drop(0, inplace = True)

        # delete last row
        censusData = censusData.iloc[:-1]
        
        # remove second column
        censusData = censusData.drop(['Geographic Area Name'], axis=1)

        # remove last column (a rogue NaN)  ***NEED TO WRITE A TEST FOR THIS, NOT SURE WHY IT SHOWS UP***
        censusData = censusData.iloc[:,:-1]
 
        # delete all columns containing 'margin of error' 
        marginsOfError = [col for col in censusData.columns if "Margin of Error" in col]
        censusData.drop(censusData[marginsOfError], axis=1, inplace = True)

        # delete all columns containing 'margin of error' 
        marginsOfError = [col for col in censusData.columns if "Margin of Error" in col]
        censusData.drop(censusData[marginsOfError], axis=1, inplace = True)

        # rename first column header TotalPop
        censusData = censusData.rename(columns={"Estimate!!Total:": "TotalPop"})

        # strip "Estimate!!Total:!!" from other column headers
        for col in censusData.columns:
            if "Estimate!!Total:!!" in col:
                newCol = col.removeprefix("Estimate!!Total:!!")
                censusData = censusData.rename(columns={col: newCol})

        # simplying column heads to use M and F
        for col in censusData.columns:
            if "Male:!!" in col:
                newCol = col.replace("Male:!!", "M_")
                censusData = censusData.rename(columns={col: newCol})
            elif "Female:!!" in col:
                newCol = col.replace("Female:!!", "F_")
                censusData = censusData.rename(columns={col: newCol})

        # further simplify columns to remove 'years' and eliminate spaces
        for col in censusData.columns:
            if "years and over" in col:
                newCol = col.replace(" years and over", "+")
            else:
                newCol = col.removesuffix(" years")
                if "Under" in newCol:
                    newCol = newCol.replace("Under ", "under")
                elif "and" in newCol:
                    newCol = newCol.replace(" and ", "and")
                else:
                    newCol = newCol.replace(" to ", "to")                
            censusData = censusData.rename(columns={col: newCol})

        # simplify column names
        censusData = censusData.rename(columns={
            "Male:": "totalMale",
            "Female:": "totalFemale"
        })

        # create FIPS from GEOID (Geography column) by removing first 9 characters
        fips = [geoid[9:] for geoid in censusData.Geography]
        censusData["FIPS"] = fips
        # move it to the front
        last_col = censusData.iloc[:, -1]
        censusData = pd.concat([last_col, censusData.iloc[:, :-1]], axis=1)

        # remove Geography column
        censusData = censusData.drop(['Geography'], axis=1)

        # make all columns numeric
        censusData = censusData.apply(pd.to_numeric)

        # create columns grouping age in decades, combining M and F
        ## under 10
        censusData["totalUnder10"] = censusData["M_under5"] + censusData["M_5to9"] + censusData["F_under5"] + censusData["F_5to9"]
        ## relocating total age groups to front
        col = censusData.pop("totalUnder10")
        censusData.insert(3, "totalUnder10", col)

        ## under 20
        censusData["totalUnder20"] = censusData["M_10to14"] + censusData["M_15to17"] + censusData["M_18and19"] + censusData["F_10to14"] + censusData["F_15to17"] + censusData["F_18and19"]
        col = censusData.pop("totalUnder20")
        censusData.insert(4, "totalUnder20", col)

        ## under 30
        censusData["totalUnder30"] = censusData["M_20"] + censusData["M_21"] + censusData["M_22to24"] + censusData["M_25to29"] + censusData["F_20"] + censusData["F_21"] + censusData["F_22to24"] + censusData["F_25to29"]
        col = censusData.pop("totalUnder30")
        censusData.insert(5, "totalUnder30", col)

        ## under 40
        censusData["totalUnder40"] = censusData["M_30to34"] + censusData["M_35to39"] + censusData["F_30to34"] + censusData["F_35to39"]
        col = censusData.pop("totalUnder40")
        censusData.insert(6, "totalUnder40", col)

        ## under 50
        censusData["totalUnder50"] = censusData["M_40to44"] + censusData["M_45to49"] + censusData["F_40to44"] + censusData["F_45to49"]
        col = censusData.pop("totalUnder50")
        censusData.insert(7, "totalUnder50", col)

        ## under 60
        censusData["totalUnder60"] = censusData["M_50to54"] + censusData["M_55to59"] + censusData["F_50to54"] + censusData["F_55to59"]
        col = censusData.pop("totalUnder60")
        censusData.insert(8, "totalUnder60", col)

        ## under 70
        censusData["totalUnder70"] = censusData["M_60and61"] + censusData["M_62to64"] + censusData["M_65and66"] + censusData["M_67to69"] + censusData["F_60and61"] + censusData["F_62to64"] + censusData["F_65and66"] + censusData["F_67to69"]
        col = censusData.pop("totalUnder70")
        censusData.insert(9, "totalUnder70", col)

        ## under 80
        censusData["totalUnder80"] = censusData["M_70to74"] + censusData["M_75to79"] + censusData["F_70to74"] + censusData["F_75to79"]
        col = censusData.pop("totalUnder80")
        censusData.insert(10, "totalUnder80", col)

        ## 80 plus
        censusData["total80+"] = censusData["M_80to84"] + censusData["M_85+"] + censusData["F_80to84"] + censusData["F_85+"]
        col = censusData.pop("total80+")
        censusData.insert(11, "total80+", col)

        # testing accuracy of calculations
        # censusData["totalsA"] = censusData["totalUnder10"] + censusData["totalUnder20"] + censusData["totalUnder30"] + censusData["totalUnder40"] + censusData["totalUnder50"] + censusData["totalUnder60"] + censusData["totalUnder70"] + censusData["totalUnder80"] + censusData["total80+"]
        # censusData["totalsB"] = censusData["totalMale"] + censusData["totalFemale"]

        # relocate totalFemale column
        col = censusData.pop("totalFemale")
        censusData.insert(3, "totalFemale", col)

        # drop extra columns
        censusData.drop(censusData.iloc[:, 13:], axis=1, inplace = True)

        print(censusData[:5]) # for testing
        # print(list(censusData.columns))
    
    except Exception as issue:
        print("Oops! An error occured: ", issue)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser() # lets you prompt users for arguments, gives error when not supplied
    # parser.add_argument("inputFile", type=Path) # makes the input text an actual file path
    # results = parser.parse_args()
    # print(results)
    cleanData(censusData)
