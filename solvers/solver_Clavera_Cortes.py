#!/usr/local/bin/python3
'''
Autor1: Alejandro Clavera Poza
Autor2: Ivan Cortes Garrido 
'''
import random
import copy
import argparse

SOLVER_NAME = 'solver_Clavera_Cortes'

class Codification:
    '''
    ## Codification Class
    '''
    def __init__(self, variable_set=[]):
        self.true_part = 0
        self.not_part = 0
        self.max_true_part = -1
        self.max_not_part = -1
        for var in variable_set:
            if var < 0:
                # Codificate variables with not value
                var = abs(var)
                self.not_part = self.not_part | (1 << var - 1)
                if self.max_not_part == -1 or var > self.max_not_part:
                    self.max_not_part = var
            else:
                # Codificate variables with value true
                self.true_part = self.true_part | (1 << var - 1)
                if self.max_true_part == -1 or var > self.max_true_part:
                    self.max_true_part = var

    def descodification(self):
        descodification = []
        # Descodification of true part
        for index in range(self.max_true_part + 1):
            # if bit of index position == 1 insert index + 1 in list
            if (self.true_part >> index) & 1 == 1:
                descodification.insert(index, index + 1)
        # Descodification of not part
        for index in range(self.max_not_part):
            if (self.not_part >> index) & 1 == 1:
                descodification.insert(index, -1 * (index + 1))
        return descodification

    def __str__(self):
        return str(self.descodification())

    def __and__(self, other):
        if self.true_part & other.true_part != 0:
            return 1
        elif self.not_part & other.not_part != 0:
            return 1
        else:
            return 0

    def modify_variable(self, variable):
        # Check if the variable is valid, and it set value to mask
        n_max = max(self.max_not_part, self.max_true_part)
        mask = 0 if variable > n_max else (1 << variable - 1)
        self.true_part = self.true_part ^ mask
        self.not_part = self.not_part ^ mask

    @staticmethod
    def random_codification(num_variables, seed=None):
        random_codification = Codification()
        # The next value contain num_variables - 1 bits with value 1
        max_number = (2 ** (num_variables)) - 1
        # Generate random number for codification
        random.seed(seed)
        value = random.randint(1, max_number)
        random_codification.true_part = value
        random_codification.max_true_part = num_variables
        # Set not part codification value
        random_codification.not_part = value ^ max_number
        random_codification.max_not_part = num_variables
        return random_codification

class Clause:
    def __init__(self, clause):
        self.clause = Codification(clause)

    def __str__(self):
        return str(self.clause)
    
    def get_variables(self):
        return self.clause.descodification()

    def is_model(self, interpretation):
        return self.clause & interpretation.interpretation != 0

class Interpretation:
    '''
    ## Interpretation Class
    '''

    def __init__(self, interpretation=[]):
        self.interpretation = Codification(interpretation)

    def __str__(self):
        return str(self.interpretation)

    def flip(self, variable):
        self.interpretation.modify_variable(variable)

    @staticmethod
    def random_interpretation(n_variables):
        rdn_inter = Interpretation()
        rdn_inter.interpretation = Codification.random_codification(n_variables)
        return rdn_inter

    def copy(self):
        return copy.deepcopy(self)

def load_file(path):
    info = {
        'n_variables': 0,
        'n_clauses': 0,
        'clauses': None,
        'variables': {}
    }
    clauses = []
    cnf_file = open(path, 'r')
    # Read lines of file
    for index, line in enumerate(cnf_file):
        # split line
        line = line.replace('\n', '').split(' ')
        # Process line
        if line[0] == 'p':
            info['n_variables'] = int(line[2])
            info['n_clauses'] = int(line[3])
        elif line[0] != 'c':
            # Range the line clause
            line_clause = [
                int(variable) for variable in line if variable != '0'
            ]
            for variable in line:
                if variable != '0':
                    info['variables'][int(variable)] = info['variables'].get(int(variable), 0) + 1 
            # If no empty, append to list
            if line_clause:
                clauses.append(Clause(line_clause))
    info['clauses'] = clauses
    return info

def satisfy(formula, interpretation):
    for clause in formula:
        if not (clause.is_model(interpretation)):
            return False
    return True

def not_satify(formula, interpretation):
    # Find not satisfy clauses
    not_satify_clauses = []
    for clause in formula:
        if not (clause.is_model(interpretation)):
            not_satify_clauses.append(clause)
    return not_satify_clauses

def select_clause(clauses):
    # select random_clause
    selection = random.randint(0, len(clauses) - 1)
    return clauses[selection]

def min_broken(formula, variables):
    # looks for the variable that breaks the least clauses
    min_broken_variable = None 
    min_broken_value = -1
    for variable in variables:
        n_broken = formula['variables'][variable]
        if min_broken_variable is None or n_broken < min_broken_value:
            min_broken_variable = variable
            min_broken_value = n_broken
    return min_broken_variable, min_broken_value

# Random solver
def solve_random(formula, max_tries=100):
    for i in range(max_tries):
        random_interpretation = Interpretation.random_interpretation(5)
        if satisfy(formula, random_interpretation):
            print(str(random_interpretation) + ' is SATISFIABLE')
            return True
    print("Not found result")
    return False

def walksat_solver(formula, max_tries=1000, max_flips=100, probability=0.5):
    # Walksat implementation
    for i in range(max_tries):
        interpretation = Interpretation.random_interpretation(formula['n_variables'])
        for flip in range(max_flips):
            not_satify_clauses = not_satify(formula['clauses'], interpretation)
            if len(not_satify_clauses) == 0:
                # the interpretation satisfy f
                return interpretation
            clause = select_clause(not_satify_clauses)
            variables = clause.get_variables()
            # Select variable to flip
            min_broken_variable, n_brocken = min_broken(formula, variables)
            if n_brocken > 0 and random.randint(0,1) >= 1 - probability:
                # Flip random variable
                variable_to_flip = random.randint(1, len(variables) - 1)
                interpretation.flip(abs(variables[variable_to_flip]))
            else:
                interpretation.flip(abs(min_broken_variable))        
    print("Not found result")

def check(formula, interpretation):
    error = False
    for cl in formula['clauses']:
        if not cl.is_model(interpretation):
            error = True
            break
    if error:
        print('Error solver')
    else:
        print('Satisfactible')

def print_solution(interpretation):
    interpretation = str(interpretation).replace(',', '').strip('[]')
    print('c {0}'.format(SOLVER_NAME))
    print('s SATISFIABLE')
    print('v ',end='')
    print(interpretation, end=' 0\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SAT SOLVER')
    parser.add_argument('input_cnf_formula', type=str, help='cnf_formula path')
    argparse = parser.parse_args()
    try:
        cnf = load_file(argparse.input_cnf_formula)
    except:
        print('Load file error')
        exit(-1)
    interpretation = walksat_solver(cnf, max_tries=1000, max_flips=40000 ,probability=0.5)  
    print_solution(interpretation)
