import networkx as nx
import doubly_linked_list as dl


"""Initiating a graph """
graph = nx.Graph()


def creating_graph(g):
    """The for loop below will loop for all the values in line dict created in 'doubly_linked_list.py'
        adding edges by iterating through every node in the line"""
    for i in dl.line:

        """For the loop the inintal node is needed witch is the start_node"""

        g.add_edge(dl.line[i].start_node.item[1], dl.line[i].start_node.item[2],
                   weight=dl.line[i].start_node.item[3], line=dl.line[i].start_node.item[0])
        n = dl.line[i].start_node

        """while loop used to iterate through all the nodes/stations in the tube line, same technique used as 
            doubly linked list to traverse the list. 
            Making a variable n and assigning it to start_node will allow to traverse through the list"""
        while n is not None:
            if n.next is None:
                break
            else:

                g.add_edge(n.item[1], n.item[2], weight=n.item[3], line=n.item[0])
                n = n.next


"""Function creating the graph"""
creating_graph(graph)

"""This is how the data is stored as list in the nodes for each tube line, obviously print is not necessary"""
# print(dl.Bakerloo.traversing_the_list())

"""This is the format to extract the data from the graph, obvuiously print is not necessary when just using/redirecting
    the data"""
# print(graph.get_edge_data('Harrow & Wealdstone', 'Kenton'))

"""For the dijkstra algorithm"""


def dijkstra():
    pass
