from datetime import datetime, time
import doubly_linked_list as dl
import networkx as nx
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
    heapx = []  # Holds Heap within Array Format
    for vertex in g:
        if vertex == src:
            ''' As there are no values present within the Heap,
            The first Vertex will be initiated as the 'root' '''
            d[vertex] = 0
            g.nodes[vertex]['cum_wg'] = 0
        else:
            ''' All other Vertex's having a value of 'positive infinity' '''
            d[vertex] = float('inf')
        heapq.heappush(heapx, (d[vertex], vertex))
        heapq.heapify(heapx)
        ''' The heapify function is needed to retain heap order
            - Containing actions such as Bubbling up-heap or down-heap'''

    ''' This loop encompasses the 'Relaxation step' found within all Dijkstra's Algorithm's'''
    while len(heapx) != 0:
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


path = []
'''path has tuple with format: (station, line, cum_wg)
    we could make this path a stack 
    doing this would decrease the time complexity '''


def shortest(src, des):
    station = None
    next = des
    # heapq.heappush(path, (graph.nodes[src]['cum_wg'], src))
    while next != src:
        i = float('inf')
        for adjacent in graph.neighbors(next):
            if graph.nodes[adjacent]['cum_wg'] < i:
                i = graph.nodes[adjacent]['cum_wg']
                station = adjacent
        # heapq.heappush(path, (graph.nodes[next]['cum_wg'], next))
        path.append((next, graph.nodes[next]['line'], graph.nodes[next]['cum_wg']))
        next = station

    graph.nodes[next]['line'] = graph.get_edge_data(src, path[-1][0])['line']
    path.append((src, [graph.nodes[next]['line']], graph.nodes[src]['cum_wg']))
    #print(path)
    path.reverse()


cur_time = datetime.utcnow().time()

''' Takes two arguments (cur_time, time being added (in mins))
    - cur_time has multiple parameters (..seconds)
    - Turns cur_time into string + Cuts out (slicing) the not needed'''

'''     Cleans up the cur_time value to print it out as wanted (+ cum_time)     '''
def cum_time(time, add_on):
    time = str(time)[:5]
    hours = int(time[:2])
    minutes = int(time[3:])
    minutes = minutes + add_on
    if minutes // 60 > 0:
        hours = hours + (minutes // 60)
        rem_min = (minutes / 60) - (minutes // 60)
        minutes = int(60 * rem_min)

    if minutes < 10:
        minutes = '0' + str(minutes)
    final = "{}:{}".format(hours, minutes)
    return final


def spec_bakerloo():
    cond = (time(9, 00) <= cur_time <= time(16, 00)) or (time(19, 00) <= cur_time <= time(0))
    if cond:
        for vertices in dl.Bakerloo.traversing_the_list():
            graph.nodes[vertices]['cum_wg'] = (((graph.nodes[vertices]['cum_wg'] - 1) / 2) + 1)


'''final in form (station, [line], cum_wg)'''

"""Function creating the graph"""
creating_graph(graph)

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
    temp = None
    temp2 = None
    compare = None
    for i in range(len(path)):
        temp = set(path[i][1])
        if i == 1:
            compare = temp
        else:
            if compare is not None:
                if compare & temp2 == set():
                    compare = temp2 & temp
                else:
                    compare = compare & temp2
        #print(compare)
        if compare is not None:
            final.append((path[i][0], list(compare), path[i][2]))
        else:
            hanger = set(path[i][1]) & set(path[i+1][1])
            final.append((path[i][0], list(hanger), path[i][2]))
        temp2 = set(path[i][1])
    #print(final)

def display():
    path_finder()
    temp = None
    line_cur = None
    for i in final:
        if i == 0:
            temp = i
            line_cur = i[1]
            print(i[1] + ' ' + str(cur_time)[:5])
        if line_cur == i[1]:
            temp = i
            print(('\t- ' + i[0]))
        else:
            temp = i
            line_cur = i[1]
            print(str(i[1]) + ' ' + str(cum_time(cur_time, int(temp[2]))))
            print('\t- ' + i[0])
    print('Total time: {}'.format(cum_time(cur_time, int(temp[2]))))
    #print(final)



