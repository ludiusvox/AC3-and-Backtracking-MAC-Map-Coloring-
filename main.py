#!/usr/bin/env python
# MapColor.py
# Skeleton Code.
from __future__ import generators
from utils import *
from backtrack import *
from map import *
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import sudoku

# Imports
# ====================================
import networkx
import re

import numpy as np
import sys
import scipy
import copy

from scipy.sparse import coo_matrix

import argparse
import sys




"""
default sudokus' grid
"""


"""
solve
solves a sudoku based on its String grid
"""








# Data Structures for the Graph.
# =================================

class Variablex(object):
    """
    The Variables will be used to store
    the individual variables for our
    constraint problem.  Each one will be
    defined from the file and will store
    the total domain and the current
    domain.
    """

    def __init__(self, Name, Values):
        """
        Set the initial value for the variables.
        """

        # Set the name.
        self.Name = Name

        # The full domain for the values.
        self.FullDomain = Values








    def returnname(self):

        return self.Name
    def returnvalue(self):
        return self.FullDomain

    def assignValue(self, Val):
        """
        Assign a specific value to the variable by
        cutting the domain down to a single value.
        """
        self.CurrDomain = set([Val])


    def dropValue(self, Val):
        """
        Drop the specified value from
        the Current Domain.
        """
        self.CurrDomain.remove(Val)

    def restoreValue(self, Val):
        """
        Add in the value back into the
        current domain.  Raise an error
        if it is not in the primary.
        """
        self.CurrDomain.add(Val)

    def resetCurrDomain(self):
        """
        Restore the oroginal domain.
        """
        self.CurrDomain = copy.copy(self.FullDomain)


class ConstraintGraph(object):
    """
    The constraint graph class will store the
    individual variables and not equal constraints.
    """

    def __init__(self, Constraints, Variables):
        """
        Define the basic contents.
        """
        self.Graph = networkx.Graph()
        # Set storage for the variables and arcs.
        self.b = []


        self.Variables = Variables

        self.Constraints = set(Constraints)

        # The relationship can be used as a graph.





        # Iterate over the variables and
        # add them in by name as a dict.
        self.dict = dict(self.Variables)

        for Name in range(len(self.Variables)):
            self.Graph.add_nodes_from(self.dict)



        # Now add the constraint pairs as
        # tuples and in the graph so that
        # we can find them later.
        for (VarA, VarB) in Constraints:
            self.Graph.add_edge(VarA, VarB, nodetype=int)


        print("Edges is # for data confirmation " + str(self.Graph.number_of_edges()))


        #networkx.draw(self.Graph, with_exampleels=True, font_size=16)
        #plt.show()


    def returnvariables(self):
        values = []
        for key, value in self.dict.items():
            values.append(value)
        return values


    def isCompletenumerical(self):
        for Var in self.Variables:

            if (len(self.Variables.CurrDomain) != 1):
                return (False)
        self.A = networkx.adjacency_matrix(self.Graph)
        import numpy
        self.B = numpy.array(self.A)
        print(self.B)
        return self.B
    def isComplete(self):
        """
        Return True if this is complete, that is
        each variable has only one value remaining
        in its current domain.
        """

        self.A = networkx.adjacency_matrix(self.Graph)
        self.B = coo_matrix(self.A, dtype=np.int8).toarray()
        #print(self.B)
        #print(self.B.shape)

        return self.B
    def nodes(self):



        return self.Graph.nodes()











class Graph():

        def __init__(self, vertices):
            self.V = vertices
            self.graph = [[0 for column in range(vertices)] \
                          for row in range(vertices)]
            self.output = []
        # A utility function to check
        # if the current color assignment
        # is safe for vertex v
        def isSafe(self, v, colour, c):
            for i in range(self.V):
                if self.graph[v][i] == 1 and colour[i] == c:
                    return False
            return True

        # A recursive utility function to solve m
        # coloring  problem
        def graphColourUtil(self, m, colour, v):
            if v == self.V:
                return True

            for c in range(1, m + 1):
                if self.isSafe(v, colour, c) == True:
                    colour[v] = c
                    if self.graphColourUtil(m, colour, v + 1) == True:
                        return True
                    colour[v] = 0

        def graphColouring(self,m):
            colour = [0] * self.V
            if self.graphColourUtil(m, colour, 0) == None:
                return False

            # Print the solution
            print("Solution exist and Following are the assigned colours: ")

            for c in colour:
                self.output.append(c)
            return self.output





# Read in the constraint code.
# =================================
VAR_START = re.compile("^VARS")
VAR_END = re.compile("^ENDVARS")
VAR_ROW = re.compile("^(?P<Name>[A-Z]+) : (?P<Vals>[A-Za-z0-9 ]+)")
CONST_START= re.compile("^CONSTRAINTS")
CONST_END = re.compile("^ENDCONSTRAINTS")
CONST_ROW = re.compile("^(?P<Condition>[!=<>]+) (?P<Name>[A-Z]+) (?P<Name2>[A-Z]+)")

def readConstraintGraph(InFile):
    """
    Read in the constraint graph.  This
    relies on the regular expressions
    to match each row.
    """









    # Now add in the construction.

def readConstraints(InputStream):
    Constraints= []
    with open(InputStream, 'r') as InputStream:
        First = InputStream.readline()[:-1]
        #print("Reading: |{}|".format(First))
        if(VAR_START.match(First) == True):
            NextLine = InputStream.readline()[:-1]
            #print(NextLine)
            pass
        NextLine = InputStream.readline()[:-1]




        while VAR_END.match(NextLine) == None:

            # At this point we have a variable row so
            # Generate a match.
            #print("Reading but not writing: |{}|".format(NextLine))
            match = VAR_ROW.match(NextLine)


            Line3 = str.split(match.groups()[1], ' ')


            NextLine = InputStream.readline()[:-1]
        NextLine = InputStream.readline()[:-1]
        #print("Reading: |{}|".format(NextLine))
        NextLine = InputStream.readline()[:-1]
        while CONST_END.match(NextLine) == None:
            #print("Reading: |{}|".format(NextLine))
            Match1 = CONST_ROW.match(NextLine)
            #print("Groups found: {}".format(Match1.groups()))
            str.split(NextLine, '\n')
            str.split(Match1.groups()[1], ' ')
            Name= Match1.groups()

            Constraint = Name[1:2]
            Name = Name[1:]
            Constraints.append(Name)

            NextLine = InputStream.readline()[:-1]
    print("End Reading Constraints")

    return Constraints


def readVarsBT(InputStream):
    """
    Read in the first var line then read until we
    reach the endvars.  Then return the variables.
    """

    # Allocate storage for the vars.
    Variable = {}
    G = networkx.Graph()
    # Read in and print the first line.
    with open(InputStream, 'r') as InputStream:
        First = InputStream.readline()[:-1]
        #print("Reading: |{}|".format(First))

        if (VAR_START.match(First) == None):
            raise RuntimeError("Line Mismatch")

    # Read in each of the variable lines.

        NextLine = InputStream.readline()[:-1]
        count=1
        while VAR_END.match(NextLine) == None:
            count= count+1# At this point we have a variable row so
        # Generate a match.
            #print("Reading: |{}|".format(First))
            Match = VAR_ROW.match(NextLine)
            #print("Groups found: {}".format(Match.groups()))

        # At this point the variable values should be split
        # via string.split and then a new variable instance
        # should be made.  That is left to students.
            NextLine2 = Match.groups()
            state = NextLine2[0]
            values = NextLine2[1].split()
            Line3 = Match.groups()[1:5]

            Variable[state] = values

            data = list(Variable.items())
            an_array = np.array(data, dtype=object)

            # And read the next line.
            NextLine = InputStream.readline()[:-1]
        print("End Read Vars")


        return (data)
def readVarsAC3(InputStream):
    """
    Read in the first var line then read until we
    reach the endvars.  Then return the variables.
    """

    # Allocate storage for the vars.
    Variable = {}
    G = networkx.Graph()
    # Read in and print the first line.
    with open(InputStream, 'r') as InputStream:
        First = InputStream.readline()[:-1]
        #print("Reading: |{}|".format(First))

        if (VAR_START.match(First) == None):
            raise RuntimeError("Line Mismatch")

    # Read in each of the variable lines.

        NextLine = InputStream.readline()[:-1]
        count=1
        while VAR_END.match(NextLine) == None:
            count= count+1# At this point we have a variable row so
        # Generate a match.
            #print("Reading: |{}|".format(First))
            Match = VAR_ROW.match(NextLine)
            #print("Groups found: {}".format(Match.groups()))

        # At this point the variable values should be split
        # via string.split and then a new variable instance
        # should be made.  That is left to students.
            NextLine2 = Match.groups()
            state = NextLine2[0]
            values = NextLine2[1].split()
            Line3 = Match.groups()[1:5]
            Variable[state] = values

            data = list(Variable.items())


            Variablex(state,Line3)







            # And read the next line.
            NextLine = InputStream.readline()[:-1]
        print("End Read Vars")


        return state

def readVarsAC3state(InputStream):
    """
    Read in the first var line then read until we
    reach the endvars.  Then return the variables.
    """

    # Allocate storage for the vars.
    Variable = {}
    G = networkx.Graph()
    # Read in and print the first line.
    with open(InputStream, 'r') as InputStream:
        First = InputStream.readline()[:-1]
        #print("Reading: |{}|".format(First))

        if (VAR_START.match(First) == None):
            raise RuntimeError("Line Mismatch")

    # Read in each of the variable lines.

        NextLine = InputStream.readline()[:-1]
        count=1
        while VAR_END.match(NextLine) == None:
            count= count+1# At this point we have a variable row so
        # Generate a match.
            #print("Reading: |{}|".format(First))
            Match = VAR_ROW.match(NextLine)
            #print("Groups found: {}".format(Match.groups()))

        # At this point the variable values should be split
        # via string.split and then a new variable instance
        # should be made.  That is left to students.
            NextLine2 = Match.groups()
            state = NextLine2[0]
            values = NextLine2[1].split()
            Line3 = set()
            Line3 = Match.groups()[1:5]

            Variablex(state,values)







            # And read the next line.
            NextLine = InputStream.readline()[:-1]
        print("End Read Vars")

def readVarsAC3values(InputStream):
            """
            Read in the first var line then read until we
            reach the endvars.  Then return the variables.
            """

            # Allocate storage for the vars.
            Variable = {}
            G = networkx.Graph()
            # Read in and print the first line.
            with open(InputStream, 'r') as InputStream:
                First = InputStream.readline()[:-1]
                # print("Reading: |{}|".format(First))

                if (VAR_START.match(First) == None):
                    raise RuntimeError("Line Mismatch")

                # Read in each of the variable lines.

                NextLine = InputStream.readline()[:-1]
                count = 1
                while VAR_END.match(NextLine) == None:
                    count = count + 1  # At this point we have a variable row so
                    # Generate a match.
                    # print("Reading: |{}|".format(First))
                    Match = VAR_ROW.match(NextLine)
                    # print("Groups found: {}".format(Match.groups()))

                    # At this point the variable values should be split
                    # via string.split and then a new variable instance
                    # should be made.  That is left to students.
                    NextLine2 = Match.groups()
                    state = NextLine2[0]
                    values = NextLine2[1].split()
                    Line3 = set()
                    Line3 = Match.groups()[1:5]


                    G = Variablex(state,values)


                    # And read the next line.
                    NextLine = InputStream.readline()[:-1]
                print("End Read Vars")

            return G
import BinaryCSP

def get_lines(fileName):
    lines = []
    with open(fileName,'r') as readFile:
        for line in readFile:
            lines.append(line)
    return lines


""" Takes a list of lines and creates a CSP representation.
    Format:
    variable values ...
    ...
    0
    binary_constraint_type inputs ...
    ...
    0
    unary_constraint_type inputs ... 
    ... """
def csp_parse(csp_lines):
    i = 0
    variables = []
    domains = []
    while csp_lines[i].strip() != '0':
        line = csp_lines[i].split()
        variables.append(line[0])
        domains.append(set(line[1:]))
        i += 1
    i += 1

    binary_constraints = []
    while csp_lines[i].strip() != '0':
        line = csp_lines[i].split()
        binary_constraints.append(getattr(BinaryCSP, line[0])(*line[1:]))
        i += 1
    i += 1

    unary_constraints = []
    while i < len(csp_lines):
        line = csp_lines[i].split()
        unary_constraints.append(getattr(BinaryCSP, line[0])(*line[1:]))
        i += 1

    return BinaryCSP.ConstraintSatisfactionProblem(variables, domains, binary_constraints, unary_constraints)

""" Takes a list of lines and creates an Assignment representation.
    Format:
    csp_filename
    variable new_domain_values ...
    ...
    0
    variable assigned_value
    ... """
def assignment_parse(assignment_lines):
    csp = None
    with open(assignment_lines[0].strip()) as csp_file:
        csp = csp_parse(csp_file.readlines())
    assignment = BinaryCSP.Assignment(csp)

    i = 1
    while assignment_lines[i].strip() != '0':
        line = assignment_lines[i].split()
        assignment.varDomains[line[0]] = set(line[1:])
        i += 1
    i += 1

    while i < len(assignment_lines):
        line = assignment_lines[i].split()
        assignment.assignedValues[line[0]] = line[1]
        assignment.varDomains[line[0]] = set([line[1]])
        i += 1

    return assignment








if __name__ == '__main__':
    InputStream = sys.argv[2]

    Variables = readVarsBT(InputStream)
    #instansiate variable class

    domains = readVarsAC3values(InputStream)
    vars = domains.returnname()
    print(vars)


    Constraints = readConstraints(InputStream)

    LittleG = ConstraintGraph(Constraints,Variables)
    LittleG1 = LittleG.isComplete()
    LittleG2 = LittleG.nodes()
    LittleG3 = LittleG.returnvariables()

    g = Graph(48)
    G = LittleG1
    g.graph = LittleG1
    m = 5
    a = g.graphColouring(m)
    c = LittleG.nodes()
    d = zip(a,c)

    # AC3 Instansiate class
    CSP = BinaryCSP.ConstraintSatisfactionProblem(LittleG2,LittleG3, Constraints)
    solution = BinaryCSP.AC3(a,CSP)
    e = zip(solution,c)
    if sys.argv[1] == 'MAC':
        print("Backtracking " + str(list(d)))
    if sys.argv[1] == 'AC3':
        print("AC3: " + str(list(e)))











