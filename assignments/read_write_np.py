import logging
from os.path import join
import numpy as np
import pandas as pd
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

def read_and_split_line(f, floats=True):
    return np.array([
        float(x) if floats else int(x) 
        for x in f.readline().split()])

def construct_A(m, f, basic_vars, decision_vars, floats=True):
    return pd.DataFrame([read_and_split_line(f, floats) for i in range(m)],
            index=basic_vars, columns = decision_vars)

def read_dict_file(path, file_name):
    f = open(join(path, file_name), 'r')
    m, n = read_and_split_line(f, False)
    logging.info('m = {0}, n = {1}'.format(m, n))
    basic_var = read_and_split_line(f, False)
    logging.info('basic variables: {0}'.format(basic_var))
    decision_var = read_and_split_line(f, False)
    logging.info('decision variables: {0}'.format(decision_var))
    b = read_and_split_line(f)
    logging.info('basic coefficients (b): {0}'.format(b))

    A = construct_A(m, f, basic_var, decision_var)
    A.insert(0, 'b', b)
    logging.info('A ({1}x{2} + b)=\n{0}'.format(A, m, n))

    z = pd.Series(read_and_split_line(f), index=['b'] + list(decision_var))
    logging.info('z (objectives) =\n{0}'.format(z))

    f.close()

    return {
            'm_n': (m, n), 
            'basic_vars': basic_var,
            'decision_vars': decision_var,
            'b': b,
            'A': A,
            'z': z
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
