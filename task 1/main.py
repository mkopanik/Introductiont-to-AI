# %%
from Edge import Edge
from os import curdir
from Graph import Graph
import numpy as np
np.random.seed(4)

# %%
g_undir_full = Graph(is_fixed=False)
g_undir_partial = Graph(is_fixed=True, is_full=False)
g_dir_full = Graph(is_fixed=True, is_directional=True)
g_dir_partial = Graph(is_fixed=True, is_full=False, is_directional=True)

# %%
def shortest_path(paths, g):
    min_distance = np.inf
    min_path = []
    for path in paths:
        distance = g.full_path_cost(path)
        if distance < min_distance:
            min_distance, min_path = distance, path
    return min_distance, min_path

# %%
graph = g_undir_full
starting_city = 0

# inadmissible - average of unvisited * number of remaining steps
# admissible - min of unvisited * number of remaining steps


def get_unvisited_edges(path, graph):
    A = 0
    B = 1
    all_edges = graph.get_all_edges() # edge is (i, j, distance)
    unvisited = []                   # path is list of numbers of vertices
    for edge in all_edges:
        if edge[B] == path[0]: #entering start
            if edge[A] not in path:
                unvisited.append(edge)
                continue
        if edge[A] == path[-2]: #exiting the last
            if edge[B] not in path:
                unvisited.append(edge)
                continue
        if (edge[A] not in path) and (edge[B] not in path):
            unvisited.append(edge)
    return unvisited


def h_inadm(path, graph):
    unvisited = get_unvisited_edges(path, graph)
    if not unvisited:
        return 0
    mean = np.mean(unvisited, axis=0)[-1] # mean of the distances
    return mean * (graph.nodes_count() - len(path) + 1)


def h_adm(path, graph):
    unvisited = get_unvisited_edges(path, graph)
    if not unvisited:
        return 0
    minimum = np.min(unvisited, axis=0)[-1] # min of the distances
    return minimum * (graph.nodes_count() - len(path) + 1)

# %%
print("DFS", shortest_path(graph.dfs(starting_city), graph))
print("BFS", shortest_path(graph.bfs(starting_city), graph))

print("Dijkstra", graph.dijkstra(starting_city))
print("NN", graph.nn(starting_city))
print("ACO", graph.aco(starting_city, 40, 40))

print("A* adm", graph.a_star(starting_city, h_adm))
print("A* inadm", graph.a_star(starting_city, h_inadm))

# %%
