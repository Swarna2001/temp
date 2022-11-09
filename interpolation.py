import matplotlib.pyplot as plt

def draw_plot(x,y):
  plt.plot(x,y)
  plt.show()

def u_cal(u, n):
  temp = u
  for i in range(1, n):
    temp = temp * (u - i)
  return temp
 
def fact(n):
  f = 1
  for i in range(2, n + 1):
    f *= i
  return f

def print_forward_difference_table(x, forward_difference_table):
  n = len(x)
  for i in range(n):
    print(x[i], end='\t')
    for j in range(n - i):
      print(forward_difference_table[i][j], end = '\t')
    print("")

def plot_graph(x,y, prediction_list, error_list, xlabel, ylabel):
  plt.plot(x,prediction_list,color='blue')
  plt.plot(x,error_list,color='red')
  plt.scatter(x,y,color='green')
  plt.legend(['prediction','error','actual'])
  plt.title('Actual vs Predicted')
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.show()

def forward_interpolation(x, actual_y, compute= lambda x:x):
  n = len(actual_y)
  forward_diff_table = [[0 for _ in range(n)] for _ in range(n)]
  for i in range(n):
    forward_diff_table[i][0] = compute(actual_y[i])
  for i in range(1, n):
    for j in range(n-i):
      forward_diff_table[j][i] = forward_diff_table[j + 1][i - 1] - forward_diff_table[j][i - 1]
  return forward_diff_table

def find_difference(x, actual_y, forward_diff_table):
  n = len(x)
  predictionList,errorList=[],[]
  for j in range(len(actual_y)):
    value = x[j]
    prefix_sum = forward_diff_table[0][0]
    u = (value - x[0]) / (x[1] - x[0])
    for i in range(1,n):
      prefix_sum += (u_cal(u, i) * forward_diff_table[0][i]) / fact(i)
    p1=round(prefix_sum, 6)
    predictionList.append(p1)
    errorList.append(p1-actual_y[j])
  return predictionList, errorList

def compute_forward_interpolation(x, forward_diff_table ,value):
  res,n = forward_diff_table[0][0],len(x)
  u = (value - x[0]) / (x[1] - x[0])
  for i in range(1,n):
    res += (u_cal(u, i) * forward_diff_table[0][i]) / fact(i)
  return res

def t_test(a,b):
  a_sum, b_sum = sum(a), sum(b)
  a_square_sum, b_square_sum = sum(n*n for n in a), sum(n*n for n in b)
  len_A, len_B = len(a), len(b)
  mean_A, mean_B = a_sum/len_A, b_sum/len_B
  df = (len_A-1)+(len_B-1)
  numerator = mean_A - mean_B
  denominator = ((1/len_A)+(1/len_B)) * ( (a_square_sum - ((a_sum**2)/len_A)) + (b_square_sum - ((b_sum**2)/len_B)) ) * (1/df)
  denominator = pow(denominator, 0.5)
  return numerator/denominator

def proterm(i, value, x):
  pro = 1
  for j in range(i):
      pro = pro * (value - x[j])
  return pro

def apply_newton_divided_difference(x, y, value):
  n = len(x)
  res = y[0][0]
  for i in range(1, n):
      res += (proterm(i, value, x) * y[0][i]);
  return res

def newton_divided_difference(x, actual_y):
  n = len(x)
  y = [[0 for _ in range(n)] for _ in range(n)]
  for i in range(n):
    y[i][0] = actual_y[i]
  for i in range(1, n):
    for j in range(n - i):
      y[j][i] = ((y[j][i - 1] - y[j + 1][i - 1]) / (x[j] - x[i + j]));
  return y

from common import draw_plot, find_difference, forward_interpolation, plot_graph, print_forward_difference_table, compute_forward_interpolation
from scipy import stats

x = [1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995]
data = [731, 782, 833, 886, 956, 1049, 1159, 1267, 1367, 1436, 1505]
draw_plot(x,data)
forward_difference_table = forward_interpolation(x[:9],data[:9])
print_forward_difference_table(x[:9], forward_difference_table)

prediction_list, error_list = [], []
for value in x[9:]:
  prediction_list.append(compute_forward_interpolation(x[9:], forward_difference_table, value))

error_list = [ t2-t1 for t1,t2 in zip(prediction_list, data[9:])]
print_forward_difference_table(x[9:], forward_difference_table)
plot_graph(x[9:],data[9:], prediction_list, error_list, 'Years', 'Expenditure')
print(stats.ttest_ind(prediction_list, error_list))

from common import newton_divided_difference, apply_newton_divided_difference

x = [0, 1, 2, 5.5, 11, 13, 16, 18]
y = [0.5, 3.134, 5.3, 9.9, 10.2, 9.35, 7.2, 6.2]

newton_diff_table = newton_divided_difference(x,y)
for v in [0.5, 3]:
  print(apply_newton_divided_difference(x, newton_diff_table, v))

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline, interp1d, PPoly,splrep

x = [0, 8, 16, 24, 32, 40]
y = [14.621, 11.843, 9.870, 8.418, 7.305, 6.413]

cs = CubicSpline(x, y, extrapolate=True)
print(cs.c)
linear_int = interp1d(x,y)
  
xs = np.arange(x[0], x[-1], 0.1)
ys = linear_int(xs)
  
plt.plot(x, y,'o', label='data')
plt.plot(xs,ys,  label='interpolation', color='green')
plt.legend(loc='upper right', ncol=2)
plt.title('Linear Interpolation')
plt.show()

plt.plot(x, y, 'o', label='data')
plt.plot(xs, cs(xs), label='Cubic spline')  
plt.legend(loc='upper right', ncol=2)
plt.title('Cubic Spline Interpolation')
plt.show()
  
print('Value of double differentiation at 2 and 30 are %s and %s'%(cs(2,2),cs(30,2)))
