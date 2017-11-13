import pandas as pd
from astroquery.simbad import Simbad
import matplotlib.pyplot as plt

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure, output_file, show

default_color = "blue"
highlight_color = "red"


def get_data():
    df = pd.read_csv("lambdaboo/TYCHOII_targs.txt", sep='|')
    df = df.rename(columns = {df.columns[1]:'name'})

    data = {}

    for name in df['name'][0:100]:
        name = name.strip()
        print ('Fetching Data for '+ name)
        Simbad.add_votable_fields('flux(V)', 'flux(K)')
        table1 = Simbad.query_object(name)

        data[name] = dict(
        RA = table1['RA'][0],
        DEC = table1['DEC'][0],
        V = table1['FLUX_V'][0],
        K = table1['FLUX_K'][0],
        color = default_color)

    data = pd.DataFrame(data)
    print(data.T.head())
    data = data.T
    return data

#Get data and put into dictionary via bokeh
data = get_data()
source = ColumnDataSource(data=dict(V=data.V,K=data.K))


#temp plot
#output_file=("test.html")
#plot = figure()
#plot.scatter('V','K', source=source)
#show(plot)


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

    select_targs(data, m, b, w)




#update data and generate new target list
def select_targs(data,slope,yint,width):
    targs = (data.K < slope * data.V + yint) & (data.K > slope * data.V + yint - width) #creates boolean (T/F) for each entry
    colors = targs.map(lambda x: highlight_color if x else default_color) #selects targets for which K/V < 1 (true)
    source.data = dict(V=data.V,K=data.K,color=colors)


plot = figure(title="K vs V",tools="crosshair,pan,reset,save,wheel_zoom",x_axis_label="K",y_axis_label="V")
select_targs(data,m,b,w)
plot.scatter('V','K',color="color",source=source)


for w in[slope,yint,width]:
    w.on_change('value',update_data)


inputs = widgetbox(text, slope, yint, width)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
