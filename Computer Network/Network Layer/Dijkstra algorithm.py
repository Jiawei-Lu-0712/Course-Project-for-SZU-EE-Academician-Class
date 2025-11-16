import heapq
def dijkstra(graph, start_node):
    #用无穷大作为初始化距离，并将start_node设为0
    distances={node: float('inf') for node in graph}
    distances[start_node]=0
    #使用起始节点初始化priority queue
    priority_queue=[(0, start_node)]
    #跟踪路径
    paths={node: [] for node in graph}
    paths[start_node]=[start_node]
    while priority_queue:
        current_distance,current_node=heapq.heappop(priority_queue)
        #如果距离未更新，则跳过此节点
        if current_distance>distances[current_node]:
            continue
        #探索当前节点的相邻节点
        for neighbor,weight in graph[current_node].items():
            distance=current_distance+weight
            #如果找到到相邻节点的较短路径
            if distance<distances[neighbor]:
                distances[neighbor]=distance
                heapq.heappush(priority_queue,(distance, neighbor))
                paths[neighbor]=paths[current_node]+[neighbor]
    return distances, paths
#示例用法
if __name__ == "__main__":
    #将图形定义为邻接表
    graph = {
        0: {1: 1, 3: 6},
        1: {0: 1, 2: 3, 3: 4},
        2: {1: 3, 3: 2, 4: 6},
        3: {0: 6, 1: 4, 2: 2, 4: 9, 5: 2},
        4: {2: 6, 3: 9},
        5: {3: 2}
    }
    #指定起始节点
    start_node=0
    #运行Dijkstra算法
    distances, paths=dijkstra(graph, start_node)
    #打印结果
    print("Distances from node",start_node,"to all other nodes:")
    for node, distance in distances.items():
        print(f"Node {node}: {distance}")
    print("\nPaths from node", start_node, "to all other nodes:")
    for node, path in paths.items():
        print(f"Node {node}: {' -> '.join(map(str, path))}")