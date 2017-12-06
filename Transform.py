import numpy as np
from skimage import transform as tf
from skimage import data as sampledata
import pandas as pd
import matplotlib.pyplot as plt



#src = np.array([[10.5, 0.0, 9.88], [10.5, 0.0, 0.0], [1.0, 1.0, 1.0]])
#dst = np.array([[10.5, 0.0, 9.88], [10.5, 0.0, 0.0], [1.0, 1.0, 1.0]])


#w = x_prime.dot(x.transpose()).dot(np.linalg.inv(x.dot(x.transpose())))

data = pd.read_csv("all_tychoii_data.csv")
data = data.dropna()
data = data.set_index('name')
data = data.drop(['DEC', 'RA'], 1)

ax, fig = plt.subplots()
samp = data.sample(frac=1.0)
fig.set_xlim(-4, 11)
fig.set_ylim(4, 16)
fig.scatter(samp['K'], samp['V'])

dst = np.array([
    [0.0, 0.0],
    [0.0, 1.0 ],
    [1.0,  1.0],
    [1.0,0.0],

])
src = np.array([
    [0.0 ,  6.0],
    [0.0,   9.88],
    [10.5, 10.5],
    [7.0,   6.62],
])

tform = tf.ProjectiveTransform()
tform.estimate(src, dst)
values = data.values
mat = tform.params


srcpts = np.array([
    [0.0 ,  6.0, 1],
    [0.0,   9.88, 1],
    [10.5, 10.5, 1],
    [7.0,   6.62, 1],
])



print('Source pts translated to ', np.round(mat.dot(srcpts.transpose()), 2))

valT = values.transpose()
ones = np.ones((1,valT.shape[1]))
valT = np.vstack((valT, ones))

warped = mat.dot(valT)

ax, fig = plt.subplots()
fig.scatter(warped[0], warped[1])

#plt.scatter(valT[0],valT[1])

warped_df = pd.DataFrame({'k':warped[0], 'v':warped[1]})
warped_df = warped_df.set_index('k')
warped_df.hist(bins=200)
warped_df = warped_df.reset_index()
warped_df = warped_df.set_index('v')
warped_df.hist(bins=200)
