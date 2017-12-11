import numpy as np
import pandas as pd
from skimage import transform as tf
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, column
from bokeh.models.widgets import  TextInput
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import brewer


palette = brewer['Spectral'][11]
palette[0] = '#FFFFFF'

x_range = [-10, 10]
y_range = [-10, 10]
#y_range = [4.5, 12]


def k_hist():
    global k_hist_source
    p = figure(
        plot_height=400,
        plot_width=400,
        tools='pan,box_zoom,reset, wheel_zoom')
    p.quad(source=k_hist_source, left='left', right='right', top='top', fill_color="#036564", line_color="#033649", bottom='bottom')
    return p

def v_hist():
    global v_hist_source
    p = figure(
        plot_height=400,
        plot_width=400,
        tools='pan,box_zoom,reset, wheel_zoom')
    p.quad(source=v_hist_source, left='left', right='right', top='top', fill_color="#036564", line_color="#033649", bottom='bottom')
    return p


def hist2d(src):
    p = figure(
        plot_height=400,
        plot_width=400,
        x_range=(src.data['x'][0], src.data['x'][0]+src.data['dw'][0]),
        y_range=(src.data['y'][0], src.data['y'][0]+src.data['dh'][0]),
        tools='pan,box_zoom,reset, wheel_zoom')
    p.image(image='image', x='x', y='y', dw='dw', dh='dh', source=src, palette=palette)
    return p


def draw(attr, old, new):
    at = tf.AffineTransform(rotation=float(rotation_ti.value), shear=float(shear_ti.value))
    mat = at.params
    warped = mat.dot(sample)
    source.data = {x_label:warped[0], y_label:warped[1]}
    #orig_source.data = {x_label: sample[0], y_label: sample[1]}
    orig_hist2d.data=get_2dhist_coldatsrc_dict(sample, orig_fig)
    transformed_hist2d.data=get_2dhist_coldatsrc_dict(warped, transformed_fig)
    hist, edges = np.histogram(source.data[x_label], bins=200)
    k_hist_source.data=dict(top=hist, left=edges[:-1], right=edges[1:], bottom=np.zeros(len(hist)))
    hist, edges = np.histogram(source.data[y_label], bins=200)
    v_hist_source.data=dict(top=edges[:-1], left=np.zeros(len(hist)), right=hist, bottom=edges[1:])




# Widgets

rotation_ti = TextInput(title="rotation -0.014", value='-0.014')
rotation_ti.on_change('value', draw)
shear_ti = TextInput(title='shear 1.2', value='1.2')
shear_ti.on_change('value', draw)


# Data Setup
data = pd.read_csv("all_tychoii_data.csv")
data = data.dropna()
data = data.set_index('name')
data = data.drop(['DEC', 'RA'], 1)
x_label = data.columns[0]
y_label = data.columns[1]


# Initial transform
sample = data.sample(frac=0.1)
sample = sample.values
sample = sample.transpose()
ones = np.ones((1,sample.shape[1]))
sample = np.vstack((sample, ones))

at = tf.AffineTransform(rotation=float(rotation_ti.value), shear=float(shear_ti.value))
mat = at.params
warped = mat.dot(sample)
source = ColumnDataSource(data={x_label: warped[0], y_label: warped[1]})
#orig_source = ColumnDataSource(data={x_label: sample[0], y_label: sample[1]})

def get_2dhist_coldatsrc_dict(sample, fig=None):
    bins = [np.linspace(sample[1].min(), sample[1].max(), 200), np.linspace(sample[0].min(), sample[0].max(), 200)]
    H, xedges, yedges = np.histogram2d(sample[1], sample[0], bins=bins)
    H = np.log10(H + 1)

    if fig is not None:
        fig.x_range.start = xedges[0]
        fig.x_range.end = xedges[-1]
        fig.y_range.start = yedges[0]
        fig.y_range.end = yedges[-1]
    return dict(image=[H], x=[yedges[0]], y=[xedges[0]], dw=[yedges[-1]-yedges[0]], dh=[xedges[-1]-xedges[0]])


orig_hist2d = ColumnDataSource(data=get_2dhist_coldatsrc_dict(sample))
orig_fig = hist2d(orig_hist2d)

transformed_hist2d = ColumnDataSource(data=get_2dhist_coldatsrc_dict(warped))
transformed_fig = hist2d(transformed_hist2d)


hist, edges = np.histogram(source.data[x_label], bins=200)
k_hist_source = ColumnDataSource(data=dict(top=hist, left=edges[:-1], right=edges[1:], bottom=np.zeros(len(hist))))
hist, edges = np.histogram(source.data[y_label], bins=200)
v_hist_source = ColumnDataSource(data=dict(top=edges[:-1], left=np.zeros(len(hist)), right=hist, bottom=edges[1:]))




# final ui setup
controls = widgetbox([rotation_ti, shear_ti], width=200)

mid_col = column(transformed_fig, k_hist())
right_col = column(v_hist(), controls)
layout = row(orig_fig, mid_col, right_col)
curdoc().add_root(layout)

