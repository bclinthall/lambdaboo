import os
import pandas as pd

saves = os.listdir("saves")

x_range = (-3.2267892822868247, 12.408789680922686)
y_range = (1.251577550841048, 16.948423212098408)

for save in saves:
    df = pd.DataFrame.from_csv(os.path.join('saves', save))
    print(df.head())
    df.plot.scatter('K', 'V', title=save, xlim=x_range, ylim=y_range)
