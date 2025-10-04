from collections import deque
import csv

# Алгоритм Едмондса-Карпа
def bfs(residual_graph, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        u = queue.popleft()
        for v in residual_graph[u]:
            if v not in visited and residual_graph[u][v] > 0:
                parent[v] = u
                visited.add(v)
                queue.append(v)
                if v == sink:
                    return True
    return False

def edmonds_karp(graph, source, sink):
    residual_graph = {u: dict(v) for u, v in graph.items()}
    parent = {}
    max_flow = 0

    while bfs(residual_graph, source, sink, parent):
        
        path_flow = float("inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]

        
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v].setdefault(u, 0)
            residual_graph[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow
    return max_flow, residual_graph



graph = {
    "Source": {"T1": float("inf"), "T2": float("inf")},

    # Терминалы -> Склады
    "T1": {"S1": 25, "S2": 20, "S3": 15},
    "T2": {"S3": 15, "S4": 30, "S2": 10},

    # Склады -> Магазины
    "S1": {"M1": 15, "M2": 10, "M3": 20},
    "S2": {"M4": 15, "M5": 10, "M6": 25},
    "S3": {"M7": 20, "M8": 15, "M9": 10},
    "S4": {"M10": 20, "M11": 10, "M12": 15, "M13": 5, "M14": 10},

    # Магазины -> Сток
    "M1": {"Sink": 15},
    "M2": {"Sink": 10},
    "M3": {"Sink": 20},
    "M4": {"Sink": 15},
    "M5": {"Sink": 10},
    "M6": {"Sink": 25},
    "M7": {"Sink": 20},
    "M8": {"Sink": 15},
    "M9": {"Sink": 10},
    "M10": {"Sink": 20},
    "M11": {"Sink": 10},
    "M12": {"Sink": 15},
    "M13": {"Sink": 5},
    "M14": {"Sink": 10},
    "Sink": {}
}


max_flow, residual = edmonds_karp(graph, "Source", "Sink")
print(f"Максимальний потік: {max_flow}")


flows = []

for t in ["T1", "T2"]:
    for s in graph[t]:
        if s.startswith("S"): 
            used_capacity = graph[t][s] - residual[t].get(s, 0)
            if used_capacity > 0:
               
                for shop in graph[s]:
                    delivered = graph[s][shop] - residual[s].get(shop, 0)
                    if delivered > 0:
                        flows.append((t, shop, delivered))


for row in flows:
    print(f"{row[0]} -> {row[1]} : {row[2]}")


with open("terminal_to_shop.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Термінал", "Магазин", "Фактичний Потік (одиниць)"])
    for row in flows:
        writer.writerow(row)
