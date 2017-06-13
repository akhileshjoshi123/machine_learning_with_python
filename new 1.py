import quandl
import pandas as pd

query = "FMAC/HPI_TX"
df = quandl.get(query, authtoken="jSHLhdZwPT7tqob6ipwY")
#df.rename(columns={'Value':abbv}, inplace=True)

print("###############################################")
print(df['Value'])
print("###############################################")
print(df['Value'][1])