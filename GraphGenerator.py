import networkx as nx
import math
# - La primera línea indica, separados por espacio:
# Los valores n, m y a, siendo n = nº de nodos, m = nº de aristas y a = valor de alfa para el problema.
# Las siguientes m líneas incluyen las aristas del grafo.
# Cada una de las líneas contiene, separados también por espacio, el nodo origen y destino de una arista.
# Estos grafos son no dirigidos, por lo que si existe una arista de 1 a 2, también asumimos que existe la arista de 2 a 1.
# Los nodos están numerados de 0 a n-1.
# Ten en cuenta que hay instancias con más de una componente conexa.
# En esos casos, trabajaremos para calcular el separador mínimo de la componente más grande.

# desde el main:
    # - llamas clase que mira el directorio donde estan las instancias
    # - eso se lo pasas a esta clase, esta devuelve un adjList
    # - y luego sobre esa adyacencia ejecutas algoritmo

# carga de datos:

#  leer datos:
#   1 leer fichero
#   2 crearse ArrayList vacio que va a tener el numero maximo de nodos que puede tener cada componente para cada grafo
#   3 leer primera linea
#       3.1 añadir a arrayList de paso 2º el valor de a.n
#       3.2 for de 0 m sin incuir m
#         3.2.1 leer linea y crear variable arista
#   4 generar lista adyacencia

def genAdjList(fileName:str):
    Graph = nx.Graph()
    conectedComponent = nx.Graph()  # genero 2 grafos porque luego iterare 
    # sobre la lista de adyacencia de uno para eliminar los nodos no conectados a la componete conexa mas grande en otro
    # y este segundo grafo al que se han quitado los nodos es el grafo con el que se empieza ya a operar el algoritmo. 
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
    # print()
    # print()
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
        # nodeList se encarga de tenr la lista de nodos que tiene el garfo
        # luego a esta se le quitaran los nodos de corte para generar el subgrafo 
            graphAdjList.append(intAdjList)
        
    adjList = sorted(graphAdjList, key=lambda x: x[0])
     
    while len(adjList) + len(nodesNotConected) < n:
        adjList.append([])
            
    return (adjList,nodesList,maxNodePerCompoment,conectedComponent,nodesNotConected)
# he notado que ya la lista de adyacencia y alguna variable que tiene que ver con ella como nodesNotConected 
# al solo utilizar la lista de nodos del garfo , el grafo y poco mas. 
# Al igual que con todo el proceso de generarlo que va a partir de: "for line in nx.generate_adjlist(Graph):"
# Pero no sé si la manera en la que lo estoy enfocando es correcta