# Construct a problem from scratch with variables of various
# types. Adds Special Ordered Sets (SOSs) and shows how to
# retrieve such data once it has been added to the problem
# using the API functions.
#
# (C) Fair Isaac Corp., 1983-2024

from __future__ import print_function
import xpress as xp

N = 40
S = range(N)

m = xp.problem("test restriction")

m.controls.miprelstop = 0

#
# All variables used in this example
#

v1 = m.addVariable(lb=0, ub=10, threshold=5, vartype=xp.continuous)
v2 = m.addVariable(lb=1, ub=7, threshold=5, vartype=xp.continuous)
v3 = m.addVariable(lb=5, ub=10, threshold=7, vartype=xp.semicontinuous)
v4 = m.addVariable(lb=1, ub=7, threshold=3, vartype=xp.semiinteger)
vb = m.addVariable(vartype=xp.integer, lb=0, ub=1)

y = [m.addVariable(name="y{0}".format(i), lb=0, ub=2*N) for i in S]

cc = xp.constraint(body=v1 - v2, lb=2, ub=15)
m.addConstraint(cc)

# Indices of variables can be retrieved both using their name and
# their Python object.

print("index of y[0] from name: ", m.getIndexFromName(xp.names_column, "y0"))
print("index of y[0]:           ", m.getIndex(y[0]))

s = m.addSOS([v1, v2], [2, 4], name="mynewsos", type=2)

# Showcases the use of getIndex()

print("get index: var v1 -->", m.getIndex(v1), "; con cc -->",
      m.getIndex(cc), "; sos -->", m.getIndex(s))

print("SOS:", s.name, s)

# objective overwritten at each setObjective()
m.setObjective(xp.Sum([i*y[i] for i in S]))

m.optimize()

# Retrieve a solution: first declare an empty string, then call the
# getmipsol() function to fill it up.

mipsol = []

m.getmipsol(mipsol)

s1 = m.getSolution(v1, v2, y[10:30])  # get a subset of the solutions
s2 = m.getSolution(S)                 # can get it with indices as well

print("v1: ", m.getSolution(v1),
      ", v2: ", m.getSolution(v2),
      "; sol vector: ", m.getSolution(),
      "; obj: ", m.getObjVal(),
      sep="")  # default separator between strings is " "

# Adds yet another constraint to the problem and saves it, then
# removes an SOS and saves another version

m.addConstraint((1.25 * v1 - 2.5*v2 + 4.3) * (3.1 * v2 - 2 * v1 - 5.2)
                + 72.5 * v1**2 + 73 * v2**2 <= 1950)

m.write("restriction", "lp")

m.delSOS(s)
m.write("restriction-noSOS", "lp")

m.optimize()
