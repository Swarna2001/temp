

import matplotlib.pyplot as plt
import random
import pprint
import math
from scipy import stats
from statistics import mean

#functions
def ncr(n, r,forward):
  val = 1

  for i in range(r):
    if forward == True:
      val *= (n - i)
    else:
      val *= (n + i)

  if r == 1:
    return val

  a = val / math.factorial(r)
  
  return a


def interpolation(y_0, n, fdt, u, forward):
  val = y_0
  if forward == True:
    for i in range(n):
      val += ncr(u, i+1,forward) * fdt[i][0]
  else:
    for i in range(n):
      val += ncr(u, i+1,False) * fdt[i][-1]

  return val



def forward_diff_tab(arr):
  forward_diff_table=[]

  while len(arr)>1:
    temp=[]
    
    for i in range(1,len(arr)):
      temp.append(arr[i]-arr[i-1])
    forward_diff_table.append(temp)
    arr = temp

  return forward_diff_table

#main func
#stoping dist - automob
year=[1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995]

exp=[731, 782, 833, 886, 956, 1049, 1159, 1267, 1367, 1436, 1505]

forward_diff_table = forward_diff_tab(exp)

h=1

y_cap = []
for i in range(len(year)):
  u = (year[i]-year[0])/h
  y_cap.append(interpolation(exp[0], len(forward_diff_table), forward_diff_table, u, True))

#print(forward_diff_table)

#print(y_cap)

plt.plot(year, y_cap)
#plt.show()



#ttest

t,p = stats.ttest_ind(exp, y_cap)

print(t,p)   #t < p ----> good model




