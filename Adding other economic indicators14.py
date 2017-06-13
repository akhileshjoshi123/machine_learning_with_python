import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt

from matplotlib import interactive
interactive(True)
from matplotlib import style
style.use('fivethirtyeight')


def read_us_states () :
    read_states = pd.read_html("https://simple.wikipedia.org/wiki/List_of_U.S._states")
    return read_states[0][0][1:]

def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken="jSHLhdZwPT7tqob6ipwY")
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    return df

#print(mortgage_30y())

#read_states contains list of dataframes
#print(read_states)

#we want only the table that contains abbr
#print(read_states[0])

#we want abbr from the table
#print(read_states[0][0])

def grab_initial_date():
    states= read_us_states()
    main_df=pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_"+str(abbv)
        df = quandl.get(query, authtoken="jSHLhdZwPT7tqob6ipwY")
        df.rename(columns={'Value':abbv}, inplace=True)
        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0]  * 100.0
        #print(df)
        
        if main_df.empty :
           main_df = df
        else:
            main_df = main_df.join(df)

    print(main_df.head())

    pickle_out = open('state_pickle_pctChange_1.pickle','wb')
    pickle.dump(main_df,pickle_out)
    pickle_out.close()


def benchmark() :
    df1 = quandl.get('FMAC/HPI_USA', authtoken="jSHLhdZwPT7tqob6ipwY")
    df1['Value'] = (df1['Value'] - df1['Value'][0]) / df1['Value'][0]  * 100.0
    df1.rename(columns={'Value':'bench'}, inplace=True)
    return df1


def sp500_data():
    df = quandl.get("YAHOO/INDEX_GSPC", trim_start="1975-01-01", authtoken="jSHLhdZwPT7tqob6ipwY")
    df["Adjusted Close"] = (df["Adjusted Close"]-df["Adjusted Close"][0]) / df["Adjusted Close"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Adjusted Close':'sp500'}, inplace=True)
    df = df['sp500']
    return df

def gdp_data():
    df = quandl.get("BCB/4385", trim_start="1975-01-01", authtoken="jSHLhdZwPT7tqob6ipwY")
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'GDP'}, inplace=True)
    df = df['GDP']
    return df

def us_unemployment():
    df = quandl.get("ECPI/JOB_G", trim_start="1975-01-01", authtoken="jSHLhdZwPT7tqob6ipwY")
    df["Unemployment Rate"] = (df["Unemployment Rate"]-df["Unemployment Rate"][0]) / df["Unemployment Rate"][0] * 100.0
    df=df.resample('1D').mean()
    df=df.resample('M').mean()
    return df



#call the function for first time , then comment
#grab_initial_date()

# comment above code to run pickleling part
pickle_in = open('state_pickle_pctChange_1.pickle','rb')
HPI_data = pickle.load(pickle_in)

m30 = mortgage_30y()
sp500 = sp500_data()
gdp = gdp_data()
HPI_Bench = benchmark()
unemployment = us_unemployment()
m30.columns=['M30']
HPI = HPI_data.join([HPI_Bench,m30,sp500,gdp,unemployment])

print("Number of cols : " , HPI.shape[0])
HPI.dropna(inplace=True)
print("Number of cols after drop na : " , HPI.shape[0])

HPI.to_pickle("economic_indicators.pickle")


print(HPI)