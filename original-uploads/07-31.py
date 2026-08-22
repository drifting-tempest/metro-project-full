import csv
lines={ "tokyo sakura":['Minowabashi', 'Arakawa-itchumae',
    'Arakawakuyakushomae', 'Arakawa-nichome', 'Arakawa-nanachome',
    'Machiya-ekimae', 'Machiya-nichome', 'Higashi-ogu-sanchome',
    'Kumanomae', 'Miyanomae', 'Odai', 'Arakawa-yuenchimae',
    'Arakawa-shakomae', 'Kajiwara', 'Sakaecho', 'Oji-ekimae',
    'Asukayama', 'Takinogawa-itchome', 'Nishigahara-yonchome',
    'Shin-koshinzuka', 'Koshinzuka', 'Sugamoshinden', 'Otsuka-ekimae',
    'Mukohara', 'Higashi-ikebukuro-yonchome', 'Toden-zoshigaya',
    'Kishibojimmae', 'Gakushuinshita', 'Omokagebashi', 'Waseda'],
    "asakusa":['Nishi-magome', 'Magome', 'Nakanobu', 'Togoshi',
    'Gotanda', 'Takanawadai', 'Sengakuji', 'Mita', 'Daimon',
    'Shimbashi', 'Higashi-ginza', 'Takaracho', 'Nihombashi',
    'Ningyocho', 'Higashi-nihombashi', 'Asakusabashi', 'Kuramae',
    'Asakusa', 'Honjo-azumabashi', 'Oshiage'], "mita":['Meguro',
    'Shirokanedai', 'Shirokane-takanawa', 'Mita', 'Shibakoen',
    'Onarimon', 'Uchisaiwaicho', 'Hibiya', 'Otemachi', 'Jimbocho',
    'Suidobashi', 'Kasuga', 'Hakusan', 'Sengoku', 'Sugamo',
    'Nishi-sugamo', 'Shin-itabashi', 'Itabashi-kuyakushomae',
    'Itabashihoncho', 'Motohasunuma', 'Shimura-sakaue',
    'Shimura-sanchome', 'Hasune', 'Nishidai', 'Takashimadaira',
    'Shin-takashimadaira', 'Nishi-takashimadaira'],
    "nippori":['Nippori', 'Nishi-nippori', 'Akado-shogakkomae',
    'Kumanomae', 'Adachi-odai', 'Ogi-ohashi', 'Koya', 'Kohoku',
    'Nishiaraidaishi-nishi', 'Yazaike', 'Toneri-koen', 'Toneri',
    'Minumadai-shinsuikoen'], "oedo":['Tochomae', 'Shinjuku-nishiguchi',
    'Higashi-shinjuku', 'Wakamatsu-kawada', 'Ushigome-yanagicho',
    'Ushigome-kagurazaka', 'Iidabashi', 'Kasuga', 'Hongo-sanchome',
    'Ueno-okachimachi', 'Shin-okachimachi', 'Kuramae', 'Ryogoku',
    'Morishita', 'Kiyosumi-shirakawa', 'Monzen-nakacho', 'Tsukishima',
    'Kachidoki', 'Tsukijishijo', 'Shiodome', 'Daimon', 'Akabanebashi',
    'Azabu-juban', 'Roppongi', 'Aoyama-itchome', 'Kokuritsu-kyogijo',
    'Yoyogi', 'Shinjuku', 'Tochomae', 'Nishi-shinjuku-gochome',
    'Nakano-sakaue', 'Higashi-nakano', 'Nakai',
    'Ochiai-minami-nagasaki', 'Shin-egota', 'Nerima', 'Toshimaen',
    'Nerima-kasugacho', 'Hikarigaoka'], "shinjuku":['Shinjuku',
    'Shinjuku-sanchome', 'Akebonobashi', 'Ichigaya', 'Kudanshita',
    'Jimbocho', 'Ogawamachi', 'Iwamotocho', 'Bakuro-yokoyama',
    'Hamacho', 'Morishita', 'Kikukawa', 'Sumiyoshi', 'Nishi-ojima',
    'Ojima', 'Higashi-ojima', 'Funabori', 'Ichinoe', 'Mizue',
    'Shinozaki', 'Motoyawata'] }

import sys #cross the normal limit
sys.setrecursionlimit(5000)



def dfs_all_paths(graph, current, end, visited=None, path=None, all_paths=None): #DFS algorithm
    if visited is None:
        visited = set()
    if path is None:
        path = []
    if all_paths is None:
        all_paths = []

    visited.add(current)
    path.append(current)

    if current == end:
        all_paths.append(list(path))
    else:
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                dfs_all_paths(graph, neighbor, end, visited, path, all_paths)

    # Backtrack
    path.pop()
    visited.remove(current)

    return all_paths
def build_graph(line_data):#adjency list
    graph = {}
    for stations in line_data.values():
        for i, station in enumerate(stations):
            if station not in graph:
                graph[station] = set()
            if i > 0:
                graph[station].add(stations[i - 1])
            if i < len(stations) - 1:
                graph[station].add(stations[i + 1])
    return graph

def load_distances(csv_file):
    """Loads segment distances into a lookup table: distances[staA][staB] = distance"""
    distances = {}
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            staA, staB = row["Station A"], row["Station B"]
            dis = float(row["distance"])
            
            if staA not in distances:
                distances[staA] = {}
            if staB not in distances:
                distances[staB] = {}
                
            distances[staA][staB] = dis
            distances[staB][staA] = dis
    return distances

def get_path_distance(path, distances):
    """Calculates total distance for a route."""
    total = 0.0
    for i in range(len(path) - 1):
        staA, staB = path[i], path[i + 1]
        total += distances.get(staA, {}).get(staB, 0.0)
    return total


# --- Usage ---
distances = load_distances("station_graph_edges.csv")
metro_graph = build_graph(lines)
paths = dfs_all_paths(metro_graph, "Roppongi", "Asakusa")

# Sort paths by total distance calculated from CSV
paths.sort(key=lambda p: get_path_distance(p, distances))

# Print sorted results
print(f"Found {len(paths)} path(s) sorted by total distance:\n")
for idx, path in enumerate(paths, 1):
    dist = get_path_distance(path, distances)
    print(f"Path {idx} ({dist:.2f} km, {len(path) - 1} stops):")
    print(" -> ".join(path))
    print("-" * 50)