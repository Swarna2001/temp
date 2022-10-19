n = 3
period = [1, 2, 3]    # time units
D = [3, 2, 4]         # demand for period i (units)
K = [3, 7, 6]         # setup cost for period i (dollars)
H = [1, 3, 2]         # holding cost for period i (dollars)

x = [0 for i in range(n+1)]
x[0] = 1

def c(z, i):
    '''marginal production cost function for period i'''
    if z <= 3:
        return 10 * z
    else:
        return 30 + 20 * (z - 3)
    
def C(z, i):
    '''total production cost for period i'''
    if z == 0:
        return 0
    else:
        return K[i] + c(z, i)
    
f_table = {}

i = 0
f_table[i] = {}
low_x = 0
high_x = sum([d for d in D[i+1:]])

print("-" * 30)
print("Iteration ", i+1)
print("-" * 30)
for x_next in range(low_x, high_x+1):
    z_current = x_next + D[i] - x[i]
    f_value = C(z_current, i) + H[i] * x_next
    print(f'x: {x_next}, z: {z_current}, f: {f_value}')
    f_table[i][x_next] = {'z': z_current, 'f': f_value} 

for i in range(1, len(period)):
    print("-" * 30)
    print("Iteration ", i+1)
    print("-" * 30)

    f_table[i] = {}
    low_x = 0
    high_x = sum([d for d in D[i+1:]])
    for x_next in range(low_x, high_x+1):
        low_z = 0
        high_z = x_next + D[i]
        min_z = 0
        min_f = 1000
        for z_current in range(low_z, high_z+1):
            f_value = C(z_current, i) + H[i] * x_next + f_table[i-1][x_next + D[i] - z_current]['f']
            print(f'x: {x_next}, z: {z_current}, f: {f_value}')
            if f_value < min_f:
                min_z = z_current
                min_f = f_value
        f_table[i][x_next] = {'z': min_z, 'f': min_f}