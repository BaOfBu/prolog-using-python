import sys
import time
from knowledge_base import KnowledgeBase
from term import Term
from Utils import process_string, unify, print_output
import globals

abstract_var = 1
abstract_name = '_/*'
not_have_anything_new = False

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


# while inference_choice <= 0 or inference_choice >=4:
#     inference_choice = int(input('1. Forward chaining \t 2. Backward chaining \t 3. Resolution \nChoose inference: '))
print("Backward chaining")
f = open(output_file,'w')

index = 1
for query in knowledge_base.list_of_query:
    binding_list = knowledge_base.backward_chaining_ask(query)
    print_output(f,query,binding_list,index)
    index += 1