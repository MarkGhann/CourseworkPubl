class Ind:
    
    def __init__(self,vals,fit,mut=20):
        self.vals = vals
        self.mutval = mut
        self.fitness = fit

class Soul:
    
    def __init__(self,WCRT):
        self.WCRT = WCRT
