#!/usr/bin/python3

# SAT Solver
# Joel Aumedes 48051307Y
# Joel Farré 78103400T

import sys
import random
import os


# Checks if a literal evaluates as True
def is_true(lit, intr):
	return (lit > 0 and intr is True) or (lit < 0 and intr is not True)


# Modelization of a formula as a list of clauses
class Formula:
	def __init__(self, clauses=None, num_vars=0, num_clauses=0):
		self.clauses = clauses
		self.num_vars = num_vars
		self.num_clauses = num_clauses
		self.neighbour_nums = min(getClauseLen(self.clauses[0]),50)
		self.max_tries=1500000

	# Check if an interpretation satisfies the formula
	def is_sat(self, interpretation=None):
		insats = 0
		if len(self.clauses) == 0:
			return True
		for cl in self.clauses:
			if not cl.is_sat(interpretation):
				insats += 1
		if insats == 0:
			return True, 0
		else:
			return False, len(self.clauses) - insats

	# Finds if a formula is SAT or UNSAT, and finds a model if possible
	def solve(self):
		interpretation = [None] * self.num_vars
		while not self.is_sat(interpretation):
			for cl in self.clauses:
				if cl.is_sat(interpretation):
					continue
				else:
					for lit in cl.literals:
						if lit > 0 and interpretation[abs(lit) - 1] is None:
							interpretation[abs(lit) - 1] = True
							break
					else:
						for lit in cl.literals:
							if lit < 0 and interpretation[abs(lit) - 1] is True:
								interpretation[abs(lit) - 1] = False
								break
						else:
							return None
		return interpretation
		
	def solve_steepest(self, interpretation=None, total_tries=0):
		if interpretation is None:
			interpretation = [None] * self.num_vars
		while total_tries < 150000:
			sat_val = self.is_sat(interpretation)
			if sat_val[0]:
				return interpretation
			else:
				best_inter_index = None
				best_res = sat_val
				for i in range(self.neighbour_nums):
					random_index = random.randint(0, len(interpretation) - 1)
					if interpretation[random_index] is not True:
						interpretation[random_index] = True
					else:
						interpretation[random_index] = False
					current_val = self.is_sat(interpretation)
					if current_val[0]:
						return interpretation
					elif current_val < best_res:
						best_inter_index = random_index
						best_res = current_val[1]
					if interpretation[random_index] is not True:
						interpretation[random_index] = True
					else:
						interpretation[random_index] = False
				if best_inter_index == None:
					total_tries += self.neighbour_nums
				else:
					if interpretation[best_inter_index] is not True:
						interpretation[best_inter_index] = True
					else:
						interpretation[best_inter_index] = False
					total_tries += self.neighbour_nums
				


# Modelization of a clause as a list of literals
class Clause:
	def __init__(self, literals=None):
		self.literals = literals

	# Check if an interpretation satisfies the clause
	def is_sat(self, interpretation=None):
		if len(self.literals) == 0:
			return False
		for lit in self.literals:
			# print(lit, abs(lit) - 1, interpretation[abs(lit) - 1])
			if is_true(lit, interpretation[abs(lit) - 1]):
				return True
		return False


# Returns length of a clause
def getClauseLen(cl):
	return len(cl.literals)


# Read the input file into a formula
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
				clauses.append(Clause(list(sorted([int(elem) for elem in ln]))))

	clauses = list(set(clauses))
	return Formula(list(sorted(clauses, key=getClauseLen, reverse=True)), num_vars, num_clauses)


# Prints the solution found in the correct format
def printSolution(result):
	print("c J&J Solver")
	if result is None:
		print("s UNSATISFIABLE")
	else:
		print("s SATISFIABLE")
		print("v " + " ".join(transcriptSolution(result)))


# Creates a list of literals from a list of booleans
def transcriptSolution(result):
	solution = []
	for i, elem in enumerate(result):
		if elem is not True:
			solution.append(str(-(i + 1)))
		elif elem is True:
			solution.append(str(i + 1))
	solution.append("0")
	return solution


# Main program
if __name__ in "__main__":
	random.seed()
	if len(sys.argv) < 2:
		print("ERROR: Atributs")
		sys.exit(-1)
	formula = read_file(sys.argv[1])

	result = formula.solve_steepest()

	printSolution(result)
