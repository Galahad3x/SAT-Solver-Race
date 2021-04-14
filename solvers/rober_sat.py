#!/usr/bin/python
#######################################################################
# Code made by:
# Moises Bernaus Lechosa - 47903568L
# Marc Cervera Rosell - 47980320C
#######################################################################

# Libraries

from random import *
import numpy as np
import sys


# Classes

# First of all, we read the input file in this function and we take the data that we need.

def read_file(filename):
    clauses_list = []
    for line in open(filename):
        if line.startswith('c'):  # Comment line
            continue
        if line.startswith('p'):  # Data => clauses and variables
            vars = line.split()[2]
            continue
        clause = [int(x) for x in line[:-2].split()]  # Constructing a clause
        clauses_list.append(clause)
    return clauses_list, int(vars)


# We generate a random solution to use in the solver

def random_solution_generator(vars):
    solution = np.arange(1, vars + 1)  # Return evenly spaced values within a given interval
    for i in range(len(solution)):
        if random() < 0.5:
            solution[i] *= -1
    return solution


# This function returns the formula that results from the parameters of the function.

def formula_struct(clauses, vars):
    formula = []
    for i in range(vars * 2):
        formula.append([])
    for c in range(len(clauses)):
        for x in clauses[c]:
            if x <= 0:
                formula[x].append(c)
            else:
                formula[x - 1].append(c)

    return formula


# This function returns de number of the satisfiable literals.

def sat_literals_count(formula, solution):
    count = 0
    sat_literals = [0] * len(formula)
    for clauses in formula:
        for literal in clauses:
            if literal == solution[abs(literal) - 1]:
                sat_literals[count] += 1
        count += 1
    return sat_literals


# This is the principal method (the function of the solver) we will use it to find the solution and show if
# it is satisfactory or not in addition to showing the model and the name of our solver

def walk_sat(clauses, vars):
    formula = clauses
    formula_struct(formula, vars)
    while 1:
        solution = random_solution_generator(vars)
        sat_literals = sat_literals_count(formula, solution)
        for i in range(3 * vars):
            zero_positions = [i for i, j in enumerate(sat_literals) if j == 0]
            print("c rober_sat")
            if len(zero_positions) == 0:
                return print("s SATISFIABLE" + "\nv " + ' '.join(str(e) for e in solution) + " 0")
            else:
                return print("s UNSATISFIABLE")
            x = zero_positions[randint(0, len(zero_positions) - 1)]
            pivot_var = pivot_var(formula[x], sat_literals, literals_in_clauses, solution)
            if pivot_var[1] > 0 and random() < 0.30:
                to_flip = abs(formula[x][randint(0, len(formula[0]) - 1)])
            else:
                to_flip = pivot_var[0]
            flip(sat_literals, literals_in_clauses, to_flip, solution)


# This function flips the value of a literal.

def flip(sat_literals, lit_in_clause, to_flip, solution):
    if solution[to_flip - 1] < 0:
        for x in lit_in_clause[-to_flip]:
            sat_literals[x] -= 1
        for x in lit_in_clause[to_flip - 1]:
            sat_literals[x] += 1
    else:
        for x in lit_in_clause[to_flip - 1]:
            sat_literals[x] -= 1
        for x in lit_in_clause[-to_flip]:
            sat_literals[x] += 1

    solution[to_flip - 1] *= -1


def pivot(clause, sat_literals, lit_in_clause, solution):
    min = 999999999
    for literal in clause:
        pivot = 0
        if solution[abs(literal) - 1] >= 0:
            for x in lit_in_clause[abs(literal) - 1]:
                if sat_literals[x] == 1:
                    pivot += 1
        else:
            for x in lit_in_clause[-abs(literal)]:
                if sat_literals[x] == 1:
                    pivot += 1
        if pivot < min:
            min = pivot
            to_flip = literal
    return abs(to_flip), min


# Main

if __name__ == '__main__':
    clauses, vars = read_file(sys.argv[1])
    walk_sat(clauses, vars)
