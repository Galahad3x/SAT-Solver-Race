#!/usr/bin/python3

import sys
import os
import glob
import re
import stat
import subprocess
import random

MAX = 999999999999


def prepare(clauses):
    prepared_clauses = []
    num = 0
    for clause in clauses:
        if(clause[0] == "c"):
            pass
        elif(clause[0] == "p"):
            sep_cla = clause.split(" ")
            num_vars = int(sep_cla[2])
            all_vars = []
            for _ in range(int(num_vars) * 2 + 1):
                all_vars.append([])
        else:
            temp_clause = []
            for var in clause[:-2].split():
                temp_clause.append(int(var))
                all_vars[int(var)].append(num)
            prepared_clauses.append(temp_clause)
            num = num + 1
    return prepared_clauses, all_vars, num_vars


def initialAssignations(num_vars, clauses):
    form = []
    sat_vars = []
    # assingation random incial i
    for i in range(num_vars + 1):
        if random.random() < 0.5:
            form.append(i)
        else:
            form.append(-i)
    # ficar valors del numero de variables que satisfa la asignació random
    for i in clauses:
        sat_vars.append(0)
    for i, clause in enumerate(clauses):
        for var_tmp in clause:
            if form[abs(var_tmp)] == var_tmp:
                sat_vars[i] += 1
    return form, sat_vars


def choseClause(unsat_clauses):
    lower = MAX
    for cl in unsat_clauses:
        count = len(cl)
        if count <= lower:
            lower = len(cl)
            unsat_clause = cl
    return unsat_clause


def choseVar(sat_vars, all_vars, unsat_clause):
    lower = MAX
    best_vars = []
    tmp = 0
    check = 0
    for var in unsat_clause:
        count = 0
        check = 0
        for i in all_vars[-var]:
            if sat_vars[i] == 1:
                count += 1
        if count < lower:
            lower = count
            best_vars = [var]
            tmp = var
        elif count == lower:
            if best_vars == [] and check == 0:
                best_vars.append(tmp)
            check = 1
            best_vars.append(var)
    if lower > 0 and random.random() < 0.425:  # fixan la possibilitat ω -> 0.425 (la mes optima)
        best_vars = unsat_clause

    return random.choice(best_vars)


def choseSwap(form, sat_vars, all_vars, unsat_clauses):

    # triar clausula a cambiar
    unsat_clause = choseClause(unsat_clauses)

    # refer clausules agafan les que generen menys conflictes
    flip_val = choseVar(sat_vars, all_vars, unsat_clause)

    # fer el swap
    for i in all_vars[flip_val]:
        sat_vars[i] += 1
    for i in all_vars[-flip_val]:
        sat_vars[i] -= 1
    form[abs(flip_val)] *= -1

    return form, sat_vars


def solve(clauses, all_vars, num_vars, maxTries, maxFlips):
    flips = num_vars * maxFlips
    trys = num_vars * maxTries
    while trys != 0:
        # initial assignations to set the proper start values
        form, sat_vars = initialAssignations(num_vars, clauses)

        for _ in range(flips):
            # marcar invalides
            unsat_clauses = []
            for index, var_temp in enumerate(sat_vars):
                if not var_temp:
                    unsat_clauses.append(clauses[index])
            # es final?
            if not unsat_clauses:
                print("c MEH")
                print("s SATISFIABLE")
                print("v "+" ".join(map(str, form[1:])) + " 0")
                return 0
            # try wich val should be swaped
            form, sat_vars = choseSwap(form, sat_vars, all_vars, unsat_clauses)

        trys -= 1
    print("SOLUTION NOT FOUND")
    return 0


if __name__ == '__main__':
    clauses_prepared, all_vars, num_vars = prepare(open(sys.argv[1], "r"))
    solve(clauses_prepared, all_vars, num_vars, 5, 5)
