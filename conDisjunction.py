from statement import Statement

class Conjunction:
    #Conjunction of statements
    def __init__(self, list_of_statements = []):
        self.list_of_statements = []
        for statement in list_of_statements:
            if isinstance(statement,Statement):
                self.list_of_statements.append(Statement(predicate = statement.predicate,\
                list_of_terms = statement.list_of_terms, negative = statement.negative))
            elif isinstance(statement,Conjunction):
                self.list_of_statements.append(Conjunction(statement.list_of_statements))
            elif isinstance(statement,Disjunction):
                self.list_of_statements.append(Disjunction(statement.list_of_statements))

    def negate(self):
        new_statements = []
        for statement in self.list_of_statements:
            new_statements.append(statement.negate())
        return Disjunction(new_statements)
    
    def add_new_statement(self, statement):
        self.list_of_statements.append(statement)

    def simplify(self):
        index = 0
        while index < len(self.list_of_statements):
            if isinstance(self.list_of_statements[index],Conjunction):
                self.list_of_statements[index].simplify()
                l = len(self.list_of_statements[index].list_of_statements)
                for i,statement in enumerate(self.list_of_statements[index].list_of_statements):
                    self.list_of_statements.insert(index + i + 1,statement)
                del self.list_of_statements[index]
                index += l-1
            elif isinstance(self.list_of_statements[index],Disjunction):
                self.list_of_statements[index].simplify()
            index+=1

    def __str__(self):
        output = '('
        for statement in self.list_of_statements:
            output += str(statement)+' & '
        return output[:-3]+')'
    
    def __eq__(self,cmp):
        if len(self.list_of_statements) != len(cmp.list_of_statements):
            return False
        else:
            equal = True
            for i in range(len(self.list_of_statements)):
                if not self.list_of_statements[i] == cmp.list_of_statements[i]:
                    equal = False
                    break
            return equal
        
    def split(self):
        list_of_new_conjunction = []
        has_disjunction = False
        for index,statement in enumerate(self.list_of_statements):
            if isinstance(statement,Disjunction):
                has_disjunction = True
                for statement_dis in statement.list_of_statements:
                    new_list = self.list_of_statements.copy()
                    new_list[index] = statement_dis
                    new_conj = Conjunction(new_list)
                    new_conj.simplify()
                    list_of_new_conjunction = list_of_new_conjunction + new_conj.split()
                break
        if has_disjunction == False:
            list_of_new_conjunction.append(self)
        return list_of_new_conjunction
    
    def get_list_var(self):
        res = []
        for statement in self.list_of_statements:
            if isinstance(statement,Statement):
                res = list(set(res + statement.get_variable_list()))
            else:
                res = list(set(res + statement.get_list_var()))
        return res
    
    def standardize_abstract_variable(self):
        for statement in self.list_of_statements:
            statement.standardize_abstract_variable()

class Disjunction:
    #Disjunction of statement
    def __init__(self, list_of_statements = []):        
        self.list_of_statements = []
        for statement in list_of_statements:
            if isinstance(statement,Statement):
                self.list_of_statements.append(Statement(predicate = statement.predicate,\
                list_of_terms = statement.list_of_terms, negative = statement.negative))
            elif isinstance(statement,Conjunction):
                self.list_of_statements.append(Conjunction(statement.list_of_statements))
            elif isinstance(statement,Disjunction):
                self.list_of_statements.append(Disjunction(statement.list_of_statements))

    def negate(self):
        new_statements = []
        for statement in self.list_of_statements:
            new_statements.append(statement.negate())
        return Conjunction(new_statements)
    
    def add_new_statement(self, statement):
        self.list_of_statements.append(statement)

    def __str__(self):
        output = '('
        for statement in self.list_of_statements:
            output += str(statement)+' ; '
        return output[:-3]+')'
    
    def simplify(self):
        index = 0
        while index < len(self.list_of_statements):
            if isinstance(self.list_of_statements[index],Disjunction):
                self.list_of_statements[index].simplify()
                l = len(self.list_of_statements[index].list_of_statements)
                for i,statement in enumerate(self.list_of_statements[index].list_of_statements):
                    self.list_of_statements.insert(index + i + 1,statement)
                del self.list_of_statements[index]
                index += l-1
            elif isinstance(self.list_of_statements[index],Conjunction):
                self.list_of_statements[index].simplify()
            index+=1

    def __eq__(self,cmp):
        if len(self.list_of_statements) != len(cmp.list_of_statements):
            return False
        else:
            equal = True
            for i in range(len(self.list_of_statements)):
                if not self.list_of_statements[i] == cmp.list_of_statements[i]:
                    equal = False
                    break
            return equal
        
    def get_list_var(self):
        res = []
        for statement in self.list_of_statements:
            if isinstance(statement,Statement):
                res = list(set(res + statement.get_variable_list()))
            else:
                res = list(set(res + statement.get_list_var()))
        return res
    
    def standardize_abstract_variable(self):
        for statement in self.list_of_statements:
            statement.standardize_abstract_variable()
