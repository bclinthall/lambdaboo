import numpy as np
from skimage import transform as tf
from skimage import data as sampledata
import pandas as pd
import matplotlib.pyplot as plt



#src = np.array([[10.5, 0.0, 9.88], [10.5, 0.0, 0.0], [1.0, 1.0, 1.0]])
#dst = np.array([[10.5, 0.0, 9.88], [10.5, 0.0, 0.0], [1.0, 1.0, 1.0]])


#w = x_prime.dot(x.transpose()).dot(np.linalg.inv(x.dot(x.transpose())))

def plot_df(df, frac, pts):
    ax, fig = plt.subplots()
    samp = df.sample(frac=frac)
    fig.scatter(samp['K'], samp['V'])
    fig.plot(pts.transpose()[0], pts.transpose()[1], "ro")



data = pd.read_csv("all_tychoii_data.csv")
data = data.dropna()
data = data.set_index('name')
data = data.drop(['DEC', 'RA'], 1)
#data = data.sample(frac="0.1")

dst = np.array([
    [0.0, 0.0],
    [0.0, 1.0 ],
    [1.0, 1.0],
    [1.0,0.0],

])
src = np.array([
    [0.0,  6.0],
    [0.0,   9.88],
    [10.5, 10.5],
    [7.0,   6.62]
])
"""

dst = np.array([
    [0.0, 0.0],
    [0.0, 1.0 ],
    [1.0,  1.0],
    [1.0,0.0],

])
src = np.array([
    [-10.5 ,-0.62],
    [0.0, 9.88],
    [10.5, 10.5],
    [0.0,0.0],
])
"""



srcpts = np.array([
    [0.0 ,  6.0, 1],
    [0.0,   9.88, 1],
    [10.5, 10.5, 1],
    [7.0,   6.62, 1],
])

plot_df(data, 0.01, src)


'''
srcpts = np.array([
    [-10.5 ,-0.62, 1],
    [0.0, 9.88, 1],
    [10.5, 10.5, 1],
    [0.0,0.0, 1],
])
'''

tform = tf.AffineTransform()
tform.estimate(src, dst)
values = data.values
mat = tform.params





print('Source pts translated to ')
print(np.round(mat.dot(srcpts.transpose()), 2))

valT = values.transpose()
ones = np.ones((1,valT.shape[1]))
valT = np.vstack((valT, ones))

warped = mat.dot(valT)




#plt.scatter(valT[0],valT[1])

warped_df = pd.DataFrame({'K': warped[0], 'V': warped[1]})
warped_df = warped_df.set_index('K')
warped_df.hist(bins=200)
warped_df = warped_df.reset_index()
warped_df = warped_df.set_index('V')
warped_df.hist(bins=200)
warped_df = warped_df.reset_index()

plot_df(warped_df, 0.01, dst)

