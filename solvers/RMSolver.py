#!/usr/bin/python3

import sys
import random
import time
import os

class RMSolver:
	def __init__(self,variables,clause_len,literal_position,formula):
		self.variables = variables
		self.claus_len = clause_len
		self.literal_position = literal_position
		self.formula = formula

	def get_sat_literals(self,interpretation):
		true_sat_lit = [0 for _ in self.formula]
		for index, clause in enumerate(self.formula):
			for lit in clause:
				if interpretation[abs(lit)] == lit:
					true_sat_lit[index] += 1
		return true_sat_lit

	def get_initial_interpretation(self):
		#Returns a list with an initial interpretation
		return [i if random.random() < 0.5 else -i for i in range(int(self.variables) + 1)]

	def satisfied_clauses(self, literal):
		#Returns the length of the clause specified by the literal
		return len(self.literal_position[literal])

	def check_best_literal_to_flip(self,literals):
		#Checks the best literal to be flipped
		best = 0
		bestvalue = 0
		for lit in literals:
			result1 = self.satisfied_clauses(lit)
			reslut2 = self.satisfied_clauses(-lit)
			result = abs(result1-reslut2)

			if result>=bestvalue:
				best = lit
				bestvalue = result

		return bestvalue

	def get_unsat_clauses(self,sat_literals):
		#Returns unsatisfiable clauses
		unsat_clauses = []
		for i, lit in enumerate(sat_literals):
			if not lit: 
				unsat_clauses.append(i) 

		return unsat_clauses

	def best_literal(self,clause,sat_literals):
		best_literal = []
		min_value = 999999

		for lit in clause:				
			value = 0				
			for index in self.literal_position[-lit]:
				if sat_literals[index] == 1:
					value+=1
			
			if min_value == value:
				best_literal.append(lit)

			elif min_value > value:
				min_value = value
				best_literal.clear()
				best_literal.append(lit)

		if random.random() > 0.65 and min_value>0: best_literal = clause
		return random.choice(best_literal)

	def update(self,lit,interpretation,sat_literals):
		#Update interpretation and literals
		for i in self.literal_position[lit]: 
			sat_literals[i] += 1
		for i in self.literal_position[-lit]: 
			sat_literals[i] -= 1

		interpretation[abs(lit)]*=-1

	def solve(self):
		max_flips = int(self.variables)*4
		
		while True:
			interpretation = self.get_initial_interpretation()
			sat_literals = self.get_sat_literals(interpretation)

			for i in range(max_flips):
				unsat_clauses = self.get_unsat_clauses(sat_literals)
				
				if not unsat_clauses: 
					return interpretation
				
				unsat_clause = self.formula[random.choice(unsat_clauses)]
				bestLiteral = self.best_literal(unsat_clause,sat_literals) 	
			
				self.update(bestLiteral,interpretation,sat_literals)


def generateSolver(file):
	count = 0
	formula = []
	for line in file:
		if line.startswith('c'):
			pass
		elif line.startswith('p'):
			p, cnf, num_variables, num_clauses = line.split() 
			lit_position = [[] for _ in range(2*int(num_variables)+1)]
		else:
			clause = []
			for lit in line.split():
				if int(lit) != 0:
					clause.append(int(lit))
					lit_position[int(lit)].append(count)
		
			count+=1
			formula.append(clause)

	#print("CNF FORMULA = ", formula)
	return RMSolver(num_variables,len(line.split()[:-1]),lit_position,formula)


def print_results(result):
	message = 's SATISFIABLE \n'
	message +='v '

	for i,val in enumerate(result): 
		if i>0:
			if val>0: message+=str(i)+' '
			else: 
				message+='-'+str(i)+' '

	message+='0'
	print(message) #Write the result in the terminal
	output_file = open("output.cnf", "w") #Write the result in the file "output.cnf"
	output_file.write(message)
	output_file.close()


if __name__ == "__main__":

	if len(sys.argv) != 2:
		sys.exit("Use: ./RMSolver.py <input_cnf_formula>")

	formula = str(sys.argv[1])
	if not formula.endswith('.cnf'):
		sys.exit("ERROR: input_cnf_formula must end with .cnf")

	Solver = generateSolver(open(formula, 'r'))
	result = Solver.solve()
	print_results(result)