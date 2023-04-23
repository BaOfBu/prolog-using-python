class Rule:
    #Define a rule with left and right hand side are Conjunction of statements
    def __init__(self, lhs, rhs = None):
        self.lhs = lhs
        self.rhs = rhs
        self.difference = []
        self.supported = [[] for _ in range(len(rhs.list_of_statements))]
    def __str__(self):
        return str(self.lhs) + ' <- ' + str(self.rhs)
    def split(self):
        from statement import Statement
        list_of_new_rules = []
        new_conj = self.rhs.split()
        for conj in new_conj:
            list_of_new_rules.append(Rule(Statement(list_of_terms=self.lhs.list_of_terms,predicate = self.lhs.predicate, negative = self.lhs.negative),conj))
        return list_of_new_rules
    def get_supported_fact(self,list_of_facts):
        for index in range(len(self.rhs.list_of_statements)):
            for fact in list_of_facts:
                if fact.is_unificable(self.rhs.list_of_statements[index]):
                    self.supported[index].append(fact)
    def standardlize_variable(self):
        bind_dict = {}
        bind_dict = self.lhs.standardlize_variable(bind_dict=bind_dict)
        for statement in self.rhs.list_of_statements:
            bind_dict = statement.standardlize_variable(bind_dict=bind_dict)
        for difference in self.difference:
            difference[0].term = bind_dict[difference[0].term]
            difference[1].term = bind_dict[difference[1].term]
    def list_supported_facts(self):
        from statement import Statement
        support_list = [[]]
        for fact_list in self.supported:
            if len(fact_list) == 0:
                return []
            else:
                new = []
                for fact in fact_list:
                    for sublist in support_list:
                        new_sublist = []
                        for statement in sublist:
                            new_sublist.append(Statement(predicate= statement.predicate, negative = statement.negative,\
                            list_of_terms = statement.list_of_terms))
                        new_sublist.append(fact)
                        new.append(new_sublist)
                support_list = new
        return support_list
    def check_difference(self, binding):
        differ = True
        for difference in self.difference:
            if binding.bind(difference[0]) == binding.bind(difference[1]):
                differ = False
                break
        return differ
    def eliminate_difference(self):
        from term import Term
        for index,statement in enumerate(self.rhs.list_of_statements):
            if statement.predicate =='\=':
                self.difference.append([Term(statement.list_of_terms[0].term),Term(statement.list_of_terms[1].term)])
                del self.rhs.list_of_statements[index]
                del self.supported[index]
