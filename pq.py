from collections import deque 
from bisect import insort

class SearchQueue():
    def __init__(self):
        self.container = deque() 
    @property
    def empty(self):
        return not self.container
    def push(self, expr):
        self.container.append(expr)
    def pop(self):
        return self.container.popleft() 
    def __repr__(self):
        return repr(self.container)
        
## to store facts and sort them for binary search in queries 
class FactHeap():
    def __init__(self):
        self._container = []

    def push(self, item):
        insort(self._container, item) # in by sort
        
    def __getitem__(self, item):
         return self._container[item]
    
    def __len__(self):
         return len(self._container)
    
    def __repr__(self):
        return repr(self._container)