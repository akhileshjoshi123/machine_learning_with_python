import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

web_stats = {'Day':[1,2,3,4,5,6],
             'Visitors':[43,34,65,56,29,76],
             'Bounce_Rate':[65,67,78,65,45,52]}

df = pd.DataFrame(web_stats)

print(df.head())
print(df.tail(n=2))

print("before: " , df)


df.set_index('Day',inplace=True)

print("after: " , df)

print(df['Visitors'])

print(df.Visitors)

df['Visitors'].plot()
plt.show()

print(df[['Visitors','Bounce_Rate']])

df[['Visitors','Bounce_Rate']].plot()
plt.show()


print("to list is : " , df.Visitors.tolist())


#print("This does not work" , df[['Visitors','Bounce_Rate']].tolist()))

print("This does not work" , np.array(df[['Visitors','Bounce_Rate']]))