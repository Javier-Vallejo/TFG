import copy
import math
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
            
            largest_component = nx.induced_subgraph(
                subgraph, largest_component_nodeList
            )
            graphCuts = list(nx.all_node_cuts(largest_component))

        
        nodeSet = random.choice(graphCuts)
        cutSet = []
        for nodeInSet in nodeSet:
            cutSet.append(nodeInSet)
            if nodeInSet in nodes:
                nodesSelected.add(nodeInSet)
                nodes.remove(nodeInSet)

        graphCutSet.append(cutSet)
        
        graphCuts.remove(nodeSet)
        
        subgraph = nx.induced_subgraph(Graph, nodes)

        components = list(nx.connected_components(subgraph))

        conectedComponents = nx.number_connected_components(subgraph)

        nodesPerComponent = getNodesPerComponent(conectedComponents, components)


        if nodesPerComponent:
            solutionFound = isSolutionNX(conectedComponents, nodesPerComponent, maxNodePerComponent)

    if not nodes:
        return -1
    
    solutionNodes,newGraphCuts = localOptimum(Graph,graphCutSet, maxNodePerComponent, firstCutSet,nodesSelected,i)
    tries = 10
    percentage = 0.25 
    
    finalSolution = finalImprovement(Graph,solutionNodes,tries,percentage,newGraphCuts,firstCutSet,maxNodePerComponent,i)
    
    
    return finalSolution


def localOptimum(Graph,graphCutSet, maxNodePerComponent, firstCutSet,solutionNodes,i):
    if moreThanOneCut(graphCutSet,firstCutSet): 
        
        cutSetsAvaliables = copy.deepcopy(graphCutSet) 
            
        for cutSet in firstCutSet:
            if cutSet in cutSetsAvaliables:
                cutSetsAvaliables.remove(cutSet)
            
        maxSize = getMaxSize(graphCutSet) 
            
        graphNodesList = list(nx.nodes(Graph))
        
        newSolution, newCutSets,solutionsChoosed = generateNewSol(Graph, graphNodesList, graphCutSet, maxNodePerComponent, firstCutSet)
            
        cutSetsAvaliables.remove(solutionsChoosed)
        
        newNodes = newSolution - solutionNodes 
            
        canImprove = isBetter(newCutSets,newNodes,maxSize)
            
        graphNodesList = list(nx.nodes(Graph))
            
        while not canImprove and cutSetsAvaliables:
            newSolution, newCutSets,solutionsChoosed = generateNewSol(Graph, graphNodesList, cutSetsAvaliables, maxNodePerComponent, firstCutSet)
            cutSetsAvaliables.remove(solutionsChoosed)

            newNodes = newSolution - solutionNodes
            if newNodes:
                canImprove = isBetter(newCutSets,newNodes,maxSize)  
        if canImprove: 
            graphCutsImproved,newSolutionNodes = improveSol(graphCutSet,newCutSets,newNodes,maxNodePerComponent,Graph)
            # solucion mejorada obtenida
            return newSolutionNodes,graphCutsImproved
            

        # solucion voraz pero no mejorada tras una serie de intentos
        return solutionNodes,graphCutSet
            

    # solucion sin posibilidad de mejora debido a un parametro alfa muy alto
    return solutionNodes,graphCutSet


def finalImprovement(graph,solutionNodes:set,tries:int,percentage:float,graphCutSets:list,firstCutSet:list,maxNodePerComponent:int,i:int):
    firstSolution = list(copy.deepcopy(solutionNodes))
    
    hasImproved = False
    
    if moreThanOneCut(graphCutSets,firstCutSet):
    
        while tries and not hasImproved:
        
           
            worseSolution,nodesDeletedFromSol,modifiedCutSets = deteriorateSolution(firstSolution,percentage,graphCutSets,firstCutSet)
            

            newSolution,remadeCutSets = remakeSolution(graph,worseSolution,firstCutSet,nodesDeletedFromSol,firstSolution,modifiedCutSets)
            
            newSolutionSet = set(newSolution)
            

            finalSolution,finalCutSets = localOptimum(graph,remadeCutSets,maxNodePerComponent,firstCutSet,newSolutionSet,i)
            
            if len(firstSolution) < len(finalSolution):
                tries = tries - 1
            else:
                solutionNodes = set(finalSolution)
                hasImproved = True
        return solutionNodes
            
    else:
        print("Solucion", i)
        return solutionNodes
    
 
def deteriorateSolution(solution:list,percentaje:float,graphCutSets:list, firstCutSet:list):
    worseSolution = copy.deepcopy(solution)
    
    copyCutSets = copy.deepcopy(graphCutSets)
    
    amountNodesDeleted =  math.floor(len(solution) * percentaje)
    
    nodesDeleted = set()
    
    i = 0 
    
    while i <= amountNodesDeleted:
        node = random.choice(solution)
        if node not in nodesDeleted:
            nodesDeleted.add(node)
            worseSolution.remove(node)
            i +=1
        
    newCutSets = deleteNodesInCutSets(copyCutSets,nodesDeleted)    
    
    return worseSolution,nodesDeleted,newCutSets


def remakeSolution(graph,solution:list,firstCutSet:list,nodesDeletedFromSol:set,bakUpSolution,modifiedCutSets:list):
    nodeList = list(nx.nodes(graph))
    
    for solutionNode in solution:
        nodeList.remove(solutionNode)
        
    
    subgraph = nx.induced_subgraph(graph, nodeList)
        
    largest_component_nodeList = max(nx.connected_components(subgraph), key=len)
    largest_component = nx.induced_subgraph(subgraph, largest_component_nodeList)
    
    newCutSets = list(nx.all_node_cuts(largest_component))
    
    newNodes = getNewNodes(newCutSets,firstCutSet,nodesDeletedFromSol)
    
    for cutSet in newCutSets:
        for node in cutSet:
            nodeSet = []
            if node in newNodes:
                nodeSet.append(node)
                modifiedCutSets.append(nodeSet)
    
    
    for node in newNodes:
        solution.append(node)
 
    return solution,modifiedCutSets
    
    

def getNewNodes(newCutSets:list,firstCutSet:list,nodesDeletedFromSol:set):
    
    newNodes = []
    for cutSet in newCutSets:
        for node in cutSet:
            if not node in nodesDeletedFromSol:
                newNodes.append(node)
    
    return newNodes
    
    
def inFirstCutSet(firstCutSet:list,node:int):
    for cutSet in firstCutSet:
        for nodeInSet in cutSet:
            if nodeInSet == node:
                return True
    return False
    

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
            nodesPerComponent.append(numberOfNodes)
    return nodesPerComponent


def generateNewSol(Graph, nodeList, graphCutSet, maxNodePerComponent, firstNodeCuts):

    newGraphCutSet = []
    nodesSelected2 = set()
    newSolFound = False
    sameCut = False

    
    cutSetChoosed = random.choice(graphCutSet)
    for firstNodeCut in firstNodeCuts:
        if cutSetChoosed == firstNodeCut:
            sameCut = True
    
                
    while sameCut:
        cutSetChoosed = random.choice(graphCutSet)
        sameCut = False
        for firstNodeCut in firstNodeCuts:
            if cutSetChoosed == firstNodeCut:
                sameCut = True    

  
    newGraphCutSet.append(cutSetChoosed[:])

    for node in cutSetChoosed:
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
                    if nodeInSet in nodeList:
                        nodesSelected2.add(nodeInSet)
                        nodeList.remove(nodeInSet)
                newGraphCutSet.append(cutSet)
        
        newGraphSolution = nx.induced_subgraph(subgraph, nodeList)

        components = list(nx.connected_components(newGraphSolution))
       
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
        


    return nodesSelected2, newGraphCutSet,cutSetChoosed


def improveSol(graphCutSets:list, newGraphCutSets:list,newNodes:set,maxNodePerComponent,graph):
    newSolutionNodes = []
    nodeList = list(nx.nodes(graph))
    previusStepList = copy.deepcopy(nodeList)
    validChangeDone = False
     
    while newNodes: 
        nodeList = previusStepList
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
                else:
                    graphCutSets = deleteNodesInCutSets(graphCutSets,bakUp)
                    
                    
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
    
    
def deleteNodesInCutSets(graphCutSets:list,bakUp:set|list):
    for cutSet in graphCutSets:
        for node in cutSet:
            if node in bakUp:
                cutSet.remove(node)
    return graphCutSets
    

def isValidImprovement(graph,nodeList:list,maxNodePerComponent): 
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
                
def isBetter(newGraphNodeCut:list,newNodes:set,maxSize:int):
    newNodesCopy = set(newNodes)
    while newNodesCopy:
        newNodeCut = newNodesCopy.pop()
        for nodeCut in newGraphNodeCut:
            for node in nodeCut:
                if node == newNodeCut and len(nodeCut) < maxSize:
                        return True
    return False
