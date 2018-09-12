"""Sudoku puzzle module.

- The puzzle consists of an n-by-n grid, where n = 4, 9, 16, or 25.
  Each square contains a uppercase letter between A and the n-th letter
  of the alphabet, or is empty.
  For example, on a 4-by-4 Sudoku board, the available letters are
  A, B, C, or D. On a 25-by-25 board, every letter A-Y is available.
- The goal is to fill in all empty squares with available letters so that
  the board has the following property:
    - no two squares in the same row have the same letter
    - no two squares in the same column have the same letter
    - no two squares in the same *subsquare* has the same letter
  A *subsquare* is found by dividing the board evenly into sqrt(n)-by-sqrt(n)
  pieces. For example, a 4-by-4 board would have 4 subsquares: top left,
  top right, bottom left, bottom right.

"""
from math import sqrt
from puzzle import Puzzle

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '1234567890'


class SudokuPuzzle(Puzzle):
    """Implementation of a Sudoku puzzle."""

    # === Private Attributes ===
    # @type _n: int
    #     The size of the board. Must be 4, 9, 16, or 25.
    # @type _grid: list[list[str]]
    #     A representation of the Sudoku grid. Consists of a list of lists,
    #     where each inner list represents a row of the grid.
    #
    #     Each item of the inner list is either an uppercase letter,
    #     or is the empty string '', representing an empty square.
    #     Each letter must be between 'A' and the n-th letter of the alphabet.
    def __init__(self, grid):
        """Create a new Sudoku puzzle with an initial grid 'grid'.

        Precondition: <grid> is a valid Sudoku grid.

        @type self: SudokuPuzzle
        @type grid: list[list[str]]
        @rtype: None
        """
        self._n = len(grid)
        self._grid = grid

    def __eq__(self, other):
        """
        Return True iff <self> and <other> are equal to equal other.   

        @type self: SudokuPuzzle
        @type other: SudokuPuzzle|object
        @rtype: bool
        """
        if not isinstance(other, SudokuPuzzle):
            return False
        else:
            return self._grid == other._grid

    def __str__(self):
        """Return a human-readable string representation of <self>.

        Note that the numbers at the top and left cycle 0-9,
        to help the user when they want to enter a move.

        @type self: SudokuPuzzle
        @rtype: str

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> print(s)
          01|23
         ------
        0|AB|CD
        1|DC|BA
         ------
        2| D|
        3|  |
        <BLANKLINE>
        """
        m = int(sqrt(self._n))
        s = ''
        # Column label
        s += '  '
        for col in range(self._n):
            s += str(col % 10)
            # Vertical divider
            if (col + 1) % m == 0 and col + 1 != self._n:
                s += '|'
        # Horizontal divider
        s += '\n ' + ('-' * (self._n + m)) + '\n'
        for i in range(self._n):
            # Row label
            s += str(i % 10) + '|'
            for j in range(self._n):
                cell = self._grid[i][j]
                if cell == '':
                    s += ' '
                else:
                    s += str(cell)
                # Vertical divider
                if (j + 1) % m == 0 and j + 1 != self._n:
                    s += '|'
            s = s.rstrip()
            s += '\n'

            # Horizontal divider
            if (i + 1) % m == 0 and i + 1 != self._n:
                s += ' ' + ('-' * (self._n + m)) + '\n'

        return s

    def is_solved(self):
        """Return whether <self> is solved.

        A Sudoku puzzle is solved if its state matches the criteria
        listed at the end of the puzzle description.

        @type self: SudokuPuzzle
        @rtype: bool

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', 'D', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        True
        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'D', 'A', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        False
        """
        # Check for empty cells
        for row in self._grid:
            if '' in row:
                return False

        # Check rows
        for row in self._grid:
            if sorted(row) != list(CHARS[:self._n]):
                return False

        # Check cols
        for i in range(self._n):
            # Note the use of a list comprehension here.
            if sorted([row[i] for row in self._grid]) != list(CHARS[:self._n]):
                return False

        # Check all subsquares
        m = int(sqrt(self._n))
        for x in range(0, self._n, m):
            for y in range(0, self._n, m):
                items = [self._grid[x + i][y + j]
                         for i in range(m)
                         for j in range(m)]

                if sorted(items) != list(CHARS[:self._n]):
                    return False

        # All checks passed
        return True

    def extensions(self):
        """Return list of extensions of <self>.

        This method picks the first empty cell (looking top-down,
        left-to-right) and returns a list of the new puzzle states
        obtained by filling in the empty cell with one of the
        available letters that does not violate any of the constraints
        listed in the problem description. (E.g., if there is
        already an 'A' in the row with the empty cell, this method should
        not try to fill in the cell with an 'A'.)

        If there are no empty cells, returns an empty list.

        @type self: SudokuPuzzle
        @rtype: list[SudokuPuzzle]

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> lst = list(s.extensions())
        >>> len(lst)
        1
        >>> print(lst[0])
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA|D
        3|DC|
        <BLANKLINE>
        """
        # Search for the first empty cell
        row_index, col_index = None, None
        for i in range(self._n):
            row = self._grid[i]
            if '' in row:
                row_index, col_index = i, row.index('')
                break

        if row_index is None:
            return []
        else:
            # Calculate possible letter to fill the empty cell
            letters = self._possible_letters(row_index, col_index)
            return [self._extend(letter, row_index, col_index)
                    for letter in letters]

    # ------------------------------------------------------------------------
    # Helpers for method 'extensions'
    # ------------------------------------------------------------------------
    def _possible_letters(self, row_index, col_index):
        """Return a list of the possible letters for a cell.

        The returned letters must be a subset of the available letters.
        The returned list should be sorted in alphabetical order.

        @type self: SudokuPuzzle
        @type row_index: int
        @type col_index: int
        @rtype: list[str]

         >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', 'D', 'C'], \
                              ['D', 'C', 'B', '']])
        >>> s._possible_letters(3, 3)
        ['A']
        """
        lst_choice = list(CHARS[:self._n])
        lst_possible = []
        lst_impossible = []

        # check for row
        for char in self._grid[row_index]:
            if char != '' and char not in lst_impossible:
                lst_impossible.append(char)

        # check for column
        for row in self._grid:
            if row[col_index] != '' and row[col_index] not in lst_impossible:
                lst_impossible.append(row[col_index])

        # check for subsquare
        m = int(sqrt(self._n))
        # the top-left letter in the square
        start_row = int(row_index / m) * m
        start_col = int(col_index / m) * m

        for row in range(m):
            for col in range(m):
                test_grid = self._grid[start_row + row][
                    start_col + col]
                if test_grid != '' and test_grid not in lst_impossible:
                    lst_impossible.append(test_grid)

        for char in lst_choice:
            if char not in lst_impossible:
                lst_possible.append(char)

        return lst_possible

    def move(self, move):
        """Return a new puzzle state specified by making the given move.

        Raise a ValueError if <move> represents an invalid move.
        Do *NOT* change the state of <self>. This is not a mutating method!

        NOTE: You can ignore this completely until Part 2.

        @type self: SudokuPuzzle
        @type move: str
        @rtype: SudokuPuzzle

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', 'D', 'C'], \
                              ['D', 'C', 'B', '']])
        >>> after_move = s.move('(3, 3) -> A')
        >>> print(after_move)
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA|DC
        3|DC|BA
        <BLANKLINE>
        """
        if move.__len__() < 11 or move[-1] not in CHARS[:self._n]:
            raise ValueError()

        for x in move[:-1]:
            if x in CHARS:
                raise ValueError()

        row = ''
        found_number = False
        row_end = 0
        for x in range(len(move)):

            if found_number:

                if move[x] not in NUMBERS:
                    found_number = False
                    row_end = x
                    break
                else:
                    row += move[x]

            if move[x] == '(':
                found_number = True

        if row_end == 0 or row == '' or int(row) >= self._n:
            raise ValueError()

        col = ''
        for x in range(row_end, len(move)):

            if found_number:

                if move[x] not in NUMBERS:
                    break
                else:
                    col += move[x]                  # Find and record col_index.

            if move[x] == ' ' and x > 0 and move[x - 1] == ',':
                found_number = True

        if col == '' or int(col) >= self._n:
            raise ValueError()
        elif move[-1] not in self._possible_letters(int(row), int(col)):
            raise ValueError()
        else:
            return self._extend(move[-1], int(row), int(col))

    def _extend(self, letter, row_index, col_index):
        """Return a new Sudoku puzzle obtained after one move.

        The new puzzle is identical to <self>, except that it has
        the value at position (row_index, col_index) equal to 'letter'
        instead of empty.

        'letter' must be an available letter.
        'row_index' and 'col_index' are between 0-3.

        @type self: SudokuPuzzle
        @type letter: str
        @type row_index: int
        @type col_index: int
        @rtype: SudokuPuzzle

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> print(s._extend('B', 2, 3))
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA| B
        3|DC|
        <BLANKLINE>
        """
        new_grid = [row.copy() for row in self._grid]
        new_grid[row_index][col_index] = letter
        return SudokuPuzzle(new_grid)

    def puzzle_to_hint(self, new_puzzle):
        """
        Return a string of a move that moves <self> to <new_puzzle> state.

        Compare the new_puzzle with self, find out how to move from 
        self to new_puzzle.

        @type self: SudokuPuzzle
        @type new_puzzle: SudokuPuzzle
        @rtype: str
        """

        for x in range(len(self._grid)):
            for y in range(len(self._grid)):
                if self._grid[x][y] == '' \
                        and new_puzzle._grid[x][y] in CHARS[:self._n]:
                    return '(' + str(x) + ', ' + str(y) + ') -> ' \
                           + new_puzzle._grid[x][y]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
