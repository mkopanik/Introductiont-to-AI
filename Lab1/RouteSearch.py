from CityMap import CitiesMap
class RouteSearch:
    def __init__(self,cities_map : CitiesMap):
        self.nodes = cities_map.cities
        self.size = cities_map.n
        self.edges = cities_map.routes
        # self.states = []

    def dfs_all_paths(self, starting_node: int):
        """
        Perform DFS to explore all possible paths, both complete and incomplete.
        
        Parameters:
        starting_node : int - the node from which to start the search
        
        Returns:
        list : A list of paths. Path can be incomplete or complete.
        """
        # Stack for DFS
        stack = [[starting_node]]
        all_paths = []

        while stack:
            path = stack.pop()
            last_node = path[-1]
            
            
            # Record the current (incomplete or complete) path and its cost
            all_paths.append(path)

            # If the path includes all cities, check if it can return to the start
            if len(path) == self.size:
                return_to_start_cost = self.edges[last_node][starting_node]
                if return_to_start_cost != 0:     # to make sure that we can return to start from there
                    # Record the completed cycle (path returns to the start)
                    all_paths.append(path + [starting_node])

            # Explore all unvisited neighbors (continue DFS)
            for neighbor in range(self.size - 1, -1, -1):  # reverse order to simulate stack behavior
                if neighbor not in path and self.edges[last_node][neighbor] != 0:
                    new_path = path + [neighbor]
                    stack.append(new_path)
                    
        return all_paths    
    
    def bfs_all_paths(self, starting_node: int):
        """
        Perform BS to explore all possible paths, both complete and incomplete.
        
        Parameters:
        starting_node : int - the node from which to start the search
        
        Returns:
        list : A list of paths. Path can be incomplete or complete.
        """
        # queue for bfs
        queue = [[starting_node]]
        all_paths = []

        while queue:
            path = queue.pop(0)   # take first element from list (queue)
            last_node = path[-1]
            
            # Record the current (incomplete or complete) path and its cost
            all_paths.append(path)

            # If the path includes all cities, check if it can return to the start
            if len(path) == self.size:
                return_to_start_cost = self.edges[last_node][starting_node]   # to make sure that we can return to start from there
                if return_to_start_cost != 0:
                    # Record the completed cycle (path returns to the start)
                    all_paths.append(path + [starting_node])

            # Explore all unvisited neighbors (continue bfs)
            for neighbor in range(0, self.size):  # normal queue order
                if neighbor not in path and self.edges[last_node][neighbor] != 0:
                    new_path = path + [neighbor]
                    queue.append(new_path)
                   

        return all_paths

    
    def get_min_distance(self,state_tree):
        """ Requires state tree object from for example dfs or bfs algo, calculate distance only for full paths"""
        from sys import maxsize
        min_distance = maxsize
        shortest_route = []
        for cycle in state_tree:
            if (len(cycle)==self.size + 1):  # we calculate distance only in case of full cycle
                distance = 0
                # we're now looping through one full cycle len n+1
                for index in range(self.size):  # it's in fact len(state_tree) - 1 -> exactly what we need in this approach
                    distance += self.edges[cycle[index]][cycle[index+1]]  # we need to extract ith and ith+1 element of our cycle 
            
                if (distance < min_distance):
                    min_distance = distance
                    shortest_route = cycle

        return (shortest_route,min_distance)
    def nn(self,start):
            from sys import maxsize
            path = [start]
            
            while(len(path)!=self.size):
                dist = maxsize  # initialize distance as maxsize
                node = path[-1]  # get last node from path as a new 'starting node'
                target = -1  # initialize target as a number from outside matrix index
                for neighbour in range(self.size):   # iterate over neighbours of 'new' target                 
                    cur_dist = self.edges[node][neighbour] 
                    if ((neighbour not in path) & (0 < cur_dist < dist)):    # if path exists and is shorter than previous lower from this starting point 
                        target = neighbour   # store neighbour
                        dist = cur_dist   # store shortest distance 
                        
                if target == -1:    # we got in the dead end 
                    return path , "Didn't find complete route"
                path.append(target)
            
            if (self.edges[target][start]!=0):    # if we reached there and we can go back to start we found complete circle
                path.append(start)
                return path , self.get_distance(path)
    def dijkstra(self,start):
        # I think my implementation might be briefly described as bascilly brut force one but with usage of priority queue we should handle not fully connected graphes better
       
        from queue import PriorityQueue
        from sys import maxsize
        
        # Priority queue to get something dijkstra like 
        pq = PriorityQueue()
        pq.put((0, start, [start], {start}))
        
        # Track the best solution
        best_tour = None
        best_distance = maxsize
        
        while not pq.empty():
            current_distance, current_node, current_path, visited = pq.get()
            
            # If we've visited all cities, try to return to start
            if len(visited) == self.size:
                if self.edges[current_node][start] != 0:
                    total_distance = current_distance + self.edges[current_node][start]
                    complete_path = current_path + [start]
                    
                    # Update best tour if this is shorter
                    if total_distance < best_distance:
                        best_tour = complete_path    # assigning only in situation that we got complete tour 
                        best_distance = total_distance
                continue
            
            # Explore neighboring cities
            for next_city in range(self.size):
                # Check if city is not visited and there's a valid route
                if next_city not in visited and self.edges[current_node][next_city] != 0:
                    # Calculate new distance
                    new_distance = current_distance + self.edges[current_node][next_city]
                    
                    # Create new path and visited set
                    new_path = current_path + [next_city]
                    new_visited = visited.union({next_city})
                    
                    # Add to priority queue
                    pq.put((new_distance, next_city, new_path, new_visited))
        
        return best_tour, best_distance
    
    def dijkstra_nn(self,start):
        
        from queue import PriorityQueue
        from sys import maxsize
        
        # Initialize path with start node
        path = [start]
        total_distance = 0
        unvisited = set(range(self.size)) - {start}
        
        current_node = start
        
        while unvisited:
            # Priority queue to store potential next nodes
            pq = PriorityQueue()
            
            # Check all unvisited cities
            for next_city in unvisited:
                # If there's a route to this city
                if self.edges[current_node][next_city] != 0:   # add all neighbours to priority queue
                    # Priority is the distance to the city
                    pq.put((self.edges[current_node][next_city], next_city))
            
            # If no routes found, we're stuck  
            if pq.empty():
                return path, "Couldn't complete route - no connections"
            
            # Get the nearest city  extracting city 
            _, nearest_city = pq.get()  
            
            # Add distance and update path
            total_distance += self.edges[current_node][nearest_city]
            path.append(nearest_city)
            
            # Update current node and unvisited set
            current_node = nearest_city
            unvisited.remove(nearest_city)
        
        # Try to return to start
        if self.edges[current_node][start] != 0:
            total_distance += self.edges[current_node][start]
            path.append(start)
            return path, total_distance
        
        return path, "Couldn't complete route - no return to start"
                       