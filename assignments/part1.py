import logging
from read_write import *
from simple_pivot import *

def run_part1(path, file_name):
    new_dict = read_dict_file(path, file_name)
    logging.info('New dict: {0}'.format(new_dict))
    entering_variable, entering_coefficient = find_entering_variable(
            new_dict['objective_coefficients'])
    leaving_variable, constraint, a_coef = find_leaving_variable(entering_variable, 
            new_dict['basic_variables'], new_dict['basic_coefficients'], 
            new_dict['A'])
    new_objective = get_objective_value(new_dict['z'], entering_coefficient,
            leaving_variable, constraint)
    logging.info("\n--- {0}: entering = {1}, leaving = {2}, new objective = {3} ---\n".format(
        file_name, entering_variable, leaving_variable, new_objective))
    write_out_answers('part1TestCases/answers', file_name, entering_variable, leaving_variable, new_objective)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

logging.info("Unit tests")
for i in range(1, 11):
    run_part1('part1TestCases/unitTests', 'dict' + str(i))

logging.info("Assignment parts for grading")
for i in range(1, 6):
    run_part1('part1TestCases/assignmentParts', 'part{0}.dict'.format(i))
