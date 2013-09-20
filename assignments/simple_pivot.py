import logging

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
            basic_variables[i]: {
                'constraint': -1 * basic_coefficients[i] / A[i].get(entering_variable),
                'a_coef': A[i].get(entering_variable) }
            for i in range(len(basic_coefficients))
            if A[i].get(entering_variable) < 0 }
    logging.info("Potential leaving constraints: {0}".format(entering_constraints))

    if len(entering_constraints) == 0:
        logging.info('Unbounded problem.')
        return ('UNBOUNDED', None, None)

    min_constraint = min([x['constraint'] 
        for x in entering_constraints.values()])
    constraints_at_min = { key: value 
            for key, value in entering_constraints.items()
            if value['constraint']  == min_constraint }

    leaving_variable = min(constraints_at_min)
    bland_constraint = constraints_at_min[leaving_variable]['constraint']
    a_coef = constraints_at_min[leaving_variable]['a_coef']

    logging.info("Leaving variable: variable = {0}, constraint = {1}, A_coef = {2}".format(
        leaving_variable, bland_constraint, a_coef))
    return (leaving_variable, bland_constraint, a_coef)

def get_objective_value(z, entering_coefficient, leaving_variable, constraint):
    if leaving_variable == 'UNBOUNDED':
        return 'UNBOUNDED'
    new_objective = z + (constraint * entering_coefficient)
    logging.info('New objective = {0}'.format(new_objective))
    return new_objective

