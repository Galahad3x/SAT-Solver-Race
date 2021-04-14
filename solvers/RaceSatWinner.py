#!/bin/python3

import sys
import random
import time
import os


class raceSatWinner:
    def getFormula(file):

        c = 0   # c will be our counter.
        f = []  # f will be our formula clauses.
        for l in file:  # l will be every single line in our file.
            if l[0] == 'c':
                pass
            elif l[0] == 'p':
                p, cnf, var, key = l.split()
                position_list = [[] for _ in range(2 * int(var) + 1)]
            else:
                clause = []
                for lit in l.split():
                    if int(lit) != 0:
                        clause.append(int(lit))
                        position_list[int(lit)].append(c)

                c += 1
                f.append(clause)

        return raceSatWinner(var, len(l.split()[:-1]), position_list, f)

    def __init__(self, var, num_claus, position_list, f):
        self.var = var
        self.num_claus = num_claus
        self.position_list = position_list
        self.f = f

    def interpretate_all(self):
        return [i if random.random() < 0.5 else -i for i in range(int(self.var) + 1)]

    def sat_literals(self, translator):

        good_literals = [0 for _ in self.f]

        for index, clause in enumerate(self.f):
            for literal in clause:
                if translator[abs(literal)] == literal:
                    good_literals[index] += 1

        return good_literals

    def sat_clauses(self, literal):
        return len(self.position_list[literal])

    def unsat_clauses(self, sat_literals):

        clauses = []
        for i, literal in enumerate(sat_literals):
            if not literal:
                clauses.append(i)
        return clauses

    def best_literal(self, clause, sat_literals):

        best = []
        min = 900 # We define min to 900 because we need a high number for it becoming a first value.
        for literal in clause:
            v = 0 # v will be our value variable.

            for index in self.position_list[-literal]:
                if sat_literals[index] == 1:
                    v += 1

            if min == v:
                best.append(literal)
            elif min > v:
                min = v
                best.clear()
                best.append(literal)

        if random.random() > 0.65 and min > 0:
            best = clause
        return random.choice(best)

    def update_all(self, literal, interpretation, sat_literals):

        for lit in self.position_list[literal]:
            sat_literals[lit] += 1

        for lit in self.position_list[-literal]:
            sat_literals[lit] -= 1
        interpretation[abs(literal)] *= -1

    def solver(self):

        max = int(self.var) * 4
        while True:
            interpretation = self.interpretate_all()
            sat_literals = self.sat_literals(interpretation)

            for i in range(max):
                unsat_clauses = self.unsat_clauses(sat_literals)
                if not unsat_clauses: return interpretation
                unsat_clause = self.f[random.choice(unsat_clauses)]
                best_literal = self.best_literal(unsat_clause, sat_literals)
                self.update_all(best_literal, interpretation, sat_literals)


def makeOutput(interpretation):
    out = 's SATISFIABLE \n'
    out += 'v '
    for i, v in enumerate(interpretation):
        if i > 0:
            if v > 0:
                out += str(i) + ' '
            else:
                out += '-' + str(i) + ' '
    out += '0'
    print(out)
    f = open("output.cnf", "w")
    f.write(out)
    f.close()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Use: %s <input_cnf_formula>" % sys.argv[0])
    try:
        path = str(sys.argv[1])
    except:
        sys.exit("ERROR: input_cnf_formula not a file (%s)." % sys.argv[1])
    if path[-4:] != '.cnf':
        sys.exit("ERROR: input_cnf_formula must be ended with .cnf")

    cnf = raceSatWinner.getFormula(open(path, 'r'))
    interpretation = cnf.solver()
    makeOutput(interpretation)
