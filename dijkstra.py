import pandas as pd
import json

# Dijkstra algorith implementation in Python
# logic: shortest path from A to B
# all nodes start with distance infinity, except the starting node which is set to 0
# we add the distance from the current node to its neighbors and update if the new distance is smaller then the previous one
# once we set the node as current node we move it to visited and do not update its distance anymore or visit it again
# we repeat this process until we visit all nodes to get the distance from the start to all the other nodes

def dijkstra(graph, start, end=None):
    ''' 
    Computes the shortest path from start to end using Dijkstra's algorithm. If end is None, it computes the shortest path from start to all other nodes.

    :param graph: graph represented as a dictionary with keys being the nodes and values as a dictionary of neighbors with their distances
    :param start: starting node
    :param end: destination node (optional)

    :return: tuple of the shortest distance and the list of nodes from start to end
    '''
    #dictionary to store the distances from the start to other nodes
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()

    # dictionary to store the previous nodes in the path
    previous_nodes = {node: None for node in graph}

    while len(visited) < len(graph):

        #initialize the smallest distance and the current node
        smallest_distance = float('inf')
        current_node = None

        # find the non visited node with the smallest distance
        for node in graph:
            if node not in visited and distances[node] < smallest_distance:

                # updated the smallest distance and the current node
                smallest_distance = distances[node]
                current_node = node

        # if no node found break the loop
        if current_node is None:
            break

        # add the node to visited
        visited.add(current_node)

        # update the distances of the neighbors
        for neighbour, dist in graph[current_node].items():
            if neighbour not in visited:
                new_dist = distances[current_node] + dist
                if new_dist < distances[neighbour]:
                    distances[neighbour] = new_dist
                    previous_nodes[neighbour] = current_node

    if end is not None:
        if distances[end] == float('inf'):
            print(f"No path from {start} to {end}")
            return (float('inf'), None)

        # reconstruct the path from end to start
        path = []
        node = end
        while node is not None:
            path.append(node)
            node = previous_nodes[node]
        path.reverse()
        return (distances[end], path)
    else:
        return (distances, None)
        

def cities_to_cities(graph):
    '''
    Generates a dataframe with the distances from each city to all other cities using Dijkstra's algorithm.

    :param graph: graph represented as a dictionary with keys being the nodes and values as a dictionary of neighbors with their distances

    :return: dataframe with the distances for all city pairs
    '''
    # dictionary with the distances from each city to all other cities
    cities_dist = {city: dijkstra(graph, city)[0] for city in graph}

    # convert the dictionary to a dataframe
    cities_df = pd.DataFrame(cities_dist)
    return cities_df


# Load the graph from a JSON file
def load_graph(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    try:
        graph = load_graph('data/memphis_graph.json')
        print("Successfully loaded Memphis graph.")
        
        # Run the matrix analysis
        df = cities_to_cities(graph)
        print("\nDistance Matrix:")
        print(df)
        
    except FileNotFoundError:
        print("Error: data/memphis_graph.json not found. Please check folder structure.")