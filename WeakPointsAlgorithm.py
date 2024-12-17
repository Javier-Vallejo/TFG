# explicacion puntos criticos (cuando era a mano)
#     - antes  de hacer nada  mirar desde networkX si es conexo
#     - si lo es ya se entra, sino mirar que componente es mas grande cuando se entre (esto se hace desde el paso anterior):
#  - coger nodo de set (es añadirle como condicion a la hora de hacer recorrido)
#  - hay 3 opciones de la frase anterior: 1º vistarle para que no añada nodos
#  - 2º  al final de la operacion evitar que añada pero dejar que lo visite
#  - 3º no dejar que lo visite pero tampoco marcarlo como vistado
#  - es decir la linea de if v not in visited: que sea if v not in visited: and v != critical
#  - hacer recorrido (hay que añadirle que vaya contando los nodos para luego devolver nº de nodos por componente)
#  - tambien al hacer la siguiente iteracion de for (que eso significa que no es conexo y que pasa a otro componete)
#  - entonces se tiene que resetear la variable de nodosPorComponente
#  - si se recorre el grafo entero sigue siendo conexo y se vuelve a iterar eliminando otro nodo
#  - hasta que deje de ser conexo

#     - cuando no llegas a mirar a todos los nodos y cada componente es <= (a . n) es Sol

# cosas que hacen falta:
#     - algo para los visitados:
#     - funcionEsSol (mirar si len componentes es >1 y que cada elemento de componentes sea menor que el maxNodePerComponent)
#     - funcionRecorrer: profundidad o anchura

# cosas que hacen falta para voraz local:
#     - funcion que genere nuevos puntos de corte:
#     - guadar distintos valores de solucion
#     - funcion que compare cantidad de nodos empleados para ronmper


import copy
import random
import networkx as nx


def isSolutionNX(conectedComponents: int, components: list, maxNodePerComponent: int):
    isSol = True
    if conectedComponents > 1:
        for numberOfNodes in components:
            if numberOfNodes > maxNodePerComponent:
                isSol = False
                return isSol
        return isSol
    else:
        return False


def criticalNodes(
    nodes: list, adycList: list, maxNodePerComponent: int, Graph, nodesDeleted: list
):
    graphCutSet = []
    nodesSelected = set()
    solutionFound = False
    graphCuts = list(nx.all_node_cuts(Graph))
    firstNodeCut = []
    
    for nodeCutSet in graphCuts:
                cutSet = []
                for nodeInSet in nodeCutSet:
                    cutSet.append(nodeInSet)
                firstNodeCut.append(cutSet)
    
    newNodeCut = True

    while not solutionFound and nodes:
        if not graphCuts:
            newNodeCut = True
            largest_component_nodeList = max(nx.connected_components(subgraph), key=len)
            # aqui entra despues de que haya creado el subgrafo , mirado si ya vale como solucion
            # y visto que no, entonces a partir de ese subgrafo vuelve a generar otros putnos de corte
            largest_component = nx.induced_subgraph(
                subgraph, largest_component_nodeList
            )
            graphCuts = list(nx.all_node_cuts(largest_component))

        
        nodeSet = random.choice(graphCuts)
        cutSet = []
        for nodeInSet in nodeSet:
            cutSet.append(nodeInSet)
        graphCutSet.append(cutSet)
        

        # if newNodeCut:
        #     for nodeCutSet in graphCuts:
        #         cutSet = []
        #         for nodeInSet in nodeCutSet:
        #             cutSet.append(nodeInSet)
        #         graphCutSet.append(cutSet)
        #     newNodeCut = False

        graphCuts.remove(nodeSet)
      

        for node in nodeSet:
            if node in nodes:
                nodesSelected.add(node)
                nodes.remove(node)

        subgraph = nx.induced_subgraph(Graph, nodes)

        components = list(nx.connected_components(subgraph))

        conectedComponents = nx.number_connected_components(subgraph)

        nodesPerComponent = getNodesPerComponent(conectedComponents, components)
        # esto tendrá cuantos nodos hay por componente

        # habia intentado ver si era mas rapido con este codigo:
        #  if len(components) > 1:
        #     for component in components:
        #         numberOfNodes = len(component)
        #         # si component es una lista que tiene los nodos que han surgido tras separar el grafo len de eso se queda con el numero
        #         nodesPerComponent.append(numberOfNodes)
        #     # se comprueba si es solucion solo en el caso de que haya mas de un componente
        #     solutionFound = isSolutionNX(nodesPerComponent,maxNodePerComponent)
        # Pero tarda como 10 segundos mas por grafo en lugar de 40 va a 50
        if nodesPerComponent:
            solutionFound = isSolutionNX(conectedComponents, nodesPerComponent, maxNodePerComponent)

    if not nodes:
        return -1
    sol2, newCutSets = generateNewSol(Graph, nx.nodes(Graph), graphCutSet, maxNodePerComponent, firstNodeCut)
    
    newNodes = sol2 - nodesSelected
    
    while not isBetter(newCutSets,newNodes):
        sol2, newCutSets = generateNewSol(Graph, nx.nodes(Graph), graphCutSet, maxNodePerComponent, firstNodeCut)
        newNodes = sol2 - nodesSelected

    

    graphCutsImproved,newSolutionNodes = improveSol(graphCutSet,newCutSets,newNodes,maxNodePerComponent,Graph,nodesSelected)

    

    # while not betterSol:
    #     sol2 = generateNewSol(Graph, nx.nodes(Graph), graphNodeCut, maxNodePerComponent, firstNodeCut)
    #     betterSol = isBetterSol(sol2,nodesSelected)

    # nodesBestSol = list(nx.nodes(Graph))

    # for node in sol2:
    #     nodesBestSol.remove(node)

    # subgraphBS = nx.induced_subgraph(Graph, nodesBestSol)

    # components = list(nx.connected_components(subgraphBS))

    # conectedComponents = nx.number_connected_components(subgraphBS)

    # nodesPerComponent = getNodesPerComponent(conectedComponents, components)

    # solutionFoundB = isSolutionNX(conectedComponents, nodesPerComponent, maxNodePerComponent)

    return sol2


def getNodesPerComponent(numberOfComponents, components):
    nodesPerComponent = []
    if numberOfComponents > 1:
        for component in components:
            numberOfNodes = len(component)
            # si component es una lista que tiene los nodos que han surgido tras separar el grafo len de eso se queda con el numero
            nodesPerComponent.append(numberOfNodes)
    return nodesPerComponent


def generateNewSol(Graph, nodes, graphCutSet, maxNodePerComponent, firstNodeCuts):

    newGraphCutSet = []
    nodesSelected2 = set()
    nodeList = list(nodes)
    newSolFound = False
    
    sameCut = False

    nodeCut = random.choice(graphCutSet)
    for firstNodeCut in firstNodeCuts:
        if nodeCut == firstNodeCut:
            sameCut = True
            
    while sameCut:
        nodeCut = random.choice(graphCutSet)
        sameCut = False
        for firstNodeCut in firstNodeCuts:
            if nodeCut == firstNodeCut:
                sameCut = True
            
    # se comprueba que el primero no es de la siguiente forma:
    # 1º se escoge uno y se comprueba con los primeros nodos de corte que no coincida
    # 2º Si se ha dado el caso de que sea Iguakse entra en el while
    # donde se escoge otro y se parte de que no es igual. 
    # SI no es igual no entrara en el if y se saldra 
    # y si es igual se vuelve a poner a true la variable 
    # y se volvera a iterar el while
  
    
    # nodeCutT = max(graphNodeCut, key=len)
    # if nodeCutT == firstNodeCut:
    #     nodeCutT = sorted(graphNodeCut, key=len, reverse=True)[1]
    # coger el segundo mas gradne si justo el primero es el primero
    #  que se cogio al principio del algoritmo
    newGraphCutSet.append(nodeCut[:])

    for node in nodeCut:
        if node in nodeList:
            nodesSelected2.add(node)
            nodeList.remove(node)

    subgraph = nx.induced_subgraph(Graph, nodeList)

    largest_component_nodeList = max(nx.connected_components(subgraph), key=len)

    largest_component = nx.induced_subgraph(subgraph, largest_component_nodeList)

    while not newSolFound:

        subGraphNodesCuts = list(nx.all_node_cuts(largest_component))

        for nodeCutSet in subGraphNodesCuts:
                cutSet = []
                for nodeInSet in nodeCutSet:
                    cutSet.append(nodeInSet)
                newGraphCutSet.append(cutSet)

        for nodeSet in subGraphNodesCuts:
            for node in nodeSet:
                if node in nodeList:
                    nodesSelected2.add(node)
                    nodeList.remove(node)

        newGraphSolution = nx.induced_subgraph(subgraph, nodeList)

        components = list(nx.connected_components(newGraphSolution))

        conectedComponents = nx.number_connected_components(newGraphSolution)

        nodesPerComponent = getNodesPerComponent(conectedComponents, components)

        newSolFound = isSolutionNX(
            conectedComponents, nodesPerComponent, maxNodePerComponent
        )

        largest_component_nodeList = max(
            nx.connected_components(newGraphSolution), key=len
        )

        largest_component = nx.induced_subgraph(
            newGraphSolution, largest_component_nodeList
        )

    return nodesSelected2, newGraphCutSet


def improveSol(graphCutSets:list, newGraphCutSets:list,newNodes:set,maxNodePerComponent,graph,nodesSelected):
    newSolutionNodes = []
    a = len(nodesSelected)
    nodeList = list(nx.nodes(graph))
    # previusStepList = nodeList[:]
    previusStepList = copy.deepcopy(nodeList)
    # smaller = False
    validChangeDone = False
     
    while newNodes: 
        nodeList = previusStepList
        # if validChangeDone:
        #     for node in bakUp:
        #         nodeList.remove(node) 
        newCutSet = getNodeCut(newGraphCutSets,newNodes)
        for node in newCutSet:
            newNodes.discard(node)
            
        # smaller = False
        validChangeDone = False 
    
        for i  in range(len(graphCutSets)):
            cutSet = graphCutSets[i]
            if len(newCutSet) < len(cutSet) and not validChangeDone:
                bakUp = cutSet[:]
                graphCutSets[i] = newCutSet 
                # smaller = True
                nodeList,newSolutionNodes = generateNewNodeList(graphCutSets,nodeList,bakUp)
                # nodesDeleted = nodesSelected - newSolutionNodes
                validChangeDone = isValidImprovement(graph,nodeList,maxNodePerComponent)
                if not validChangeDone:
                    graphCutSets[i] = bakUp
                    nodeList = list(nx.nodes(graph))
                #     nodeList = previusStepList
                # previusStepList = nodeList[:]
                #  si el cambio no es valido se deshace
                else:
                    graphCutSets = deleteNodesInCutSets(graphCutSets,bakUp)
        if validChangeDone:
            print(bakUp)
                    
                     
                   
                    
          
        
    return graphCutSets,newSolutionNodes

def generateNewNodeList(graphCutSets:list,nodeList:list,bakUp:list):
    newSolutionNodes = set()
    nodeListCopy = copy.deepcopy(nodeList)
    for cutSet in graphCutSets:
        for node in cutSet:
            if node in nodeListCopy and not node in bakUp:
                newSolutionNodes.add(node)
                nodeListCopy.remove(node)
    return nodeListCopy,newSolutionNodes
    
    
def deleteNodesInCutSets(graphCutSets:list,bakUp:list):
    for cutSet in graphCutSets:
        for node in cutSet:
            if node in bakUp:
                cutSet.remove(node)
    return graphCutSets
    

def isValidImprovement(graph,nodeList:list,maxNodePerComponent):
        newGraphSolution = nx.induced_subgraph(graph, nodeList)

        components = list(nx.connected_components(newGraphSolution))

        conectedComponents = nx.number_connected_components(newGraphSolution)

        nodesPerComponent = getNodesPerComponent(conectedComponents, components)

        newSolFound = isSolutionNX(
            conectedComponents, nodesPerComponent, maxNodePerComponent
        )
        return newSolFound

def getNodeCut(newGraphNodeCut:list,newNodes:set):
    newNodeSet = []
    newNodeCut = newNodes.pop()
    for nodeCut in newGraphNodeCut:
        for node in nodeCut:
            if node == newNodeCut:
                    newNodeSet = nodeCut[:]                   
                    return newNodeSet
                
                
def isBetter(newGraphNodeCut:list,newNodes:set):
    newNodesCopy = set(newNodes)
    while newNodesCopy:
        newNodeCut = newNodesCopy.pop()
        for nodeCut in newGraphNodeCut:
            for node in nodeCut:
                if node == newNodeCut and len(nodeCut) == 1:
                        return True
    



def isBetterSol(sol1, sol2):
    if len(sol1) < len(sol2):
        return True
    else:
        return False


# 