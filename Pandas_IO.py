# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:29:12 2017

@author: Joshyancha Akhilesh
"""

#data set deals with houding prices in Austin ,TX
#https://www.quandl.com/data/ZILL/Z77006_3B-Zillow-Home-Value-Index-ZIP-Three-Bedroom-Homes-77006


import pandas as pd

df = pd.read_csv('ZILL-Z77006_3B.csv')

print(df.head())

df.set_index('Date',inplace=True)
df.to_csv('indexed_housing_austin.csv')


print("does not indexed with date")
df = pd.read_csv('indexed_housing_austin.csv')
print(df.head())

#this does not preserves index Date that we saved earlier
#to work with indexed we will use

print("indexed with date")
df = pd.read_csv('indexed_housing_austin.csv',index_col=0)
print(df.head())


print("renaming the columns")
#note date is an index so it wont be a column
#HPI : house price index
df.columns = ['Austin_HPI']
print(df.head())
df.to_csv('indexed_housing_austin.csv',header=False)


df = pd.read_csv('indexed_housing_austin.csv',names=['Date','Austin_HPI'])
print(df)

df.to_html('indexed_housing_austin.html')


#this renames a particular column
print(df.rename(columns={'Austin_HPI':'Prices'}))

#to make changes permanant
print(df.rename(columns={'Austin_HPI':'Prices'},inplace=True))



