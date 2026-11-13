n = int(input("Enter number of vertices: "))

graph = []
for i in range(n):
    graph.append(list(map(int, input().split())))

src = int(input("Enter source: "))

dist = [999] * n
visited = [False] * n
parent = [-1] * n
dist[src] = 0

for _ in range(n):
    u = -1

    for i in range(n):
        if not visited[i] and (u == -1 or dist[i] < dist[u]):
            u = i

    if u == -1 or dist[u] == 999:
        break

    visited[u] = True

    for v in range(n):
        if graph[u][v] > 0 and not visited[v]:
            if dist[u] + graph[u][v] < dist[v]:
                dist[v] = dist[u] + graph[u][v]
                parent[v] = u

print("Shortest Distance and Path:")

for i in range(n):
    path = []
    j = i

    while j != -1:
        path.append(str(j))
        j = parent[j]

    path.reverse()

    if dist[i] == 999:
        print(src, "to", i, "= No Path")
    else:
        print(src, "to", i, "=", dist[i], "Path:", " -> ".join(path))