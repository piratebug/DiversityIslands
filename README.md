# Diversity Islands
A set of GIS tools to calculate diversity indeces from census data and automate the workflow of creating islands of diversity for a geographic area.

These tools are designed to work best in the following order, but should function on their own individually.
* PrepCensusData.py - A script to clean up the standard formatting of ACS Census Data [INCOMPLETE]
* DiversityIndexCalculator.py - Designed for use in ArcGIS Pro. Given a table and specified fields, calculates the [Diversity Index](https://www.statology.org/shannon-diversity-index/). [COMPLETE]
