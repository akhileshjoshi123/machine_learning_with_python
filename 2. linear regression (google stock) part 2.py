import quandl  , datetime
import pandas as pd
import math ,time
import numpy as np
from sklearn import preprocessing , cross_validation , svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

quandl.ApiConfig.api_key = 'jSHLhdZwPT7tqob6ipwY'

data = quandl.get_table('WIKI/PRICES')
data = data[["adj_open","adj_high","adj_close","adj_low","adj_volume"]]
data["HL_PCT"] = data["adj_high"] - data["adj_low"] / data["adj_low"] * 100
data["PCT_CHANGE"] = data["adj_close"] - data["adj_open"] / data["adj_open"] * 100

data = data[["adj_close", "HL_PCT" , "PCT_CHANGE" , "adj_volume" ]]


forecast_col = "adj_close"
data.fillna(-9999,inplace=True)

print(data.head())

print("length of data frame before " + str  (len(data)) )


forecast_out = int(math.ceil(0.001*len(data)))
print("forecast out is : " + str  (forecast_out) )
data["label"] = data[forecast_col].shift(-forecast_out)

print(data)


X = np.array(data.drop(['label'],1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X= X[:-forecast_out]

print ("X_lately : ")
print(X_lately)


print ("X : ")
print(X)

print("lengths of X lately and X are : " , len(X_lately) , len(X) )

data.dropna(inplace = True)
y = np.array(data['label'])

print ("Y : ")
print(y)



X_train , X_test ,y_train , y_test = cross_validation.train_test_split(X,y,test_size=0.2)

model = LinearRegression(n_jobs=-1)
#njobs gives no. of jobs that we want to run , -1 states maximum possible number of jobs that we can run
model.fit(X_train,y_train)

accuracy = model.score(X_test,y_test)

forcast_set = model.predict(X_lately)

print("accuracy is " , accuracy*100 , "%")

print (forcast_set)

data["Forecast"] =np.nan #assign new column with nan

last_date = data.iloc[-1].name
pqr = last_date
print("last-date" , pqr)
#last_unix = last_date.timestamp()
#last_unix = time.mktime(last_date.timetuple())
last_unix = time.mktime(pqr.timetuple())
one_day = 86400 #no. of seconds in  a day 
next_unix = last_unix + one_day


for i in  forcast_set :
	next_date = datetime.datetime.fromtimestamp(next_unix)
	next_unix = next_unix + one_day
	data.loc[next_date] = [np.nan for _ in range (len(data.columns)-1)] + [i]
	

data["adj_close"].plot()
data["Forecast"].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()