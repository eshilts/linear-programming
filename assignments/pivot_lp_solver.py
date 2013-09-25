import logging
from simple_pivot import *

def get_entering_coef(A, entering_var, leaving_var):
    return A.get(leaving_var).get(entering_var)

def get_row_entering_coef(A_row, entering_var):
    return A_row.get(entering_var, 0)

def get_leaving_coef(leaving_row, var):
    return leaving_row.get(var)

def adjust_row(A_row, leaving_row, entering_coef, leaving_var, entering_var):
    enter_row_coef = get_row_entering_coef(A_row, entering_var)
    new_row = {
            key: value - ((enter_row_coef * get_leaving_coef(key)) / 
                entering_coef)
            for key, value in A_row.items()
            if key != entering_var }
    new_row[leaving_var] = -1 * enter_row_coef / entering_coef

    return new_row

def add_entering_row(leaving_row, entering_coef, leaving_var, entering_var):
    new_row = { key: -1 * value / entering_coef
            for key, value in leaving_row.items() 
            if key != entering_var }
    new_row[leaving_var] = -1 / entering_coef

    return new_row
    

def pivot_lp_solver(dict_to_solve, dict_name):
    steps = 0
    A = dict_to_solve['A']
    b = dict_to_solve['basic_coefficients']
    z = dict_to_solve['z']

    while True:
        pivot_data = simple_pivot(dict_to_solve)
        logging.info(("--- {0}: entering = {1}, leaving = {2}," 
            "new objective = {3} ---\n").format(
                dict_name, pivot_data['entering_variable'], 
                pivot_data['leaving_variable'], pivot_data['new_objective']))

        if pivot_data['entering_variable'] == None:
            break
        if pivot_data['leaving_variable'] == 'UNBOUNDED':
            return ('UNBOUNDED', None)

        leaving_row = A.get(pivot_data['leaving_variable'])
        entering_coef = get_entering_coef(A, pivot_data['entering_variable'],
                pivot_data['leaving_variable'])

        logging.debug("Leaving row for [{0}]: {1}".format(
            pivot_data['leaving_variable'], leaving_row))

        for key, value in A.items():
            logging.debug('Row [{0}] - before adjustment: {1}'.format(key, value))
            A[key] = adjust_row(value, leaving_row, entering_coef, 
                    pivot_data['leaving_variable'],
                    pivot_data['entering_variable'])
            logging.debug('Row [{0}] - after adjustment: {1}'.format(key, value))

        A[entering_var] = add_entering_row(leaving_row, entering_coef, 
                pivot_data['leaving_variable'], pivot_data['entering_variable'])

        b = adjust_row(b, leaving_row, entering_coef, 
                pivot_data['leaving_variable'], pivot_data['entering_variable'])
        b[entering_var] = 1 / entering_coef

        steps += 1
        logging.debug('Step {0} completed.'.format(steps))

        if steps >= 100:
            break

    return True




