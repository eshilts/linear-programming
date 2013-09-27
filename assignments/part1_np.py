import logging
from read_write_np import *
from simple_pivot_np import *

def run_part1(path, file_name):
    new_dict = read_dict_file(path, file_name)
    pivot_data = simple_pivot(new_dict)
    logging.info(("\n--- {0}: enter = {1}, leave = {2}," 
        "objective = {3} ---\n").format(
            file_name, pivot_data['enter_var'], 
            pivot_data['leave_var'], pivot_data['objective']))
    #write_out_answers_part1('part1TestCases/answers', 
    #        file_name, pivot_data['enter_var'], 
    #        pivot_data['leave_var'], pivot_data['objective'])

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

logging.info("Unit tests")
for i in range(1, 11):
    run_part1('part1TestCases/unitTests', 'dict' + str(i))

#logging.info("Assignment parts for grading")
#for i in range(1, 6):
#    run_part1('part1TestCases/assignmentParts', 'part{0}.dict'.format(i))
