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

def write_out_answers_part1(
        out_path, input_file, 
        entering_variable, leaving_variable, objective_value):
    logging.info("Writing answers to: {0}".format(join(out_path, input_file)))
    f = open(join(out_path, input_file), 'w')
    if objective_value == 'UNBOUNDED':
        f.write(objective_value)
    else:
        f.writelines([str(l) + '\n' 
            for l in [entering_variable, leaving_variable, objective_value]])
    f.close()
