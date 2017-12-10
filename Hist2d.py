import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

plt.close()
x_range = [-3.226753235247827, 12.408753633883688]
y_range = [1.2810713904244559, 16.918929372514999]



data = pd.read_csv("all_tychoii_data.csv")
data = data.dropna()
data = data.set_index('name')

range = [np.arange(x_range[0], x_range[1], 0.05), np.arange(y_range[0], y_range[1],0.05)]

plt.hist2d(data.K, data.V, bins=range, range=[x_range, y_range], norm=LogNorm())
plt.colorbar()
plt.show()

