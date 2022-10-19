import math
class EOQPriceBreak:
    y_star = 0       # Order quantity (number of units) - optimum
    D = 0            # Demand rate (units per unit time)
    t_star = 0       # Ordering cycle length (time units)

    K = 0            # Setup cost (dollars per order)
    h = 0            # Holding cost (dollars per inventory unit per unit time)
    L = 0            # Lead time (time units)
    
    c1 = 0           # Price per unit without discount
    c2 = 0           # Price per unit with discount
    q = 0            # Order quantity for availing discount
    
    def __init__(self, D, K, h, c1, c2, q, L=0):
        self.D = D
        self.K = K
        self.h = h
        self.c1 = c1
        self.c2 = c2
        self.q = q
        self.L = L
        
    def TCU1(self, y):
        ''' Total cost per unit time calculation '''
        return (self.c1 * self.D) + (self.K)/(y/self.D) + (self.h)*(y/2)
    
    def generate_policy(self):
        y_m = int(math.sqrt((2 * self.K * self.D) / self.h))
        self.y_star = y_m
        if self.q > y_m:
            a = 1
            b = 2 * ((self.c2 * self.D - self.TCU1(y_m)) / self.h)
            c = 2 * ((self.K * self.D) / self.h)
        
            root1 = int( (-b + math.sqrt(b**2 - 4*a*c)) / (2*a) )
            root2 = int( (-b - math.sqrt(b**2 - 4*a*c)) / (2*a) )
            Q = 0
            
            if root1 > y_m:
                Q = root1
            else:
                Q = root2
            
            if self.q < Q:
                self.y_star = self.q
                
        self.t_star = int(self.y_star / self.D)
        
        if self.L == 0:
            print(f'Order y* = {self.y_star} units every t0* = {self.t_star} time units.')
        elif self.L < self.t_star:
            print(f'Order y* = {self.y_star} units whenever the inventory level drops to {self.L * self.D} units.')
        else:
            n = self.L // self.t_star
            L_e = int(self.L - n * self.t_star)
            print(f'Order y* = {self.y_star} units whenever the inventory level drops to {int(L_e * self.D)} units.')
            
obj = EOQPriceBreak(187.5, 20, 0.02, 3, 2.5, 1000, 12)
obj.generate_policy()