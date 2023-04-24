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

#Change to Reverse Polish Notation
def change_to_RPN(tokens):
    operator_stack = []
    output = []
    for token in tokens:
        if token == '(':
            operator_stack.append(token)
        elif token == ')':
            operator = operator_stack.pop()
            while operator != '(':
                output.append(operator)
                operator = operator_stack.pop()
        elif is_operator(token):
            while len(operator_stack)>0 and (operator_stack[-1].endswith('*') or \
            is_higher_precedence(operator_stack[-1],token) or operator_stack[-1]==token) and (operator_stack[-1]!='('):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        else:
            if token.endswith('*'):
                operator_stack.append(token)
            else:
                output.append(token)
    operator_stack.reverse()
    output = output + operator_stack
    return output

#Process RPN and convert to conjunction
def convert_to_conjunction(tokens):

    from statement import Statement
    from conDisjunction import Conjunction, Disjunction
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
    #Turn string to list of tokens
    tokens = []
    name = ''
    for ch in s:
        if is_operator(ch) or ch == '(' or ch == ')':
            if name!='':
                if ch == '(':
                    name += '*'
                tokens.append(name)
                name = ''
            tokens.append(ch)
        elif ch==' ':
            continue
        else:
            name+=ch
    rpn = change_to_RPN(tokens)
    #print(rpn)
    output_line = convert_to_conjunction(rpn)
    return output_line


def unify(x,y, binding):

    from statement import Statement
    from conDisjunction import Conjunction, Disjunction
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
        if x.is_unificable(y):
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

def print_output(f, query, binding_list,index):
    #print('?- ' + str(query))
    f.write(str(index) + '?- ' + str(query) + '\n')
    is_fail = 'true'
    res = ''
    for binding in binding_list.binding_list:
        if binding.is_fail == False:
            is_fail = 'false'
            str_bind = ''
            for term in query.get_list_var():
                if not term.startswith(abstract_name):
                    if term in binding.binding_dict:
                        temp = '' + binding.binding_dict[term]
                        if not temp in str_bind:
                            str_bind += term + ' = ' + binding.binding_dict[term]
            if res.count(str_bind) == 0:
                res += str_bind + ' ;\n'

    if (is_fail == 'true'):
        is_fail = 'false'
    else: is_fail = 'true'

    if res == '':
        #print(is_fail + ' .\n')
        f.write(is_fail + ' .\n\n')
    else:
        res = res[:-3]
        res += '.\n\n'
        #print(res)
        f.write(res)
