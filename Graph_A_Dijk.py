
import doubly_linked_list as dl
import networkx as nx
import heapq

"""Initiating a graph """
graph = nx.Graph()


def creating_graph(g):
	"""The for loop below will loop for all the values in line dict created in 'doubly_linked_list.py'
		adding edges by iterating through every node in the line"""
	for i in dl.line:

		"""For the loop the inintal node is needed witch is the start_node"""
		g.add_node(dl.line[i].start_node.item[1].strip(), cum_wg=None, line=dl.line[i].start_node.item[0])
		g.add_node(dl.line[i].start_node.item[2].strip(), cum_wg=None, line=dl.line[i].start_node.item[0])
		g.add_edge(dl.line[i].start_node.item[1].strip(), dl.line[i].start_node.item[2].strip(),
				   weight=dl.line[i].start_node.item[3], line=dl.line[i].start_node.item[0])
		n = dl.line[i].start_node

		"""while loop used to iterate through all the nodes/stations in the tube line, same technique used as 
			doubly linked list to traverse the list. 
			Making a variable n and assigning it to start_node will allow to traverse through the list"""
		while n is not None:
			if n.next is None:
				break
			else:
				g.add_node(n.item[1].strip(), cum_wg=None, line=n.item[0])
				g.add_node(n.item[2].strip(), cum_wg=None, line=n.item[0])
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
					d[e] = d[u] + weight
					g.nodes[e]['cum_wg'] = d[e]
					''' Pushing updated distances onto heap'''
					heapq.heappush(heapx, (d[e], e))


path = []
'''path has tuple with format: (station, line, cum_wg)'''


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
	print(path)
	path.append((src, graph.nodes[next]['line'], graph.nodes[src]['cum_wg']))


def display():
	temp = None
	while len(path) != 0:
		if temp is None:
			temp = path[-1]
			print(path[-1][1])
			print('\t- ' + path.pop(-1)[0])
		if temp[1] != path[-1][1]:
			if temp[2] is None:
				pass
			else:
				print(str(path[-1][1]) + ' ' + str(temp[2]))
			temp = path[-1]
			print('\t- ' + path.pop(-1)[0])
		else:
			temp = path[-1]
			print('\t- ' + path.pop(-1)[0])
	print('Total time: {}'.format(temp[2]))


"""Function creating the graph"""
creating_graph(graph)