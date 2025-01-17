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
    nodes: list, adycList: list, maxNodePerComponent: int, Graph, nodesDeleted: list , i:int
):
    graphCutSet = []
    nodesSelected = set()
    solutionFound = False
    if i == 8:
        print()
    graphCuts = list(nx.all_node_cuts(Graph))
    firstCutSet = []
    
    for nodeCutSet in graphCuts:
                cutSet = []
                for nodeInSet in nodeCutSet:
                    cutSet.append(nodeInSet)
                firstCutSet.append(cutSet)
    

    while not solutionFound and nodes:
        if not graphCuts:
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

        if nodesPerComponent:
            solutionFound = isSolutionNX(conectedComponents, nodesPerComponent, maxNodePerComponent)

    if not nodes:
        return -1
    
    # a partir de aqui algorimto de mejora
    
    if moreThanOneCut(graphCutSet,firstCutSet): # esto comprueba que la solucion 
        #se llega con mas de una iteracion de los kcutsets
        # porque si no no hay por donde mejorar
        
        cutSetsAvaliables = copy.deepcopy(graphCutSet) # esto esta para comprobar el optimo local
        # porque se intenta sacar a partir de un conjunto de corte que no sea de los primeros 
        # y que este te de una solucion que puedas hacer un cambio
        # de un conjunto de corte por otro de un tamaño menor
        
        # entonces se hace esta nueva variable para ir iteranbdo 
        # sobre los distintos nuevos puntos o conjuntos de corte
        
        for cutSet in firstCutSet:
            cutSetsAvaliables.remove(cutSet)
            
        # lo primero es que se le quitan los conjuntos que se hayan usado al principio 
        # ya que esos no valen
        
        maxSize = getMaxSize(graphCutSet) # con esto se obtiene el tamaño del conjunto de corte
        # mas grande del grafo
    
        sol2, newCutSets,solutionsChoosed = generateNewSol(Graph, nx.nodes(Graph), graphCutSet, maxNodePerComponent, firstCutSet)
        # aqui se genera una nueva solucion se obtiene tambien unos nuevos conjuntos de corte 
        # y se obtiene el primer conjunto usado para buscar la mejora.
        
        newNodes = sol2 - nodesSelected # despues de obtienen que nuevos nodos se han utilizado
        
        canImprove = isBetter(newCutSets,newNodes,maxSize) # con esta funcion se quiere mirar si 
        # se ha generado una solucion que tenga por lo menos 1 conjunto de corte de tamaño menor 
        # a los mas grandes de la primera solucion 
        
        while not canImprove and cutSetsAvaliables:
            sol2, newCutSets,solutionsChoosed = generateNewSol(Graph, nx.nodes(Graph), cutSetsAvaliables, maxNodePerComponent, firstCutSet)
            cutSetsAvaliables.remove(solutionsChoosed)
            # se quita la solucion usada para evitar volver a usarla 
            # y asi ir agilizando en el proceso
            newNodes = sol2 - nodesSelected
            if newNodes:
                canImprove = isBetter(newCutSets,newNodes,maxSize)
        
        # este while se utiliza para que se generen nuevas soluciones mientras 
        # queden opciones por utilizarse y que aun no se haya generado una que tenga opcion de mejora
        
        # se saldra o porque se ha llegado a una solucion que permita la mejora o
        # que se hayan usado todas las opciones posibles


        if canImprove: # si se entra en este if es que se puede mejorar 
            # asi que se devuelve esa mejora en la sol
            graphCutsImproved,newSolutionNodes = improveSol(graphCutSet,newCutSets,newNodes,maxNodePerComponent,Graph,nodesSelected)
            print("Solucion Mejorada: ", i)
            return newSolutionNodes
        
        # si se llega aqui es que se han usado todas las opciones posibles. 
        # asi que no se ha podido mejorar
        print("Solucion Casi mejorada: ", i)
        return nodesSelected
        
    # y este ultimo caso es cuando se genere una solucion con unos unicos conjuntos de corte.
    print("Solucion: ", i)
    return nodesSelected

def getMaxSize(graphCutSet:list):
    larguestCut = max(graphCutSet, key=len)
        
    maxSize = len(larguestCut)
    return maxSize
    

def moreThanOneCut(graphCutSet,firstNodeCut):
    for cutSet in graphCutSet:
        if not cutSet in firstNodeCut:
            return True
    return False 


def getNodesPerComponent(numberOfComponents, components):
    nodesPerComponent = []
    if numberOfComponents > 1:
        for component in components:
            numberOfNodes = len(component)
            # si component es una lista que tiene los nodos que han surgido tras separar el grafo 
            # usar len en eso se queda con el numero
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
    # 2º Si se ha dado el caso de que sea Igual se entra en el while
    # donde se escoge otro y se parte de que no es igual. 
    # SI no es igual no entrara en el if y se saldra 
    # y si es igual se vuelve a poner a true la variable 
    # y se volvera a iterar el while
  
    newGraphCutSet.append(nodeCut[:])

    for node in nodeCut:
        if node in nodeList:
            nodesSelected2.add(node)
            nodeList.remove(node)

    subgraph = nx.induced_subgraph(Graph, nodeList) # despues de hacer el primer cambio en el grafo
    # y quitar los primeros nodos se genera el siguiente sugrafo

    largest_component_nodeList = max(nx.connected_components(subgraph), key=len)
    # para ver su nueva lista de nodos

    largest_component = nx.induced_subgraph(subgraph, largest_component_nodeList)
    # de donde luego sacar su componente mas gradne para volver a separarlo

    while not newSolFound:

        subGraphNodesCuts = list(nx.all_node_cuts(largest_component))

        for nodeCutSet in subGraphNodesCuts:
                cutSet = []
                for nodeInSet in nodeCutSet:
                    cutSet.append(nodeInSet)
                newGraphCutSet.append(cutSet)
        
        # este fragmento del algoritmo se encarga de generar una lista con los conjuntos de corte

        for nodeSet in subGraphNodesCuts:
            for node in nodeSet:
                if node in nodeList:
                    nodesSelected2.add(node)
                    nodeList.remove(node)
        
        # despues de se vuelve a quitar los nodos del grafo y añadirlos a una solucion
        
        # y se genera el sugrafo siguiente para quedarse con los nodos que haya por componete conexa
        # en el subgrafo y despues se comprueba si esos nodos que han generado el subgrafo ya son solucion o no
        

        newGraphSolution = nx.induced_subgraph(subgraph, nodeList)

        components = list(nx.connected_components(newGraphSolution))
        # esta variable es una lista de listas donde cada lista es un componente conexo
        # y los elementos de esa lista son los nodos de ese componente

        numberOfComponents = nx.number_connected_components(newGraphSolution)

        nodesPerComponent = getNodesPerComponent(numberOfComponents, components)

        newSolFound = isSolutionNX(
            numberOfComponents, nodesPerComponent, maxNodePerComponent
        )

        largest_component_nodeList = max(
            nx.connected_components(newGraphSolution), key=len
        )

        largest_component = nx.induced_subgraph(
            newGraphSolution, largest_component_nodeList
        )
        
        # si no se llega a ser solucion, entonces se queda con el subgarfo mas grande del primer subgrafo 
        # y con este se volverá a iterar en el while 

    return nodesSelected2, newGraphCutSet,nodeCut


def improveSol(graphCutSets:list, newGraphCutSets:list,newNodes:set,maxNodePerComponent,graph,nodesSelected):
    newSolutionNodes = []
    a = len(nodesSelected)
    nodeList = list(nx.nodes(graph))
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
            
        validChangeDone = False 
    
        for i  in range(len(graphCutSets)):
            cutSet = graphCutSets[i]
            if len(newCutSet) < len(cutSet) and not validChangeDone:
                bakUp = cutSet[:]
                graphCutSets[i] = newCutSet 
                nodeList,newSolutionNodes = generateNewNodeList(graphCutSets,nodeList,bakUp)
                validChangeDone = isValidImprovement(graph,nodeList,maxNodePerComponent)
                if not validChangeDone:
                    graphCutSets[i] = bakUp
                    nodeList = list(nx.nodes(graph))
                #  si el cambio no es valido se deshace poniendo otra vez el conjunto que habia al principio
                #  y dejando los nodos del grafo como al principio para que el algorimto funcione correctamente
                else:
                    graphCutSets = deleteNodesInCutSets(graphCutSets,bakUp)
                    # si el cambio es bueno se mira si el nodo que se empleaba en un conjunto de corte sigue en otros 
                    # y se elimina para que no se utilice en ninguna ocasion como conjunto de corte
                    # por ejemplo: si no se utiliza el conjunto {2,3}
                    # quiere decir que ni el 2 ni el 3 son nodos que sean puntos criticos
                    # asi que tampoco se podria utlizar el conjunto {3,6} o {2,5} se quedarian como {6} o como {5}
                    
                     
                   
                    
          
        
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
    # genera los nuevos nuevos nodos como soluciom de puntos criticos y los elimina de los nodos del grafo 
    # para luego usarlos para comprobar si este cambio de conjuntos de corte es valido
    
def deleteNodesInCutSets(graphCutSets:list,bakUp:list):
    for cutSet in graphCutSets:
        for node in cutSet:
            if node in bakUp:
                cutSet.remove(node)
    return graphCutSets
    

def isValidImprovement(graph,nodeList:list,maxNodePerComponent): 
    
        # esto con la nueva lista de nodos verifica que siga teniendo el grafo separado y que se cumpla la condicion de solucion
        # haciendo la misma comprobacion que se hacia para generar las primeras soluciones
        
        newGraphSolution = nx.induced_subgraph(graph, nodeList)

        components = list(nx.connected_components(newGraphSolution))

        numberOfComponents = nx.number_connected_components(newGraphSolution)

        nodesPerComponent = getNodesPerComponent(numberOfComponents, components)

        newSolFound = isSolutionNX(
            numberOfComponents, nodesPerComponent, maxNodePerComponent
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
    
    # esto se utiliza para a traves de los nodos que se han encontrado como solucion
    # se obtenga su punto de corte de correspondiente
                
                
def isBetter(newGraphNodeCut:list,newNodes:set,maxSize:int):
    newNodesCopy = set(newNodes)
    while newNodesCopy:
        newNodeCut = newNodesCopy.pop()
        for nodeCut in newGraphNodeCut:
            for node in nodeCut:
                if node == newNodeCut and len(nodeCut) < maxSize:
                        return True
    return False

# y esta funcion se encarga de verificar que la nueva solucion generada tenga opcion de mejora
# es decir tenga algun de corte que sea de menor tamaño que los que tiene la primera solucion
    