#!/usr/bin/python3

import sys
import scipy.optimize

threshold = 2.18

def compute(V, init = 10):
	if len(V) <= 1:
		return
	def h(x):
		return sum([x**(-v) for v in V])-1
	X = scipy.optimize.brenth(h,1, init)
	return X

def choose(L, k, n = None):
	if n == None:
		n = len(L)
	if k == 0:
		return [[]]
	R = []
	for i in range(k-1,n):
		for S in choose(L, k-1, i):
			R.append(S+[L[i]])
	return R

def all_subsets(L):
	R = []
	for i in range(len(L)+1):
		R += choose(L, i)
	return R

def make_graph(E):
	if E == []:
		n = 1
	else:
		n = 1 + max([max(x) for x in E])
	G = [[] for x in range(n)]
	for e in E:
		G[e[0]].append(e[1])
		G[e[1]].append(e[0])
	return G

def find_P4(G):
	for v1 in range(len(G)):
		for v2 in G[v1]:
			for v3 in G[v2]:
				if v3 == v1: continue
				if v3 in G[v1]: continue
				for v4 in G[v3]:
					if v4 in [v1,v2]: continue
					if v4 in G[v1] or v4 in G[v2]: continue
					return True
	return False

def swap(x, twins):
	if x == twins[0]:
		return twins[1]
	elif x == twins[1]:
		return twins[0]
	else:
		return x

def swap_pair(p, twins):
	p1 = swap(p[0], twins)
	p2 = swap(p[1], twins)
	return (min(p1,p2),max(p1,p2))

def check(L, D, twins = []):
	D1 = set(D)
	for X in L:
		if X.issubset(D1):
			return True
	if twins != []:
		D2 = [swap_pair(z,twins) for z in D]
		D2 = set(D2)
		for X in L:
			if X.issubset(D2):
				return True
	return False

def minimal_deletion_sets(E, twins):
	if not find_P4(make_graph(E)):
		return []
	L = []
	V = []
	for k in range(1, len(E)+1):
		for Del in choose(E, k):
			if check(L, Del, twins):
				continue
			E2 = [x for x in E if x not in Del]
			G = make_graph(E2)
			if not find_P4(G):
				L.append(set(Del))
				V.append(len(Del))
	return V

def compute_branching_number1(E, twins):
	X = 999
	n = 1 + max([max(x) for x in E])
	for del_v in all_subsets(range(n)):
		E2 = [x for x in E if x[0] not in del_v and x[1] not in del_v]
		V2 = minimal_deletion_sets(E2, twins)
		if V2 != []:
			X2 = compute(V2)
			if X2 < X:
				X = X2
				V = V2
				D = del_v
			if X < threshold:
				return X,V,D
	return X,V,D

def compute_branching_number2(E0, twins):
	if twins == []:
		return compute_branching_number1(E0, [])

	X2,V2,D2 = compute_branching_number1(E0, [])
	if X2 < threshold:
		return X2,V2,D2

	# The two vertices are twins in the whole graphs
	X,V,D = compute_branching_number1(E0, twins)
	print(" ",X,V,D,"twins")

	# The two vertices are NOT twins in the whole graphs
	n = 1 + max([max(x) for x in E0])
	E2_list = all_subsets([(i,n) for i in range(n) if i not in twins])
	for E2 in E2_list:
		E = E0+[(twins[0],n)]+E2
		X2,V2,D2 = compute_branching_number1(E, [])
		if X2 > X:
			X = X2
			V = V2
			D = D2
		print(" ",X2,V2,D2,E2)
	return X,V,D

def compute_branching_number(E0, E1_list = [[]], E2_list = [[]], E3_list = [[]], exceptions_list = [], twins = []):
	X = 0
	for E1 in E1_list:
		for E2 in E2_list:
			for E3 in E3_list:
				if E1+E2+E3 in exceptions_list:
					continue
				print("-"*77)
				print("E0",E0)
				print("E1",E1)
				if E2_list != [[]]:
					print("E2",E2)
				if E3_list != [[]]:
					print("E3",E3)
				E = E0+E1+E2+E3
				E = [(min(x),max(x)) for x in E]
				X2,V2,D2 = compute_branching_number2(E, twins)
				X = max(X, X2)
				if D2 != []:
					print(X2,V2,"deleted:",D2)
				else:
					print(X2,V2)
	return X

# List of possible cases for the edges of vertex 4 in Pother(A)
Pother_list_4 = [
	[(4,0)],
	[(4,1)],
	[(4,0),(4,1)],
	[(4,0),(4,2)],
	[(4,0),(4,3)],
	[(4,0),(4,1),(4,2)],
	[(4,0),(4,1),(4,3)]]

# List of possible cases for the edges of vertex 4 in P(A)
P_list_4 = [[(4,1),(4,2)]]+Pother_list_4

# list of possible cases for the edges of vertex 5 in Pother(A)
Pother_list_5 = [
	[(5,0)],
	[(5,1)],
	[(5,2)],
	[(5,3)],
	[(5,0),(5,1)],
	[(5,2),(5,3)],
	[(5,0),(5,2)],
	[(5,1),(5,3)],
	[(5,0),(5,3)],
	[(5,0),(5,1),(5,2)],
	[(5,1),(5,2),(5,3)],
	[(5,0),(5,1),(5,3)],
	[(5,0),(5,2),(5,3)] ]

# list of possible cases for the edges of vertex 5 in P(A)
P_list_5 = [[(5,1),(5,2)]]+Pother_list_5

def compute_B1():
	X = []
	# obs 2.3
	E0 = [(0,1),(1,2),(2,3),  (6,0),(6,1),(6,2),(6,3),  (6,4),(4,5)]
	E1_list = [[]]+P_list_4 # u in I/P
	E2_list = [[]]+P_list_5 # v in I/P
	X.append(compute_branching_number(E0, E1_list, E2_list))

	E0 = [(0,1),(1,2),(2,3),  (6,5)]
	E1_list = [[(4,0),(4,1),(4,2),(4,3)]]+P_list_4 # u in T/P
	E2_list = [[(5,0),(5,1),(5,2),(5,3)]]+P_list_5 # v in T/P
	exceptions_list = [[(4,0),(5,3)]]
	X.append(compute_branching_number(E0, E1_list, E2_list, [[]], exceptions_list))

	# obs 2.4
	E0 = [(0,1),(1,2),(2,3),  (5,0),(5,1),(5,2),(5,3),(6,0),(6,1),(6,2),(6,3), (5,4)]
	E1_list = [[]]+P_list_4 # v in I/P
	X.append(compute_branching_number(E0, E1_list))

	E0 = [(0,1),(1,2),(2,3),  (5,6),(6,4)]
	E1_list = [[(4,0),(4,1),(4,2),(4,3)]]+P_list_4 # v in T/P
	exceptions_list = [[(4,0)]]
	X.append(compute_branching_number(E0, E1_list, [[]], [[]], exceptions_list))

	# obs 2.6
	E0 = [(0,1),(1,2),(2,3),  (5,0),(5,1),(5,2),(5,3),(6,0),(6,1),(6,2),(6,3)]
	E1_list = P_list_4 # v in P
	E2_list = [[],[(5,6)]] # x,y can be adjacent or non-adjacent
	X.append(compute_branching_number(E0, E1_list, E2_list))

	E0 = [(0,1),(1,2),(2,3),  (4,5),(4,6)]
	E1_list = P_list_4 # v in P
	E2_list = [[],[(5,6)]] # x,y can be adjacent or non-adjacent
	X.append(compute_branching_number(E0, E1_list, E2_list))

	# obs 2.7
	E0 = [(0,1),(1,2),(2,3), (6,0),(6,1),(6,2),(6,3)]
	E1_list = P_list_4 # u in P
	E2_list = P_list_5 # v in P
	E3_list = [[], [(4,5)]]
	X.append(compute_branching_number(E0, E1_list, E2_list, E3_list))

	E0 = [(0,1),(1,2),(2,3), (6,4),(6,5)]
	E1_list = P_list_4 # u in P
	E2_list = P_list_5 # v in P
	E3_list = [[], [(4,5)]]
	exceptions_list = [[(4,0),(5,3)]]
	X.append(compute_branching_number(E0, E1_list, E2_list, E3_list, exceptions_list))

	# obs 2.14
	E0 = [(0,1),(1,2),(2,3),  (5,0),(5,1),(5,2),(5,3), (5,6)]
	E1_list = P_list_4 # v in P
	X.append(compute_branching_number(E0, E1_list))

	E0 = [(0,1),(1,2),(2,3),  (6,0),(6,1),(6,2),(6,3), (4,5),(4,6)]
	E1_list = P_list_4
	X.append(compute_branching_number(E0, E1_list))

	# Fact 2.15
	E0 = [(0,1),(1,2),(2,3),  (5,0),(5,1),(5,2),(5,3), (4,6)]
	E1_list = P_list_4
	X.append(compute_branching_number(E0, E1_list))

	E0 = [(0,1),(1,2),(2,3),  (6,0),(6,1),(6,2),(6,3), (4,5),(5,6)]
	E1_list = P_list_4
	X.append(compute_branching_number(E0, E1_list))

	# Fact 2.15
	E0 = [(0,1),(1,2),(2,3),  (6,0),(6,1),(6,2),(6,3),(7,0),(7,1),(7,2),(7,3), (4,6),(5,7),(6,7)]
	E1_list = P_list_4
	X.append(compute_branching_number(E0, E1_list))

	E0 = [(0,1),(1,2),(2,3),  (5,0),(5,1),(5,2),(5,3), (4,7),(5,6),(4,5)]
	E1_list = P_list_4
	X.append(compute_branching_number(E0, E1_list))

	return max(X)

# P6 + 1 vertex
def compute_B2():
	E0 = [(0,1),(1,2),(2,3),(3,4),(4,5)]
	E1_list = all_subsets([(0,6),(1,6),(2,6),(3,6),(4,6),(5,6)])
	exceptions_list = [ [], [(0,6)], [(5,6)], [(0,6),(5,6)], [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6)] ]
	return compute_branching_number(E0, E1_list, [[]], [[]], exceptions_list)

#  3 P vertices, at least one in Pother
def compute_B3():
	return max(compute_B3a(), compute_B3b(), compute_B3c())

# 2 Pmid + 1 Pother
def compute_B3a():
	E0 = [(0,1),(1,2),(2,3),(5,1),(5,2),(6,1),(6,2)]
	E1_list = Pother_list_4
	# 5,6 are not twins in G[B]. WLOG 4 is adjacent to 5 and not to 6
	E2_list = [[(4,5)]]
	E3_list = [[], [(5,6)]]
	X1 = compute_branching_number(E0, E1_list, E2_list, E3_list)

	# 5,6 are twins in G[B].
	E2_list = [[], [(4,5),(4,6)]] # 4 is either adjacent to both 5,6 or to neither vertex
	E3_list = [[], [(5,6)]]
	X2 = compute_branching_number(E0, E1_list, E2_list, E3_list, [], [5,6])
	return max(X1, X2)

# 3 Pother with same neighbors in A
def compute_B3b():
	E0 = [(0,1),(1,2),(2,3)]
	E1_list = [ x+[(5,y[1]) for y in x]+[(6,y[1]) for y in x] for x in Pother_list_4]
	# There will always be a pair of vertices from 4,5,6 which are twins in G[B]
	# WLOG 4,5 are twins.
	E2_list = [ [], [(4,6),(5,6)] ] # 6 is either adjacent to both 4,5 or to neither vertex
	E3_list = [[], [(4,5)]]
	return compute_branching_number(E0, E1_list, E2_list, E3_list, [], [4,5])

# 3 Pother or 2 Pother + 1 Pmid
def compute_B3c():
	X = []
	E0 = [(0,1),(1,2),(2,3)]
	E1_list = Pother_list_4
	E2_list = Pother_list_5
	E3_list = [ [(6,y[1]) for y in x] for x in P_list_5]
	# Ignore the case that 4,5,6 have the same neighbors in A which was considered in compute_B3b
	exceptions_list = [ x+[(5,y[1]) for y in x]+[(6,y[1]) for y in x] for x in Pother_list_4]
	for e in all_subsets([(4,5),(4,6),(5,6)]):
		X.append(compute_branching_number(E0+e, E1_list, E2_list, E3_list, exceptions_list))
	return max(X)

X1 = compute_B1()
X2 = compute_B2()
X3 = compute_B3()

print("\n")
print("B1",X1)
print("B2",X2)
print("B3",X3)


