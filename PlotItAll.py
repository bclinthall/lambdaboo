import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("all_tychoii_data.csv")
data = data.dropna()
data = data.set_index('name')

plt.close()
plt.scatter(data.K, data.V)
plt.xlabel('K')
plt.ylabel('V')
