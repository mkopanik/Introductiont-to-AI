import random
import numpy

class CitiesMap():
    def __init__(self,n,seed = None):
        """
        initialize with number of cities to include in graph 
        """    
        
        if seed is not None:
            random.seed(seed)
        self.seed = seed
        
        self.cities = []
        self.routes = dict()
        for i in range(n):
            self.cities.append((random.randint(-101,101),random.randint(-101,101),random.randint(-51,51)))

        # now let's make sure that we don't have duplicated cities so we'll get derired number of unique cities
        
        len_check = len(set(self.cities))
        
        while (len_check != n):
            self.cities.append((random.randint(-101,101),random.randint(-101,101),random.randint(-51,51)))
            len_check = len(set(self.cities))
        

        