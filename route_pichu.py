#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Srinivas Kini | skini | skini@iu.edu
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys


# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]


# def parse_map_str(map):
#     return [[char for char in row] for row in map.split('\n')]


# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
    return 0 <= pos[0] < n and 0 <= pos[1] < m


# Find the possible moves from position (row, col)
def moves(map, row, col):
    moves = ((row + 1, col, 'D'), (row - 1, col, 'U'), (row, col - 1, 'L'), (row, col + 1, 'R'))
    # Add the notation to represent directions as a part of the moves tuple

    # Return only moves that are within the house_map and legal (i.e. go through open space ".")
    return [move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@")]


# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
    pichu_loc = [(row_i, col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if
                 house_map[row_i][col_i] == "p"][0]
    fringe = [(pichu_loc, 0, '')]
    visited = set()  # maintain a set of visited nodes to avoid revisiting
    while fringe:
        (curr_move, curr_dist, pos) = fringe.pop(0)  # current node being explored
        if house_map[curr_move[0]][curr_move[1]] == "@":
            return len(pos), pos
        visited.add(curr_move)
        valid_moves = moves(house_map, *curr_move)  # successor functions
        for move in valid_moves:
            if move not in visited:
                fringe.append(((move[0], move[1]), curr_dist + 1, pos + move[2]))

    return -1, None


# Main Function
if __name__ == "__main__":
    house_map = parse_map(sys.argv[1])
    print("Shhhh... quiet while I navigate!")
    solution = search(house_map)
    print("Here's the solution I found:")
    print(str(solution[0]) + " " + solution[1])
