import networkx as nx
import math
def genAdjList(fileName:str):
    Graph = nx.Graph()
    conectedComponent = nx.Graph()  
    file = open("Graphs\\"+fileName)
    firstLine = file.readline()
    n, m, alpha = map(float, firstLine.strip().split())
    n = int(n)
    m = int(m)
    maxNodePerCompoment = math.floor(alpha * n)
    for _ in range(m):
        edge = file.readline()
        origin, destiny = map(int, edge.strip().split())
        Graph.add_edge(origin, destiny)
        conectedComponent.add_edge(origin, destiny)

    components = nx.number_connected_components(Graph)
    if components >1:
        largest_component = max(nx.connected_components(Graph), key=len)
    graphAdjList = []
    nodesList = []
    nodesNotConected = []
    for line in nx.generate_adjlist(Graph):
        nodeConected = True
        strAdjList = line.strip().split()
        intAdjList = list(map(int, strAdjList))
        if components >1: 
            for node in intAdjList:
                if node not in largest_component:
                    nodeConected = False
                    if node in conectedComponent:
                        conectedComponent.remove_node(node)
                        nodesNotConected.append(node)
        if nodeConected:
            nodesList.append(intAdjList[0]) 
            graphAdjList.append(intAdjList)
        
    adjList = sorted(graphAdjList, key=lambda x: x[0])
     
    while len(adjList) + len(nodesNotConected) < n:
        adjList.append([])
            
    return (adjList,nodesList,maxNodePerCompoment,conectedComponent,nodesNotConected)
