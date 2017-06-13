import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import interactive
import numpy as np
interactive(True)


bridge_height = {'meters':[10.26, 10.31, 10.27, 10.22, 10.23, 6212.42, 10.28, 10.25, 10.31]}

df = pd.DataFrame(bridge_height)
df['STD'] = df['meters'].rolling(window=2, center=False).std()
print(df)

df_std = df.describe()
print(df_std)


df_std = df.describe()['meters']['75%']
print(df_std)

#following operation removes outlier
df = df [ (df['STD'] < df_std*2 )]
print(df)

df.plot()
plt.show()