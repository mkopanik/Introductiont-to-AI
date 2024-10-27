import random
from support import euclidean_distance,euclidean_distance_assymetrical
class CitiesMap():
    def __init__(self,n,seed = None):
        """
        initialize with number of cities to include in graph 
        """    
        
        if seed is not None:
            random.seed(seed)
        self.seed = seed
        self.n = n 
        self.cities = []
        self.routes = [[0 for _ in range(n)] for _ in range(n)]
        # we can represent routes between cities as a matrix with n x n shape 
        for i in range(n):
            self.cities.append((random.randint(-101,101),random.randint(-101,101),random.randint(-51,51)))

        # now let's make sure that we don't have duplicated cities so we'll get derired number of unique cities
        
        len_check = len(set(self.cities))
        
        while (len_check != n):
            self.cities.append((random.randint(-101,101),random.randint(-101,101),random.randint(-51,51)))
            len_check = len(set(self.cities))
        self.cities = list(set(self.cities))
    
    
    def calculate_distance(self,symmetrical: bool = True , connections: float = 1):
        """
        Fill matrix with distnaces between city i and j  0 < i,j < n with 0 on main diagonal , conenctions 1 means all cities will be connected
        0.5 only half of them and so on 
        
        """
             
        if (symmetrical):
            if (connections==1):   
                for i in range(self.n):
                    for j in range(i+1 , self.n):  # to not double calcualte
                        
                        distance = euclidean_distance(self.cities[i], self.cities[j])
                    
                        # Store the route only once, as it is undirected
                        self.routes[i][j] = distance
                        self.routes[j][i] = distance
                return self.routes
            else:
                # in this case we nned to delete number of connections that equals to connections * (n^2-n)/2 
                
                n_to_delete = int(round((1 - connections) * ((self.n**2 - self.n) / 2),0))

                indexes_list = []    
                                
                for i in range(self.n):
                    for j in range(i+1 , self.n):  # to not double calcualte
                        
                        indexes_list.append((i,j))
                        
                        distance = euclidean_distance(self.cities[i], self.cities[j])
                    
                        # Store the route only once, as it is undirected
                        self.routes[i][j] = distance
                        self.routes[j][i] = distance
            
                indexes_to_delete = random.sample(indexes_list,n_to_delete)
                
                for i in indexes_to_delete:
                    # in the list that we iterate over we have pair of matrix indexes when let's say i means position with 0 index in matrix rows, j column
                    self.routes[i[0]][i[1]] = 0     # deletes i,i
                    self.routes[i[1]][i[0]] = 0        # deletes j,i 
                    
                    
                
                
                return self.routes
                
                
                
        else: 
            if (connections==1):  
                for i in range(self.n):
                    for j in range(self.n):
                        self.routes[i][j] = euclidean_distance_assymetrical(self.cities[i], self.cities[j])
                        
                return self.routes  
            else:
                # in this case we nned to delete number of connections that equals to connections * (n^2-n) # assymetrical 
                
                n_to_delete = int(round((1 - connections) * ((self.n**2 - self.n) / 2),0))
                indexes_list = []    
                                
                for i in range(self.n):
                    for j in range(self.n):
                        # however with connections to delete we'll keep approach from previous one as I understand that lack connections means no road between two points 
                        # no matter how long 
                        
                        self.routes[i][j] = euclidean_distance_assymetrical(self.cities[i], self.cities[j])
                        
                        # adds to indexes base only ones from above main diagonal 
                        if (j>i):
                            indexes_list.append((i,j))
                
                indexes_to_delete = random.sample(indexes_list,n_to_delete)
                
                
                for i in indexes_to_delete:
                    # in the list that we iterate over we have pair of matrix indexes 
                    self.routes[i[0]][i[1]] = 0     # deletes i,i
                    self.routes[i[1]][i[0]] = 0
                    
                    
                
                
                return self.routes
                
                
    
    