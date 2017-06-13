#pickle helps us to store the classifier after we train it ; this helps us saving the results in pickle file and we don't have to run the classifier with training data again.

#tips
#1. run classifier with training data and save it to pickle file with wb mode (write mode)
#2. comment the part where you train the classifier with train data and just use the pickle file with rb mode(read mode)


import pickle
import quandl
import pandas as pd
import math 
import numpy as np
from sklearn import preprocessing , cross_validation , svm
from sklearn.linear_model import LinearRegression



import sys, os

def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

print ('Current working directory : ', os.getcwd())
os.chdir(getScriptPath())
print ('Changed working directory : ', os.getcwd())


quandl.ApiConfig.api_key = 'jSHLhdZwPT7tqob6ipwY'

data = quandl.get_table('WIKI/PRICES')
data = data[["adj_open","adj_high","adj_close","adj_low","adj_volume"]]
data["HL_PCT"] = data["adj_high"] - data["adj_low"] / data["adj_low"] * 100
data["PCT_CHANGE"] = data["adj_close"] - data["adj_open"] / data["adj_open"] * 100

data = data[["adj_close", "HL_PCT" , "PCT_CHANGE" , "adj_volume" ]]


forecast_col = "adj_close"
data.fillna(-9999,inplace=True)

print("length of data frame before " + str  (len(data)) )


forecast_out = int(math.ceil(0.001*len(data)))
print("forecast out is : " + str  (forecast_out) )
data["label"] = data[forecast_col].shift(-forecast_out)

data.dropna(inplace = True) #used to remove the NaN values created at last of column since we shifted the column with forecast_out (100) rows above



print("length of data frame after " + str  (len(data)) )

#now we will make our test and train 
# X represents the features and y represents the Class

X = np.array(data.drop(['label'],1))
y= np.array(data['label'])

print("lengths of X and y are : " , len(X) , len(y) )

X = preprocessing.scale(X)
y = np.array(data['label'])

X_train , X_test ,y_train , y_test = cross_validation.train_test_split(X,y,test_size=0.2)

model = LinearRegression(n_jobs=-1)
#njobs gives no. of jobs that we want to run , -1 states maximum possible number of jobs that we can run
#model.fit(X_train,y_train)
#with open ('linearregression.pickle','wb') as f: 
#	pickle.dump(model,f)

pickle_in = open('linearregression.pickle','rb')
model = pickle.load(pickle_in)

accuracy = model.score(X_test,y_test)

print("accuracy is " , accuracy*100 , "%")



model_svm = svm.SVR()
model_svm.fit(X_train,y_train)

accuracy_svm = model_svm.score(X_test,y_test)

print("accuracy with SVM is " , accuracy_svm*100 , "%")
