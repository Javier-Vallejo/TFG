
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


import random
import networkx as nx



    
    
def isSolutionNX(conectedComponents: int, component: list,maxNodePerComponent:int):
    isSol = True
    if conectedComponents > 1:
        for numberOfNodes in component:
            if numberOfNodes > maxNodePerComponent:
                isSol = False
                return isSol
        return isSol
    else:
        return False


def criticalNodes(nodes: list, adycList: list, maxNodePerComponent: int,Graph,nodesDeleted:list):
    nodesSelected = set()
    solutionFound = False
    nodesCuts = list(nx.all_node_cuts(Graph))
    while not solutionFound and nodes:
        if not nodesCuts:
            # aqui entra despues de que haya creado el subgrafo , mirado si ya vale como solucion
            # y visto que no, entonces a partir de ese subgrafo vuelve a generar otros putnos de corte
            largest_component_set = max(nx.connected_components(subgraph), key=len)
            largest_component = nx.induced_subgraph(Graph,largest_component_set)
            nodesCuts = list(nx.all_node_cuts(largest_component))
            
        nodeSet = random.choice(nodesCuts) 
        nodesCuts.remove(nodeSet)
        
        for node in nodeSet:
            if node in nodes:
                nodesSelected.add(node)
                nodes.remove(node) 
                   
        subgraph = nx.induced_subgraph(Graph,nodes)
        
        components = list(nx.connected_components(subgraph))
        
        conectedComponents = nx.number_connected_components(subgraph)
        
        nodesPerComponent = []
        # esto tendrá cuantos nodos hay por componente
        if conectedComponents > 1:       
            for component in components:
                numberOfNodes = len(component)
                # si component es una lista que tiene los nodos que han surgido tras separar el grafo len de eso se queda con el numero
                nodesPerComponent.append(numberOfNodes)
            
            
        # habia intentado ver si era mas rapido con este codigo:
        #  if len(components) > 1:       
        #     for component in components:
        #         numberOfNodes = len(component)
        #         # si component es una lista que tiene los nodos que han surgido tras separar el grafo len de eso se queda con el numero 
        #         nodesPerComponent.append(numberOfNodes)
        #     # se comprueba si es solucion solo en el caso de que haya mas de un componente
        #     solutionFound = isSolutionNX(nodesPerComponent,maxNodePerComponent)        
        # Pero tarda como 10 segundos mas por grafo en lugar de 40 va a 50
        
        solutionFound = isSolutionNX(conectedComponents,nodesPerComponent,maxNodePerComponent)        
        

    if not nodes:
        return -1
    return nodesSelected



        

