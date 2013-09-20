import logging
from os.path import join
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

def read_and_split_line(f, floats=True):
    return [float(x) if floats else int(x) for x in f.readline().split()]

def assign_decision_variables(decision_variables, some_list):
    return {key: value for key, value in zip(decision_variables, some_list)}

def construct_A(decision_variables, m, f, floats=True):
    return [assign_decision_variables(decision_variables, read_and_split_line(f, floats))
            for i in range(m) ]

def read_dict_file(path, file_name):
    f = open(join(path, file_name), 'r')
    m, n = read_and_split_line(f, False)
    logging.info('m = {0}, n = {1}'.format(m, n))
    basic_variables = read_and_split_line(f, False)
    logging.info('basic variables: {0}'.format(basic_variables))
    decision_variables = read_and_split_line(f, False)
    logging.info('decision variables: {0}'.format(decision_variables))
    basic_coefficients = read_and_split_line(f)
    logging.info('basic coefficients: {0}'.format(basic_coefficients))
    
    A = construct_A(decision_variables, m, f)
    logging.info('A = {0}'.format(A))

    objectives = read_and_split_line(f)
    z = objectives[0]
    objective_coefficients = assign_decision_variables(decision_variables, objectives[1:])
    logging.info('z = {0}, objective coefficients: {1}'.format(z, objective_coefficients))

    f.close()

    return {
            'm_n': (m, n), 
            'basic_variables': basic_variables,
            'decision_variables': decision_variables,
            'basic_coefficients': basic_coefficients,
            'A': A,
            'z': z,
            'objective_coefficients': objective_coefficients
            }

def find_entering_variable(objective_coefficients):
    variable_coefficient = { var: coef 
            for var, coef in objective_coefficients.items() 
            if coef > 0 }
    logging.info("Potential entering variables: {0}".format(variable_coefficient))
    min_variable = min(variable_coefficient)
    min_coefficient = variable_coefficient.get(min_variable)
    logging.info("Min variable & associated coefficient: {0}, {1}".format(
        min_variable, min_coefficient))
    return (min_variable, min_coefficient)

def find_leaving_variable(entering_variable, basic_variables, basic_coefficients, A):
    entering_constraints = {
            basic_variables[i]: -1 * basic_coefficients[i] / A[i].get(entering_variable)
            for i in range(len(basic_coefficients))
            if A[i].get(entering_variable) < 0 }
    logging.info("Potential leaving constraints: {0}".format(entering_constraints))

    if len(entering_constraints) == 0:
        logging.info('Unbounded problem.')
        return ('UNBOUNDED', None)

    min_constraints = { key: value 
            for key, value in entering_constraints.items()
            if value == min(entering_constraints.values()) }
    leaving_variable = min(min_constraints)
    min_constraint = min_constraints.get(leaving_variable)
    logging.info("Leaving variable: variable = {0}, constraint = {1}".format(
        leaving_variable, min_constraint))
    return (leaving_variable, min_constraint)

def get_objective_value(z, entering_coefficient, leaving_variable, constraint):
    if leaving_variable == 'UNBOUNDED':
        return 'UNBOUNDED'
    new_objective = z + (constraint * entering_coefficient)
    logging.info('New objective = {0}'.format(new_objective))
    return new_objective

def write_out_answers(out_path, input_file, entering_variable, leaving_variable, objective_value):
    logging.info("Writing answers to: answers/{0}".format(input_file))
    f = open(join(out_path, input_file), 'w')
    if objective_value == 'UNBOUNDED':
        f.write(objective_value)
    else:
        f.writelines([str(l) + '\n' 
            for l in [entering_variable, leaving_variable, objective_value]])
    f.close()

def run_part1(path, file_name):
    new_dict = read_dict_file(path, file_name)
    logging.info('New dict: {0}'.format(new_dict))
    entering_variable, entering_coefficient = find_entering_variable(
            new_dict['objective_coefficients'])
    leaving_variable, constraint = find_leaving_variable(entering_variable, 
            new_dict['basic_variables'], new_dict['basic_coefficients'], 
            new_dict['A'])
    new_objective = get_objective_value(new_dict['z'], entering_coefficient,
            leaving_variable, constraint)
    logging.info("\n--- {0}: entering = {1}, leaving = {2}, new objective = {3} ---\n".format(
        file_name, entering_variable, leaving_variable, new_objective))
    write_out_answers('part1TestCases/answers', file_name, entering_variable, leaving_variable, new_objective)

logging.info("Unit tests")
for i in range(1, 11):
    run_part1('unitTests', 'dict' + str(i))

logging.info("Assignment parts for grading")
for i in range(1, 6):
    run_part1('assignmentParts', 'part{0}.dict'.format(i))
