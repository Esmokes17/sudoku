import json
import random
from time import time

import numpy as np

from sim import Sudoku, Interface

class AI:
    def __init__(self):
        pass

    # the solve function takes a json string as input
    # and outputs the solved version as json
    def solve(self, problem):
        problem_data = json.loads(problem)
        alg = self.simulated_annealing
        initial_state = Sudoku(problem_data["sudoku"])
        solved = alg(initial_state)
        finished = Interface.perceive(solved)

        # finished is the solved version
        return finished

    def simulated_annealing(self, sudoku: Sudoku, with_prepare=True) -> Sudoku:
        interface = Interface()
        T = 9 * 9 * 10
        Epsilon = 1e-20
        random.seed(time())
        
        current = interface.copy_state(sudoku)
        if with_prepare:
            current.expand_fixed_grid()
        current.random_fill()
        current.display()
        current_error = interface.compute_error(current)
        
        best_find = interface.copy_state(current)

        while(current_error != 0):
            T *= 0.9
            if T <= Epsilon: break
            neighbor = interface.copy_state(current)
            if current_error <= 15:
                neighbor.random_change()
                while neighbor == current:
                    neighbor.random_change()
            else:
                neighbor.random_fill()
                while neighbor == current:
                    neighbor.random_fill()
            current_error = interface.compute_error(current)
            neighbor_error = interface.compute_error(neighbor)
            delta_E = 81 - (neighbor_error - current_error)
            if (delta_E < 0 or (random.random() <= (np.exp(-delta_E / T)))):
                current = neighbor
                if interface.compute_error(current) < interface.compute_error(best_find):
                    best_find = interface.copy_state(current)
                current.display()
                print(f"Correctness: {81 - current.error}")
        print(f"Best Correctness: {81 - best_find.error}")
        return best_find

    def GA(self, sudoku: Sudoku, init_population=20, with_prepare=False, epoch=int(1e10)):
        random.seed(time())
        interface = Interface()
        population = [interface.copy_state(sudoku) for _ in range(init_population)]
        for p in population:
            if with_prepare:
                p.expand_fixed_grid()
            p.random_fill()
        population = list(set(population))
        best_find = None
        for i in range(epoch):
            if len(population) > 1:
                new_population = set([])
                for _ in population:
                    child = Sudoku(sudoku.init_table)
                    errors = np.array([interface.compute_error(p) for p in population])
                    idx1, idx2 = errors.argsort()[:2]
                    rand_crossover = int(random.random() * 8)
                    child.table[:rand_crossover,:] = population[idx1].table[:rand_crossover,:]
                    child.table[rand_crossover:,:] = population[idx2].table[rand_crossover:,:]
                    new_population.add(child)
                    if (best_find is None
                        or interface.compute_error(best_find) > interface.compute_error(child)
                    ):
                        best_find = interface.copy_state(child)
                    if best_find.error == 0: break
                    if (random.random() <= 0.1): child.random_change()
                    child.display()
                    print(f"Correctness: {81 - interface.compute_error(child)}")
                population = list(new_population)
            else:
                population = [interface.copy_state(sudoku) for i in range(18)]
                for p in population:
                    p.random_fill()
                population = list(set(population))
                if len(population) == 1:
                    # so we dont have another possible
                    child = population[0]
                    child.display()
                    print(f"Correctness: {81 - interface.compute_error(child)}")
                    return child
        print(f"Best Correctness: {81 - interface.compute_error(best_find)}")
        return best_find