import sys

from crossword import *
from collections import deque


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """" For every variable make sure its domain satisfy its unary constrins """
        for var in self.domains:
            for value in self.domains[var].copy():
                if len(value) != len(self.domains[var]):
                    self.domains[var].remove(value)

    def revise(self, x, y):

        # revised initially set as false i.e. no changes
        revised = False

        # if there is an overlap save it, otherwise return false
        (i, j) = self.crossword.overlaps[x, y]
        if (i, j) is None:
            return revised

        # for every word in x domain with letter i, check if it satisfy word y with letter j
        for X in self.domains[x].copy():
            for Y in self.domains[y].copy():
                if X[i] != Y[j]:
                    self.domains[x].remove(X)
                    revised = True

        return revised

    def ac3(self, arcs=None):
        # if arcs is not empty create a deque with given arcs, if empty create one with all arcs
        if arcs != None:
            arcs = deque(arcs)
        else:
            arcs = deque()
            for i in self.crossword.variables:
                for j in self.crossword.neighbors(i):
                    arcs.appendleft((i, j))

        # just the pseudocode provided in note
        while arcs:
            (x, y) = arcs.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.appendleft((z, x))

        return True

    def assignment_complete(self, assignment):

        # if a certain variable isn't in the assignment just return false
        for key in self.crossword.variables:
            if key not in assignment:
                return False
        return True

    def consistent(self, assignment):

        # check if values are unique
        if len(set(assignment.values())) != len(assignment.keys()):
            return False

        # check if values are of correct length
        for key in assignment:
            if len(assignment[key]) != len(key):
                return False

        # check if values overlap
        for key in assignment:
            for neighbor in self.crossword.neighbors(key):
                if neighbor in assignment.keys():
                    (i, j) = self.crossword.overlaps[key, neighbor]
                    if assignment[key][i] != assignment[neighbor][j]:
                        return False

        return True

    def order_domain_values(self, var, assignment):

        counter = 0
        for neighbor in self.crossword.neighbors(var):
            if neighbor in assignment:
                break

            (i, j) = self.crossword.overlaps[var, neighbor]
            for value in self.domains[neighbor]:
                if var[i] != value[j]:
                    counter += 1

        return sorted(self.domains[var], key=counter)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
