# SAT Solver
# Joel Aumedes 48051307Y
# Joel Farré 78103400T

import sys


def is_true(lit, intr):
	return (lit > 0 and intr) or (lit < 0 and not intr) or (lit < 0 and intr is None)


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
			if is_true(lit, interpretation[abs(lit) - 1]):
				return True
		return False


def read_file(filename):
	if filename is None or not filename.endswith(".cnf"):
		print("ERROR: Nom de fitxer dolent")
		sys.exit(-1)
	clauses = []
	with open(filename, "r") as f:
		for line in f.readlines():
			ln = line.rstrip(' 0 \n').split(" ")
			if ln[0].startswith("c"):
				continue
			if ln[0].startswith("p"):
				num_vars = int(ln[2])
				num_clauses = int(ln[3])
			else:
				clauses.append(Clause([int(elem) for elem in ln]))
	return Formula(clauses, num_vars, num_clauses)


def prova():
	my_c = Clause([1, 2])
	my_c2 = Clause([1, -2])
	my_f = Formula([my_c, my_c2])
	print(my_f.is_sat([True, True]))
	print(my_f.is_sat([None, True]))


if __name__ in "__main__":
	if len(sys.argv) < 2:
		print("ERROR: Atributs")
		sys.exit(-1)
	formula = read_file(sys.argv[1])
	# Comprovar casos extrems (Formula buida es SAT, Formula amb clausula buida es INSAT)
	# Resoldre amb algoritme
	result = formula.solve()

	# Printar solucio
	print(result)
