import logging
import numpy as np
from pandas import Series
from simple_pivot_np import *


def switch_variables(A, z, enter_var, leave_var):
    logging.debug('Before switch: A =\n{0}'.format(A))
    A.rename(columns={enter_var: leave_var}, inplace=True)
    logging.debug('before index_vals = {0}'.format(A.index.values))
    index_vals = np.array([enter_var if i_v == leave_var else i_v 
            for i_v in A.index.values])
    logging.debug('after index_vals = {0}'.format(index_vals))
    A.reset_index(drop=True, inplace=True)
    A.set_index(index_vals, inplace=True)
    logging.debug('After switch: A =\n{0}'.format(A))
    z = Series(z.values, index=A.columns.values)
    logging.debug('After switch: z =\n{0}'.format(z))

    return (A, z)
    

def pivot_A_z(A, z, enter_var, leave_var, enter_coef, constraint):
    logging.info("Pivoting A: enter_var = {0}, leave_var = {1}, "
            "enter_coef = {2}, enter_constraint = {3}".format(
                enter_var, leave_var, enter_coef, constraint))
    enter_coefs = A[enter_var]
    enter_coefs_np = np.array(enter_coefs.values)
    leave_row = A.loc[leave_var]

    logging.debug("Old A:\n{0}".format(A))
    A_new = A.apply(
            lambda x: x - ((x[enter_var] / enter_coef) * leave_row),
            axis=1)
    A_new.loc[leave_var] = (-1 / enter_coef) * leave_row
    A_new[enter_var] = (1 / enter_coef) * enter_coefs_np
    A_new[enter_var].loc[leave_var] = 1 / enter_coefs.loc[leave_var]
    logging.debug("New A:\n{0}".format(A_new))

    logging.debug("Old z:\n{0}".format(z))
    z_new = z - ((z[enter_var] / enter_coef) * leave_row)
    z_new[enter_var] = (1 / enter_coef) * z[enter_var]
    logging.debug("New z:\n{0}".format(z_new))

    A_new, z_new = switch_variables(A_new, z_new, enter_var, leave_var)

    return (A_new, z_new)


def pivot_lp_solver(dict_to_solve):
    steps = 0
    A = dict_to_solve['A']
    z = dict_to_solve['z']

    while True:
        logging.debug('A =\n{0}'.format(A))
        logging.debug('z =\n{0}'.format(z))
        pivot_data = simple_pivot(dict_to_solve)
        logging.info(("--- Simple pivot results: enter = {0}, leave = {1}, " 
            "new objective = {2} ---\n").format(
                pivot_data['enter_var'], 
                pivot_data['leave_var'], pivot_data['objective']))

        if pivot_data['enter_var'] is None or pivot_data['leave_var'] is None:
            unbounded = pivot_data['enter_var'] is not None
            logging.debug('Stopping after {0} steps. Unbounded = {1}'.format(
                steps, unbounded))
            break

        A, z = pivot_A_z(A, z,
                pivot_data['enter_var'], pivot_data['leave_var'],
                pivot_data['enter_coef'], pivot_data['constraint'])

        dict_to_solve['A'] = A
        dict_to_solve['z'] = z

        steps += 1
        logging.debug('Step {0} completed.'.format(steps))

        if steps >= 100:
            break

    logging.debug("===== Final A=\n{0}".format(A))
    logging.debug("===== Final z=\n{0}".format(z))

    return (steps, A, z, unbounded)




