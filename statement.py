import globals

class Statement:
    def __init__(self, list_of_terms = [], predicate = '', negative = False):
        from term import Term
        self.list_of_terms = []
        for term in list_of_terms:
            self.list_of_terms.append(Term(term.term))
        self.negative = negative
        if predicate.startswith('\+'):
            predicate = predicate[2:]
            self.negative = not self.negative
        self.predicate = predicate
        
    def negate(self):
        return Statement(list_of_terms=self.list_of_terms, predicate=self.predicate, negative = not self.negative)
    
    def add_new_term(self,term):
        self.list_of_terms.append(term)

    def simplify(self):
        from conDisjunction import Conjunction
        if len(self.list_of_terms) == 1 and isinstance(self.list_of_terms[0],Conjunction):
            self.list_of_terms = self.list_of_terms[0].list_of_statements

    def __str__(self):
        output = self.predicate + '('
        for term in self.list_of_terms:
            output += str(term) + ', '
        output = output[:-2]+')'
        return output

    def __eq__(self, cmp):
        equal = True
        if len(self.list_of_terms) != len(cmp.list_of_terms):
            return False
        else:
            for i in range(len(self.list_of_terms)):
                if not self.list_of_terms[i] == cmp.list_of_terms[i]:
                    equal = False
                    break
        return self.predicate == cmp.predicate and self.negative == cmp.negative and equal
    
    def is_identical(self,cmp):
        equal = True
        if len(self.list_of_terms) != len(cmp.list_of_terms):
            return False
        else:
            for i in range(len(self.list_of_terms)):
                if self.list_of_terms[i].is_var == False and cmp.list_of_terms[i].is_var == False \
                and not self.list_of_terms[i] == cmp.list_of_terms[i]:
                    equal = False
                    break
        return self.predicate == cmp.predicate and self.negative == cmp.negative and equal
    
    def is_unifiable(self,obj):
        return self.predicate == obj.predicate and self.negative == obj.negative and \
        len(self.list_of_terms) == len(obj.list_of_terms)
    
    def is_opposite(self,obj):
        return self.predicate == obj.predicate and self.negative != obj.negative and \
        len(self.list_of_terms) == len(obj.list_of_terms)
    
    def standardize_variable(self,bind_dict = {}):
        #global name_identity
        from term import Term
        for index, term in enumerate(self.list_of_terms):
            if term.is_var:
                if not term.term in bind_dict:
                    globals.name_identity += 1
                    bind_dict[term.term] = '_' + str(globals.name_identity)
                self.list_of_terms[index] = Term(term = bind_dict[term.term])
        return bind_dict
    
    def standardize_abstract_variable(self):
        global abstract_var
        global abstract_name
        for term in self.list_of_terms:
            if term.term == '_':
                term.term = abstract_name + str(abstract_var)
                abstract_var+=1

    def get_variable_list(self):
        res = []
        for term in self.list_of_terms:
            if term.is_var:
                res.append(term.term)
        return res
