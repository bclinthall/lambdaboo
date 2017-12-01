import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.close()
x_range = [4, 11]
y_range = [4, 11]


data = pd.read_csv("all_tychoii_data.csv")
data = data.dropna()
data = data.set_index('name')

range = np.arange(4, 11, 0.01)

plt.hist2d(data.K, data.V, bins=range, range=[x_range, y_range])
plt.colorbar()
plt.show()

