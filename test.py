from Utils import regex_and_or
from expr import Expr
import re
def parse(fact):
    fact = fact.replace(" ", "")
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
        lh = Expr(fact)
        rhs = []
        fact = lh.to_string()

parse("Rules(X,Y):- condition(X), condition(Y)")