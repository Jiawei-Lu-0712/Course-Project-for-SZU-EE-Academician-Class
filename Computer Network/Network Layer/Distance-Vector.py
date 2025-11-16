import numpy as np
#将拓扑图定义为邻接矩阵
INF=float('inf')  #将无法到达的节点表示为无穷大
graph=[
    [0,1,INF,6,INF,INF],  #节点0
    [1,0,3,4,INF,INF],    #节点1
    [INF,3,0,2,6,INF],    #节点2
    [6,4,2,0,9,2],        #节点3
    [INF,INF,6,9,0,INF],  #节点4
    [INF,INF,INF,2,INF,0] #节点5
]
num_nodes=len(graph)
#初始化距离向量和路径表
distance_vectors=np.full((num_nodes,num_nodes),INF)  #距离
next_hop=[[-1] * num_nodes for _ in range(num_nodes)]  #路径
#初始化每个节点的距离向量和直连
for i in range(num_nodes):
    for j in range(num_nodes):
        if graph[i][j] != INF and i != j:
            distance_vectors[i][j]=graph[i][j]
            next_hop[i][j]=j
        elif i==j:
            distance_vectors[i][j]=0
            next_hop[i][j]=i
#Bellman-Ford 更新
def distance_vector_routing():
    global distance_vectors, next_hop
    updated=True
    while updated:
        updated=False
        for u in range(num_nodes):
            for v in range(num_nodes):
                for w in range(num_nodes):
                    if distance_vectors[u][w]+graph[w][v]<distance_vectors[u][v]:
                        distance_vectors[u][v]=distance_vectors[u][w]+graph[w][v]
                        next_hop[u][v]=next_hop[u][w]
                        updated=True
#运行
distance_vector_routing()
#打印结果
def display_routing_table():
    for i in range(num_nodes):
        print(f"Routing table for Node {i}:")
        for j in range(num_nodes):
            if i!=j:
                path=reconstruct_path(i,j)
                print(f" - To Node {j}: Distance={distance_vectors[i][j]},Path={path}")
        print()
#根据next_hop表重建路径
def reconstruct_path(start,end):
    if next_hop[start][end]==-1:
        return "No Path"
    path=[start]
    while start!=end:
        start=next_hop[start][end]
        path.append(start)
    return path
#输出路由表
display_routing_table()