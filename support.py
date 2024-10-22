import math

def euclidean_distance(a,b)->float:  
    """ 
    points as a 
    tuple or list for example a = (1,2,3) , b = (4,5,6)
    """
    import math
    dimension = len(a)
    if (dimension !=len(b)):
        print("Dimension missmatch")
        return 0 
    dist = 0
    for i in range(dimension):
        dist += math.pow(a[i]-b[i],2)
    return math.sqrt(dist)
    
    
    
def euclidean_distance_assymetrical(a,b)->float:  
    """ 
    points as a 
    tuple or list for example a = (1,2,3) , b = (4,5,6)
    """
    
    dimension = len(a)
    if (dimension !=len(b)):
        print("Dimension missmatch")
        return 0 
    dist = 0
    for i in range(dimension-1): # let's assume last dimesion as high 
        dist += math.pow(a[i]-b[i],2)
        
    if ((a[-1]-b[-1]) > 0):   # a is higher than b so distance from a to b 
        dist += math.pow(0.9*(a[-1]-b[-1]),2)
    else:
        dist += math.pow(1.1*(a[-1]-b[-1]),2)
    
    return math.sqrt(dist)



def name_city(n):
    """Name cities in Excel convention starting from A after Z going to AA then AAA and so on 
            Then calculating distances.
    """
    name = ""
    while True:
        
        rest = n % 26  # getting so called rest and then convert to letter
        name = chr(65+rest) + name # add to already mapped values
        
        
        n  = n // 26 - 1 # move on to 'next' char -1 is neccessary because we have some problem with index without it 26 is mapped to 0->A at last position but 26 // 26 -> 1 at first 

        if (n < 0 ):        # will be fullfiled when we iterate through last chat -> n // 26 - 1  = 0 -1 = -1 
            break
    return name
        

