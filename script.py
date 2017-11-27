import pandas as pd

from bokeh.io import curdoc, save
from bokeh.layouts import row, widgetbox
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models.widgets import Slider
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import Patch

x_range = [-1, 11]
y_range = [4.5, 12]
hover = HoverTool(tooltips=[
    ('k', '@x'),
    ('v', '@y'),
    ('name', '@name')
])

'''plot_data = data.sample(frac=percent_of_data.value)
targs = (plot_data.K < m * plot_data.V + y) & (plot_data.K > m * plot_data.V + y - w)
plot_data['color'] = targs.map(lambda x: 'red' if x else 'blue')
p = figure(plot_height=600, plot_width=800, x_range=x_range,y_range=y_range, tools='pan,box_zoom,reset')
'''
#add_patch(p)

#p.circle('x', 'y', source=source, color='color')


def create_figure():

    p = figure(plot_height=600, plot_width=800, x_range=x_range, y_range=y_range, tools='pan,box_zoom,reset')


    p.add_glyph(patch_source, patch_glyph)
    p.circle(x='K', y='V', color='color', source=source)
    #p.add_tools(hover)
    return p

m = 1.0
b = 0.0
w = 1.0
perc = 0.01
def update(attrname, old, new):
    global m, b, w
    m = slope.value
    b = yint.value
    w = width.value
    perc = percent_of_data.value
    plot_data = data.sample(frac=perc)
    targs = (plot_data.V < m * plot_data.K + b) & (plot_data.V > m * plot_data.K + b - w)
    plot_data['color'] = targs.map(lambda x: 'red' if x else 'blue')
    source.data = plot_data.to_dict('list')

    patch_xs = [x_range[0], x_range[1], x_range[1], x_range[0]]
    patch_ys = [m * x + b for x in patch_xs]
    patch_ys[2] -= w
    patch_ys[3] -= w
    patch_source.data = dict(x=patch_xs, y=patch_ys)



data = pd.read_csv("all_tychoii_data.csv")
data = data.dropna()
data = data.set_index('name')
plot_data = data.sample(frac=perc)
targs = (plot_data.V < m * plot_data.K + b) & (plot_data.V > m * plot_data.K + b - w)
plot_data['color'] = targs.map(lambda x: 'red' if x else 'blue')
source = ColumnDataSource(plot_data.to_dict('list'))


patch_xs = [x_range[0], x_range[1], x_range[1], x_range[0]]
patch_ys = [m * x + b for x in patch_xs]
patch_ys[2] -= w
patch_ys[3] -= w
patch_source = ColumnDataSource(dict(x=patch_xs, y=patch_ys))
patch_glyph = Patch(x='x', y='y')

slope = Slider(title="slope", value=m, start=-10.0, end=10.0, step=0.001)
yint = Slider(title="yint", value=b, start=-10.0, end=10.0, step=0.1)
width = Slider(title="width",value=w,start=0.0, end=10.0,step=0.01)
percent_of_data = Slider(title='sample %', value=perc, start=0.001, end=1.0, step=0.001)
widgets = [slope, yint, width, percent_of_data]
for widget in widgets:
    widget.on_change('value', update)
controls = widgetbox(widgets, width=200)

layout = row(controls, create_figure())
curdoc().add_root(layout)

#save('bokeh.html')

#   "C:\Program Files\Anaconda3\Scripts\bokeh.exe" serve --show script.py

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
