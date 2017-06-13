import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib import interactive
import numpy as np
interactive(True)
 
import pylab

style.use('ggplot')


def read_us_states () :
    read_states = pd.read_html("https://simple.wikipedia.org/wiki/List_of_U.S._states")
    return read_states[0][0][1:]

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
    return df1



#call the function for first time , then comment
#grab_initial_date()

# comment above code to run pickleling part

pickle_in = open('state_pickle_pctChange_1.pickle','rb')
HPI_data = pickle.load(pickle_in)

#HPI_data['TX'].plot(ax = ax1,legend=True,label="Texas w/o resampling")


#resampling options
#B	Business day
#D	Calendar day
#W	Weekly
#M	Month end
#Q	Quarter end
#A	Year end
#BA	Business year end
#AS	Year start
#H	Hourly frequency
#T, min	Minutely frequency
#S	Secondly frequency
#L, ms	Millisecond frequency
#U, us	Microsecond frequency
#N, ns	Nanosecond frequency


fig = plt.figure()
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0),sharex=ax1)


HPI_data['TX12MA'] = pd.rolling_mean(HPI_data['TX'],12)
HPI_data['TX12SD'] = pd.rolling_std(HPI_data['TX'],12)

print(HPI_data[['TX','TX12MA']].head())
print(HPI_data[['TX','TX12SD']].head())

HPI_data[['TX','TX12MA']].plot(ax = ax1)
HPI_data['TX12SD'].plot(ax=ax2)


plt.legend( loc = 4)
plt.show()


fig1 = plt.figure()
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0),sharex=ax1)


TX_AK_CORR = pd.rolling_corr(HPI_data['TX'],HPI_data['AK'],12)


HPI_data['TX'].plot(ax = ax1,label='TX')
HPI_data['AK'].plot(ax = ax1,label='AK')
TX_AK_CORR.plot(ax=ax2,label='AKTXCORR')
plt.legend( loc = 4)
plt.show()
