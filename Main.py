import os
import time
import GraphGenerator
import WeakPointsAlgorithm


if __name__ == "__main__":
    directoryPath = "Graphs"
    graphList = os.listdir(directoryPath)
    solutions = []
    graphTimes = []
    graphIndex = 1
    totalTime = 0.0
    percentage = 1 
    instancesUsed = int(len(graphList)*percentage)
    for i in range(instancesUsed):
        fileName = graphList[i]
        adjList, nodes, alpha,Graph,nodesDeleted = GraphGenerator.genAdjList(fileName)
        startTime = time.time()
        criticalNodes = WeakPointsAlgorithm.criticalNodes(nodes, adjList, alpha,Graph,nodesDeleted,graphIndex)
        while criticalNodes == -1:
            criticalNodes = WeakPointsAlgorithm.criticalNodes(nodes, adjList, alpha,Graph,nodesDeleted,graphIndex)
        endTime = time.time()
        graphEjecutionTime = endTime - startTime
        totalTime = totalTime + graphEjecutionTime
        graphTimes.append(graphEjecutionTime)
        graphIndex+=1
        solutions.append(criticalNodes)
    print() 