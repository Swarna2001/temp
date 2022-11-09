def f(x,y):
  return x**2+y**2

def get_k1(xi,yi):
  return f(xi, yi)

def get_yi_plus_1(xi, yi, h):
  k1 = h*get_k1(xi, yi)
  k2 = h*f(xi + (h/2), yi + (k1/2))
  k3 = h*f(xi + (h/2), yi + (k2/2))
  k4 = h*f(xi + h, yi+k3)
  print(k1,k2,k3,k4)
  return yi + (1/6*(k1 + 2*k2 + 2*k3 + k4))

print(get_yi_plus_1(1,1.2,0.05))
