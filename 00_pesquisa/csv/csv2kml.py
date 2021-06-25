import csv
import xml.dom.minidom
import sys


def GPSCoord(row):
  # combine lat-longs from their columns, returned as a string.
  return '%s,%s' % (row['longitude'],row['latitude'])

def createPlacemark(kmlDoc, row, order):
  # This creates a  element for a row of data.
  # A row is a dict.
  # Added option for place-mark label
  placemarkElement = kmlDoc.createElement('Placemark')
  nameElement = kmlDoc.createElement('name')
  placemarkElement.appendChild(nameElement)
  nameText = kmlDoc.createTextNode(row['ID'])
  # //Change 'ID' in nameText to the CSV column heading with desired labels.
  nameElement.appendChild(nameText)
  extElement = kmlDoc.createElement('ExtendedData')
  placemarkElement.appendChild(extElement)
  styleUrlElement = kmlDoc.createElement('styleUrl')
  styleUrlText = kmlDoc.createTextNode('#caseStyle')
  styleUrlElement.appendChild(styleUrlText)
  placemarkElement.appendChild(styleUrlElement)

  # Loop through the columns and create a  element for every field that has a value.
  for key in order:
    if row[key]:
      dataElement = kmlDoc.createElement('Data')
      dataElement.setAttribute('name', key)
      valueElement = kmlDoc.createElement('value')
      dataElement.appendChild(valueElement)
      valueText = kmlDoc.createTextNode(row[key])
      valueElement.appendChild(valueText)
      extElement.appendChild(dataElement)


  pointElement = kmlDoc.createElement('Point')
  placemarkElement.appendChild(pointElement)
  coordinates = GPSCoord(row)
  coorElement = kmlDoc.createElement('coordinates')
  coorElement.appendChild(kmlDoc.createTextNode(coordinates))
  pointElement.appendChild(coorElement)
  return placemarkElement


def createKML(csvReader, fileName, order):
  # This constructs the KML document from the CSV file.
  kmlDoc = xml.dom.minidom.Document()

  kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
  kmlElement.setAttribute('xmlns','http://earth.google.com/kml/2.2')
  kmlElement = kmlDoc.appendChild(kmlElement)
  documentElement = kmlDoc.createElement('Document')
  documentElement = kmlElement.appendChild(documentElement)

  #Setting style for normal place-markers.
  styleElement = kmlDoc.createElement('Style')
  documentElement.appendChild(styleElement)
  styleIDElement = kmlDoc.createElement('id')
  idText = kmlDoc.createTextNode('NormIconID')
  styleIDElement.appendChild(idText)
  styleElement.appendChild(styleIDElement)
  iconElement = kmlDoc.createElement('Icon')
  styleElement.appendChild(iconElement)
  hrefElement = kmlDoc.createElement('href')
  iconElement.appendChild(hrefElement)
  iconLocation = kmlDoc.createTextNode('blu-diamond.png')
  # //Change 'blu-diamond.png' to a web address or any other image in the same directory as the CSV + application. 
  #This image can be embedded when the KML is converted to KMZ (in google earth).
  hrefElement.appendChild(iconLocation)
  labelStyleElement = kmlDoc.createElement('LabelStyle')
  styleElement.appendChild(labelStyleElement)
  scaleElement = kmlDoc.createElement('scale')
  scaleText = kmlDoc.createTextNode('0.4')
  #//change label scaling to desired value 
  scaleElement.appendChild(scaleText)
  labelStyleElement.appendChild(scaleElement)

  #Setting style for place-markers when hovered over.
  styleElement = kmlDoc.createElement('Style')
  documentElement.appendChild(styleElement)
  styleIDElement = kmlDoc.createElement('id')
  idText = kmlDoc.createTextNode('HoverIconID')
  styleIDElement.appendChild(idText)
  styleElement.appendChild(styleIDElement)
  iconStyleElement = kmlDoc.createElement('IconStyle')
  iconElement = kmlDoc.createElement('Icon')
  iconStyleElement.appendChild(iconElement)
  scaleElement = kmlDoc.createElement('scale')
  scaleText = kmlDoc.createTextNode('1.2')
  #//change place-marker scaling to desired value 
  scaleElement.appendChild(scaleText)
  iconStyleElement.appendChild(scaleElement)
  styleElement.appendChild(iconStyleElement)
  hrefElement = kmlDoc.createElement('href')
  iconElement.appendChild(hrefElement)
  iconLocation = kmlDoc.createTextNode('blu-diamond.png')
  #//Change 'blu-diamond.png' to a web address or any other image in the same directory as the CSV + application. 
  #This image can be embedded when the KML is converted to KMZ (in google earth).
  hrefElement.appendChild(iconLocation)
  labelStyleElement = kmlDoc.createElement('LabelStyle')
  styleElement.appendChild(labelStyleElement)
  scaleElement = kmlDoc.createElement('scale')
  scaleText = kmlDoc.createTextNode('0.44')
  #//change label hover scaling to desired value 
  scaleElement.appendChild(scaleText)
  labelStyleElement.appendChild(scaleElement)

  #The style map
  styleMapElement = kmlDoc.createElement('StyleMap')
  documentElement.appendChild(styleMapElement)
  styleMapID = kmlDoc.createElement('id')
  styleMapIDtext = kmlDoc.createTextNode('caseStyle')
  styleMapID.appendChild(styleMapIDtext)
  styleMapElement.appendChild(styleMapID)
  pairElement = kmlDoc.createElement('Pair')
  styleMapElement.appendChild(pairElement)
  keyElement = kmlDoc.createElement('key')
  keyText = kmlDoc.createTextNode('normal')
  keyElement.appendChild(keyText)
  pairElement.appendChild(keyElement)
  styleUrl = kmlDoc.createElement('styleUrl')
  styleURLtext = kmlDoc.createTextNode('#NormIconID')
  styleUrl.appendChild(styleURLtext)
  pairElement.appendChild(styleUrl)
  pairElement = kmlDoc.createElement('Pair')
  styleMapElement.appendChild(pairElement)
  keyElement = kmlDoc.createElement('key')
  keyText = kmlDoc.createTextNode('highlight')
  keyElement.appendChild(keyText)
  pairElement.appendChild(keyElement)
  styleUrl = kmlDoc.createElement('styleUrl')
  styleURLtext = kmlDoc.createTextNode('#HoverIconID')
  styleUrl.appendChild(styleURLtext)
  pairElement.appendChild(styleUrl)

  # Skip the header line.
  csvReader.__next__()

  for row in csvReader:
    placemarkElement = createPlacemark(kmlDoc, row, order)
    documentElement.appendChild(placemarkElement)
  kmlFile = open(fileName, 'wb')
  kmlFile.write(kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))

def main():
  # This reader opens up 'data.csv', which should be replaced with your own.
  # It creates a KML file called 'Output.kml'.

  # If an argument was passed to the script, it splits the argument on a comma
  # and uses the resulting list to specify an order for when columns get added.
  # Otherwise, it defaults to the order used in the sample.

  if len(sys.argv) >1: order = sys.argv[1].split(',')
  else: order = ['latitude','longitude','ID','Column3','column9','column5','columnN']
  #//Change to match columns in CSV. They can be in what ever order you like.
  csvreader = csv.DictReader(open('data.csv'),order)
  #//Change to your input file name. No directory needed if Python application and CSV in the same folder.
  kml = createKML(csvreader, 'Output.kml', order)
  #//Change output.kml to desired output name.
  
if __name__ == '__main__':
  main()