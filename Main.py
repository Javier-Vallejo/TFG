import os
import GraphGenerator
import WeakPointsAlgorithm


if __name__ == "__main__":
    directoryPath = "Graphs"
    graphList = os.listdir(directoryPath)
    solutions = []
    i = 1
    for fileName in graphList:
        adjList, nodes, alpha,Graph,nodesDeleted = GraphGenerator.genAdjList(fileName)
        # he comporbado que por lo general no me suele tardar mucho en hacer este paso
        criticalNodes = WeakPointsAlgorithm.criticalNodes(nodes, adjList, alpha,Graph,nodesDeleted,i)
        while criticalNodes == -1:
            criticalNodes = WeakPointsAlgorithm.criticalNodes(nodes, adjList, alpha,i)
        i+=1
        solutions.append(criticalNodes)
    print()
