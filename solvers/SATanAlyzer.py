#!/usr/bin/python3

import sys
import random
import os


# Participants: Joel Solaní Núñez (48255828B)
# Solver name: SATanAlyzer


class Clause():
    """A Boolean clause"""

    def __init__(self, literals):
        """
		Initialization
		length: Clause length
		lits: List of literals
		"""
        # self.length = len(literals)
        self.lits = None
        self.append_literals(literals)

    def append_literals(self, literals):
        """Appends literals (reads one clause)"""
        self.lits = []
        while len(self.lits) < len(literals) + 2:  # Set the variables of the clause
            new_lit = int(literals.pop())  # "Gets the first literal from the clause"
            self.lits.append(new_lit)  # Add it to the clause

    def show(self):
        """Prints a clause to the stdout"""
        sys.stdout.write("%s\n" % " ".join(str(lit) for lit in self.lits))

    def copy(self):
        new_clause = []
        for i in range(len(self.lits)):
            new_clause.append(self.lits[i])
        return new_clause


class CNF():
    """A CNF formula"""

    def __init__(self, cnf_file):
        """
		Initialization
		num_vars: Number of variables
		num_clauses: Number of clauses
		clauses: List of clauses
		"""
        self.num_vars = 0
        self.num_clauses = 0
        self.clauses = None
        self.append_clauses(cnf_file)

    def append_clauses(self, cnf_file):
        """Appends clauses (reads the formula)"""
        self.clauses = []
        instance = open(cnf_file, "r")
        for line in instance:  # Read the file
            if line[0] in ["c"]:  # Pass comments
                continue
            if line[0] in ["p"]:  # Check program line
                self.num_vars = int(line.split(' ')[2])
                self.num_clauses = int(line.split(' ')[3])
                continue
            literals = list(line.split())
            literals.pop()  # Remove last 0
            clause = Clause(literals).copy()
            self.clauses.append(clause)
        # print(self.clauses)

    """def copy(self):
        clauses = []
        for clause in self.clauses:
            clauses.append(clause)
        return clauses"""

    def show(self):
        """Prints the formula to the stdout"""
        # sys.stdout.write("c Random CNF formula\n")
        # sys.stdout.write("p cnf %d %d\n" % (self.num_vars, self.num_clauses))
        for clause in self.clauses:
            print(clause)


class Interpretation():
    """An interpretation is an assignment of the possible values to variables"""

    def __init__(self, clauses, num_l):
        """
		Initialization
		clauses: The problem to solve (CNF class)
		num_literals: Number of variables to encode the problem
		literals:
		assigned_values:
		"""
        self.clauses = clauses.copy()
        self.num_literals = num_l
        self.literals = []
        self.assigned_values = []
        self.getcost = None
        self.get_random_interpretation()

    def get_random_interpretation(self):  # Used to get the first interpretation (start point)
        for lit in range(self.num_literals + 2):  # First "v" then n literals and Last 0
            if lit == 0:
                self.assigned_values.append("v")
            elif lit == self.num_literals + 1:
                self.assigned_values.append(0)
            else:
                if random.random() < 0.5:
                    self.assigned_values.append(lit)
                else:
                    self.assigned_values.append(lit * -1)

    def get_all_neighbors(self):
        neighbors = []
        for value in range(1, len(self.assigned_values) - 1):  # Avoid first element ("v") and last element (0)
            new_neighbor = self.copy()
            new_neighbor.assigned_values[value] *= -1  # Flip literal
            neighbors.append(new_neighbor)
            # print("neighbor:")
            # new_neighbor.show()
            # new_neighbor.cost()
        return neighbors

    def select_a_neighbor(self):
        best_cost = self.cost()
        best_neighbor = 0
        neighbors = self.get_all_neighbors()
        for inb, nb in enumerate(neighbors):
            if nb.cost() < best_cost:  # Gets a better neighbor
                best_neighbor = inb
                best_cost = nb.getcost
        if best_cost == self.getcost and best_cost > 0:  # if the best_cost is 0 we already have the solution
            # Perform a Random Walk selecting a random neighbor
            best_neighbor = random.randint(0, len(neighbors) - 1)
        # print(self.assigned_values)
        # print(self.cost())
        # print(neighbors[best_neighbor].assigned_values)
        # print(best_cost)
        # print(neighbors[best_neighbor].cost())
        return neighbors[best_neighbor]

    def cost(self):
        # print("cost")
        # print(self.clauses)
        # print(self.assigned_values)
        cost = len(self.clauses)
        for clause in self.clauses:
            for value in clause:
                if value == self.assigned_values[abs(value)]:
                    cost -= 1
                    break
        self.getcost = cost
        return cost

    def copy(self):
        # Copy the values of this instance of the class Interpretation to another instance
        interpretation = Interpretation(self.clauses, self.num_literals)
        interpretation.literals = self.literals.copy()
        interpretation.assigned_values = self.assigned_values.copy()
        return interpretation

    def show(self):
        sys.stdout.write("c Cost of the best solution found: " + str(self.cost()) + "\n")
        if self.getcost == 0:
            sys.stdout.write("s SATISFIABLE\n")
        else:
            sys.stdout.write("s UNKNOWN\n")
        sys.stdout.write(' '.join(map(str, self.assigned_values)) + "\n")


class Solver():
    """The class Solver implements an algorithm to solve a given problem instance"""

    def __init__(self, problem):
        """
		Initialization
		problem: An instance of a problem
		best_sol: Best solution found so far
		best_cost: Cost of the best solution
		"""
        self.problem = problem
        self.best_sol = None
        self.best_cost = None

    def solve(self, max_tries=100, max_restarts=50):
        formula = CNF(self.problem)
        curr_sol = Interpretation(formula.clauses, formula.num_vars).copy()  # Random initial interpretation
        self.best_sol = curr_sol.copy()  # Makes that if the first interpretation is cost 0 we have it instead of None
        self.best_cost = curr_sol.cost()
        for curr_rest in range(max_restarts):
            for curr_try in range(max_tries):
                curr_sol = curr_sol.select_a_neighbor()
                if curr_sol.cost() < self.best_cost:
                    self.best_sol = curr_sol.copy()
                    self.best_cost = curr_sol.getcost
                    if self.best_sol == 0:
                        return self.best_sol
        return self.best_sol


# Main
if __name__ == '__main__':
    # Check parameters
    if len(sys.argv) < 2:
        sys.exit("Use: %s <N> [<input_cnf_formula>]" % sys.argv[0])

    if os.path.isfile(sys.argv[1]):  # Checks the argument is a file (not only .cnf)
        benchmark_file = sys.argv[1]
    else:
        sys.exit("ERROR: Argument must be a file (if possible cnf file) (%s)." % sys.argv[1])

    # Initialize random seed (current time)
    random.seed(None)

    # proves
    # formula = CNF(benchmark_file)
    # formula.show()
    # I = Interpretation(formula.clauses, formula.num_vars)
    # I.show()
    # I.get_all_neighbors()
    # I.show()
    # I.cost()
    # I.select_a_neighbor()

    # Create a solver instance with the problem to solve
    solver = Solver(benchmark_file)
    # Solve the problem and get the best solution found
    best_sol = solver.solve()
    # Show the best solution found
    best_sol.show()
