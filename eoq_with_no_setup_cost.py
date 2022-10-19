import copy
month = [1, 2, 3, 4]             # Time period (in months)
regular = [90, 100, 120, 110]    # Regular capacity (in units)
overtime = [50, 60, 80, 70]      # Overtime capacity (in units)
demand = [100, 190, 210, 160]    # Demand (in units)

regular_prod_cost = 6            # Unit production cost for regular
overtime_prod_cost = 9           # Unit production cost for overtime

holding_cost = 0.10              # Holding cost per unit per month

R = copy.deepcopy(regular)
O = copy.deepcopy(overtime)
D = copy.deepcopy(demand)

schedule = []
total_cost = 0

for i in range(len(D)):
    print("-" * 30)
    print("Iteration ", i)
    print("-" * 30)
    print("D: ", D)
    print("R: ", R)
    print("O: ", O)
    
    
    if R[i] >= D[i]:
        schedule.append(f"Regular {i}: Produce {D[i]} units for period {i}.")
        total_cost += (regular_prod_cost * D[i])
        R[i] = R[i] - D[i]
        D[i] = 0
        continue
        
    schedule.append(f"Regular {i+1}: Produce {R[i]} units for period {i+1}.")
    
    D[i] = D[i] - R[i]
    total_cost += (regular_prod_cost * R[i])
    R[i] = 0
    
    for j in range(i, -1, -1):
        cost = overtime_prod_cost
        if i > j:
            cost = overtime_prod_cost + (i-j) * holding_cost
            
        if O[j] > D[i]:
            O[j] = O[j] - D[i]
            schedule.append(f"Overtime {j+1}: Produce {D[i]} units for period {i+1}.")
            total_cost += (cost * D[i])
            D[i] = 0
            break
            
        if O[j] == 0:
            continue
            
        D[i] = D[i] - O[j]
        schedule.append(f"Overtime {j+1}: Produce {O[j]} units for period {i+1}.")
        total_cost += (cost * O[j])
        O[j] = 0
    
print("-" * 30)
print("Iteration ", i)
print("-" * 30)
print("D: ", D)
print("R: ", R)
print("O: ", O)

print("\n\nOptimal cost for carrying out the operation: $", total_cost)
print("\n\nSchedule:\n\n")
for line in schedule:
    print(line)