import logging
from read_write import *
from simple_pivot import *
from pivot_lp_solver import *

def run_part2(path, file_name):
    new_dict = read_dict_file(path, file_name)
    pivot_lp_solver(new_dict, file_name)
    
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

logging.info("Unit tests")
for i in range(1, 3):
    run_part2('part2TestCases/unitTests', 'dict' + str(i))

#logging.info("Assignment parts for grading")
#for i in range(1, 6):
#    run_part1('part1TestCases/assignmentParts', 'part{0}.dict'.format(i))
