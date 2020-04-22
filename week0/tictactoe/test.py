"""
Tic Tac Toe Player
"""

import math
import copy


X = "X"
O = "O"
EMPTY = None


State = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
x_h = [[EMPTY, EMPTY, EMPTY], [X, X, X], [EMPTY, EMPTY, EMPTY]]
o_h = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [O, O, O]]
x_v = [[X, EMPTY, EMPTY], [X, EMPTY, EMPTY], [X, EMPTY, EMPTY]]
o_v = [[EMPTY, EMPTY, O], [EMPTY, EMPTY, O], [EMPTY, EMPTY, O]]
x_d = [[X, EMPTY, EMPTY], [EMPTY, X, EMPTY], [EMPTY, EMPTY, X]]
o_d = [[EMPTY, EMPTY, O], [EMPTY, O, EMPTY], [O, EMPTY, EMPTY]]
x_d_1 = [[EMPTY, EMPTY, X], [EMPTY, X, EMPTY], [X, EMPTY, EMPTY]]
o_d = [[EMPTY, EMPTY, O], [EMPTY, O, EMPTY], [O, EMPTY, EMPTY]]
o_d_1 = [[O, EMPTY, EMPTY], [EMPTY, O, EMPTY], [EMPTY, EMPTY, O]]
full = [[X, O, X], [O, X, O], [O, X, O]]
n_full = [[X, O, X], [O, EMPTY, O], [O, X, O]]

x_almost = [[X, O, EMPTY], [EMPTY, EMPTY, O], [X, O, O]]
o_almost = [[EMPTY, O, O], [X, X, EMPTY], [EMPTY, EMPTY, EMPTY]]
center = [[EMPTY, EMPTY, EMPTY], [EMPTY, X, EMPTY], [EMPTY, EMPTY, X]]


a_u_test = [x_almost]
tests = [State, x_h, o_h, x_v, o_v, x_d, o_d, x_d_1, o_d_1, x_almost, o_almost]

def draw_state(state):
    for rows in state:				
        for cell in rows:
            if cell == None:
                print("#", end='')
            else:
                print(cell, end='')	
        print()            			    								
  


def player(board):
    """
    Returns player who has the next turn on a board. Need to replace print with return once done
    """
    X_count = 0
    O_count = 0
    

    for lists in board:
        X_count += lists.count("X")
        O_count += lists.count("O")		 
	
    if X_count <= O_count:
        # and not terminal state
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                action_set.add((i,j))
    return action_set									       		

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    turn = player(board)
    
    possible_moves = actions(board)
    if action not in possible_moves:
        raise ValueError("Not a legal move")
    else:
        result_board = copy.deepcopy(board)
        result_board[action[0]][action[1]] = turn
    
    return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontals
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O
    
    # Verticals
    for j in range(0,3):
        if [row[j] for row in board].count(X) == 3:
            return X
        elif [row[j] for row in board].count(O) == 3:
            return O
     
    # Diagonals
    if [board[i][i] for i in range(0,3)].count(X) == 3:
        return X
    elif [board[i][i] for i in range(0,3)].count(O) == 3:
        return O
    
    if [board[2-i][i] for i in range(0,3)].count(X) == 3:
        return X
    elif [board[2-i][i] for i in range(0,3)].count(O) == 3:
        return O
    
    else:
        return None        

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not winner(board) == None:
        return True
    elif len(actions(board)) == 0:
        return True     
    else:
        return False
        
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) == True:
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # TODO alphabeta pruning
    turn = player(board)
    action_utility = {}
    
    
    for action in actions(board):
        print(action)
        new_state = result(board,action)
        u_new_state = utility(new_state)
        action_utility[action] = u_new_state  
    
    if turn == X:
        return max(action_utility.items(), key=lambda k: k[1])[0]
    else: 
        return min(action_utility.items(), key=lambda k: k[1])[0]
        

