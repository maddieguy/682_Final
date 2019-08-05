#Maddie Guy
#GEOG682, Final Project
#4 August 2019

#This script automates the process of analyzing DC crime in 2017 using Shot Spotter data, crime data, and election wards from 2012.
#This script outputs number of gun crimes and number of Shot Spotter incidents IN 2017 per 10,000 people per each ward.

###########################
###### PRE-ANALYSIS STEPS ######
###########################

from qgis.PyQt.QtCore import QVariant #Import QVariant tools
import processing #Import QGIS processing tools
wards = "S:/682/Summer19/mguy1/final/Ward_from_2012.shp" #Save 2012 election wards shapefile as new variable "wards"
crime = "S:/682/Summer19/mguy1/final/Crime_Incidents_in_2017.shp" #Save crime incidents shapefile as new variable "crime"
shotspotter = "S:/682/Summer19/mguy1/final/Shot_Spotter_Gun_Shots.shp" #Save shot spotter data as new variable "shotspotter"

######CRIME######
iface.addVectorLayer(crime,"crime","ogr") #Add crime shapefile to map
crimeLayer = processing.getObject(crime) #Selects the crime layer for processing
expr = "METHOD = 'GUN'" #Defines an expression to be used to select all crimes where a gun was used
selection = crimeLayer.getFeatures(QgsFeatureRequest().setFilterExpression(expr)) #Defines selection criteria based on the expression defined above. Returns list of ids that fit selection criteria
crimeLayer.setSelectedFeatures([k.id() for k in selection]) #Selects the ids from  the list above in the target layer

_writer = QgsVectorFileWriter.writeAsVectorFormat(crimeLayer, 'S:/682/Summer19/mguy1/final/Gun_Crime.shp', "utf-8", None, "ESRI Shapefile", onlySelected=True) #Exports selected features (gun crimes) to new shapefile
gunCrime = "S:/682/Summer19/mguy1/final/Gun_Crime.shp" #Defines new Gun_Crime shapefile to gunCrime variable
iface.addVectorLayer(gunCrime,"gunCrime","ogr") #Adds gunCrime shapefile to map

######SHOTSPOTTER######
iface.addVectorLayer(shotspotter,"shotspotter","ogr") #Add shotspotter shapefile to map
ssLayer = processing.getObject(shotspotter) #Selects the shotspotter layer for processing
expr2 = "year(DATETIME) = 2017" #Defines an expression to be used to select all shots from 2017
selection2 = ssLayer.getFeatures(QgsFeatureRequest().setFilterExpression(expr2)) #Defines selection criteria based on the expression defined above. Returns list of ids that fit selection criteria
ssLayer.setSelectedFeatures([k.id() for k in selection2]) #Selects the ids from the list above in the target layer

_writer2 = QgsVectorFileWriter.writeAsVectorFormat(ssLayer, 'S:/682/Summer19/mguy1/final/ss17.shp', "utf-8", None, "ESRI Shapefile", onlySelected=True) #Exports selected features (Shot Spotter shots in 2017) to new shapefile
ss17 = "S:/682/Summer19/mguy1/final/ss17.shp" #Defines new ss17 shapefile to ss17 variable
iface.addVectorLayer(ss17,"ss17","ogr") #Add shotspotter 2017 shapefile to map

######WARDS######
iface.addVectorLayer(wards,"wards","ogr") #Add wards crime shapefile to map

########################
###### ANALYSIS STEPS ######
########################

#Runs the processing tool "Join Attributes by Location" based on inputs specified in the second line. In this case, the districts
#are the "target" layer and the crime locations are the "join" layer.
processing.runalg("qgis:joinattributesbylocation",
    {'TARGET':wards,'JOIN':gunCrime,'PREDICATE':u'contains','SUMMARY':1,'KEEP':1,'OUTPUT':"S:/682/Summer19/mguy1/final/ward_gun_crime.shp"})
ward_gunCrime = "S:/682/Summer19/mguy1/final/ward_gun_crime.shp" #Defines joined ward and gun crime shapefiles to ward_gunCrime variable
iface.addVectorLayer(ward_gunCrime,"ward_gunCrime","ogr") #Adds ward_gunCrime shapefile to map

processing.runalg("qgis:joinattributesbylocation",
    {'TARGET':ward_gunCrime,'JOIN':ss17,'PREDICATE':u'contains','SUMMARY':1,'KEEP':1,'OUTPUT':"S:/682/Summer19/mguy1/final/ward_crime_ss.shp"})
ward_crime_ss = "S:/682/Summer19/mguy1/final/ward_crime_ss.shp" #Defines joined shapefiles to ward_crime_ss variable
QgsMapLayerRegistry.instance().removeAllMapLayers() #Removes all layers for ease of processing
iface.addVectorLayer(ward_crime_ss,"ward_crime_ss","ogr") #Adds joined shapefile to map

ward_crime_ss = iface.activeLayer() #Selects the ward_crime_ss layer to the ward_crime_ss variable
features = ward_crime_ss.getFeatures() #Fetchs features (rows) of ward_crime_ss layer
#The following for loop is used to run through each feature of the ward_crime_ss shapefile and print the number of gun crimes and 
#Shot Spotter incidents in 2017 for each ward. Because Ward 3 did not have any reported shotspotter incidents, the for loop is 
#coded to avoid a divide by zero error when dividing to get incidents per 10,000 people.
for feature in features: #Loops through each feature (all 8 wards)
    if feature["count_1"] == NULL: #This if statement avoids the divide by zero error for the NULL value in count_1
        print(feature["NAME"] + " had")
        print(feature["count"]/(feature["POP_2010"]/10000)) #Divides population in 2010 by 10,000, and then gun crimes by that number to get number of gun crimes per 10,000 people
        print("gun crimes per 10,000 people in 2017, and 0 Shotspotter incidents in 2017.")
        print(" ")
    else: #The else statement is used when a count_1 value does NOT equal NULL
        print(feature["NAME"] + " had")
        print(feature["count"]/(feature["POP_2010"]/10000)
        print("gun crimes per 10,000 people in 2017, and")
        print(feature["count_1"]/(feature["POP_2010"]/10000)) #In addition to gun crimes per 10,000, this prints shot spotter incidents per 10,000 as well
        print( "Shot Spotter incidents per 10,000 people in 2017.")
        print(" ")

######################
###### END OF CODE ######
######################