import pandas as pd
from astroquery.simbad import Simbad

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models.widgets import Slider
from bokeh.models.glyphs import Patch
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

x_range = [-1,11]
y_range = [4.5,12]
hover = HoverTool(tooltips=[
    ('k', '@x'),
    ('v', '@y'),
    ('name', '@name')
])
def get_patch_y(x):
    return slope.value * x + yint.value

def add_patch(figure):

    xpts = [x_range[0], width.value, width.value, x_range[0]]
    ypts = [get_patch_y(x) for x in xpts]
    source = ColumnDataSource(dict(x=xpts, y=ypts))
    glyph = Patch(x='x', y='y')
    figure.add_glyph(source, glyph)

plot_data = data.sample(frac=percent_of_data.value)
targs = (plot_data.K < m * plot_data.V + y) & (plot_data.K > m * plot_data.V + y - w)
plot_data['color'] = targs.map(lambda x: 'red' if x else 'blue')
source = ColumnDataSource(data=dict(x=plot_data.K, y=plot_data.V, color=plot_data.color, name=plot_data.index))
p = figure(plot_height=600, plot_width=800, x_range=x_range,y_range=y_range, tools='pan,box_zoom,reset')
#add_patch(p)

p.circle('x', 'y', source=source, color='color')
p.add_tools(hover)


def create_figure():
    m = slope.value
    y = yint.value
    w = width.value
    targs = (plot_data.K < m * plot_data.V + y) & (plot_data.K > m * plot_data.V + y - w)
    plot_data['color'] = targs.map(lambda x: 'red' if x else 'blue')
    return p


def update(attrname, old, new):
    layout.children[1] = create_figure()

data = pd.read_csv("all_tychoii_data.csv")
data = data.dropna()
data = data.set_index('name')
slope = Slider(title="slope", value=0.0, start=-10.0, end=10.0, step=0.01)
yint = Slider(title="yint", value=0.0, start=-10.0, end=10.0, step=0.1)
width = Slider(title="width",value=1.0,start=0.0, end=10.0,step=0.01)
percent_of_data = Slider(title='sample %', value=0.01, start=0, end=1.0, step=0.01)
widgets = [slope, yint, width, percent_of_data]
for widget in widgets:
    widget.on_change('value', update)
controls = widgetbox(widgets, width=200)
layout = row(controls, create_figure())
curdoc().add_root(layout)

show(create_figure())
'''
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





fig, ax = plt.subplots()
plot_data(data,"blue",fig,ax)
plot_data(select_targs(data,0.9,0, 1),"red",fig,ax)

inputs = widgetbox(text, slope, yint, width)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
'''
