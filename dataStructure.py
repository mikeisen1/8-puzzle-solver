import heapq

#This class is a priority queue that relies on a function for ordering. It uses
    #heapq due to its efficient placing of a new element when it is pushed on to
    #the queue.
class PriorityQueue:
    #creating the priority queue. self.function is the function that performs
        #the ordering. It should be an n-tuple or list of functions, so that
        #ties can be broken if the intial function priority value is the same
        #for two elements.
    def __init__(self, function):
        self.lst = [] #actual queue, which is represented as a heapq
        self.function = function
        
    #checking if the queue (self.lst) is empty
    def isEmpty(self):
        return len(self.lst) == 0

    #pushing an element onto the queue; positioning is based on its priority
        #value.
    def push(self, element):
        #the map function applies each function in self.function to the element
            #being pushed onto the queue. It then returns a map object.
        order = map(lambda x: x(element), self.function)
        #we must convert the map object (order) to a list so we can use the
            #values to determine the position of element in the queue
        insertedElement = (list(order), element)
        heapq.heappush(self.lst, insertedElement)

    #removes the first element, which has the lowest priority value.
    def pop(self):
        #we only care about the element being removed. For the 8-puzzle
            #problem, the actual cost from start state to current state is part
            #of poppedElement, which will be a tuple. However, the priority
            #values could be returned in some situations (in which case, the _
            #would become some variable name and we could determine how many of
            #the priority values we would want to return).
        (_, poppedElement) = heapq.heappop(self.lst)
        return poppedElement
