#linear regression to fit data into line y=mx+c

from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

xs = np.array([3,2,3,2,5,6], dtype=np.float64)
ys = np.array([5,4,6,5,6,7],dtype=np.float64)


def slope_intersect(xs,ys) :
	a = mean(xs) * mean(ys)
	b = mean(xs*ys)
	c = mean(xs) * mean(xs)
	d = mean (xs**2)
	m = (a-b) / (c-d)
	b = mean(ys) - m*mean(xs)
	return m,b

m,b = slope_intersect(xs,ys)

regression_line = [(m*x)+b for x in xs]

#print(regression_line)


def squared_error(y_orig,y_line) :
	return sum((y_orig-y_line)**2)

def coefficient_of_determination(y_orig,y_line) :
	y_mean_line = [mean(ys) for y in y_orig]
	sqrd_error_line = squared_error(y_orig,y_line)
	sqrd_error_ymean = squared_error(y_orig,y_mean_line)
	return 1 - ( sqrd_error_line / sqrd_error_ymean ) 

r_squared = coefficient_of_determination(ys,regression_line)
	
print ("R squared error is : " , r_squared)


plt.scatter(xs,ys, color = "blue")
plt.plot(xs,regression_line)
plt.show()