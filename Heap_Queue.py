class PriorityQueueBase:
    ''' Composition design pattern - assured that each element
        remained paired with its associated count in our
        primary data structure'''
    class Item:
        __slots__ = 'key', 'value'  #storing items internally as pairs

        def __init__(self, k, v):
            self.key = k
            self.value = v

        def __it__(self, other):
            return self.key < other.key #compare items based on their keys

    def is_empty(self):
        return len(self) == 0 #return True if priority queue is empty

class HeapPriorityQueue(PriorityQueueBase):
    ''' NONPUBLIC BEHAVIOURS'''
    def parent(self, j):
        return (j-1)//2 #Inverse way of plotting children

    def left(self, j):
        return (2*j) + 1 #Plotting Left Child

    def right(self, j):
        return (2*j) + 2 #Plotting right child

    def has_left(self, j):
        return self.left(j) < len(self.data)

    def has_right(self, j):
        return self.right(j) < len(self.data)

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def upheap(self, j): # 'bubbling up'
        parent = self.parent(j)
        if j > 0 and self.data[j] < self.data[parent]:
            # j is not the parent and value is smaller than parent value
            self.swap(j, parent) #call upon '.swap'
            self.upheap(parent) #recursively call itself until heap order is met

    def downheap(self, j): # 'bubbling down'
        if self.has_left(j): #check if left node is present
            left = self.left(j) #value of left child = left
            small_child = left # although right maybe smaller
            if self.has_right(j): #check if right child is present
                right = self.right(j)
                if self.data[right] < self.data[left]: #if right is smaller
                    small_child = right # assign right as the smaller child
            if self.data[small_child] < self.data[j]: # if the value of small child is smaller than 'j'
                self.swap(j, small_child)  #swap values
                self.downheap(small_child) #recursively call itself until heap order is met

    '''PUBLIC BEHAVIOURS'''

    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def add(self, key, value):
        self.data.append(self.Item(key, value))
        self.upheap(len(self.data) - 1)

    def min(self):
        if self.is_empty():
            raise Exception('Priority Queue is empty')
        item = self.data[0] #root node
        return(item.key, item.value)

    def remove_min(self):
        if self.is_empty():
            raise Exception('Priority Queue is empty')
        self.swap(0, len(self.data) - 1)
        item = self.data.pop()
        self.downheap(0)
        return (item.key, item.value)


class AdaptableHeapPriorityQueue(HeapPriorityQueue): #subclass of HeapPriorityQueue
    '''A locator-based priority queue implemented with a binary heap.
        - When operations are performed, and items are relocated
          within our structure, we reposition the locator instances
          within the list.
        - updating the third field of each locator to reflect its new index'''

    class Locator(HeapPriorityQueue.Item):
        ''' The list is a sequence of references to locator instance'''
        __slots__ = '_index' #Adding index as an initial field

        def __init__(self, k, v, j):# key, value, index
            ''' 3rd element of each locator instance corresponds to the index
                of the item within the array'''
            super().__init__(k,v)
            self._index = j

    def swap(self, i, j):
        ''' Overrides swap to record new indices'''
        super().swap(i, j)
        self.data[i]._index = i
        self.data[j]._index = j

    def bubble(self, j):
        ''' Manages the reinstatement of the heap-order property when
        a key has changed at an arbitrary position within the heap '''
        if j > 0 and self.data[j] < self.data[self.parent(j)]:
            ''' Depending if the given locator has a parent with a smaller key...'''
            self.upheap(j)
        else:
            self.downheap(j)

    def add(self, key, value):
        ''' The Locator instance is utilised here rather than the original item instance'''
        token = self.Locator(key, value, len(self.data))
        self.data.append(token)
        self.upheap(len(self.data) - 1)
        return token

    def update(self, loc, newkey, newval):
        ''' Performs a more robust checking of validity of a locator
            compared to prior implementations'''
        j = loc._index
        if not (0 <= j < len(self) and self.data[j] is loc):
            raise ValueError("Invalid Locator")
        loc.key = newkey
        loc.value = newval
        self.bubble(j)

    def remove(self, loc):
        ''' Remove and return the key value (k,v) pair identified by Locator loc'''
        j = loc._index
        if not (0 <= j < len(self) and self.data[j] is loc):
            raise ValueError("Invalid Locator")
        if j == len(self) - 1: #if item is at the last position
            self.data.pop()
        else:
            self.swap(j, len(self) - 1)
            self.data.pop()
            self.bubble(j)
        return(loc.key, loc.value)

