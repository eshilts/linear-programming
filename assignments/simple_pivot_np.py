import logging

def find_enter_var(z):
    potential_enter = (z[1:][z[1:] > 0]).sort_index()
    logging.info("Finding enter variable among:\n{0}".format(
        potential_enter))

    if len(potential_enter) == 0:
        logging.info("No enter variable. Stopping.")
        return None

    return potential_enter.index.values[0]

def find_leave_var(enter_var, A, z):
    if enter_var is None:
        logging.info("No enter variable: stopping finding leave variable.")
        return None

    A_enter_coefs = A.loc[:, enter_var]

    logging.info("A_enter_coefs =\n{0}".format(A_enter_coefs))
    potential_con = (
            -1 * A['b'] / A_enter_coefs[A_enter_coefs < 0]
            ).dropna().order()
    logging.info("Potential leave constraints:\n{0}".format(
        potential_con))

    if len(potential_con) == 0:
        logging.info('Unbounded problem. Stopping.')
        return None

    min_constraint = potential_con[
            potential_con == potential_con.min()].sort_index()

    return min_constraint.index.values[0]

def find_enter_constraint(enter_var, leave_var, A):
    if enter_var is None or leave_var is None:
        return None
    return -1 * A.ix[leave_var, 'b'] / A.loc[leave_var, enter_var]

def find_enter_coefficient(enter_var, leave_var, A):
    if enter_var is None or leave_var is None:
        return None
    return A.loc[leave_var, enter_var]

def get_objective_value(z, enter_coef, enter_var, leave_var, enter_constraint):
    if leave_var is None and enter_var is not None:
        return float('inf')
    elif enter_var is None:
        return z[0]

    new_objective = z[0] + (z[enter_var] * enter_constraint)
    logging.info('New objective = {0}'.format(new_objective))
    return new_objective

def simple_pivot(dict_to_pivot):
    logging.info('Incoming dict: {0}'.format(dict_to_pivot))
    enter_var = find_enter_var(dict_to_pivot['z'])
    logging.info("Entering variable = {0}".format(enter_var))
    leave_var = find_leave_var(enter_var,
            dict_to_pivot['A'], dict_to_pivot['z'])
    logging.info("Leaving variable = {0}".format(leave_var))

    enter_constraint = find_enter_constraint(
            enter_var, leave_var, dict_to_pivot['A'])
    logging.info('Entering constraint = {0}'.format(enter_constraint))
    enter_coef = find_enter_coefficient(
            enter_var, leave_var, dict_to_pivot['A'])
    logging.info('Entering coefficient = {0}'.format(enter_coef))
    objective = get_objective_value(dict_to_pivot['z'], enter_coef, 
            enter_var, leave_var, enter_constraint)
    logging.info('Objective = {0}'.format(objective))

    return {
            'enter_var': enter_var,
            'leave_var': leave_var,
            'enter_coef': enter_coef,
            'constraint': enter_constraint,
            'objective': objective
            }


