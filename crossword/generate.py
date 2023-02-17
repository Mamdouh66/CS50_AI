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

        # loop over every values of a variable and make sure it satisfy unary constrains
        for var in self.domains.copy():
            for val in self.domains[var].copy():
                if len(val) != var.length:
                    self.domains[var].remove(val)

    def revise(self, x, y):
        # check psuedocode in lecture
        revised = False
        # if overlap is None return false
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return revised
        i = overlap[0]
        j = overlap[1]
        # loop over every value in domain of x
        for xVal in self.domains[x].copy():
            # initilize boolean to false to check if to delete this value or not
            xDelete = False
            for yVal in self.domains[y]:
                # if it doesn't satisfy binary constraint change it to true
                if xVal[i] != yVal[j]:
                    xDelete = True
                    break
            # delete that value from domain of x
            if xDelete:
                self.domains[x].remove(xVal)
                revised = True
        return revised

    def ac3(self, arcs=None):

        # if arc is empty, create a deque of every arc
        if arcs is None:
            queue = deque()
            for xVal in self.domains.keys():
                for yVal in self.domains.keys():
                    if xVal != yVal:
                        queue.appendleft((xVal, yVal))
        else:
            # if not just create one with initial arcs
            queue = deque()
            for val in arcs:
                queue.appendleft(val)

        # psuedocode in the lecture
        while queue:
            arc = queue.pop()
            if arc is not None:
                i = arc[0]
                j = arc[1]
                if self.revise(i, j):
                    if len(self.domains[i]) == 0:
                        return False
                    for z in self.crossword.neighbors(i) - {j}:
                        queue.append(z, i)
        return True

    def assignment_complete(self, assignment):

        for var in self.domains:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):

        # if not unique return false
        if len(set(assignment.values())) != len(assignment.values()):
            return False

        # if they are not of correct length return false
        for key in assignment:
            if key.length != len(assignment[key]):
                return False

        # if variable overlaps wiht neighbor return false
        for key in assignment:
            neigborKey = self.crossword.neighbors(key)
            for nKey in neigborKey:
                overlap = self.crossword.overlaps[key, nKey]
                if overlap is not None:
                    i = overlap[0]
                    j = overlap[1]
                    if nKey in assignment:
                        if assignment[key][i] != assignment[nKey][j]:
                            return False
        return True

    def order_domain_values(self, var, assignment):

        values = ((variable, sum(variable in self.domains[neighbor] for neighbor in self.crossword.neighbors(var)))
                  for variable in self.domains[var] if variable not in assignment)
        sorted_values = sorted(values, key=lambda item: item[1])
        return [item[0] for item in sorted_values]

    def select_unassigned_variable(self, assignment):

        unassigned_variables = [
            i for i in self.domains.keys() if i not in assignment]
        variable = min(unassigned_variables, key=lambda i: (
            len(self.domains[i]), -len(self.crossword.neighbors(i) or [])))
        degree = len(self.crossword.neighbors(variable) or [])
        return variable

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return True
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            assignment[var] = val
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
        return None


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
