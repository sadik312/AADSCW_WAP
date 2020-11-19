from datetime import datetime, time
import doubly_linked_list as dl
import networkx as nx
from tkinter import font
import heapq

"""Initiating a graph """
graph = nx.Graph()


def creating_graph(g):
    """The for loop below will loop for all the values in line dict created in 'doubly_linked_list.py'
        adding edges by iterating through every node in the line"""
    ''' line = list'''
    for i in dl.line:
        if dl.line[i].start_node.item[1].strip() in g.nodes():
            if i not in g.nodes[dl.line[i].start_node.item[1].strip()]['line']:
                g.nodes[dl.line[i].start_node.item[1].strip()]['line'].append(i)
        else:
            g.add_node(dl.line[i].start_node.item[1].strip(), cum_wg=None, line=[dl.line[i].start_node.item[0]])
        """For the loop the inintal node is needed witch is the start_node"""

        if dl.line[i].start_node.item[2].strip() in g.nodes():
            if i not in g.nodes[dl.line[i].start_node.item[2].strip()]['line']:
                g.nodes[dl.line[i].start_node.item[2].strip()]['line'].append(i)
        else:
            g.add_node(dl.line[i].start_node.item[2].strip(), cum_wg=None, line=[dl.line[i].start_node.item[0]])

        g.add_edge(dl.line[i].start_node.item[1].strip(), dl.line[i].start_node.item[2].strip(),
                   weight=dl.line[i].start_node.item[3], line=dl.line[i].start_node.item[0])
        n = dl.line[i].start_node

        """while loop used to iterate through all the nodes/stations in the tube line, same technique used as 
            doubly linked list to traverse the list. 
            Making a variable n and assigning it to start_node will allow to traverse through the list"""
        while n is not None:
            if n.item[1].strip() in g.nodes():
                if i not in g.nodes[n.item[1].strip()]['line']:
                    g.nodes[n.item[1].strip()]['line'].append(i)
            else:
                g.add_node(n.item[1].strip(), cum_wg=None, line=[n.item[0]])

            if n.item[2].strip() in g.nodes():
                if i not in g.nodes[n.item[2].strip()]['line']:
                    g.nodes[n.item[2].strip()]['line'].append(i)
            else:
                g.add_node(n.item[2].strip(), cum_wg=None, line=[n.item[0]])
            g.add_edge(n.item[1].strip(), n.item[2].strip(), weight=n.item[3], line=n.item[0])
            n = n.next


"""This is how the data is stored as list in the nodes for each tube line, obviously print is not necessary"""
# print(dl.Bakerloo.traversing_the_list())

"""This is the format to extract the data from the graph, obvuiously print is not necessary when just using/redirecting
    the data"""
# print(graph.get_edge_data('Harrow & Wealdstone', 'Kenton')['weight'])

"""For the dijkstra algorithm"""


def dijkstra(g, src):
    d = {}
    vised = {}  # Maps the Visited Vertices to its 'distance to vertex' value
    pred = {}
    heapx = []  # Holds Heap within Array Format
    for vertex in g:
        pred[vertex] = vertex
        if vertex == src:
            ''' As there are no values present within the Heap,
            The first Vertex will be initiated as the 'root' '''
            d[vertex] = 0
            g.nodes[vertex]['cum_wg'] = 0
            heapq.heappush(heapx, (d[vertex], vertex))
        else:
            ''' All other Vertex's having a value of 'positive infinity' '''
            d[vertex] = float('inf')
        heapq.heappush(heapx, (d[vertex], vertex))
        heapq.heapify(heapx)
        ''' The heapify function is needed to retain heap order
            - Containing actions such as Bubbling up-heap or down-heap'''

    ''' This loop encompasses the 'Relaxation step' found within all Dijkstra's Algorithm's'''
    while heapx:
        key, u = heapq.heappop(heapx)
        vised[u] = key
        ''' For all the outgoing/neighbouring edges '''
        for e in g.neighbors(u):
            if e not in vised:
                weight = int(g.get_edge_data(u, e)['weight'])
                ''' Relaxation step on edges (e, u)'''
                '''is the accumulated value better than d[e]'''
                if d[u] + weight < d[e]:
                    d[e] = d[u] + weight + 1
                    g.nodes[e]['cum_wg'] = d[e]
                    ''' Pushing updated distances onto heap'''
                    heapq.heappush(heapx, (d[e], e))
                    pred[e] = u
    return pred


path = []
'''path has tuple with format: (station, line, cum_wg)
    we could make this path a stack 
    doing this would decrease the time complexity '''


def shortest2(g, s, d, time):
    pred = dijkstra(g, s)
    spec_bakerloo(time)
    node = d
    short = []
    while True:
        short.append((node, graph.nodes[node]['line'], graph.nodes[node]['cum_wg']))
        if node == pred[node]:
            break
        node = pred[node]
    return short[::-1]


cur_time = datetime.utcnow().time()
print(cur_time)
''' Takes two arguments (cur_time, time being added (in mins))
    - cur_time has multiple parameters (..seconds)
    - Turns cur_time into string + Cuts out (slicing) the not needed'''

'''     Cleans up the cur_time value to print it out as wanted (+ cum_time)     '''
def cum_time(time, add_on):
    time = str(time)[:5]
    hours = int(time[:2])
    minutes = int(time[3:5])
    minutes = minutes + add_on
    if minutes // 60 > 0:
        hours = hours + (minutes // 60)
        rem_min = (minutes / 60) - (minutes // 60)
        minutes = int(60 * rem_min)

    if minutes < 10:
        minutes = '0' + str(minutes)
    final_form = "{}:{}".format(hours, int(minutes))
    return final_form


def spec_bakerloo(h):
    a = 9 <= h < 16 or 19 <= h < 24
    cond = (time(9, 00) <= cur_time <= time(16, 00)) or (time(19, 00) <= cur_time <= time(0))
    if cond or a:
        for vertices in dl.Bakerloo.traversing_the_list():
            graph.nodes[vertices]['cum_wg'] = (((graph.nodes[vertices]['cum_wg'] - 1) / 2) + 1)


'''final in form (station, [line], cum_wg)'''

final = []

''' final = holds final printable values as a tuple with format (station,[lines], cum_time)
    - final is the updated version of "path = []" '''

''' path_finder = 
    Finds all the tube lines that could be taken from one station to another 
        - uses sets 
        (path holds all the lines available to take from the station)
        - final holds all the lines that could be taken between src and destination
        - final is called from the output function (GUI)'''

def path_finder():
    compare = None
    for i in path:
        if i == path[0]:
            compare = set(i[1]) & set(path[1][1])
        elif i == path[-1]:
            pass
        else:
            compare = set(i[1]) & set(path[path.index(i) + 1][1])
        final.append((i[0], list(compare), i[2]))


def display(time):
    cur_time = time
    path_finder()
    temp = final[1]
    line_cur = None

    for i in final:

        if i[1] == temp:
            if i == final[0]:
                #print("\033[1m" + i[0] + ' {}'.format(cur_time[:5]) + "\033[0m")
                #print('\t{}'.format(str(i[1])))
                pass
            elif i == final[-1]:
                print("\033[1m" + i[0] + "\033[0m")
                print("\033[1m" + 'Final time:{}'.format(cum_time(cur_time, i[2])) + "\033[0m")
            else:
                lines = len(i[1])
                print('\t  ' + "\033[1m" + '|' * lines + "\033[0m" + '-{}'.format(i[0]))
        else:
            print("\033[1m" + i[0] + "\033[0m")
            print('\t{}\t{}'.format(str(i[1]), cum_time(cur_time, i[2])))

        temp = i[1]


"""Function creating the graph"""
creating_graph(graph)


