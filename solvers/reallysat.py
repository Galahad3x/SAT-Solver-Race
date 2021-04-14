#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    ------------------------- reallySAT -------------------------

    reallySAT is a local search solver for SAT solving.
    More precisely, this solver is an efficient implementation of
    the walkSAT algorithm explained in APAI.

    AUTHORS: Guillem Camats and Martí La Rosa

"""
import sys
import os
import random


def get_cnf(cnf_path):
    """Given the path of the cnf, returns the clauses, the number of variables
        and the number of clauses.
    """
    with open(cnf_path) as fcnf:
        name = fcnf.readline().strip()
        conf_line = fcnf.readline().strip().split()
        num_vars = int(conf_line[2])
        num_clauses = int(conf_line[3])
        clauses = []
        clause_line = fcnf.readline().strip().split()
        while clause_line:
            clause_line = sorted(
                clause_line[:-1], key=lambda clause: int(clause.lstrip("-")))  # sort clause by variable
            clauses.append([int(cl) for cl in clause_line])
            clause_line = fcnf.readline().strip().split()
    return clauses, num_vars, num_clauses


def print_solution(solution):
    """Prints the proposed solution."""
    sys.stdout.write("c %s\n" % sys.argv[0][:-3])
    if solution:
        sys.stdout.write("s SATISFIABLE\n")
        sys.stdout.write("v %s\n" % " ".join(
            [str(cl) for cl in solution]))
    else:
        sys.stdout.write("s SOLUTION NOT FOUND\n")


def get_random_interpretation(num_vars):
    """Gets a random interpretation."""
    return [i if random.random() < 0.5 else -i for i in range(1, num_vars + 1)]


def get_lit_to_clauses(clauses, num_vars):
    """Get fast access data structure.
       Each position represents the according literal
          and keeps a list of indexes of clauses that has
          the respective literal.
    """
    # First position NULL, easier index access
    lit_to_clauses = [[] for _ in range(1 + num_vars*2)]
    for idx, clause in enumerate(clauses):
        for lit in clause:
            lit_to_clauses[lit].append(idx)
    return lit_to_clauses


def get_unsat_clauses_idx(clauses_sat_lit):
    """Get the indexes of the unsatisfied clauses."""
    unsat_clauses_idx = []
    for idx, val in enumerate(clauses_sat_lit):
        if val == 0:
            unsat_clauses_idx.append(idx)
    return unsat_clauses_idx


def get_clauses_sat_lit(clauses, interpretation, num_clauses):
    """Get the satisfied literals for each clause and the indexes of the unsatisfied clauses."""
    clauses_sat_list = [0 for _ in range(num_clauses)]
    unsat_clauses = []
    for idx, clause in enumerate(clauses):
        sat_counter = 0
        for lit in clause:
            if lit == interpretation[abs(lit) - 1]:
                sat_counter += 1
        clauses_sat_list[idx] = sat_counter
        if sat_counter == 0:  # is current clause unsatisfied by the interpretation?
            unsat_clauses.append(idx)
    return clauses_sat_list, unsat_clauses


def get_random_unsat_clause_idx(unsat_clauses_idx):
    """Pick randomly an index of an unsatisfied clause."""
    return unsat_clauses_idx[random.randint(0, len(unsat_clauses_idx) - 1)]


def get_min_break(unsat_clause, lit_to_clauses, clauses_sat_lit, num_clauses):
    """Gets the variables that minimizes the break score."""
    min_break = num_clauses
    min_break_literals = []
    for literal in unsat_clause:
        current_break = 0
        for clause_idx in lit_to_clauses[-literal]:  # satisfied clauses
            # if current literal flips, this clause will go unsat
            if clauses_sat_lit[clause_idx] == 1:
                current_break += 1
        if current_break < min_break:
            min_break = current_break
            min_break_literals = [literal]
        elif current_break == min_break:
            min_break_literals.append(literal)
    return min_break_literals, min_break


def flip_var(interpretation, var):
    """Given an interpretation and a variable, flips the variable value in the interpretation."""
    interpretation[abs(var) - 1] *= -1


def update_sat_literals(fvar, lit_to_clauses, clauses_sat_lit, unsat_clauses_idx):
    """updates the number of satisfied literals each clause has.
       it also updates the list of indexes of unsatisfied clauses."""
    for old_idx in lit_to_clauses[-fvar]:
        clauses_sat_lit[old_idx] -= 1
        if clauses_sat_lit[old_idx] == 0:
            unsat_clauses_idx.append(old_idx)

    for new_idx in lit_to_clauses[fvar]:
        clauses_sat_lit[new_idx] += 1
        if clauses_sat_lit[new_idx] == 1:
            unsat_clauses_idx.remove(new_idx)


def run_reallysat(clauses, num_vars, num_clauses):
    """runs reallySAT solver with given clauses, number of variables and number of clauses"""
    max_flips = int(1/4 * num_vars ** 2)
    lit_to_clauses = get_lit_to_clauses(clauses, num_vars)
    prob = 0.45
    while 1:
        interpretation = get_random_interpretation(num_vars)
        clauses_sat_lit, unsat_clauses_idxs = get_clauses_sat_lit(
            clauses, interpretation, num_clauses)
        for _ in range(max_flips):
            if not unsat_clauses_idxs:
                return interpretation
            cidx = get_random_unsat_clause_idx(unsat_clauses_idxs)
            unsat_clause = clauses[cidx]
            bvars, break_score = get_min_break(
                unsat_clause,
                lit_to_clauses,
                clauses_sat_lit,
                num_clauses)
            if break_score > 0 and random.random() < prob:
                fvar = random.choice(unsat_clause)
            else:
                fvar = bvars[-1]  # picks the only var in b_vars

            update_sat_literals(fvar, lit_to_clauses,
                                clauses_sat_lit, unsat_clauses_idxs)

            flip_var(interpretation, fvar)


def main():
    """parses arguments, runs reallySAT solver and prints the solution"""
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Incorrect number of arguments. Given %s. Expected 2.\n" %
                         len(sys.argv))
        sys.exit("Use: %s CNF_file" % sys.argv[0])
    cnf_path = sys.argv[1]
    if not os.path.isfile(cnf_path):
        sys.exit("ERROR: CNF file %s does not exist." % cnf_path)

    clauses, num_vars, num_clauses = get_cnf(cnf_path)
    solution = run_reallysat(clauses, num_vars, num_clauses)
    print_solution(solution)


if __name__ == "__main__":
    main()
