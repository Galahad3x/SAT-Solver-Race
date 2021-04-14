"""
Miguel Ángel Barraza Sobrino
Didac Colominas Abalde
Pau Escolà Barragan
"""

import sys
import random
import time

def read_benchmark(input_cnf_formula):
  n_vars = -1
  n_clauses = -1
  clauses = []

  with open(input_cnf_formula,"r") as benchmark:
    for line in benchmark:
      #Ignore comments
      if line[0] in ["c"]:
        continue

      #Read problem line
      if line[0]=="p":
        splitted_line = line.split()
        n_vars = int(splitted_line[2])
        n_clauses = int(splitted_line[3])
        continue

      #Read clauses
      clause = list(map(int,line.split()))
      clause.pop()
      clauses.append(clause)

  return Problem(n_vars,n_clauses,clauses)


class Problem():

  def __init__(self,n_vars, n_clauses,clauses):
    self.n_vars = n_vars
    self.n_clauses = n_clauses
    self.clauses = clauses
    self.solution = None
    self.literals_list = self.compute_literals_list(clauses,n_vars)
  
  #List that tracks in which clauses a literal appears
  def compute_literals_list(self,clauses,n_vars):
    literals_list = [[] for i in range((n_vars*2)+1)]
    for index,clause in enumerate(clauses):
      for literal in clause:
        literals_list[literal].append(index)
    return literals_list

  #walksat algorythm implementation
  def walksat(self,max_tries=10, max_flips=10, prob=0.5):



    for i in range(max_tries):

      if i==0:
        interpretation = self.allocation()
      else:
        interpretaion = self.random_interpretation()

      

      #We compute the satisfied literals of each clause of the generated interpretation 
      satisfied_literals_list = self.compute_satisfied_list(interpretation)


      for j in range(max_flips): 

        #List of unsat clauses
        unsatisfied_clauses = [clause for clause, sat_literal in enumerate(satisfied_literals_list) if not sat_literal]
        
        #If the interpretation is sat we save it and return it
        if len(unsatisfied_clauses)==0:
          self.solution = interpretation
          return interpretation
        
        #Select an insat clause
        insat_clause_index = random.choice(unsatisfied_clauses)
        insat_clause = self.clauses[insat_clause_index]

        #Compute the literals that generate less brokens and the min broken
        best_vars, min_broken = self.broken(insat_clause, satisfied_literals_list)

        #We take an var to flip according the algorythm (walksat)
        var_to_flip = self.select_var(best_vars,min_broken,insat_clause,prob)

        self.flip_literal(interpretation,satisfied_literals_list,var_to_flip)
            
    return None

  #Generates a random interpretation of the problem, each position in the array represents the value of a variable, it can be the same number in negative or positive
  def random_interpretation(self):
    interpretation = []
    interpretation.append(0) #To make variable 'i' represented at potition 'i'
    for var in range(self.n_vars):
      interpretation.append(random.choice([len(interpretation),-len(interpretation)]))
    return interpretation

  def allocation(self,pad = 1.8, nad = 0.56):
    interpretation = []
    interpretation.append(0)
    for var in range(1,self.n_vars+1):
      if len(self.literals_list[-var]) == 0:
        vad = pad+1
      else:
        vad = len(self.literals_list[var])/len(self.literals_list[-var])

      if vad>pad:
        interpretation.append(var)
      elif vad<nad:
        interpretation.append(-var)
      else:
        interpretation.append(random.choice([var,-var]))
    return interpretation

  #Compute the satisfied list.    
  def compute_satisfied_list(self,interpretation):
    satisfied_literals_list = []
    for clause in self.clauses:
      clause_score = self.check_clause(clause,interpretation)
      satisfied_literals_list.append(clause_score)
    return satisfied_literals_list

  #Returns the number of satisfied literals in a clause      
  def check_clause(self,clause, interpretation):
    score = 0
    for var in clause:
      if var == interpretation[abs(var)]:
        score += 1
    return score

  #Compute the literals that generate less brokens
  def broken(self, clausula, satisfied_literals_list,prob=0.5):
    best_vars=[]
    min_broken = self.n_clauses #inicializo en el peor de los casos
    for var in clausula:
      count = 0
      for clause in self.literals_list[-var]:
        if satisfied_literals_list[clause] == 1:
          count+=1
      if count < min_broken:
        min_broken = count
        best_vars=[]
        best_vars.append(var)
      elif count == min_broken:
        best_vars.append(var)

    return best_vars, min_broken

  #Compute all the changes in the satisfied literals list and in the interpretation that flipping a literals does
  def flip_literal(self,interpretation,satisfied_literals_list,var_to_flip):
    for clause in self.literals_list[var_to_flip]:
      satisfied_literals_list[clause] += 1

    for clause in self.literals_list[-var_to_flip]:
      satisfied_literals_list[clause] -= 1

    interpretation[abs(var_to_flip)] *= -1

  #Select the a variable to flip according to the walksat algorythm
  def select_var(self,best_vars,min_broken,insat_clause,prob):    
    if min_broken != 0 and random.random()<prob:
      var_to_flip = random.choice(insat_clause)
    else:
      var_to_flip = random.choice(best_vars)
    return var_to_flip

  def print_solution(self):
    if self.solution == None :
      print ("No result")
      return None
    print("s SATISFIABLE")
    print("v ",end="")
    for var in self.solution:
      if var == 0:
        continue
      print(str(var)+" ",end="")
    print("0")
    
class taboo_list():
  def __init__(self,n_vars):
    self.list = []

if __name__=='__main__':
  #Check and read parameters
  if (len(sys.argv) != 2):
	  sys.exit("Use: Solver <input_cnf_formula>")

  input_cnf_formula = sys.argv[1]

  #Set seed to actual time
  random.seed(time.time()*1000)

  #Read the input cnf formula
  problem = read_benchmark(input_cnf_formula)

  #Solve the formula
  problem.walksat(5,30000)
  #Print the results
  problem.print_solution()
