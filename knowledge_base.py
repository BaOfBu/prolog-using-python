from rule import Rule
from statement import Statement
from conDisjunction import Conjunction, Disjunction
from binding import Binding, ListOfBinding
from Utils import process_string, unify

class KnowledgeBase:
    #Knowledge Base with set of rules (facts are rules without conditions)
    def __init__(self):
        self.list_of_rules = []
        self.list_of_facts = []
        self.list_of_query = []

    def input_from_file(self, filename_input,queries_input):
        with open(filename_input,'r') as f:
            index = 1
            for line in f:
                index += 1
                line = line.strip()
                line = line.replace(" ","")
                line = line.replace("),",")&")
                if not line.startswith('%') and line != '':
                    expr = line.split(':-')
                    new_rule = None
                    if len(expr) == 1:
                        new_rule = process_string(expr[0]).list_of_statements[0]
                        new_rule.standardize_variable()
                        self.list_of_facts.append(new_rule)
                    else:
                        new_rule = Rule(process_string(expr[0]).list_of_statements[0], process_string(expr[1]))
                        self.list_of_rules.append(new_rule)
        with open(queries_input,'r') as f1:
            index = 1
            for line in f1:
                index += 1
                line = line.strip()
                line = line.replace(" ","")
                line = line.replace("),",")&")
                if line.startswith('?-'):
                    line = line[2:].strip()
                    query = process_string(line)
                    query.standardize_abstract_variable()
                    self.list_of_query.append(query)
                    
        # Split rule
        list_of_new_rule = []
        for rule in self.list_of_rules:
            list_of_new_rule = list_of_new_rule + rule.split()
        self.list_of_rules = list_of_new_rule
        # Get supported fact for each rule
        for rule in self.list_of_rules:
            rule.eliminate_difference()
            rule.get_supported_fact(self.list_of_facts)
            rule.standardize_variable()
    
    def __str__(self):
        output = ''
        for rule in self.list_of_rules:
            output+= str(rule) + '\n'
        for fact in self.list_of_facts:
            output+= str(fact) + '\n'
        return output
    
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
            if fact.is_unifiable(goal):
                binding = Binding()
                unify(fact,goal,binding)
                if not binding.is_fail:
                    binding_list.binding_list.append(binding)
        for rule in self.list_of_rules:
            if rule.left.is_unifiable(goal):
                binding = Binding()
                unify(rule.left, goal, binding)
                if not binding.is_fail:
                    binding_list = binding_list.merge_or(self.backward_chaining_and(rule,binding))
        return binding_list
    
    def backward_chaining_and(self, rule, binding_right):
        binding_list = ListOfBinding([binding_right])
        new_rule = binding_right.bind(rule.right)
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