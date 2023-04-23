from rule import Rule
from statement import Statement
from conDisjunction import Conjunction, Disjunction
from binding import Binding, ListOfBinding
from cnf import CNF
from term import Term
from Utils import process_string, unify

class KnowledgeBase:
    #Knowledge Base with set of rules (facts are rules without right hand side)
    def __init__(self):
        self.list_of_rules = []
        self.list_of_facts = []
        self.list_of_query = []
    def input_from_file(self, filename):
        with open(filename,'r') as f:
            for line in f:
                line = line.strip()
                line = line.replace(" ","")
                line = line.replace("),",")&")
                if line.startswith('?-'):
                    line = line[2:].strip()
                    query = process_string(line)
                    query.standardlize_abstract_variable()
                    self.list_of_query.append(query)
                elif not line.startswith('%') and line != '':
                    expr = line.split(':-')
                    #print(expr[0])
                    new_rule = None
                    if len(expr) == 2:
                        new_rule = Rule(process_string(expr[0]).list_of_statements[0], process_string(expr[1]))
                        self.list_of_rules.append(new_rule)
                    elif len(expr)==1:
                        new_rule = process_string(expr[0]).list_of_statements[0]
                        new_rule.standardlize_variable()
                        self.list_of_facts.append(new_rule)
        # Split rule
        list_of_new_rule = []
        for rule in self.list_of_rules:
            list_of_new_rule = list_of_new_rule + rule.split()
        self.list_of_rules = list_of_new_rule
        # Get supported fact for each rule
        for rule in self.list_of_rules:
            rule.eliminate_difference()
            rule.get_supported_fact(self.list_of_facts)
            rule.standardlize_variable()
    
    def __str__(self):
        output = ''
        for rule in self.list_of_rules:
            output+= str(rule) + '\n'
        for fact in self.list_of_facts:
            output+= str(fact) + '\n'
        return output
    def forward_chaining_ask(self, goal):
        list_of_binding = None
        if isinstance(goal,Statement):
            return self.forward_chaining(goal)
        elif isinstance(goal,Conjunction):
            for subgoal in goal.list_of_statements:
                if list_of_binding!=None:
                    list_of_binding = list_of_binding.merge_and(self.forward_chaining_ask(subgoal))
                else:
                    list_of_binding = self.forward_chaining_ask(subgoal)
        elif isinstance(goal,Disjunction):
            for subgoal in goal.list_of_statements:
                if list_of_binding!=None:
                    list_of_binding = list_of_binding.merge_or(self.forward_chaining_ask(subgoal))
                else:
                    list_of_binding = self.forward_chaining_ask(subgoal)
        return list_of_binding
    def forward_chaining(self,goal):
        global not_have_anything_new
        list_of_binding = ListOfBinding([])
        for fact in self.list_of_facts:
            if fact.is_unificable(goal):
                binding = Binding()
                unify(fact,goal,binding)
                if not binding.is_fail:
                    list_of_binding = list_of_binding.merge_or(binding)
        if not not_have_anything_new:
            while True:
                new = []
                for rule in self.list_of_rules:
                    supported_facts_list = rule.list_supported_facts()
                    if len(supported_facts_list)==0:
                        continue
                    for fact_list in supported_facts_list:
                        new_conj = Conjunction(fact_list)
                        binding = Binding()
                        unify(rule.rhs,new_conj,binding)
                        if not binding.is_fail and rule.check_difference(binding):
                            new_fact = binding.bind(rule.lhs)
                            already_has = False
                            for fact in new:
                                if fact.is_identical(new_fact):
                                    already_has = True
                                    break
                            if not already_has:
                                for fact in self.knowledge_base.list_of_facts:
                                    if fact.is_identical(new_fact):
                                        already_has = True
                                        break
                            if not already_has:
                                new.append(new_fact)
                                if goal.is_unificable(new_fact):
                                    goal_bind = Binding()
                                    unify(goal,new_fact,goal_bind)
                                    if not goal_bind.is_fail:
                                        list_of_binding = list_of_binding.merge_or(goal_bind)
                self.list_of_facts += new
                for rule in self.list_of_rules:
                    rule.get_supported_fact(new)
                if len(new)==0:
                    not_have_anything_new = True
                    break
        return list_of_binding
    # Backward chaining
    def backward_chaining_ask(self,goal):
        list_of_binding = None
        if isinstance(goal,Statement):
            return self.backward_chaining_or(goal)
        elif isinstance(goal,Conjunction):
            for subgoal in goal.list_of_statements:
                if list_of_binding!=None:
                    list_of_binding = list_of_binding.merge_and(self.backward_chaining_ask(subgoal))
                else:
                    list_of_binding = self.backward_chaining_ask(subgoal)
        elif isinstance(goal,Disjunction):
            for subgoal in goal.list_of_statements:
                if list_of_binding!=None:
                    list_of_binding = list_of_binding.merge_or(self.backward_chaining_ask(subgoal))
                else:
                    list_of_binding = self.backward_chaining_ask(subgoal)
        return list_of_binding
    def backward_chaining_or(self,goal):
        binding_list = ListOfBinding([])
        for fact in self.list_of_facts:
            if fact.is_unificable(goal):
                binding = Binding()
                unify(fact,goal,binding)
                if not binding.is_fail:
                    binding_list.binding_list.append(binding)
        for rule in self.list_of_rules:
            if rule.lhs.is_unificable(goal):
                binding = Binding()
                unify(rule.lhs, goal, binding)
                if not binding.is_fail:
                    binding_list = binding_list.merge_or(self.backward_chaining_and(rule,binding))
        return binding_list
    def backward_chaining_and(self, rule, binding_rhs):
        binding_list = ListOfBinding([binding_rhs])
        new_rule = binding_rhs.bind(rule.rhs)
        for goal in new_rule.list_of_statements:
            or_binding = self.backward_chaining_or(goal)
            var_list = goal.get_variable_list()
            for binding in or_binding.binding_list:
                new_dict = {}
                for key in binding.binding_dict.keys():
                    if key in var_list:
                        new_dict[key] = binding.binding_dict[key]
                binding.binding_dict = new_dict
            binding_list = binding_list.merge_and(or_binding)
        for binding in binding_list.binding_list:
            if (not rule.check_difference(binding)) or binding.is_fail:
                binding_list.binding_list.remove(binding)
        return binding_list
    def resolution(self):
        list_of_cnfs = []
        binding_query = []
        for fact in self.list_of_facts:
            list_of_cnfs.append(CNF(Disjunction([fact])))
        for rule in self.list_of_rules:
            new_dis = rule.rhs.negate()
            new_dis.list_of_statements.append(rule.lhs)
            list_of_cnfs.append(CNF(new_dis,rule.difference))
        for query in self.list_of_query:
            binding = self.resolution_ask(list_of_cnfs,query)
            binding_query.append(binding)
        return binding_query
    def resolution_ask(self,list_of_cnfs,goal):
        list_of_binding = None
        if isinstance(goal,Statement):
            return self.resolution_step(list_of_cnfs, Disjunction([goal.negate()]))
        elif isinstance(goal,Conjunction):
            for subgoal in goal.list_of_statements:
                if list_of_binding!=None:
                    list_of_binding = list_of_binding.merge_and(self.resolution_ask(list_of_cnfs,subgoal))
                else:
                    list_of_binding = self.resolution_ask(list_of_cnfs,subgoal)
        elif isinstance(goal,Disjunction):
            for subgoal in goal.list_of_statements:
                if list_of_binding!=None:
                    list_of_binding = list_of_binding.merge_or(self.resolution_ask(list_of_cnfs,subgoal))
                else:
                    list_of_binding = self.resolution_ask(list_of_cnfs,subgoal)
        return list_of_binding
    def resolution_step(self,list_of_cnfs,goal):
        list_of_binding = ListOfBinding()
        if len(goal.list_of_statements) == 0:
            list_of_binding = ListOfBinding(Binding())
            return list_of_binding
        goal_list = goal.list_of_statements
        for cnf in list_of_cnfs:
            cnf.standardlize_variable()
            cnf_list = cnf.body.list_of_statements
            subgoal = goal_list[0]
            
            for statement in cnf_list:
                if statement.is_opposite(subgoal):                        
                    binding = Binding()
                    unify(statement.negate(),subgoal,binding)
                    if not binding.is_fail:
                        difference = []
                        for differ in cnf.difference:
                            difference.append([Term(differ[0].term),Term(differ[1].term)])
                        new_binding = ListOfBinding(binding)
                        new_list_of_statements = goal_list[1:] + [x for x in cnf_list if not x == statement]
                        new_dis = Disjunction(new_list_of_statements)
                        new_dis = binding.bind(new_dis)
                        subgoal_bind = new_binding.merge_and(self.resolution_step(list_of_cnfs,new_dis))
                        # Check difference
                        for bind in subgoal_bind.binding_list:
                            differ = True
                            for pair in difference:
                                if bind.bind(pair[0]) == bind.bind(pair[1]):
                                    differ = False
                                    break
                            if not differ:
                                subgoal_bind.binding_list.remove(bind)
                        list_of_binding = list_of_binding.merge_or(subgoal_bind)
        return list_of_binding                   
    