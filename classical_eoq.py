import math
class ClassicalEOQ:
    y_star = 0       # Order quantity (number of units) - optimum
    D = 0            # Demand rate (units per unit time)
    t_star = 0     # Ordering cycle length (time units)

    K = 0            # Setup cost (dollars per order)
    h = 0            # Holding cost (dollars per inventory unit per unit time)
    L = 0            # Lead time (time units)
    
    def __init__(self, D, K, h, L=0):
        self.D = D
        self.K = K
        self.h = h
        self.L = L
    

    def TCU(self, y):
        ''' Total cost per unit time calculation '''
        return (self.K)/(y/self.D) + (self.h)*(y/2)
    
    def generate_policy(self):
        self.y_star = int(math.sqrt((2 * self.K * self.D) / self.h))
        self.t_star = int(self.y_star / self.D)
        
        if self.L == 0:
            print(f'Order y* = {self.y_star} units every t0* = {self.t_star} time units.')
        elif self.L < self.t_star:
            print(f'Order y* = {self.y_star} units whenever the inventory level drops to {int(self.L * self.D)} units.')
        else:
            n = self.L // self.t_star
            L_e = self.L - n * self.t_star
            print(f'Order y* = {self.y_star} units whenever the inventory level drops to {int(L_e * self.D)} units.')

obj = ClassicalEOQ(100, 100, 0.02, 12)
obj.generate_policy()