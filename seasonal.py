import math
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from scipy import stats


def percent_cyclic(act, pred):
  per_cyc=[]
  for i in range(len(act)):
    per_cyc.append((act[i]/pred[i])*100)
  return per_cyc


def relative_cyclic(act, pred):
  rel_cyc=[]
  for i in range(len(act)):
    rel_cyc.append(((act[i]-pred[i])/pred[i])*100)
  return rel_cyc


def ttest(act,pred):
  t1,p1=stats.ttest_ind(act,pred)
  return t1,p1

def linear_reg(x, y):
  n = len(x)
  x_y = [i*j for i,j in zip(x, y)]
  x_2 = [i**2 for i in x]
  b1 = (n*sum(x_y) - sum(x)*sum(y)) / (n*sum(x_2) - sum(x)**2)
  b0 = (1/n) * (sum(y) - b1*sum(x))
  print("\nModel Coefficients are:")
  print("\nb0(slope): ", b0)
  print("\nb1(intercept): ", b1)
  print("\n")
  return [b0, b1]

def predict_val(b0, b1, x):
  ans = []

  for i in x:
    ans.append((b0 + b1*i))

  return ans



def compute_seasonal_index(x, num_yrs):
  
  four_quar_mov_avg = []
  four_quar_cen_mov_avg = []
  per_act_to_mov_avg = []
  j = 0

  for i in range(len(x)-3):
    temp = (x[i] + x[i+1] + x[i+2] + x[i+3]) / 4
    four_quar_mov_avg.append(temp)

  #print("\n4-quarter moving averages: ", four_quar_mov_avg)

  for i in range(len(four_quar_mov_avg)-1):
    temp = (four_quar_mov_avg[i] + four_quar_mov_avg[i+1]) / 2
    four_quar_cen_mov_avg.append(temp)

  #print("\n4-quarter centered moving averages: ", four_quar_cen_mov_avg)

  for i in range(2, len(x)-2):
    temp = (x[i] / four_quar_cen_mov_avg[j]) * 100
    j += 1
    per_act_to_mov_avg.append(temp)

  #print("\nPercentage of actual to moving averages: ", per_act_to_mov_avg)

  diff = [0, 0] + per_act_to_mov_avg
  n = len(diff) % 4
  diff += [0 for i in range(n)]

  #print("\nDiff values: ", diff)

  quar_val = []
  modified_mean = []
  width = len(diff) // num_yrs

  for i in range(4):
    temp = []

    for j in range(0, num_yrs):
      temp.append(diff[width*j+i])

    quar_val.append(temp)
  
  #print("\nTrack values: ", quar_val)

  for i in range(len(quar_val)):
    quar_val[i] = [i for i in quar_val[i] if i != 0]
    a = min(quar_val[i])
    b = max(quar_val[i])
    quar_val[i].remove(a)
    quar_val[i].remove(b)
    n = len(quar_val[i])
    modified_mean.append(sum(quar_val[i]) / n)

  #print("\nModified means / Trimmed means: ", modified_mean)

  toi = sum(modified_mean)
  adjusting_factor = 400 / toi
  seasonal_indices = []

  for i in range(len(modified_mean)):
    seasonal_indices.append(modified_mean[i] * adjusting_factor)

  #print("\nSeasonal indices: ", seasonal_indices)

  modified_seasonal_indices = [i/100 for i in seasonal_indices]
  modified_seasonal_indices = modified_seasonal_indices * num_yrs

  deseasonalized_data = []

  for i in range(len(x)):
    deseasonalized_data.append((x[i] / modified_seasonal_indices[i]))

  #print("\nDeseasonalized data: ", deseasonalized_data)

  ans_dict = {'4 quarter moving avg':four_quar_mov_avg, 
              'four_quarter_centered_moving_avg':four_quar_cen_mov_avg, 
              'percent_actual_to_moving_avg':per_act_to_mov_avg, 'diff':diff, 
              'quar_val':quar_val, 
              'modified_mean':modified_mean, 
              'seasonal_indices':seasonal_indices, 
              'deseasonalized_data':deseasonalized_data}

  return ans_dict



def identify_trend(x, num_yrs):
  n = len(x)
  coding = [0 for i in range(n)]

  mid = (n//2) - 1
  coding[mid] = -0.5
  coding[mid+1] = 0.5

  for i in range(mid-1, -1, -1):
    coding[i] = coding[i+1] - 1

  for i in range(mid+2, n):
    coding[i] = coding[i-1] + 1

  for i in range(n):
    coding[i] *= 2

  xy = [i*j for i,j in zip(coding, x)]
  x_2 = [i**2 for i in coding]

  sum_y = sum(x)
  sum_x_2 = sum(x_2)
  sum_xy = sum(xy)

  # print("\nSummation y: ", sum_y)
  # print("\nSummation xy: ", sum_xy)
  # print("\nSummation x2: ", sum_x_2)

  b = sum_xy / sum_x_2
  a = sum_y / (num_yrs * 4)

  ans_dict = {'a':a, 'b':b, 'coding':coding}
  
  return ans_dict



#main func

actual_sales = [293, 246, 231, 282, 301, 252, 227, 291, 304, 259, 239, 296, 306, 265, 240, 300]

seasonal_index = compute_seasonal_index(actual_sales, 4)
print("\n****Seasonal Index :*****\n")
pprint(seasonal_index)
coeff = identify_trend(seasonal_index['deseasonalized_data'], 4)

coeff

pred_val = predict_val(coeff['a'], coeff['b'], coeff['coding'])

percent_of_trend = []

for i in range(len(pred_val)):
  temp = (seasonal_index['deseasonalized_data'][i] / pred_val[i]) * 100
  percent_of_trend.append(temp)

percent_of_trend

plt.plot(actual_sales, color="r")
plt.plot(seasonal_index['deseasonalized_data'],"--", color="b",)
plt.plot(pred_val, color="g")
