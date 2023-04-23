from Utils import is_variable

class Binding:
    def __init__(self):
        self.binding_dict = {}
        self.is_fail = False
    def add_new_binding(self, key, value):
        #Key and value is term
        self.binding_dict[key.term] = value.term
    def already_has(self, key):
        return key.term in self.binding_dict
    def bind(self,x):

        from conDisjunction import Conjunction, Disjunction
        from statement import Statement
        from term import Term
        
        if isinstance(x,Term):
            if x.term in self.binding_dict:
                return Term(self.binding_dict[x.term])
            else:
                return x
        elif isinstance(x,Statement):
            list_of_terms = []
            for term in x.list_of_terms:
                list_of_terms.append(self.bind(term))
            return Statement(list_of_terms=list_of_terms,predicate=x.predicate, negative = x.negative)
        elif isinstance(x,Conjunction):
            list_of_statements = []
            for statement in x.list_of_statements:
                list_of_statements.append(self.bind(statement))
            return Conjunction(list_of_statements=list_of_statements)
        elif isinstance(x,Disjunction):
            list_of_statements = []
            for statement in x.list_of_statements:
                list_of_statements.append(self.bind(statement))
            return Disjunction(list_of_statements=list_of_statements)
    def merge(self,obj):
        res = Binding()
        if self.is_fail or obj.is_fail:
            res.is_fail = True
        else:
            is_fail = False
            for key in self.binding_dict.keys():
                term = self.binding_dict[key]
                while is_variable(term) and term in self.binding_dict:
                    term = self.binding_dict[term]
                while is_variable(term) and term in obj.binding_dict:
                    term = obj.binding_dict[term]
                if key in res.binding_dict and term != res.binding_dict[key]:
                    is_fail =True
                    break
                res.binding_dict[key] = term
            for key in obj.binding_dict.keys():
                term = obj.binding_dict[key]
                while is_variable(term) and term in obj.binding_dict:
                    term = obj.binding_dict[term]
                while is_variable(term) and term in self.binding_dict:
                    term = self.binding_dict[term]
                if key in res.binding_dict and term != res.binding_dict[key]:
                    is_fail =True
                    break
                res.binding_dict[key] = term
            res.is_fail = is_fail
        return res
    
class ListOfBinding:
    def __init__(self, binding_list = []):
        if isinstance(binding_list,Binding):
            binding_list = [binding_list]
        self.binding_list = binding_list
    def merge_or(self, obj):
        if isinstance(obj,Binding):
            obj = ListOfBinding(binding_list=[obj])
        new_binding_list = []
        for binding in self.binding_list:
            if not binding.is_fail:
                new_binding_list.append(binding)
        for binding in obj.binding_list:
            if not binding.is_fail:
                new_binding_list.append(binding)
        return ListOfBinding(new_binding_list)
    def merge_and(self,obj):
        if isinstance(obj,Binding):
            obj = ListOfBinding(binding_list=[obj])
        new_binding_list = []
        for self_bind in self.binding_list:
            for obj_bind in obj.binding_list:
                if not self_bind.is_fail and not obj_bind.is_fail:
                    new_bind = self_bind.merge(obj_bind)
                    if not new_bind.is_fail:
                        new_binding_list.append(new_bind)
        return ListOfBinding(new_binding_list)