"""
Date: May 2025
Project: Diversity Index Calculator Tool for GIS Programming Class
This program will take a series of spreadsheets from the census and use the fields
to calculate a diversity index for the respective area.

Final tool should look something like...
GEOID: [field select]
Race Table: [user input]
Race Table Fields: [user input]
Age & Gender Table: [user input]
Age & Gender Table Fields: [user input]

and will function something like...
-get FID from GEOID
-identify total pop for each race (consolidate if needed)
-calculate total men
-calculate total women
-calculate ages into 10 year groups
-calculate percentage of overall population for each
-calculate natural logarithm of each
-multiply percentage of population by natural log for each
-calculate inverse sum for each category (race, age, gender)
-weighted overlay to balance the final categories
"""
# Imports
import pandas as pd
import arcpy

# Set workspace as a user specified parameter
ws = arcpy.GetParameterAsText(0)
arcpy.env.workspace = ws

# Inputs
# set variables for the tables that will
# be manipulated, have the user designate the files



