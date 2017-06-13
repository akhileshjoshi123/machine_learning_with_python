#linear regression to fit data into line y=mx+c

from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import random

style.use('fivethirtyeight')

#xs = np.array([3,2,3,2,5,6], dtype=np.float64)
#ys = np.array([5,4,6,5,6,7],dtype=np.float64)

def create_dataset(how_much,variance,step=2,correaltion=False):
	val=1
	ys=[] #initially an empty list
	for i in range(how_much) : 
		y= val + random.randrange(-variance,variance) #range will be from - to + variance
		ys.append(y)
		if correaltion and correaltion == 'pos' :
			val = val + step
		elif correaltion and correaltion == 'neg' :
			val = val - step
	
	xs = [i for i in range(len(ys))]

	return np.array(xs,dtype=np.float64) , np.array(ys,dtype=np.float64)

def slope_intersect(xs,ys) :
	a = mean(xs) * mean(ys)
	b = mean(xs*ys)
	c = mean(xs) * mean(xs)
	d = mean (xs**2)
	m = (a-b) / (c-d)
	b = mean(ys) - m*mean(xs)
	return m,b


def squared_error(y_orig,y_line) :
	return sum((y_orig-y_line)**2)

def coefficient_of_determination(y_orig,y_line) :
	y_mean_line = [mean(ys) for y in y_orig]
	sqrd_error_line = squared_error(y_orig,y_line)
	sqrd_error_ymean = squared_error(y_orig,y_mean_line)
	return 1 - ( sqrd_error_line / sqrd_error_ymean ) 


xs, ys = create_dataset(40,80,2,correaltion='pos')

print("Value of Xs" , xs)

m,b = slope_intersect(xs,ys)

regression_line = [(m*x)+b for x in xs]

#print(regression_line)

r_squared = coefficient_of_determination(ys,regression_line)
	
print ("R squared error is : " , r_squared)


plt.scatter(xs,ys, color = "blue")
plt.plot(xs,regression_line)
plt.show()