import os
import json
from typing import List, Set, Tuple
from copy import deepcopy
import random

import numpy as np

class Sudoku:
    """Simulator class"""
    EMPTY_CHAR = 0
    def __init__(self, init_sudoku_table: List[List[int]]):
        if init_sudoku_table is None:
            return
        self.table = np.array(init_sudoku_table)
        self.error = None
        self.init_table = np.array(init_sudoku_table)
        self.fixed_grid = []
        self.empty_grid = []
        for c in range(9):
            for r in range(9):
                if self.table[r,c] == self.EMPTY_CHAR:
                    self.empty_grid.append((r, c))
                else:
                    self.fixed_grid.append((r, c))

    def random_change(self):
        while (True):
            value = self._get_random_value()
            row = int(random.random() * 8)
            col = int(random.random() * 8)
            if (row, col) not in self.fixed_grid:
                self.table[row][col] = value
                self.error = None
                return

    def random_fill(self):
        """find empty grid and fill with possible values"""
        self.expand_fixed_grid()
        self.table = deepcopy(self.init_table)
        permutation = Interface.values_list()
        available_grids = []
        for row in range(9):
            for col in range(9):
                if (row,col) not in self.fixed_grid:
                    available_grids.append((row, col))
        random.shuffle(available_grids)
        # filling
        for (row, col) in available_grids:
            row_block_start = 3 * (row // 3)
            col_block_start = 3 * (col // 3)
            row_block_end = row_block_start + 3
            col_block_end = col_block_start + 3
            non_possible_values = set(set(self.table[row,:]) | set(self.table[:,col]) | set([self.table[r][c]
            for r in range(row_block_start, row_block_end)
                for c in range(col_block_start, col_block_end)]))
            possible_values = list(permutation - non_possible_values)
            if len(possible_values) > 0:
                self.table[row,col] = int(random.choice(possible_values))
            else:
                self.table[row,col] = self._get_random_value()
        self.error = None

    def expand_fixed_grid(self):
        """fill the grids that are have just one possible to fill"""
        new_init_table = deepcopy(self.init_table)
        permutation = Interface.values_list()
        is_changed = False
        for row in range(9):
            for col in range(9):
                if (row,col) not in self.fixed_grid:
                    row_block_start = 3 * (row // 3)
                    col_block_start = 3 * (col // 3)
                    row_block_end = row_block_start + 3
                    col_block_end = col_block_start + 3
                    non_possible_values = set(set(new_init_table[row,:]) | set(new_init_table[:,col]) | set([new_init_table[r][c]
                              for r in range(row_block_start, row_block_end)
                              for c in range(col_block_start, col_block_end)]))
                    possible_values = list(permutation - non_possible_values)
                    if len(possible_values) == 1 and possible_values[0] != self.EMPTY_CHAR:
                        is_changed = True
                        self.fixed_grid.append((row, col))
                        new_init_table[row, col] = possible_values[0]
        self.init_table = new_init_table
        if is_changed:
            # check again with this new values
            self.expand_fixed_grid()

    def display(self, cache=True):
        if cache and not hasattr(self.__class__, "last_values"):
            self.__class__.last_values = self.init_table
        os.system('cls' if os.name == 'nt' else 'clear')
        for r in range(3*3):
            if r in [3, 6]:
                print('------+-------+------')
            for c in range(3*3):
                if c in [3, 6]:
                    print('|', end=" "),
                if (self.__class__.last_values is not None
                    and self.table[r][c] != self.__class__.last_values[r][c]
                ):
                    print(f'\x1b[6;31;47m' + str(self.table[r][c]) +'\x1b[0m', end=" ")
                else:
                    print(self.table[r][c], end=" ")
            print()
        if cache:
            self.__class__.last_values = deepcopy(self.table)

    def _get_random_value(self):
        return int(random.random() * 8 + 1)

    def __hash__(self):
        return hash(self.table.tobytes())
    
    def __eq__(self, __o: object) -> bool:
        return np.array_equal(__o.table, self.table)

class Interface:
    def __init__(self):
        pass

    def perceive(sudoku: Sudoku):
        return json.dumps({
            "sudoku": sudoku.table.tolist(),
        })

    @staticmethod
    def values_list() -> Set[int]:
        return set(range(1, 10))

    @staticmethod
    def copy_state(sudoku: Sudoku) -> Sudoku:
        _copy = Sudoku(None)
        _copy.table = deepcopy(sudoku.table)
        _copy.init_table = deepcopy(sudoku.init_table)
        _copy.fixed_grid = deepcopy(sudoku.fixed_grid)
        _copy.error = sudoku.error
        return _copy

    @staticmethod
    def is_valid(sudoku: Sudoku, position: Tuple[int, int]):
        row, col = position
        value = sudoku.table[row, col]
        # Check row
        for c in range(9):
            if position[1] != c and sudoku.table[row][c] == value:
                return False
        # Check column
        for r in range(9):
            if position[0] != r and sudoku.table[r][col] == value:
                return False
        # Check box
        row_block_start = 3 * (row // 3)
        col_block_start = 3 * (col // 3)
        row_block_end = row_block_start + 3
        col_block_end = col_block_start + 3
        for r in range(row_block_start, row_block_end):
            for c in range(col_block_start, col_block_end):
                if sudoku.table[r][c] == value and (r,c) != position:
                    return False
        return True

    # @staticmethod
    # def compute_error(sudoku: Sudoku) -> List[Tuple[int, int]]:
    #     if sudoku.error != None:
    #         return sudoku.error
    #     positions_error = []
    #     permutation = Interface.values_list()
    #     # cost rows
    #     for row in range(9):
    #         positions_error += list(permutation - set(sudoku.table[row,:]))
    #     # cost columns
    #     for col in range(9):
    #         positions_error += list(permutation - set(sudoku.table[:, col]))
    #     # cost blocks
    #     for row in range(0, 9, 3):
    #         for col in range(0, 9, 3):
    #             positions_error += list(permutation - set([sudoku.table[row + i][col + j] for i in range(3) for j in range(3)]))
    #     sudoku.error = len(positions_error)
    #     return sudoku.error

    @staticmethod
    def compute_error(sudoku: Sudoku) -> List[Tuple[int, int]]:
        if sudoku.error != None:
            return sudoku.error
        positions_error = []
        for r in range(9):
            for c in range(9):
                if not Interface.is_valid(sudoku, (r,c)):
                    positions_error.append((r,c))
        sudoku.error = len(positions_error)
        return sudoku.error

    @staticmethod
    def goal_test(sudoku: Sudoku) -> bool:
        #! this method is not actually used
        permutation = Interface.values_list()
        for row in range(9):
            if set(sudoku.table[row, :]) != permutation:
                return False
        for col in range(9):
            if set(sudoku.table[:, col]) != permutation:
                return False
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                row_block_start = 3* (row // 3)
                col_block_start = 3* (col // 3)
                row_block_end = row_block_start + 3
                col_block_end = col_block_start + 3
                if not(set([sudoku.table[r][c]
                          for r in range(row_block_start, row_block_end)
                          for c in range(col_block_start, col_block_end)]) == permutation
                ):
                    return False
        return True