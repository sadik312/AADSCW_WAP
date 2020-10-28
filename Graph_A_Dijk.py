import networkx as nx
import doubly_linked_list as dl
import heapq

"""Initiating a graph """
graph = nx.Graph()


def creating_graph(g):
    """The for loop below will loop for all the values in line dict created in 'doubly_linked_list.py'
        adding edges by iterating through every node in the line"""
    for i in dl.line:

        """For the loop the inintal node is needed witch is the start_node"""

        g.add_edge(dl.line[i].start_node.item[1], dl.line[i].start_node.item[2],
                   weight=dl.line[i].start_node.item[3], line=dl.line[i].start_node.item[0], Sweight=0)
        n = dl.line[i].start_node

        """while loop used to iterate through all the nodes/stations in the tube line, same technique used as 
            doubly linked list to traverse the list. 
            Making a variable n and assigning it to start_node will allow to traverse through the list"""
        while n is not None:
            if n.next is None:
                break
            else:

                g.add_edge(n.item[1], n.item[2], weight=n.item[3], line=n.item[0], Sweight=0)
                n = n.next


"""Function creating the graph"""
creating_graph(graph)

"""This is how the data is stored as list in the nodes for each tube line, obviously print is not necessary"""
# print(dl.Bakerloo.traversing_the_list())

"""This is the format to extract the data from the graph, obvuiously print is not necessary when just using/redirecting
    the data"""
# print(graph.get_edge_data('Harrow & Wealdstone', 'Kenton')['weight'])

"""For the dijkstra algorithm"""


# print(graph.edges)
# for i in graph.neighbors('Kenton'):
#    print(i)
# print(graph.get_edge_data('Kenton'))

def dijkstra(g, src):
    d = {}
    vised = {}
    heapx = []
    for vertex in g:
        if vertex == src:
            d[vertex] = 0
        else:
            d[vertex] = float('inf')
        heapq.heappush(heapx, (d[vertex], vertex))
        heapq.heapify(heapx)

    while len(heapx) != 0:
        key, u = heapq.heappop(heapx)
        vised[u] = key
        for e in g.neighbors(u):
            if e not in vised:
                weight = int(g.get_edge_data(u, e)['weight'])
                if d[u] + weight < d[e]:
                    d[e] = d[u] + weight
                    g.get_edge_data(u, e)['Sweight'] = d[e]
                    heapq.heappush(heapx, (d[e], e))

'''
For testing, dw about this
def shortest(src, des):
    path = []
    station = None
    next = des
    while next != src:
        i = float('inf')
        j=0
        print(next)
        for adjacent in graph.neighbors(next):
            if graph.get_edge_data(next, adjacent)['Sweight'] < i and i != j:
                i = graph.get_edge_data(next, adjacent)['Sweight']
                j = i
                station = adjacent
                heapq.heappush(path, (graph.get_edge_data(next, adjacent)['Sweight'], station))
        next = station
    print(heapq.heappop(path))

dijkstra(graph, 'Kenton')
shortest('Kenton', 'Bank')
'''


def shortest(src, des):
    path = []
    station = None
    next = des
    while next != src:
        i = float('inf')
        for adjacent in graph.neighbors(next):
            '''
            print(adjacent)
            print(graph.get_edge_data(next, adjacent)['Sweight'])
            '''
            if graph.get_edge_data(next, adjacent)['Sweight'] < i and adjacent not in path:
                i = graph.get_edge_data(next, adjacent)['Sweight']
                station = adjacent
        path.append(next)
        next = station
    print(path)

dijkstra(graph, 'Kenton')
shortest('Kenton', 'Bank')
