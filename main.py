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
    

input_file = 'input.txt'
output_file = 'output.txt'
inference_choice = 0
if len(sys.argv) == 2:
    input_file = sys.argv[1]
if len(sys.argv) == 3:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
if input_file =='':
    input_file = input('Input file: ')
if output_file == '':
    output_file = input('Output file: ')

knowledge_base = KnowledgeBase()
knowledge_base.input_from_file(input_file)


# while inference_choice <= 0 or inference_choice >=4:
#     inference_choice = int(input('1. Forward chaining \t 2. Backward chaining \t 3. Resolution \nChoose inference: '))
print("Backward chaining")
f = open(output_file,'w')

for query in knowledge_base.list_of_query:
    binding_list = knowledge_base.backward_chaining_ask(query)
    print_output(f,query,binding_list)