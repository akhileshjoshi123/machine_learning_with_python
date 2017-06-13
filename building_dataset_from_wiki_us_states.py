# -*- coding: utf-8 -*-
"""
Created on Mon May 15 12:55:44 2017

@author: Joshyancha Akhilesh
"""

import quandl
import pandas as pd
import pickle



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
        #print(df)
        
        if main_df.empty :
           main_df = df
        else:
            main_df = main_df.join(df)

    print(main_df.head())

    pickle_out = open('state_pickle.pickle','wb')
    pickle.dump(main_df,pickle_out)
    pickle_out.close()

#call the function for first time , then comment
#grab_initial_date()

# comment above code to run pickleling part
pickle_in = open('state_pickle.pickle','rb')
HPI_data = pickle.load(pickle_in)
print(HPI_data.head())



#usings pandas pickle version
HPI_data.to_pickle('pandas_pickle.pickle')
HPI_data2 = pd.read_pickle('pandas_pickle.pickle')