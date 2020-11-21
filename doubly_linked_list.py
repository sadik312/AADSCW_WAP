import csv

'''Node that will hold data and pointer for the linkled list. Initially the pointer are set to None 
   and are changed as new nodes are added. 'Prev' and 'next' for previous and next pointer respectively'''


class Node:
    def __init__(self, data):
        self.item = data
        self.prev = None
        self.next = None


'''Class for creating a double linked list, which hold methods to traverse, add, remove and get data from the 
    linked list.'''


class Doubly_linked_List:
    """The starting node is start_node which initially is assigned as None when the list is empty"""

    def __init__(self):
        self.start_node = None

    """ Inserting at the beginning would mean creating a new node and assigning that node to the start_node. 
    The pointer does not need altering as it has no adjacent nodes to point"""

    def inserting_at_start(self, data):
        """Creating a new Node called new_node using the class Node and data witch will be passed on as an argument
        when this method is called"""
        new_node = Node(data)
        new_node.next = self.start_node
        self.start_node = new_node
        """At the end we assign the new_node to start_node making it the start node"""

    """Inserting at end would mean creating a node with its data and changing the .next pointer of currently last node 
    to point to the location of the new node created. 
    The .prev pointer for new node created should also be assigned to point to the last previous node"""

    def inserting_at_end(self, data):

        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
            return
        n = self.start_node

        '''Continually traversing the list with while loop to reach the last node, where its .next pointer 
            is None'''

        while n.next is not None:
            n = n.next
        new_node = Node(data)
        n.next = new_node
        new_node.prev = n

    '''Inserting after a node would require a parameter (x) which is the node that we will insert after. 
    The .next pointer of .x would need to point to the node being inserted. The .prev pointer of the node after node x
    has to also point to the new node
    For the new node, .next points to the node after x and .prev points to the x '''

    def inserting_after_node(self, x, data):
        n = self.start_node
        while n is not None:
            if n.item == x:  # Finding node x
                break
            n = n.next
        if n is None:
            print("The item does not exist in the list")
        else:
            new_node = Node(data)
            new_node.next = n.next
            new_node.prev = n
            if n.next is not None:  # This is when node being inserted happens to be at the end of the list
                n.next.prev = new_node
            n.next = new_node

    def inserting_before_node(self, x, data):
        if self.start_node is None:
            print("the list is empty")
        else:
            n = self.start_node
            while n is not None:
                if n.item == x:
                    break
                n = n.next
            if n is None:
                print("The item does note exits in the list")
            else:
                new_node = Node(data)
                new_node.next = n
                new_node.prev = n.prev
                if n.prev is not None:
                    n.prev.next = new_node
                n.prev = new_node

    def traversing_the_list(self):
        tracker = 0
        stations = []
        if self.start_node is None:
            print("the list is empty")
            stations.append(n.item[1].strip())
        else:
            n = self.start_node
            while n is not None:
                tracker = tracker + 1
                stations.append(n.item[1].strip())
                if n.next is None:
                    stations.append(n.item[2].strip())
                n = n.next

            return stations

    def deleting_at_start(self):
        if self.start_node is None:
            print("the list is empty")
        if self.start_node.next is None:
            self.start_node = None
            return
        self.start_node = self.start_node.next
        self.start_node.prev = None

    def deleting_at_end(self):
        if self.start_node is None:
            print("the list is empty")
        if self.start_node.prev is None:
            self.start_node = None
            return
        self.start_node = self.start_node.prev
        self.start_node.next = None

    def deleting_an_item(self, x, data):
        if self.start_node is None:
            print("the list is empty")

        if self.start_node.next is None:
            if self.start_node.item == x:
                self.start_node = None
            else:
                print("Item is found")

        if self.start_node.item == x:
            self.start_node = self.start_node.next
            self.start_node.prev = None

        n = self.start_node
        while n is not None:
            if n.item == x:
                break
            n = n.next
        if n.next is not None:
            n.next.prev = n.prev
            n.prev.next = n.next
        else:
            if n.item == x:
                n.prev.next = None
            else:
                print("Item not found")

    def last_element(self):
        n = self.start_node
        while n is not None:
            if n.next is None:
                return n.item
            n = n.next
    def next_item(self, station):
        n = self.start_node
        while n is not None:
            if n.item == station:  # Finding node x
                break
            n = n.next
        return n.next.item

"""
Creating instances of linked list for each line
"""

Bakerloo = Doubly_linked_List()
Central = Doubly_linked_List()
Circle = Doubly_linked_List()
District = Doubly_linked_List()
Hammersmith_A_City = Doubly_linked_List()
Jubilee = Doubly_linked_List()
Metropolitan = Doubly_linked_List()
Northern = Doubly_linked_List()
Piccadilly = Doubly_linked_List()
Victoria = Doubly_linked_List()
Waterloo_A_City = Doubly_linked_List()

"""Dict holding the line instances of classes for its string representation"""
line = {'Bakerloo': Bakerloo, 'Central': Central,
        'Circle': Circle, 'District': District,
        'Hammersmith & City': Hammersmith_A_City,
        'Jubilee': Jubilee, 'Metropolitan': Metropolitan,
        'Northern': Northern, 'Piccadilly': Piccadilly,
        'Victoria': Victoria, 'Waterloo & City': Waterloo_A_City}

'''This function reads the excel file in csv format and creates classes and nodes accordingly.
    It relies on the list dictonary to get the individual tube lines and assign stations to them
'''


def create(file):
    f = open(file)
    reader = csv.reader(f, delimiter=',')
    _temp = next(reader)
    '''The temp variable is needed to keep track of the previous line read, iniitally it is set as the first line.
        previous read line is needed to compare with the current line and add the last station for each tube line'''
    for row in reader:
        if row[3] != '':
            """This is necessary to check if start node is None or not as None means the list is empty.
            Inserting_at_start should be used to add the node. If start_node is not None then node added to the end."""
            if line[row[0]].start_node is None:
                line[row[0]].inserting_at_start(row)
            else:
                line[row[0]].inserting_at_end(row)
            _cond = (_temp[2] != row[1] and _temp[2] != '')
            """Cond is used to get resolve either TRUE or FALSE for the next if statement """
            if _cond:
                pass
            _temp = row
            """Assigning the current row to _temp"""
    f.close()

'''calling the function to initiate'''
create('London Underground data.csv')
