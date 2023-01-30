"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # initiliaze counter for X and O
    counterForX = 0
    counterForO = 0

    # Basically if CounterForX equals CounterForO its X's turn, otherwise its O's
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                continue
            elif board[i][j] == X:
                counterForX += 1
            elif board[i][j] == O:
                counterForO += 1

    if board == initial_state():
        return X
    elif counterForX > counterForO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possibleActions = set()

    # Basically if the index is EMPTY just add it to the set as a tuple (row, column)
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                possibleActions.add((i, j))
            else:
                continue

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if the action is a valid action or not
    if action not in actions(board):
        raise Exception("Action is inavlid")

    # Making a deep copy for the board
    newBoard = deepcopy(board)

    # Because the action is a tuple (row, column), assign a variable for each one
    row = action[0]
    column = action[1]

    # Get the player choice with the new board
    newBoard[row][column] = player(board)

    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Checks for Horizental win
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][0] == board[i][2]:
            return board[i][0]

    # Checks for Vertical win
    for i in range(3):
        if board[0][i] == board[1][i] and board[0][i] == board[2][i]:
            return board[0][i]

    # Checks for diagnolly win
    if board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[0][0]

    if board[2][0] == board[1][1] and board[2][0] == board[0][2]:
        return board[2][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) == X:
        return True
    elif winner(board) == O:
        return True

    # if there are some None grids, and no one has won, then it's not over
    counterForNone = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                counterForNone += 1

    if counterForNone > 0:
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # alpha-beta pruning
    # alpha is the best alternative for max on a particular path, beta is the best alternative for min on a particular path
    alpha = -math.inf
    beta = math.inf

    # for the player 'X' we just call the maximizing function with sending board, alpha, beta
    # the function will return [v, actionToTake], so basicalyy [1], means just return the action to take
    # without the v
    if player(board) == X:
        return maxValue(board, alpha, beta)[1]
    else:
        return minValue(board, alpha, beta)[1]


# The maximizing function returns [v, actionToTake]
def maxValue(board, alpha, beta):

    # Firstly, initliaze which actionToTake to None, and check if the board is terminal
    actionToTake = None
    if terminal(board):
        return [utility(board), None]

    # Secondly, initilize v to be the worst case scenario, and we will always try to do better than it
    # loop over the action remaining in the board and check what would the minimizing player would do
    # and it will return the value he would take, [0] means v in [v, actionToTake]
    # give alpha the maximum value between the previous alpha and the bestScore
    # for the second if, if the bestScore is better than beta we just return because the minimizing player would never go there
    # for the third if, if the best score is better than alpha, we basically make it the new value of alpha
    v = -math.inf
    for action in actions(board):
        bestScore = minValue(result(board, action), alpha, beta)[0]
        alpha = max(alpha, bestScore)
        if bestScore > v:
            v = bestScore
            actionToTake = action
        if bestScore >= beta:
            return [v, actionToTake]
        if bestScore > alpha:
            alpha = bestScore

    return [v, actionToTake]


# The maximizing function returns [v, actionToTake]
def minValue(board, alpha, beta):

    # Firstly, initliaze which actionToTake to None, and check if the board is terminal
    actionToTake = None
    if terminal(board):
        return [utility(board), None]

    # Secondly, initilize v to be the worst case scenario, and we will always try to do better than it
    # loop over the action remaining in the board and check what would the maximizing player would do
    # and it will return the value he would take, [0] means v in [v, actionToTake]
    # give beta the minimum value between the previous minimum and the bestScore
    # for the second if, if the bestScore is lower than alpha we just return because the maximizing player would never go there
    # for the third if, if the best score is lower than beta, we basically make it the new value of beta
    v = math.inf
    for action in actions(board):
        bestScore = maxValue(result(board, action), alpha, beta)[0]
        beta = min(beta, bestScore)
        if bestScore < v:
            v = bestScore
            actionToTake = action
        if bestScore <= alpha:
            return [v, actionToTake]
        if bestScore < beta:
            beta = bestScore

    return [v, actionToTake]
