import csv
weighted_graph = {}
from graph_node import graph1
def mass(x):
        
    with open("station_graph_edges.csv", "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)

        for row in reader:
            staA = row["Station A"]
            staB = row["Station B"]
            dis = float(row["distance"])

            if staA not in weighted_graph:
                weighted_graph[staA] = {}

            if staB not in weighted_graph:
                weighted_graph[staB] = {}

            weighted_graph[staA][staB] = dis
            weighted_graph[staB][staA] = dis
    return weighted_graph[x]

#print(weighted_graph["Roppongi"])

x = graph1("Kuramae")

for i in range(0, len(x), 2):
    #print(x[i], x[i + 1],sep="\n")
    one,two=x[i], x[i + 1]
    print(mass(one),mass(two))
#print(x)
