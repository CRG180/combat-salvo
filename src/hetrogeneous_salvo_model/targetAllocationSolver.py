#!/usr/bin/env python3

from ortools.linear_solver import pywraplp
import numpy as np

#Example data for blue targeting red 
#
    #R1 #R2 #R3 #R4
#B1  X   X   X   
#B2  X           X
#B3      X       X

target_matrix = np.array([
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
])


# Traget reward matrix
target_reward_matrix = np.array([
    [100, 40, 0 , 20],
    [0, 40, 100 , 30],
    [0, 100, 0 , 10],
])

num_missile = [10, 14, 22]

over_kill = [15, 30, 25, 10]


solver = pywraplp.Solver.CreateSolver('GLOP')

# variables
num_blue = len(target_matrix)
num_red = len(target_matrix[0])
x = {}
for i in range(num_blue):
    for j in range(num_red):
        if target_matrix[i][j] ==1:
            x[i,j] = solver.NumVar(0.0, solver.infinity(), f"x[{i},{j}]")

# constraints 
# Each unit can only fire munitions it has avaiable
for i in range(num_blue):
    solver.Add(solver.Sum([x[i, j] for j in range(num_red)]) <= num_missile[i])

# overkill constraints 
for j in range(num_red):
    solver.Add(solver.Sum([x[i,j] for i in range(num_blue)]) <= over_kill[j])
    
#objective 
objective_terms = []
for i in range(num_blue):
    for j in range(num_red):
        if target_matrix[i][j] == 1:
           objective_terms.append(target_reward_matrix[i][j] * x[i, j]) 
solver.Maximize(solver.Sum(objective_terms))

# Solve
status = solver.Solve()

 # Print solution.
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f'Total Reward = {solver.Objective().Value()}\n')
    for i in range(num_blue):
        for j in range(num_red):
            if x[i,j].solution_value() >0: 
                print(f'Blue_{i+1} fires {x[i,j].solution_value()} muntions at Red_{j+1}')
    
