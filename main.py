import globals
from knowledge_base import KnowledgeBase
from Utils import print_output

globals.initialize()

print("1:royal family; 2: HCMUS")
choice = int(input())

input_file = ''
output_file = ''
queries_file = ''

if(choice == 1):
    input_file = 'input_royal.txt'
    output_file = 'output_royal.txt'
    queries_file = "queries_royal.txt"
else:
    input_file = 'input_hcmus.txt'
    output_file = 'output_hcmus.txt'
    queries_file = "queries_hcmus.txt"

knowledge_base = KnowledgeBase()
knowledge_base.input_from_file(input_file,queries_file)

print("Backward chaining")
f = open(output_file,'w')

for query in knowledge_base.list_of_query:
    binding_list = knowledge_base.backward_chaining_ask(query)
    print_output(f,query,binding_list)