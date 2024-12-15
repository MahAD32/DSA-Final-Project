import numpy as np
import random
import heapq 

class TreeNode:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.children = []

def build_decision_tree(board, depth=5):
    root = TreeNode(None, None, None)
    nodes = [root]
    for _ in range(depth):
        next_nodes = []
        for node in nodes:
            for num in range(1, 10):
                new_child = TreeNode(None, None, num)
                node.children.append(new_child)
                next_nodes.append(new_child)
        nodes = next_nodes
    return root

def generate_graph(board):
    graph = {}
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                neighbors = []
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        neighbors.append(num)
                graph[(row, col)] = neighbors
    return graph

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in board[:, col]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row + 3, start_col:start_col + 3]:
        return False
    return True

def dfs_solve(board, graph):
    if not graph:
        return True
    cell, values = next(iter(graph.items()))
    row, col = cell
    for value in values:
        if is_valid(board, row, col, value):
            board[row][col] = value
            new_graph = {k: v for k, v in graph.items() if k != cell}
            if dfs_solve(board, new_graph):
                return True
            board[row][col] = 0
    return False

def solve_sudoku_with_dfs(board):
    graph = generate_graph(board)
    return dfs_solve(board, graph)

def dfs_tree(node, depth, base_board):
    if depth == 0:
        return True
    for child in random.sample(node.children, len(node.children)):
        row, col = random.randint(0, 8), random.randint(0, 8)
        if base_board[row][col] == 0 and is_valid(base_board, row, col, child.value):
            base_board[row][col] = child.value
            if dfs_tree(child, depth - 1, base_board):
                return True
            base_board[row][col] = 0
    return False

def generate_sudoku(difficulty="medium"):
    base_board = np.zeros((9, 9), dtype=int)
    dfs_solve(base_board, generate_graph(base_board))
    if difficulty == "hard":
        decision_tree = build_decision_tree(base_board, depth=7)
        dfs_tree(decision_tree, depth=7, base_board=base_board)
    num_removed = {"easy": 40, "medium": 50, "hard": 60}[difficulty]
    for _ in range(num_removed):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while base_board[row, col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        base_board[row, col] = 0
    return base_board

def dijkstra(graph, start, end):
    pq = [(0, start)]
    distances = {start: 0}
    predecessors = {start: None}
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node == end:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = predecessors[current_node]
            return path[::-1]
        for neighbor in graph[current_node]:
            distance = current_distance + 1
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    return None
