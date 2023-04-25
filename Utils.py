from statement import Statement
from conDisjunction import Conjunction, Disjunction

abstract_name = '_/*'

def is_variable(term):
    if term[0].isupper() or term.startswith('_'):
        return True
    else:
        return False

def is_operator(c):
    return c=='&' or c == ';'

def is_higher_precedence(a,b):
    return (a == '&' or a == ',') and b == ';'

#Process RPN and convert to conjunction
def convert_to_conjunction(tokens):

    from term import Term

    stack = []
    for token in tokens:
        if token.endswith('*'):
            operands = stack.pop()
            operands = operands.term.split(',')
            list_of_terms = []
            for operand in operands:
                list_of_terms.append(Term(operand))
            statement = Statement(list_of_terms=list_of_terms,predicate=token[:-1])
            stack.append(statement)
        elif is_operator(token):
            list_of_statements = []
            list_of_statements.append(stack.pop())
            list_of_statements.append(stack.pop())
            list_of_statements.reverse()
            new_operand = []
            if token == '&':
                new_operand = Conjunction(list_of_statements=list_of_statements)
            elif token == ';':
                new_operand = Disjunction(list_of_statements=list_of_statements)
            stack.append(new_operand)
        else:
            stack.append(Term(token))
    output = Conjunction([stack.pop()])
    output.simplify()
    return output

def process_string(s):
    #convert string to Reverse Polish notation 
    output = []
    index = 0
    name =''
    string = s
    operator = []
    while len(string) > 0:
        if string.startswith(')') or string.startswith('.'):
            break
        flag = True
        if is_operator(string[0]):
            operator.append(string[0])
            if string[1] != '(':
                string = string[1:]
            else:
                string = string[2:]
                flag = False
        index1 = string.find("(")
        name = string[:index1]
        name += '*'
        index2 = string.find(")")
        terms = string[(index1 + 1):index2]
        index = index2 + 1
        string = string[index:]
        output.extend([terms, name])
        if len(string) == 0 or flag:
            for i in range(len(operator)):
                output.append(operator.pop())

    result = convert_to_conjunction(output)
    return result

def unify(x,y, binding):

    from term import Term

    if binding.is_fail:
        return binding
    elif x == y:
        return binding
    elif isinstance(x,Term) and x.is_var:
        return unify_var(x,y,binding)
    elif isinstance(y,Term) and y.is_var:
        return unify_var(y,x,binding)
    elif isinstance(x,Statement) and isinstance(y,Statement):
        if x.is_unifiable(y):
            return unify(x.list_of_terms,y.list_of_terms,binding)
    elif (isinstance(x,Conjunction) and isinstance(y,Conjunction)) or (isinstance(x,Disjunction) and isinstance(y,Disjunction)):
        if len(x.list_of_statements)==len(y.list_of_statements):
            return unify(x.list_of_statements,y.list_of_statements,binding)
    elif isinstance(x,list) and isinstance(y,list):
        if len(x) == len(y):
            return unify(x[0],y[0],unify(x[1:],y[1:],binding))
    binding.is_fail = True
    return binding

def unify_var(var,x,binding):
    if binding.already_has(var):
        return unify(binding.bind(var),x,binding)
    elif binding.already_has(x):
        return unify(var,binding.bind(x),binding)
    else:
        binding.add_new_binding(var,x)
        return binding

def print_output(f, query, binding_list):
    f.write('?- ' + str(query) + '\n')
    is_fail = True
    res = ''
    for binding in binding_list.binding_list:
        if binding.is_fail == False:
            is_fail = False
            str_bind = ''
            for term in query.get_list_var():
                if not term.startswith(abstract_name):
                    if term in binding.binding_dict:
                        temp = '' + binding.binding_dict[term]
                        if not temp in str_bind:
                            str_bind += term + ' = ' + binding.binding_dict[term]
            if res.count(str_bind) == 0:
                res += str_bind + ' ;\n'

    if res == '':
        f.write(str(not is_fail) + '.\n\n')
    else:
        res = res[:-3]
        res += '.\n\n'
        f.write(res)
