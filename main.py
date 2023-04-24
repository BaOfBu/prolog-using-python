import globals
from knowledge_base import KnowledgeBase
from Utils import print_output

globals.initialize()
    
input_file = 'input.txt'
output_file = 'output.txt'

knowledge_base = KnowledgeBase()
knowledge_base.input_from_file(input_file)

print("Backward chaining")
f = open(output_file,'w')

for query in knowledge_base.list_of_query:
    binding_list = knowledge_base.backward_chaining_ask(query)
    print_output(f,query,binding_list)
