# Recomendations for New Shot Spotter Sensors in Washington D.C. Election Wards

<b>Maddie Guy</b>

<b>4 August 2019</b>

<b>mguy1@umd.edu</b>

<b>Introduction</b>

The code contained and documented here performs an automation of a process to determine what Washington D.C. election wards should install new Shot Spotter sensors in an effort to more effectively record gun shots. This analysis is determined by conducting a geospatial analysis using D.C. gun crime data and Shot Spotter incident data from DCGIS Open Data: Public Safety. Based on the following analysis, it is recommended that more Shot Spotter sensors are installed in Ward 2; while there were only 54 gun crimes reported per in 2017, there were only 2 Shot Spotter incidents, suggesting that there are a gun shots in this ward not captured by the current Shot Spotter sensor network.

<b>Analysis</b>

Data used for this analysis was collected from DCGIS Open Data, an open source repository of GIS data managed by the D.C. government and provided for free and public use. Gun crime point data was downloaded and processed from the 2017 crime incidents dataset. Shot Spotter incident point data for 2017 was downloaded and processed from another dataset that records all Shot Spotter incidents in the sensor network. Election ward polygon data from 2012 was also downloaded from this source.

Crime data: https://opendata.dc.gov/datasets/crime-incidents-in-2017

Shot Spotter data: https://opendata.dc.gov/datasets/89bfd2aed9a142249225a638448a5276_29

Election ward data: https://opendata.dc.gov/datasets/ward-from-2012

![crime_per](crime_per.jpeg)

![ss_per](ss_per.jpeg)

<b>Automation</b>

<b>Results</b>
