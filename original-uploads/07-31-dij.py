import csv
import heapq
#fully ai btw
def load_graph_from_csv(csv_filepath):
    """
    Reads the edge CSV and builds an adjacency dictionary:
    graph['Station A'] = {'Station B': 1.2, 'Station C': 0.8}
    """
    graph = {}
    
    with open(csv_filepath, mode='r', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            staA = row["Station A"].strip()
            staB = row["Station B"].strip()
            dist = float(row["distance"])

            if staA not in graph:
                graph[staA] = {}
            if staB not in graph:
                graph[staB] = {}

            # Undirected graph (trains run both ways)
            graph[staA][staB] = dist
            graph[staB][staA] = dist

    return graph


def dijkstra_shortest_path(graph, start, end):
    """
    Calculates the shortest distance and reconstructs the shortest path.
    Returns: (total_distance, path_list)
    """
    # Stores the shortest known distance from start to each node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Stores previous node to reconstruct the best route
    previous_nodes = {}

    # Priority queue stores tuples: (current_accumulated_distance, current_node)
    pq = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        # Reached destination! (Guaranteed shortest due to heap ordering)
        if current_node == end:
            path = []
            curr = end
            while curr in previous_nodes:
                path.append(curr)
                curr = previous_nodes[curr]
            path.append(start)
            return current_dist, path[::-1]  # Return (distance, path reversed)

        # If we found a longer path to an already processed node, skip it
        if current_dist > distances[current_node]:
            continue

        # Explore adjacent stations
        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_dist + weight

            # Found a shorter path to neighbor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return float('inf'), []  # Path not found


# --- Example Execution ---
if __name__ == "__main__":
    csv_file = "station_graph_edges.csv"
    graph = load_graph_from_csv(csv_file)

    start_station = "Roppongi"
    end_station = "Asakusa"

    distance, path = dijkstra_shortest_path(graph, start_station, end_station)

    if path:
        print(f"Shortest Distance: {distance:.2f} km")
        print(f"Stops ({len(path) - 1}):")
        print(" -> ".join(path))
    else:
        print(f"No path found between {start_station} and {end_station}")