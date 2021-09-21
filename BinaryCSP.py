from collections import deque
import utils
"""
	Base class for unary constraints
	Implement isSatisfied in subclass to use
"""
class UnaryConstraint:
	def __init__(self, var):
		self.var = var

	def isSatisfied(self, value):
		utils.raiseNotDefined()

	def affects(self, var):
		return var == self.var


"""
	Implementation of UnaryConstraint
	Satisfied if value does not match passed in paramater
"""
class BadValueConstraint(UnaryConstraint):
	def __init__(self, var, badValue):
		self.var = var
		self.badValue = badValue

	def isSatisfied(self, value):
		return not value == self.badValue

	def __repr__(self):
		return 'BadValueConstraint (%s) {badValue: %s}' % (str(self.var), str(self.badValue))


"""
	Implementation of UnaryConstraint
	Satisfied if value matches passed in paramater
"""
class GoodValueConstraint(UnaryConstraint):
	def __init__(self, var, goodValue):
		self.var = var
		self.goodValue = goodValue

	def isSatisfied(self, value):
		return value == self.goodValue

	def __repr__(self):
		return 'GoodValueConstraint (%s) {goodValue: %s}' % (str(self.var), str(self.goodValue))


"""
	Base class for binary constraints
	Implement isSatisfied in subclass to use
"""
class BinaryConstraint:
	def __init__(self, var1, var2):
		self.var1 = var1
		self.var2 = var2

	def isSatisfied(self, value1, value2):
		utils.raiseNotDefined()

	def affects(self, var):
		return var == self.var1 or var == self.var2

	def otherVariable(self, var):
		if var == self.var1:
			return self.var2
		return self.var1


"""
	Implementation of BinaryConstraint
	Satisfied if both values assigned are different
"""
class NotEqualConstraint(BinaryConstraint):
	def isSatisfied(self, value1, value2):
		if value1 == value2:
			return False
		return True

	def __repr__(self):
	    return 'BadValueConstraint (%s, %s)' % (str(self.var1), str(self.var2))


class ConstraintSatisfactionProblem:
	"""
	Structure of a constraint satisfaction problem.
	Variables and domains should be lists of equal length that have the same order.
	varDomains is a dictionary mapping variables to possible domains.
	Args:
		variables (list<string>): a list of variable names
		domains (list<set<value>>): a list of sets of domains for each variable
		binaryConstraints (list<BinaryConstraint>): a list of binary constraints to satisfy
		unaryConstraints (list<BinaryConstraint>): a list of unary constraints to satisfy
	"""
	def __init__(self, variables, domains, binaryConstraints = [], unaryConstraints = []):
		self.varDomains = {}
		self.variables: variables = variables
		self.varDomains: dict[variables, dict[domains]] = domains
		self.binaryConstraints = binaryConstraints
		self.unaryConstraints = unaryConstraints

	def __repr__(self):
	    return '---Variable Domains\n%s---Binary Constraints\n%s---Unary Constraints\n%s' % ( \
	        '' + str(self.varDomains), \
	        ''.join([str(e) + '\n' for e in self.binaryConstraints]), \
	        ''.join([str(e) + '\n' for e in self.binaryConstraints]))


class Assignment:
	"""
	Representation of a partial assignment.
	Has the same varDomains dictionary stucture as ConstraintSatisfactionProblem.
	Keeps a second dictionary from variables to assigned values, with None being no assignment.
	Args:
		csp (ConstraintSatisfactionProblem): the problem definition for this assignment
	"""
	def __init__(self, csp):
		self.varDomains = {}
		for var in csp.varDomains:
			self.varDomains[var] = set(csp.varDomains[var])
		self.assignedValues = { var: None for var in self.varDomains }

	"""
	Determines whether this variable has been assigned.
	Args:
		var (string): the variable to be checked if assigned
	Returns:
		boolean
		True if var is assigned, False otherwise
	"""
	def isAssigned(self, var):
		return self.assignedValues[var] != None

	"""
	Determines whether this problem has all variables assigned.
	Returns:
		boolean
		True if assignment is complete, False otherwise
	"""
	def isComplete(self):
		for var in self.assignedValues:
			if not self.isAssigned(var):
				return False
		return True

	"""
	Gets the solution in the form of a dictionary.
	Returns:
		dictionary<string, value>
		A map from variables to their assigned values. None if not complete.
	"""
	def extractSolution(self):
		if not self.isComplete():
			return None
		return self.assignedValues

	def __repr__(self):
	    return '---Variable Domains\n%s---Assigned Values\n%s' % ( \
	        ''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]), \
	        ''.join([str(e) + ':' + str(self.assignedValues[e]) + '\n' for e in self.assignedValues]))



####################################################################################################


"""
	Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
	Do not assign value to var. Only check if this value would be consistent or not.
	If the other variable for a constraint is not assigned, then the new value is consistent with the constraint.
	Args:
		assignment (Assignment): the partial assignment
		csp (ConstraintSatisfactionProblem): the problem definition
		var (string): the variable that would be assigned
		value (value): the value that would be assigned to the variable
	Returns:
		boolean
		True if the value would be consistent with all currently assigned values, False otherwise
"""
def consistent(assignment, csp, var, value):
	currentBinaryConstraints = csp.binaryConstraints #stores the current binary constraints of passed constraint satisfaction problem
	for constraint in currentBinaryConstraints: #index through every constraint in current binary constraints
		isAffected = constraint.affects(var) # bool if constraint has an impact on variable
		if(isAffected): # if the constraint has an impact on the variable
			if(value == assignment.assignedValues[constraint.otherVariable(var)]): #if current value remains consistent with all other assignments
				return False # false if not
	return True # true if so


"""
	Recursive backtracking algorithm.
	A new assignment should not be created. The assignment passed in should have its domains updated with inferences.
	In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
	the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.
	Examples of the functions to be passed in:
	orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
	selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
	inferenceMethod: noInferences, maintainArcConsistency, forwardChecking
	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
		orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
		selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
	Returns:
		Assignment
		A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod):
	# follows pseudocode in ch.6.3 of book
	isFinished = assignment.isComplete()  #bool if current assignment is finished or not
	#PSEUDOCODE: if assignment is complete
	if(isFinished == True):
		return assignment #then return assignment
	#PSEUDOCODE: var <-- SELECT-UNASSIGNED-VARIABLE(csp)
	currentVariable = selectVariableMethod(assignment, csp) #returns variable method for current assignment
	#-------------portion of code for recursion-------------------
	if(currentVariable == None): #if variable is none, stop
		return None # no solution exists
	else:
		#PSEUDOCODE: for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do
		for currentValue in orderValuesMethod(assignment, csp, currentVariable):
			#PSEUDOCODE: if value is consistent with assignment then
			if(consistent(assignment, csp, currentVariable, currentValue)):
				# PSEUDOCODE: add {var = value} to assignment
				assignment.assignedValues[currentVariable] = currentValue # adds the current value at the current variable to the assigned values
				# PSEUDOCODE:  result <-- BACKTRACK(assignent, csp)
				recursiveProduct = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
				# PSEUDOCODE: if result != failure then
				if (recursiveProduct != None):
					# PSEUDOCODE: return result
					return recursiveProduct
				# PSEUDOCODE: remove {var = value} from assignment
				assignment.assignedValues[currentVariable] = None
	return None # no solution exists


"""
	Uses unary constraints to eleminate values from an assignment.
	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
	Returns:
		Assignment
		An assignment with domains restricted by unary constraints. None if no solution exists.
"""
def eliminateUnaryConstraints(assignment, csp):
	domains = assignment.varDomains
	for var in domains:
		for constraint in (c for c in csp.unaryConstraints if c.affects(var)):
			for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)):
				domains[var].remove(value)
				if len(domains[var]) == 0:
				 	# Failure due to invalid assignment
				 	return None
	return assignment


"""
	Trivial method for choosing the next variable to assign.
	Uses no heuristics.
"""
def chooseFirstVariable(assignment, csp):
	for var in csp.varDomains:
		if not assignment.isAssigned(var):
			return var


"""
	Selects the next variable to try to give a value to in an assignment.
	Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.
	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
	Returns:
		the next variable to assign
"""
def minimumRemainingValuesHeuristic(assignment, csp):
	# MRV heuristic picks a variable that is most likely to cause failure, pruning the tree
	# If a variable X has not legal values left, the MRV heuristic will select X and failure
	# will be detected immediately-avoiding pointless searches through remaining variables
	nextVar = None # intializes the next variable to be returned to none
	domains = assignment.varDomains # grabs domain values of assignment
	affectCounter = [0, 0] # array used to count how much each variable affects binary constraints, 0th element is the current variable 1st element is the next
	dictionaryDomainTuples = domains.items() # since varDomains is a dictionary mapping variables to possible domains, the items method returns iterators through said dictionary for later use
	for currentVariable, currentDomain in dictionaryDomainTuples: # iterate through variable, domain tuples
		if (assignment.isAssigned(currentVariable) == True): # if current variable is already assigned
			continue # skip iteration
		else: # if current variable is not already assigned
			if (nextVar == None): # if nextVar unintialized or nextVar is nothing
				nextVar = currentVariable # set the next up variable to current variable
			else: # if it is not None
				if (len(domains[nextVar]) > len(currentDomain)): # if the length of the domain of the next variable is greater than that of the current variable
					nextVar = currentVariable # set next variable to current variable
				elif (len(domains[nextVar]) == len(currentDomain)): # if the lengths are equal
					if (currentVariable != nextVar): # and if they are not the same variable
						for cspBinaryConstraint in csp.binaryConstraints: # index through all binary constraints of the problem
							if cspBinaryConstraint.affects(currentVariable): # if the current binary constraint affects the current variable
								affectCounter[0] = affectCounter[0] + 1 # add one to the affect counter for current variable
							if cspBinaryConstraint.affects(nextVar): # if the current binary constraint affects the next variable
								affectCounter[1] = affectCounter[1] + 1 # add one to the affect counter for next variable
						if affectCounter[0] > affectCounter[1]: # if the current variable affects less than the next
							nextVar = currentVariable # set next to current
	return nextVar # return calculated variable


"""
	Trivial method for ordering values to assign.
	Uses no heuristics.
"""
def orderValues(assignment, csp, var):
	return list(assignment.varDomains[var])


"""
	Creates an ordered list of the remaining values left for a given variable.
	Values should be attempted in the order returned.
	The least constraining value should be at the front of the list.
	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable to be assigned the values
	Returns:
		list<values>
		a list of the possible values ordered by the least constraining value heuristic
"""
def leastConstrainingValuesHeuristic(assignment, csp, var):
# Once a variable has been selected, the algorithm must decide on the order in which to
# examine its values. For this,the least-constraining-value heuristic can be effective in some
# cases. It prefers the value that rules out the fewest choices for the neighboring variables in
# the constraint graph.
	values = list(assignment.varDomains[var]) # pulls the assignments domain for the passed variable and stores in a list
	binaryVariables, masterConstraints, resultant = list(), list(), list() # initializes 3 lists
	return lcvSorterHelper(assignment, csp, var, values, binaryVariables, masterConstraints, resultant) # returns value of helper function

# lcvSorterHelper sorts list of masterConstraints that are tied to variables in binaryConstraints which correlate to values in the assigned domain
# to represent total dependencies. This way, a list is generated that makes it easy to pick least constraining values
#-----------------------------------START OF lcvSorterHelper-------------------------------------------------------------------------------------------------------------------
def lcvSorterHelper(assignment, csp, var, values, binaryVariables, masterConstraints, resultant):
	SUM_INDEX = 0 # const for index of sum in the coupled list of masterConstraints
	VALUE_INDEX = 1 # const for index of value in the coupled list of masterConstraints
	for cspBinaryConstraint in csp.binaryConstraints: # for every binary constraint in the constraint satisfaction problem
		if (var != None and cspBinaryConstraint.affects(var) == True): # if the variable is not empty and the variable affects the binary constraint
			binaryVariables.append(cspBinaryConstraint.otherVariable(var)) # adds these constraints to the list
	for currentValue in values: # for all values in the assigned domain of passed variable
		sum = 0 # sum value initialized to 0
		for currentVariable in binaryVariables: # for all vaariables found that are not empty and affect binaryConstraints
			if (currentValue != None and currentValue in assignment.varDomains[currentVariable]): # if the current value is in the domain of the current variable
				sum += 1 # increase sum
		masterConstraints.append((sum,currentValue)) # add the couple of the currently found value and the total sum of all of its dependents
	masterConstraints.sort(key = lambda list: list[SUM_INDEX]) # sort the master constraints by order of their sum. Use of lamba key creates anonmyous function, referenced at this URL: https://www.w3schools.com/python/ref_list_sort.asp
	for currentList in masterConstraints: # for the couples in masterConstraints
		resultant.append(currentList[VALUE_INDEX]) # add all values to the resultant list
	return resultant # return final list of just values
#-----------------------------------END OF lcvSorterHelper--------------------------------------------------------------------------------------------------------------------------
"""
	Trivial method for making no inferences.
"""
def noInferences(assignment, csp, var, value):
	return set([])


"""
	Implements the forward checking algorithm.
	Each inference should take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
	inferences made should be reversed before ending the fuction.
	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable that has just been assigned a value
		value (string): the value that has just been assigned
	Returns:
		set<tuple<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def forwardChecking(assignment, csp, var, value):
	# 	One of the simplest forms of inference is called forward checking. Whenever a vari
	# able X is assigned, the forward-checking process establishes arc consistency for it: for each
	# unassigned variable Y that is connected to X by a constraint, delete from Y's domain any
	# value that is inconsistent with the value chosen for X. Because forward checking only does
	# arc consistency inferences, there is no reason to do forward checking if we have already done
	# arc consistency as a preprocessing step
	inferences = set([]) # intializes set of inferences
	domains = assignment.varDomains # grabs all doains from passed assignment
	seenVariables = list() # initalizes list to store all seen variables
	for cspBinaryConstraint in csp.binaryConstraints: # for all binary constraints in csp
		if(cspBinaryConstraint.affects(var)): # if this binary constraint affects this variable
			if (assignment.assignedValues[cspBinaryConstraint.otherVariable(var)] != None): # if assigned values at variable are not equal to None
				continue # skip iteration
			else: # if it is None
				swap = list(domains[cspBinaryConstraint.otherVariable(var)]) # creates list to swap out variables affected by constraints
				if value in swap: # if passed value is in the swap list
					if (len(swap) == 1): # if # of domain variables is 1
						for currentVariable in seenVariables: # for all seen variables
							assignment.varDomains[currentVariable].add(value) # adds var/value to domain assignment
						return None # returns none since length is 1
					else: # if greater than 1
						seenVariables.append(cspBinaryConstraint.otherVariable(var))
						inferences.add((cspBinaryConstraint.otherVariable(var),value))
						domains[cspBinaryConstraint.otherVariable(var)].remove(value)
	return inferences # return updated inferences

"""
	Recursive backtracking algorithm.
	A new assignment should not be created. The assignment passed in should have its domains updated with inferences.
	In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
	the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.
	Examples of the functions to be passed in:
	orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
	selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
	inferenceMethod: noInferences, maintainArcConsistency, forwardChecking
	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
		orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
		selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
		inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>): a function to specify what type of inferences to use
				Can be forwardChecking or maintainArcConsistency
	Returns:
		Assignment
		A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod):
	# follows pseudocode in ch.6.3 of book
	isFinished = assignment.isComplete()  #bool if current assignment is finished or not
	#PSEUDOCODE: if assignment is complete
	if(isFinished == True):
		return assignment #then return assignment
	#PSEUDOCODE: var <-- SELECT-UNASSIGNED-VARIABLE(csp)
	currentVariable = selectVariableMethod(assignment, csp) #returns variable method for current assignment
	#-------------portion of code for recursion-------------------
	if(currentVariable == None): #if variable is none, stop
		return None # no solution exists
	else:
		#PSEUDOCODE: for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do
		for currentValue in orderValuesMethod(assignment, csp, currentVariable):
			#PSEUDOCODE: if value is consistent with assignment then
			if(consistent(assignment, csp, currentVariable, currentValue)):
				#PSEUDOCODE: inferences <-- INFERENCE(csp, var, value)
				inferenceList = inferenceMethod(assignment, csp, currentVariable, currentValue) # stores inference method in inferenceList
				if (inferenceList == None): # if nothing is in inference list
					continue # skip iteration
				# PSEUDOCODE: add {var = value} to assignment
				assignment.assignedValues[currentVariable] = currentValue # adds the current value at the current variable to the assigned values
				# PSEUDOCODE:  result <-- BACKTRACK(assignent, csp)
				recursiveProduct = recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
				# PSEUDOCODE: if result != failure then
				if (recursiveProduct != None):
					# PSEUDOCODE: return result
					return recursiveProduct
				# PSEUDOCODE: add inferences to assignment
				for (currentInferenceVariable,currentInferenceValue) in inferenceList: # for all values & variables in inference list
					assignment.varDomains[currentInferenceVariable].add(currentInferenceValue) # add to assignment
				# PSEUDOCODE: remove {var = value} from assignment
				assignment.assignedValues[currentVariable] = None
	return None # no solution exists



"""
	Helper funciton to maintainArcConsistency and AC3.
	Remove values from var2 domain if constraint cannot be satisfied.
	Each inference should take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
	inferences made should be reversed before ending the fuction.
	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var1 (string): the variable with consistent values
		var2 (string): the variable that should have inconsistent values removed
		constraint (BinaryConstraint): the constraint connecting var1 and var2
	Returns:
		set<tuple<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def revise(assignment, csp, var1, var2, constraint):
	inferences = set([]) # intializes inferences to empty set
	VARIABLE_INDEX = 0 # const for index of variable in inference list couple
	VALUE_INDEX = 1 # const for index of value in inference list couple
	passedVar1 = var1 # for sake of naming conventions
	passedVar2 = var2 # for sake of naming conventions
	domain1 = assignment.varDomains[passedVar1] # stores domain from var 1
	domain2 = assignment.varDomains[passedVar2] # stores domain from var 2
	lengthDomain2 = len(domain2) # length of 2nd domain

	for currentVariable1 in domain2: # search through first variables in 2nd domain
		satisfiedBool = False # bool value if constraint is satisfied or not, resets each iteration
		for currentVariable2 in domain1: # search through second variables in 1st domain
			if (constraint.isSatisfied(currentVariable1, currentVariable2) == True): # if variable 1 and 2 of this iteration satisfy the constraint
				satisfiedBool = True # set satisfiedBool to True
		if(satisfiedBool == False): # not satisfied, add to list of inferences
			inferences.add((passedVar2, currentVariable1)) # update inferences
	for couples in inferences: # for all var pairs in inferences
		assignment.varDomains[couples[VARIABLE_INDEX]].remove(couples[VALUE_INDEX]) # removes inconsistent values
	if lengthDomain2 <= 0: # if the length of the 2nd domain is less than 1
		for couples in inferences: # for all var pairs in inferences
			assignment.varDomains[couples[VARIABLE_INDEX]].add(couples[VALUE_INDEX]) # goes through in reverse and adds to assignments
		return None # return none if length less than 1
	return inferences # return updated inferences


"""
	Implements the maintaining arc consistency algorithm.
	Inferences take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, and
	inferences made should be reversed before ending the fuction.
	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable that has just been assigned a value
		value (string): the value that has just been assigned
	Returns:
		set<<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def maintainArcConsistency(assignment, csp, var, value):
	# The problem is that it makes the current variable arc-consistent, but does not look ahead and
	#make all the other variables arc-consistent.The algorithm called MAC (for Maintaining Arc Consistency (MAC)) detects this
	#inconsistency
	# follows description in ch. 6.2.2 in textbook
	import queue # does not work ?
	VARIABLE_INDEX = 0 # const for index of variable in inference list couple
	VALUE_INDEX = 1 # const for index of value in inference list couple
	inferences = set([]) # intializes inferences to empty set
	deQueue = deque() # use deque because it is the closest thing I can get to work

	for cspBinaryConstraint in csp.binaryConstraints: # for every binary constraint
		if(cspBinaryConstraint.affects(var)): # if constraint affects var
			binConstraintVariable = cspBinaryConstraint.otherVariable(var) # saves binary constraint variable
			deQueue.append((var, binConstraintVariable, cspBinaryConstraint))
			# pushes the passed variable, the binary constraint variable, and the binary constraint itself on to queue
	while (value != None and len(deQueue) > 0): # while value is valid and the queue is not empty
		poppedVar, nextBinConstraintVariable, poppedConstraint = deQueue.pop() # pops off queue and stores values into 3 variables
		returnedRevise = revise(assignment, csp, poppedVar, nextBinConstraintVariable, poppedConstraint) # calls helper function revise, determines inconsistent values in passed variables returns altered inferences
		if(returnedRevise == None): # if returned inferences are None
			for currentINF in inferences: # for all current inferences in inferences
				currentVariable, currentValue = currentINF[VARIABLE_INDEX], currentINF[VALUE_INDEX] # fill values of current var and val
				assignment.varDomains[currentVariable].add(currentValue) # add to domain assignment
			return None # return empty
		else: # if returned inferences are not None
			if (len(returnedRevise) >= 1): # if the length of returned inferences is greater than or equal to 1
				for cspBinaryConstraint in csp.binaryConstraints: # for every binary constraint
					if (cspBinaryConstraint.affects(nextBinConstraintVariable)): # if this current binary constraint variable affects the next binary constraint variable
						deQueue.append((nextBinConstraintVariable,cspBinaryConstraint.otherVariable(nextBinConstraintVariable),cspBinaryConstraint)) # push to queue
				inferences = inferences.union(returnedRevise) # does a union with the returned inferences and pre existing inferences, since they are both sets
	return inferences # return updated inferences



"""
	AC3 algorithm for constraint propogation. Used as a preprocessing step to reduce the problem
	before running recursive backtracking.
	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
	Returns:
		Assignment
		the updated assignment after inferences are made or None if an inconsistent assignment
"""
def AC3(assignment, csp):
	# From there, AC-3 does constraint
	# propagation in the usual way, and if any variable has its domain reduced to the empty set, the
	# call to AC-3 fails and we know to backtrack immediately
	# follows description in ch. 6.2.2 in textbook
	import queue # does not work ?
	VARIABLE_INDEX = 0 # const for index of variable in inference list couple
	VALUE_INDEX = 1 # const for index of value in inference list couple
	inferences = set([]) # intializes inferences to empty set
	deQueue = deque() # use deque because it is the closest thing I can get to work



				# pushes the passed variable, the binary constraint variable, and the binary constraint itself on to queue
	while (len(deQueue) > 0): # while value is valid and the queue is not empty
		poppedVar, nextBinConstraintVariable, poppedConstraint = deQueue.pop() # pops off queue and stores values into 3 variables
		returnedRevise = revise(assignment, csp, poppedVar, nextBinConstraintVariable, poppedConstraint) # calls helper function revise, determines inconsistent values in passed variables returns altered inferences
		if(returnedRevise == None): # if returned inferences are None
			for currentINF in inferences: # for all current inferences in inferences
				currentVariable, currentValue = currentINF[VARIABLE_INDEX], currentINF[VALUE_INDEX] # fill values of current var and val
				assignment.varDomains[currentVariable].add(currentValue) # add to domain assignment
			return None # return empty
		else: # if returned inferences are not None
			if (len(returnedRevise) >= 1): # if the length of returned inferences is greater than or equal to 1
				for cspBinaryConstraint in csp.binaryConstraints: # for every binary constraint
					if (cspBinaryConstraint.affects(nextBinConstraintVariable)): # if this current binary constraint variable affects the next binary constraint variable
						deQueue.append((nextBinConstraintVariable,cspBinaryConstraint.otherVariable(nextBinConstraintVariable),cspBinaryConstraint)) # push to queue
				inferences = inferences.union(returnedRevise) # does a union with the returned inferences and pre existing inferences, since they are both sets
	return assignment # return assignment

"""
	Solves a binary constraint satisfaction problem.
	Args:
		csp (ConstraintSatisfactionProblem): a CSP to be solved
		orderValuesMethod (function): a function to decide the next value to try
		selectVariableMethod (function): a function to decide which variable to assign next
		inferenceMethod (function): a function to specify what type of inferences to use
		useAC3 (boolean): specifies whether to use the AC3 preprocessing step or not
	Returns:
		dictionary<string, value>
		A map from variables to their assigned values. None if no solution exists.
"""
def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic, selectVariableMethod=minimumRemainingValuesHeuristic, inferenceMethod=None, useAC3=True):
	assignment = Assignment(csp)

	assignment = eliminateUnaryConstraints(assignment, csp)
	if assignment == None:
		return assignment

	if useAC3:
		assignment = AC3(assignment, csp)
		if assignment == None:
			return assignment
	if inferenceMethod is None or inferenceMethod==noInferences:
		assignment = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
	else:
		assignment = recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
	if assignment == None:
		return assignment

	return assignment.extractSolution()