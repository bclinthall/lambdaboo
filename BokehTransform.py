import numpy as np
import pandas as pd
from skimage import transform as tf
from bokeh.io import curdoc, save
from bokeh.layouts import row, widgetbox, column
from bokeh.models.widgets import Slider, Button, TextInput
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

x_range = [-10, 10]
y_range = [-10, 10]
#y_range = [4.5, 12]


def k_hist():
    global k_hist_source
    p = figure(
        plot_height=300,
        plot_width=300,
        tools='pan,box_zoom,reset')
    p.quad(source=k_hist_source, left='left', right='right', top='top', fill_color="#036564", line_color="#033649", bottom=0)
    return p

def v_hist():
    global v_hist_source
    p = figure(
        plot_height=300,
        plot_width=300,
        tools='pan,box_zoom,reset')
    p.quad(source=v_hist_source, left='left', right='right', top='top', fill_color="#036564", line_color="#033649", bottom=0)
    return p



def orig_figure():
    global orig_source
    p = figure(
        plot_height=500,
        plot_width=500,
        x_axis_label=x_label,
        y_axis_label=y_label,
        tools='pan,box_zoom,reset')
    p.circle(x=x_label, y=y_label, source=orig_source)
    return p



def create_figure():
    global source
    p = figure(
        plot_height=500,
        plot_width=500,
        tools='pan,box_zoom,reset')
    p.circle(x=x_label, y=y_label, source=source)
    return p


def draw(attr, old, new):
    at = tf.AffineTransform(rotation=float(rotation_ti.value), shear=float(shear_ti.value))
    mat = at.params
    warped = mat.dot(sample)
    source.data = {x_label:warped[0], y_label:warped[1]}
    orig_source.data = {x_label: sample[0], y_label: sample[1]}
    hist, edges = np.histogram(source.data[x_label], bins=200)
    k_hist_source.data=dict(top=hist, left=edges[:-1], right=edges[1:])
    hist, edges = np.histogram(source.data[y_label], bins=200)
    v_hist_source.data=dict(top=hist, left=edges[:-1], right=edges[1:])



def resample():
    sample = data.sample(frac=float(fraction_ti.value)).values
    sample = sample.transpose()
    ones = np.ones((1,sample.shape[1]))
    sample = np.vstack((sample, ones))
    return sample

def fraction_cb(attr, old, new):
    global sample
    sample = resample()
    draw(attr, old, new)

# Widgets
fraction_ti = TextInput(title="sample fraction", value='0.01') #0.01
fraction_ti.on_change('value', fraction_cb)

rotation_ti = TextInput(title="rotation", value='-0.014')
rotation_ti.on_change('value', draw)
shear_ti = TextInput(title='shear', value='1.2')
shear_ti.on_change('value', draw)


# Data Setup
data = pd.read_csv("all_tychoii_data.csv")
data = data.dropna()
data = data.set_index('name')
data = data.drop(['DEC', 'RA'], 1)
x_label = data.columns[0]
y_label = data.columns[1]


# Initial transform
sample = resample()
at = tf.AffineTransform(rotation=float(rotation_ti.value), shear=float(shear_ti.value))
mat = at.params
warped = mat.dot(sample)
source = ColumnDataSource(data={x_label: warped[0], y_label: warped[1]})
orig_source = ColumnDataSource(data={x_label: sample[0], y_label: sample[1]})

hist, edges = np.histogram(source.data[x_label], bins=200)
k_hist_source = ColumnDataSource(data=dict(top=hist, left=edges[:-1], right=edges[1:]))
hist, edges = np.histogram(source.data[y_label], bins=200)
v_hist_source = ColumnDataSource(data=dict(top=hist, left=edges[:-1], right=edges[1:]))


# final ui setup
controls = widgetbox([fraction_ti, rotation_ti, shear_ti], width=200)
left_col = column(controls, k_hist(), v_hist())
layout = row(orig_figure(), create_figure(), left_col,)
curdoc().add_root(layout)

