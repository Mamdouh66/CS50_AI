import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if the cell is inside the set, then just remove it and decrease the count
        # because, we are sure we removed a mine
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if the cell is inside the set, then just remove it without decreasing the count
        # beacuse its not a mine
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):

        # Add cell to the moves made, Mark it as a safe cell
        self.moves_made.add(cell)
        self.mark_safe(cell)
        # Create a set to store undetermined cells
        neighbors = set()
        # Check for the cells around the given cell
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # if it's the cell itself or its in the safe cells, just skip it
                if (i, j) == cell:
                    continue
                if (i, j) in self.safes:
                    continue
                # if its in the mines, decrease the count and skip it
                if (i, j) in self.mines:
                    count -= 1
                    continue
                # if its within the borders add it to the undetermined cells
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))
        self.knowledge.append(Sentence(neighbors, count))

        # Check if one of the sentences in the AI's KB, is an all safes or a mines sentence
        # if so, mark them as such
        for sentence in self.knowledge:
            if sentence.known_safes():
                for cells in sentence.known_safes().copy():
                    self.mark_safe(cells)
            if sentence.known_mines():
                for cells in sentence.known_mines().copy():
                    self.mark_mine(cells)

        # Check if any of the sentences are a second_sentence of anohter sentence to infer new sentences from them
        # for first_sentence in self.knowledge:
        #     for second_sentence in self.knowledge:
        #         if first_sentence is second_sentence:
        #             continue
        #         if first_sentence == second_sentence:
        #             self.knowledge.remove(second_sentence)
        #         elif first_sentence.cells.issecond_sentence(second_sentence.cells):
        #             new_sentence = Sentence(
        #                 second_sentence.cells - first_sentence.cells,
        #                  second_sentence.count - first_sentence.count)
        #             if new_sentence not in self.knowledge:
        #                 self.knowledge.append(new_sentence)

        knowledge_copied = self.knowledge.copy()
        while knowledge_copied:
            first_sentence = knowledge_copied.pop()
            first_set = first_sentence.cells
            first_count = first_sentence.count
            for second_sentence in knowledge_copied:
                second_set = second_sentence.cells
                second_count = second_sentence.count
                if first_set.issubset(second_set):
                    new_sentence = Sentence(
                        second_set - first_set, second_count - first_count)
                    if new_sentence not in self.knowledge:
                        self.knowledge.append(new_sentence)

    def make_safe_move(self):
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None

    def make_random_move(self):
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.mines and (i, j) not in self.moves_made:
                    return (i, j)
        return None
