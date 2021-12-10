#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Srinivas Kini | skini | skini@iu.edu
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys


# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]


# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([row.count('p') for row in house_map])

    # Return a string with the house_map rendered in a human-pichuly format


def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])


# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p', ] + house_map[row][col + 1:]] + house_map[row + 1:]


# Get the attacking range of a pichu placed on the board
def get_pichus_influence(pichu_loc, house_map):
    invalid_states = set()
    row_len = len(house_map)
    col_len = len(house_map[0])
    curr_row = pichu_loc[0]
    curr_col = pichu_loc[1]
    # Look up
    for j in range(curr_row, -1, -1):
        if house_map[j][curr_col] == 'X':
            break
        else:
            invalid_states.add((j, curr_col))

    # Look down
    for j in range(curr_row, row_len):
        if house_map[j][curr_col] == 'X':
            break
        else:
            invalid_states.add((j, curr_col))

    # Look left
    for j in range(curr_col, -1, -1):
        if house_map[curr_row][j] == 'X':
            break
        else:
            invalid_states.add((curr_row, j))

    # Look right
    for j in range(curr_col, col_len):
        if house_map[curr_row][j] == 'X':
            break
        else:
            invalid_states.add((curr_row, j))

    # Up right r-- c++
    i, j = curr_row - 1, curr_col + 1
    while i >= 0 and j < col_len:
        if house_map[i][j] == 'X':
            break
        else:
            invalid_states.add((i, j))
        i -= 1
        j += 1

    # Up left r-- c--
    i, j = curr_row - 1, curr_col - 1
    while i >= 0 and j >= 0:
        if house_map[i][j] == 'X':
            break
        else:
            invalid_states.add((i, j))
        i -= 1
        j -= 1

    # Down right r++ c++
    i, j = curr_row + 1, curr_col + 1
    while i < row_len and j < col_len:
        if house_map[i][j] == 'X':
            break
        else:
            invalid_states.add((i, j))
        i += 1
        j += 1

    # Down left r++ c--
    i, j = curr_row + 1, curr_col - 1
    while i < row_len and j >= 0:
        if house_map[i][j] == 'X':
            break
        else:
            invalid_states.add((i, j))
        i += 1
        j -= 1

    return invalid_states


# Get list of successors of given house_map state
def successors(house_map):
    pichu_locs = {(row_i, col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if
                  house_map[row_i][col_i] == "p"}  # get pichus' location on the matrix

    invalid_states = set()
    for pichu_loc in pichu_locs:
        invalid_states = invalid_states.union(
            get_pichus_influence(pichu_loc, house_map))  # merge the set of invalid states for all pichus

    return [add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0, len(house_map[0])) if
            house_map[r][c] == '.' and (r, c) not in invalid_states]  # pick the first available location greedily


# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k


# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map, k):
    fringe = [initial_house_map]
    seen_maps = set()  # set of visited states
    while len(fringe) > 0:
        curr_map = fringe.pop()
        seen_maps.add(printable_house_map(curr_map))  # encode the map as a string
        new_house_maps = successors(curr_map)
        for new_house_map in new_house_maps:
            if is_goal(new_house_map, k):
                return new_house_map, True
            if printable_house_map(new_house_map) not in seen_maps:  # check if state has been visited
                fringe.append(new_house_map)

    return None, False


# Main Function
if __name__ == "__main__":
    house_map = parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map, k)
    print("Here's what we found:")
    print(printable_house_map(solution[0]) if solution[1] else "False")
