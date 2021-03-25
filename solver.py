# SAT Solver
# Joel Aumedes 48051307Y
# Joel Farré 69420777X

def is_true(lit, int):
	return (lit > 0 and int) or (lit < 0 and not int)

class Formula:
	def __init__(self, clauses=None):
		self.clauses = clauses

	def is_sat(self, interpretation=None):
		if len(self.clauses) == 0:
			return True
		for cl in self.clauses:
			if not cl.is_sat(interpretation):
				return False
		return True

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


def prova():
	my_c = Clause([1, 2])
	my_c2 = Clause([1, -2])
	my_f = Formula([my_c, my_c2])
	print(my_f.is_sat([True, True]))
	print(my_f.is_sat([False, True]))


if __name__ in "__main__":
	# Llegir fórmula del fitxer

	# Comprovar casos extrems (Formula buida es SAT, Formula amb clausula buida es INSAT)
	# Resoldre amb algoritme

	# Printar solucio
	pass
