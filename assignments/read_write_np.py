import logging
from os.path import join
import numpy as np
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

def read_and_split_line(f, floats=True):
    return np.array([
        float(x) if floats else int(x) 
        for x in f.readline().split()])

def construct_A(m, f, floats=True):
    return np.array([read_and_split_line(f, floats) for i in range(m)])

def read_dict_file(path, file_name):
    f = open(join(path, file_name), 'r')
    m, n = read_and_split_line(f, False)
    logging.info('m = {0}, n = {1}'.format(m, n))
    basic_var = read_and_split_line(f, False)
    logging.info('basic variables: {0}'.format(basic_var))
    decision_var = read_and_split_line(f, False)
    logging.info('decision variables: {0}'.format(decision_var))
    b = read_and_split_line(f)
    logging.info('basic coefficients: {0}'.format(b))
    
    A = construct_A(m, f)
    logging.info('A ({1}x{2})=\n{0}'.format(A, m, n))

    objectives = read_and_split_line(f)
    z = objectives[0]
    logging.info('objectives = {0}'.format(objectives))

    f.close()

    return {
            'm_n': (m, n), 
            'basic_var': basic_var,
            'decision_var': decision_var,
            'b': b,
            'A': A,
            'z': z,
            'objectives': objectives
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
