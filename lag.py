

import matplotlib.pyplot as plt
import random
import pprint
import math
import scipy.stats as stats
from statistics import mean
from scipy import interpolate


def prevterm(i, value, x): 
    prev = 1; 
    for j in range(i): 
        prev = prev * (value - x[j]); 
    return prev

def newton_formula(value, x, y, n): 
  
    sum_temp = y[0][0]; 
  
    for i in range(1, n):
        sum_temp = sum_temp + (prevterm(i, value, x) * y[0][i]); 
      
    return sum_temp; 


def newton_divi_diff_table(x,y,n):
  divi_diff = [[0 for i in range(10)] 
        for j in range(10)]

  for i in range(n):
    divi_diff[i][0]=y[i]
    
  for i in range(1, n): 
    for j in range(n - i): 
        divi_diff[j][i] = ((divi_diff[j][i - 1] - divi_diff[j + 1][i - 1]) /(x[j] - x[i + j]));
  return divi_diff



def lag_interpolation(x,y,x_val):
  res=0
  for i in range(len(x)):
    numr=1
    denr = 1
    for j in range(len(x)):
      if j!=i:
        numr *= (x_val - x[j])
      if j!=i:
        denr *= (x[i] - x[j])
    res += ((numr/denr)*y[i])

  return res


#newton divided difference

x=[0,1,2,5.5,11,13,16,18]
y=[0.5, 3.134, 5.3, 9.9, 10.2, 9.35,7.2,6.2]


x_val=[0.5,3]
divi_diff = newton_divi_diff_table(x,y,len(x))
y_cap=[]
for i in x_val:
  y_cap.append(newton_formula(i,x,divi_diff,len(x)))

#print(divi_diff)
print(y_cap)




# lagrange's interpolation

x=[0,1,2,5.5,11,13,16,18]
y=[0.5, 3.134, 5.3, 9.9, 10.2, 9.35,7.2,6.2]

x_val = [0.5,3]
y_cap=[]
for i in x_val:
  y_cap.append(lag_interpolation(x,y,i))

print(y_cap)

