import pandas as pd
from astroquery.simbad import Simbad
import matplotlib.pyplot as plt

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

def get_data():
    #saved_data = pd.read_csv("kvdata.csv")

    names_df = pd.read_csv("TYCHOII_targs.txt", sep='|')
    names_df = names_df.rename(columns = {names_df.columns[1]:'name'})

    df = pd.DataFrame(columns=['name', 'RA', 'DEC', 'V', 'K'])

    Simbad.add_votable_fields('flux(V)', 'flux(K)')

    for name in names_df['name'][0:10]:

        name = name.strip()
        print ('Fetching Data for '+ name)
        table1 = Simbad.query_object(name)

        df.append(pd.DataFrame(dict(name=name,
            RA=table1['RA'][0],
            DEC=table1['DEC'][0],
            V=table1['FLUX_V'][0],
            K=table1['FLUX_K'][0]
        )))

#    data = pd.DataFrame(data)
    print(data.T.head())
    data = data.T
    return data

#Get data and put into dictionary via bokeh
data = get_data()
source = ColumnDataSource(data=dict(V=data.V,K=data.K))

#initial setup of widgets
text = TextInput(title="title", value='Lambda Boo Target Selection')
slope = Slider(title="slope", value=0.0, start=-10.0, end=10.0, step=0.01)
yint = Slider(title="yint", value=0.0, start=-10.0, end=10.0, step=0.1)
width = Slider(title="width",value=1.0,start=0.0, end=10.0,step=0.01)

#set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value',update_title)

def update_data(attrname, old, new):

    #get current slider values
    m = slope.value
    b = yint.value
    w = width.value

    #generate new data selection range


def plot_data(data,color,fig,ax):
    data.K = data.K.astype(float)
    data.V = data.V.astype(float)
    data = data.dropna()
    print(data.head())
    plot = figure(title="K vs V",tools="crosshair,pan,reset,save,wheel_zoom",x_label='V',y_label='K')
    plot.scatter('V','K',color=color)



def select_targs(data,slope,yint, width):
    targs = (data.K < slope * data.V + yint) & (data.K > slope * data.V + yint - width)
    targs = data[targs] #selects targets for which K/V < 1 (true)
    return targs


fig, ax = plt.subplots()
plot_data(data,"blue",fig,ax)
plot_data(select_targs(data,0.9,0, 1),"red",fig,ax)

inputs = widgetbox(text, slope, yint, width)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
