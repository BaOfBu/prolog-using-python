from .Utils import rule_terms,regex_and_or
import re
from .expr import Expr

class Fact:
    def __init__ (self, fact):
        self.parse(fact)
        
    def parse(self, fact):
        fact = fact.replace(" ", "")
        self.terms = rule_terms(fact)
        #if "rules"
        if ":-" in fact: 
            #Rules(X,Y):- condition(X), condition(Y)
            index = fact.index(":-")
            predicate = Expr(fact[:index])

            replacements, pattern = regex_and_or() #get regex pattern

            rh_holder = pattern.sub(lambda x: replacements[re.escape(x.group(0))], fact[index + 2:])
            # rh_holder = condition(X)ANDcondition(Y)

            rh_holder = re.split("AND|OR", rh_holder)
            # rh_holder = ['condition(X)', 'condition(Y)']
            
            rhs = [Expr(g) for g in rh_holder] 
            rs = [i.to_string() for i in rhs]
            fact = (predicate.to_string() + ":-" + ",".join(rs))
        else: #if it's normal fact
            self.lh = Expr(fact)
            self.rhs = []
            self.fact = self.lh.to_string()
    
    ## returning string value of the fact
    def to_string(self):
        return self.fact

    def __repr__ (self) :
        return self.fact
        
    def __lt__(self, other):
        return self.lh.terms[self.lh.index] < other.lh.terms[other.lh.index]
        