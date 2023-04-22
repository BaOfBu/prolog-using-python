class Goal :
    def __init__ (self, fact, parent = None, domain = {}, ind = 0) :
        self.fact = fact
        self.parent = parent
        self.domain = {}
        self.domain.update(domain)
        self.ind = ind
        
    def __copy__(self):
        return Goal(self.fact, self.parent, self.domain, self.ind)    
        
    def __lt__(self, other):
        return self.fact.lh.terms[self.fact.lh.index] < other.fact.lh.terms[other.fact.lh.index]