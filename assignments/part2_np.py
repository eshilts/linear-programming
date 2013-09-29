import logging
from read_write_np import *
from simple_pivot_np import *
from pivot_lp_solver_np import *

def run_part2(path, file_name):
    logging.info("--- Dict file: {0} ---".format(file_name))
    new_dict = read_dict_file(path, file_name)
    steps, A, z, unbounded = pivot_lp_solver(new_dict)

    write_out_answers_part2(
            'part2TestCases/answers', file_name, 
            steps, A, z, unbounded)
    
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

logging.info("Unit tests")
for i in range(1, 11):
    run_part2('part2TestCases/unitTests', 'dict' + str(i))

logging.info("Assignment parts for grading")
for i in range(1, 6):
    run_part2('part2TestCases/assignmentParts', 'part{0}.dict'.format(i))
