#!/usr/bin/python3

# SAT Solver
# Joel Aumedes 48051307Y
# Joel Farré 78103400T

import sys


def is_true(lit, intr):
	return (lit > 0 and intr is True) or (lit < 0 and intr is not True)


class Formula:
	def __init__(self, clauses=None, num_vars=0, num_clauses=0):
		self.clauses = clauses
		self.num_vars = num_vars
		self.num_clauses = num_clauses

	def is_sat(self, interpretation=None):
		if len(self.clauses) == 0:
			return True
		for cl in self.clauses:
			if not cl.is_sat(interpretation):
				return False
		return True

	def solve(self):
		interpretation = [None] * self.num_vars
		while not self.is_sat(interpretation):
			for cl in self.clauses:
				if cl.is_sat(interpretation):
					continue
				else:
					for lit in cl.literals:
						if lit < 0 and interpretation[abs(lit) - 1] is True:
							interpretation[abs(lit) - 1] = False
							break
						elif lit > 0 and interpretation[abs(lit) - 1] is None:
							interpretation[abs(lit) - 1] = True
							break
					else:
						return None
		return interpretation


class Clause:
	def __init__(self, literals=None):
		self.literals = literals

	def is_sat(self, interpretation=None):
		if len(self.literals) == 0:
			return False
		for lit in self.literals:
			# print(lit, abs(lit) - 1, interpretation[abs(lit) - 1])
			if is_true(lit, interpretation[abs(lit) - 1]):
				return True
		return False

def getClauseLen(cl):
	return len(cl.literals)

def read_file(filename):
	if filename is None or not filename.endswith(".cnf"):
		print("ERROR: Nom de fitxer dolent")
		sys.exit(-1)
	clauses = []
	with open(filename, "r") as f:
		for line in f.readlines():
			ln = line.rstrip('\n').split(" ")
			if ln[0].startswith("c"):
				continue
			if ln[0].startswith("p"):
				num_vars = int(ln[2])
				num_clauses = int(ln[3])
			else:
				ln = ln[:-1]
				clauses.append(Clause([int(elem) for elem in ln]))

	return Formula(list(sorted(clauses, key=getClauseLen, reverse=True)), num_vars, num_clauses)


def prova():
	my_c = Clause([1, 2])
	my_c2 = Clause([1, -2])
	my_f = Formula([my_c, my_c2])
	print(my_f.is_sat([True, True]))
	print(my_f.is_sat([None, True]))


def printSolution(result):
	print("c J&J Solver")
	if result is None:
		print("s UNSATISFIABLE")
	else:
		print("s SATISFIABLE")
		print("v " + " ".join(transcriptSolution(result)))


def transcriptSolution(result):
	solution = []
	for i, elem in enumerate(result):
		if elem is not True:
			solution.append(str(-(i + 1)))
		elif elem is True:
			solution.append(str(i + 1))
	solution.append("0")
	return solution


if __name__ in "__main__":
	if len(sys.argv) < 2:
		print("ERROR: Atributs")
		sys.exit(-1)
	formula = read_file(sys.argv[1])
	# Comprovar casos extrems (Formula buida es SAT, Formula amb clausula buida es INSAT)
	# Resoldre amb algoritme
	result = formula.solve()

	# Printar solucio
	printSolution(result)
