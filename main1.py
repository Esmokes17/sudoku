from sim import Sudoku, Interface
from time import sleep, time
import random

import os
from copy import deepcopy

import numpy as np

def display(values):
    os.system('cls' if os.name == 'nt' else 'clear')
    for r in range(3*3):
        if r in [3, 6]:
            print('------+-------+------')
        for c in range(3*3):
            if c in [3, 6]:
                print('|', end=" "),
            if display.last_values is not None and values[r][c] != display.last_values[r][c]:
                print(f'\x1b[6;31;47m' + str(values[r][c]) +'\x1b[0m', end=" ")
            else:
                print(values[r][c], end=" ")
        print()
    display.last_values = deepcopy(values)


sudoku = [[0, 0, 3, 0, 2, 0, 6, 0, 0],
          [9, 0, 0, 3, 0, 5, 0, 0, 1],
          [0, 0, 1, 8, 0, 6, 4, 0, 0],
          [0, 0, 8, 1, 0, 2, 9, 0, 0],
          [7, 0, 0, 0, 0, 0, 0, 0, 8],
          [0, 0, 6, 7, 0, 8, 2, 0, 0],
          [0, 0, 2, 6, 0, 9, 5, 0, 0],
          [8, 0, 0, 2, 0, 3, 0, 0, 9],
          [0, 0, 5, 0, 1, 0, 3, 0, 0]]

sudoku = [[1, 0, 4, 8, 6, 5, 2, 3, 7],
          [7, 0, 5, 4, 1, 2, 9, 6, 8],
          [8, 0, 2, 3, 9, 7, 1, 4, 5],
          [9, 0, 1, 7, 4, 8, 3, 5, 6],
          [6, 0, 8, 5, 3, 1, 4, 2, 9],
          [4, 0, 3, 9, 2, 6, 8, 7, 1],
          [3, 0, 9, 6, 5, 4, 7, 1, 2],
          [2, 0, 6, 1, 7, 9, 5, 8, 3],
          [5, 0, 7, 2, 8, 3, 6, 9, 4]]

sudoku = [
    [0, 0, 8, 0, 0, 0, 5, 0, 0],
    [6, 0, 0, 7, 0, 5, 0, 0, 3],
    [0, 9, 0, 8, 3, 2, 0, 0, 0],
    [0, 0, 4, 0, 1, 0, 0, 0, 0],
    [3, 8, 0, 4, 0, 7, 0, 5, 1],
    [0, 0, 0, 0, 8, 0, 2, 0, 0],
    [0, 0, 0, 1, 5, 9, 0, 7, 0],
    [8, 0, 0, 3, 0, 4, 0, 0, 5],
    [0, 0, 9, 0, 0, 0, 1, 0, 0]
]

# sudoku = [[0, 9, 0, 8, 6, 5, 2, 0, 0],
#           [0, 0, 5, 0, 1, 2, 0, 6, 8],
#           [0, 0, 0, 0, 0, 0, 0, 4, 0],
#           [0, 0, 0, 0, 0, 8, 0, 5, 6],
#           [0, 0, 8, 0, 0, 0, 4, 0, 0],
#           [4, 5, 0, 9, 0, 0, 0, 0, 0],
#           [0, 8, 0, 0, 0, 0, 0, 0, 0],
#           [2, 4, 0, 1, 7, 0, 5, 0, 0],
#           [0, 0, 7, 2, 8, 3, 0, 9, 0]]


# sudoku = [[1, 0, 0, 0, 3, 0, 0, 0, 7],
#           [0, 0, 0, 0, 0, 0, 2, 0, 0],
#           [0, 4, 9, 5, 0, 1, 0, 0, 0],
#           [0, 0, 4, 2, 0, 0, 0, 7, 1],
#           [0, 0, 0, 0, 6, 0, 0, 0, 0],
#           [9, 1, 0, 0, 0, 8, 5, 0, 0],
#           [0, 0, 0, 6, 0, 5, 9, 4, 0],
#           [0, 0, 6, 0, 0, 0, 0, 0, 0],
#           [5, 0, 0, 0, 4, 0, 0, 0, 8]]

s = Sudoku(sudoku)
display.last_values = sudoku

def simulated_annealing(sudoku):
    interface = Interface()
    T = 9 * 9 * 3 * 10
    Epsilon = 1e-20
    current = interface.copy_state(sudoku)
    current.expand_fixed_grid
    current.random_fill()
    display(current.table)
    current_error = interface.compute_error(current)
    while(current_error != 0):
        T *= 0.99
        if T <= Epsilon: return current
        neighbor = interface.copy_state(current)
        if current_error <= 20:
            neighbor.random_change()
            while neighbor == current:
                neighbor.random_change()
        else:
            neighbor.random_fill()
            while neighbor == current:
                neighbor.random_fill()
        current_error = interface.compute_error(current)
        neighbor_error = interface.compute_error(neighbor)
        delta_E = - (neighbor_error - current_error)
        if (delta_E > 0 or (random.random() <= (np.exp(delta_E / T) - 1) * 2)):
            current = neighbor
            display(current.table)
            print(current.error)

    return current

def hill_climbing(sudoku: Sudoku):
    interface = Interface()
    current = interface.copy_state(sudoku)
    current.random_fill()
    display(current.table)
    current_error = interface.compute_error(current)
    while(current_error != 0):
        neighbor = interface.copy_state(current)
        neighbor.random_fill()
        current_error = interface.compute_error(current)
        neighbor_error = interface.compute_error(neighbor)
        delta_E = - (neighbor_error - current_error)
        if (delta_E >= 0):
            current = neighbor
            display(current.table)
            # sleep(0.5)
    return current

def GA(sudoku: Sudoku):
    random.seed(time())
    interface = Interface()
    population = [deepcopy(sudoku) for i in range(20)]
    for p in population:
        p.random_fill()
    population = list(set(population))
    while(True):
        if len(population) > 1:
            new_population = set([])
            for _ in population:
                child = Sudoku(sudoku.init_table)
                errors = np.array([interface.compute_error(p) for p in population])
                idx1, idx2 = errors.argsort()[:2]
                rand_crossover = int(random.random() * 8)
                child.table[:rand_crossover,:] = population[idx1].table[:rand_crossover,:]
                child.table[rand_crossover:,:] = population[idx2].table[rand_crossover:,:]
                if interface.goal_test(child): return child
                new_population.add(child)
                if (random.random() <= 0.1): child.random_change()
                display(child.table)
                print(interface.compute_error(child))
            population = list(new_population)
        else:
            population = [deepcopy(sudoku) for i in range(18)]
            for p in population:
                p.random_fill()
            population = list(set(population))


# alg = simulated_annealing
# alg = hill_climbing
alg = GA

solved = alg(s)
display(solved.table)
print(solved.error)
print(Interface.goal_test(solved))
