
# day16 notes

graph approach, Dijkstra refresher:
https://datagy.io/dijkstras-algorithm-python/

```python
#     -6- (C) -
#    /     |    \
#   /      2     3
#  /       |      \
#(A) --3- (B) -8-- (D)

# Converting our graph to an edge list
edge_list = [('A', 'B', 3), ('A', 'C', 8), ('B', 'C', 2), ('B', 'E', 5), ('C', 'D', 1), ('C', 'E', 6), ('D', 'E', 2), ('D', 'F', 3), ('E', 'F', 5)]

# To make this easier to work with, we can change the representation of the edge list to an adjacency list. Each key will be a node and the value will be a dictionary that contains the node’s neighbors and their weights. For this, we can use a custom function:

# Converting our graph to an adjacency list
def edge_list_to_adjacency_list(edge_list):
    adj_list = {}
    for (src, dest, weight) in edge_list:
        if src not in adj_list:
            adj_list[src] = {}
        if dest not in adj_list:
            adj_list[dest] = {}
        
        adj_list[src][dest] = weight
        adj_list[dest][src] = weight

    return adj_list

adj_list = edge_list_to_adjacency_list(edge_list)
print(adj_list)

# Returns:
# {
#     'A': {'B': 3, 'C': 8},
#     'B': {'A': 3, 'C': 2, 'E': 5},
#     'C': {'A': 8, 'B': 2, 'D': 1, 'E': 6},
#     'E': {'B': 5, 'C': 6, 'D': 2, 'F': 5},
#     'D': {'C': 1, 'E': 2, 'F': 3},
#     'F': {'D': 3, 'E': 5}
#  }
# Now that we have an adjacency list, let’s begin by implementing Dijkstra’s algorithm:

# Implementing Dijkstra's Algorithm in Python
import heapq

def dijkstra(adj_list, start):
    distances = {node: float('inf') for node in adj_list}
    distances[start] = 0

    # Priority queue to track nodes and current shortest distance
    priority_queue = [(0, start)]

    while priority_queue:
        # Pop the node with the smallest distance from the priority queue
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if a shorter distance to current_node is already found
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors and update distances if a shorter path is found
        for neighbor, weight in adj_list[current_node].items():
            distance = current_distance + weight

            # If shorter path to neighbor is found, update distance and push to queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

```


