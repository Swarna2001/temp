import pandas as pd
import numpy as np

scenario = ['Recession', 'Stagnation', 'Bloom']
#k1 = [-10/100, 5/100, 10/100]
#k2 = [-13/100, 20/100, 50/100]
k1 = [-0.10, 0.05, 0.10]
k2 = [-0.13, 0.20, 0.50]
prob = [0.2, 0.5, 0.3]

E_k1 = 0
for i in range(len(scenario)):
  E_k1 += prob[i] * k1[i]
print(f"E(k1) = {E_k1}")

E_k2 = 0
for i in range(len(scenario)):
  E_k2 += prob[i] * k2[i]
print(f"E(k2) = {E_k2}")

V_k1 = 0
print("V(k1) = ", end="")
for i in range(len(scenario)):
  if i == 0:
    print(f'{prob[i]} * (({k1[i]} - {E_k1}) ** 2)', end=' ')
  else:
    print(f'+ {prob[i]} * (({k1[i]} - {E_k1}) ** 2)', end=' ')

  V_k1 += prob[i] * ((k1[i] - E_k1) ** 2)
print(f"= {V_k1}")

V_k2 = 0
print("V(k2) = ", end="")
for i in range(len(scenario)):
  if i == 0:
    print(f'{prob[i]} * (({k2[i]} - {E_k2}) ** 2)', end=' ')
  else:
    print(f'+ {prob[i]} * (({k2[i]} - {E_k2}) ** 2)', end=' ')
  V_k2 += prob[i] * ((k2[i] - E_k2) ** 2)
print(f"= {V_k2}")

cov_k1_k2 = 0
for i in range(len(scenario)):
  cov_k1_k2 += prob[i] * ((k2[i] - E_k2) * (k1[i] - E_k1))

corr_coeff = cov_k1_k2 / (pow(V_k1, 0.5) * pow(V_k2, 0.5))

print(f"corr(k1,k2) = {corr_coeff}")
