import os
import GraphGenerator
import WeakPointsAlgorithm


if __name__ == "__main__":
    directoryPath = "Graphs"
    graphList = os.listdir(directoryPath)
    solutions = []
    for fileName in graphList:
        adjList, nodes, alpha,Graph,nodesDeleted = GraphGenerator.genAdjList(fileName)
        # he comporbado que por lo general no me suele tardar mucho en hacer este paso
        conexComponents = WeakPointsAlgorithm.criticalNodes(nodes, adjList, alpha,Graph,nodesDeleted)
        while conexComponents == -1:
            conexComponents = WeakPointsAlgorithm.criticalNodes(nodes, adjList, alpha)
        solutions.append(conexComponents)
    print()
