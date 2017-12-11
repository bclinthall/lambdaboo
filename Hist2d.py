import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bokeh.palettes import brewer
from bokeh.models import ColumnDataSource

from matplotlib.colors import LogNorm

from bokeh.plotting import figure, show

plt.close()
x_range = [-3.226753235247827, 12.408753633883688]
y_range = [1.2810713904244559, 16.918929372514999]



data = pd.read_csv("all_tychoii_data.csv")
data = data.dropna()
data = data.set_index('name')

bins = [np.arange(x_range[0], x_range[1], 0.05), np.arange(y_range[0], y_range[1],0.05)]

"""
plt.hist2d(data.K, data.V, bins=bins, range=[x_range, y_range], norm=LogNorm())
plt.colorbar()
plt.show()
"""

H, xedges, yedges = np.histogram2d(data.V, data.K, bins=bins)
p = figure(x_range=x_range, y_range=y_range)

H = np.log10(H + 1)

# must give a vector of image data for image parameter
palette = brewer['Spectral'][11]
palette[0] = '#FFFFFF'

hist2dsource = ColumnDataSource(data=dict(image=[H], x=[xedges[0]], y=[yedges[0]], dw=[xedges[-1]-xedges[0]], dh=[yedges[-1]-yedges[0]]))

p.image(image='image', x='x', y='y', dw='dw', dh='dw', source=hist2dsource, palette=palette)

show(p)


