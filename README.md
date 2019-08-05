# Recomendations for New Shot Spotter Sensors in Washington D.C. Election Wards

<b>Maddie Guy</b>

<b>4 August 2019</b>

<b>mguy1@umd.edu</b>

<b>Introduction</b>

<p>The code contained and documented here performs an automation of a process to determine what Washington D.C. election wards should install new Shot Spotter sensors in an effort to more effectively record gun shots. This analysis is determined by conducting a geospatial analysis using D.C. gun crime data and Shot Spotter incident data from DCGIS Open Data: Public Safety. Based on the following analysis, it is recommended that more Shot Spotter sensors are installed in Ward 2; while there were only 54 gun crimes reported per in 2017, there were only 2 Shot Spotter incidents, suggesting that there are a gun shots in this ward not captured by the current Shot Spotter sensor network.</p>

<b>Analysis</b>

<p>Data used for this analysis was collected from DCGIS Open Data, an open source repository of GIS data managed by the D.C. government and provided for free and public use. Gun crime point data was downloaded and processed from the 2017 crime incidents dataset. Shot Spotter incident point data for 2017 was downloaded and processed from another dataset that records all Shot Spotter incidents in the sensor network. Election ward polygon data from 2012 was also downloaded from this source. The election ward polygons also contain 2010 population numbers for each ward, which was used in the analysis.</p>

<p>Crime data: https://opendata.dc.gov/datasets/crime-incidents-in-2017</p>

<p>Shot Spotter data: https://opendata.dc.gov/datasets/89bfd2aed9a142249225a638448a5276_29</p>

<p>Election ward data: https://opendata.dc.gov/datasets/ward-from-2012</p>

![crime_per](crime_per.jpeg)
<i>Figure 1: Number of gun crimes per 10,000 people in D.C.'s election wards in 2017</i>

<p>Following a geospatial analysis that joined gun crime incidents and Shot Spotter incidents to each election ward, the count of gun crime incidents per ward was divided by the 2010 population divided by 10,000 to determine the number of gun crime incidents per 10,000 people, as shown in Figure 1. As seen in the figure, most of gun crime incidents occur in the southeast of D.C. (depicted by the darker colors in figure 1).</p>

![ss_per](ss_per.jpeg)
<i>Figure 2: Number of Shot Spotter gun shots per 10,000 people in D.C.'s election wards in 2017</i>
<p>Figure 2 displays number of Shot Spotter incidents per 10,000 people in each ward. The analysis to calculate the incidents was the same as the analysis used to determine gun crimes per 10,000 people, however, the Shot Spotter incident count was used instead of gun crime count. Similar to the pattern seen in Figure 1, Shot Spotter incident reports are mostly focused in the southeast of the region, however, there is a noticeable disconnect between the number of gun crimes and Shot Spotter incidents in Ward 2 when comparing Figure 1 and Figure 2.</p>

<table>
  <tr>
    <th>Ward Number</th>
    <th>Number of gun crimes per 10,000 people in 2017</th> 
    <th>Number of Shot Spotter incidents per 10,000 people in 2017</th>
  </tr>
  <tr>
    <td>1</td>
    <td>16</td> 
    <td>18</td>
  </tr>
  <tr>
    <td>2</td>
    <td>8</td> 
    <td>0</td>
  </tr>
  <tr>
    <td>3</td>
    <td>3</td> 
    <td>0</td>
  </tr>
  <tr>
    <td>4</td>
    <td>18</td> 
    <td>23</td>
  </tr>
  <tr>
    <td>5</td>
    <td>38</td> 
    <td>60</td>
  </tr>
  <tr>
    <td>6</td>
    <td>23</td> 
    <td>40</td>
  </tr>
  <tr>
    <td>7</td>
    <td>59</td> 
    <td>238</td>
  </tr>
  <tr>
    <td>8</td>
    <td>61</td> 
    <td>304</td>
  </tr>
</table>
<i>Table 1: Counts of gun crime and shot spotter incidents in D.C.'s election wards per 10,000 people</i>

<i>Note: gun crime and Shot Spotter incident counts are rounded to the nearest whole number</i>

<p>As seen in Table 1, election wards with very high gun crime numbers, such as wards 7 and 8 also report high Shot Spotter gun shot counts. Simialrly, wards with medium to low gun crime rates report medium to low Shot Spotter gun shot counts, respectively. However, ward 2 has a medium rate of gun crime, with almost no Shot Spotter gun shots recorded.</p>

<b>Automation</b>

<p>Python code written to automate this analysis was done in QGIS using QGIS processing tools. The first section of code automatically cleans the data by pulling out gun crimes from the crime incident shapefille and Shot Spotter incidents from 2017 from the full Shot Spotter dataset.</p>
  
```py
iface.addVectorLayer(crime,"crime","ogr")
crimeLayer = processing.getObject(crime)
expr = "METHOD = 'GUN'"
selection = crimeLayer.getFeatures(QgsFeatureRequest().setFilterExpression(expr))
crimeLayer.setSelectedFeatures([k.id() for k in selection]) 

_writer = QgsVectorFileWriter.writeAsVectorFormat(crimeLayer, 'S:/682/Summer19/mguy1/final/Gun_Crime.shp', "utf-8", None, "ESRI Shapefile", onlySelected=True)
gunCrime = "S:/682/Summer19/mguy1/final/Gun_Crime.shp"
iface.addVectorLayer(gunCrime,"gunCrime","ogr")
```

<p>Following the cleaning of the data, spatial joins were performed to join counts of gun crimes and Shot Spotter incidents to the election ward polygons.</p>

```py
processing.runalg("qgis:joinattributesbylocation",
    {'TARGET':ward_gunCrime,'JOIN':ss17,'PREDICATE':u'contains','SUMMARY':1,'KEEP':1,'OUTPUT':"S:/682/Summer19/mguy1/final/ward_crime_ss.shp"})
ward_crime_ss = "S:/682/Summer19/mguy1/final/ward_crime_ss.shp" 
QgsMapLayerRegistry.instance().removeAllMapLayers()
iface.addVectorLayer(ward_crime_ss,"ward_crime_ss","ogr")
```

<p>Finally, a for loop was created to display the counts of gun crimes and Shot Spotter incidents in each ward. This loop also calculated the 2010 population divided by 10,000, and divided the counts by that number.</p>

```py
for feature in features:
    if feature["count_1"] == NULL:
        print(feature["NAME"] + " had")
        print(feature["count"]/(feature["POP_2010"]/10000))
        print("gun crimes per 10,000 people in 2017, and 0 Shotspotter incidents in 2017.")
        print(" ")
    else:
        print(feature["NAME"] + " had")
        print(feature["count"]/(feature["POP_2010"]/10000))
        print("gun crimes per 10,000 people in 2017, and")
        print(feature["count_1"]/(feature["POP_2010"]/10000))
        print( "Shot Spotter incidents per 10,000 people in 2017.")
        print(" ")
```

<b>Results</b>

<p>As described in the analysis documentation above, it is recommended that the Shot Spotter sensor network is expanded to include more sensors in Ward 2 due to the disconnect between the gun crimes and recorded Shot Spotter incidents.</p>

<p>One limitation of this analysis is that the code is not fully automated to record statistics such as the counts per 10,000 people in shapefile as an attribute for each feature. Thus, to create any maps or figures using these statistics, they must be entered manually into the attribute table.</p>

<p>Another limitation of this analysis is with the data used, specifically the gun crime data. While we know that crimes used in this analysis were gun crimes, we do not know how many shots were fired in each crime (or feature in the shapefile). Thus, there may be more or gun shots that are not captured by Shot Spotter sensors, but are also not captured in the gun crime data we are using.</p>
