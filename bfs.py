from copy import deepcopy

def print_results(board):
    print("Solution: " + board.getDirections())

def search(board):
    nodes_generated = 0
    nodes_repeated = 0
    if board.is_win():
        print_results(board)
        return board
    initial_node = deepcopy(board)
    nodes_generated += 1
    frontier = []
    frontier.append(initial_node)
    explored = set()
    keep_searching = True
    while keep_searching:
        if len(frontier) == 0:
            print("Solution not found")
            return
        else:
            current_node = frontier.pop()
            moves = current_node.moves_available()
            current_node.fdiamonds = frozenset(current_node.diamonds)
            explored.add(current_node)
            for move in moves:
                child_node = deepcopy(current_node)
                nodes_generated += 1
                child_node.move(move)
                if child_node not in explored:
                    if child_node.is_win():
                        print_results(child_node)
                        return child_node
                    frontier.append(child_node)
                else:
                    nodes_repeated += 1
