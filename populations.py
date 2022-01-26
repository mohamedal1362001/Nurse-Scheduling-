from random import random
from random import randint
import random
class Populations:

    def __init__(self,number_nurses,number_populations):
        self.number_nurses=number_nurses
        self.number_populations = number_populations
        self.days=7

    def func(n, end, start=0):
        return list(range(start, n)) + list(range(n + 1, end))
    # ----------------------------------------------------------------------

    def indvidiual(n, d):
        table = []
        for i in range(n):
            l = []
            for x in range(d):
                if not l:
                    l.append(random.randint(0, 3))
                elif l[x - 1] == 3:
                    #r = func(1, 4)
                    r=Populations.func(1,4)
                    l.append(random.choice(r))
                else:
                    l.append(random.randint(0, 3))
            table.append(l)
        return table
    #---------------------------------------------------------------
    def population(c, n, d):
        pop = []
        for i in range(c):
            pop.append(Populations.indvidiual(n, d))
        return pop

    #--------------------------------------------------------------------
    def get_populations(self):
        return Populations.population(self.number_populations,self.number_nurses,self.days)






