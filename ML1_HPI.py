import quandl
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
from matplotlib import style
style.use('fivethirtyeight')
import numpy as np
from sklearn import svm,preprocessing,cross_validation 

def create_labels(cur_hpi , fut_api):
    if fut_api > cur_hpi :
        return 1 #1 signifies it went up
    else :
        return 0

def moving_avg (values):
    return mean(values)


housing_data = pd.read_pickle("economic_indicators.pickle")

housing_data = housing_data.pct_change()
housing_data.replace([np.inf,-np.inf],np.NaN,inplace=True)

print("Number of cols : " , housing_data.shape[0])

housing_data['future_bench'] = housing_data['bench'].shift(-1)

housing_data.dropna(inplace=True)
print("Number of cols after drop na : " , housing_data.shape[0])

housing_data['label'] = list(map(create_labels,housing_data['bench'],housing_data['future_bench']))

#housing_data['moving_avg'] = housing_data['M30'].rolling(window=10, center=False).apply(moving_average,housing_data['M30'])﻿

X = np.array(housing_data.drop(['label','future_bench'],1))
X = preprocessing.scale(X) #converts data from -1 to +1
y = np.array(housing_data['label'])


X_train , X_test , y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.2)

clf = svm.SVC(kernel='linear')
clf.fit(X_train , y_train)

print(clf.score(X_test,y_test))