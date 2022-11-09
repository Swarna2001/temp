def f(x,y):
  return x+y

def get_yi_plus_1(xi,yi, h):
  return yi + h*f(xi, yi)

def get_xi_plus_1(xi,h):
  return xi+h
