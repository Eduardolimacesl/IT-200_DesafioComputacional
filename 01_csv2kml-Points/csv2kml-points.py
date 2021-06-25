import simplekml
import pandas
import gi
import folium
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from openBox import FileChooserWindow

#Open windows to choose file.
win = FileChooserWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

#Start transformation.
df = pandas.read_csv(win.filePath)
print(df) #apenas para verificação.

def csv2kml_points(df):
  kmlFile = simplekml.Kml()
  for lon,lat,name in zip(df["lng"],df["lat"],df["name"]):
    kmlFile.newpoint(name = name, coords=[(lon,lat)])
  #return kmlSave(kmlFile)
  kmlFile.save("./Points.kml")  

#Chamada das funções:
csv2kml_points(df)

#Criando o mapa para visualização.
fig = folium.Map(width=900, height=600)
