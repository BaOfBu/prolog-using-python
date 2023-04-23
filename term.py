from Utils import is_variable
abstract_name = '_/*'
class Term:
    #Constant or variable
    def __init__(self, term):
        term = term.strip()
        self.is_var = is_variable(term)
        self.term = term
    def __str__(self):
        if self.term.startswith(abstract_name):
            return '_'
        return str(self.term)
    
    def __eq__(self, cmp):
        return self.is_var == cmp.is_var and self.term == cmp.term