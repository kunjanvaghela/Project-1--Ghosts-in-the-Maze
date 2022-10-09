from calendar import c
from glob import glob
from queue import Empty
import numpy as np
import time

# Variable Declare
my_grid=[]              # To store grid
invalid_indices=[]      # To store indices which are blocked, and where ghost cannot pop up
grid_size=51           # Size of the grid
nr_of_ghosts=13          # Number of the ghosts to conjure

# To create the grid
def create_grid(grid_size, blocked_cell=0.28):
    while True:
        my_grid = np.random.rand(grid_size,grid_size)
        # Populates grid with 1 (Blocked cell) and 0 (Unblocked cell) based on probability given by blocked_cell.        
        my_grid = np.where(my_grid<=blocked_cell, 1, 0)
        # Start position and goal must be unblocked
        my_grid[0][0]=0
        my_grid[grid_size-1, grid_size-1] = 0
        print(my_grid)
        # To check using Depth First Search if grid has a path to reach from the start to the goal
        if (depth_first_search(my_grid, grid_size-1, grid_size-1)):
            break
    return my_grid


# To get randomly generated coordinates to spawn ghosts.
def get_ghost_cell_index():
    while True:
        row_index = np.random.randint(0, grid_size)
        column_index = np.random.randint(0, grid_size)
        print('Random coordinate of Ghost populated : '+str(row_index)+','+str(column_index))
        # Checks if the randomly generated coordinates is not within invalid_indices, and then returns the coordinates. 
        if [row_index,column_index] not in invalid_indices:
            #print('Indices are valid.')
            if row_index==0 and column_index==0:
                print('row_index==0 and column_index==0; invalid_indices : '+ str(invalid_indices))
                continue
            if my_grid[row_index,column_index]==1:
                print('Generated ghost on Blocked wall : '+str(row_index)+','+str(column_index))
            if (depth_first_search(my_grid, row_index, column_index)):
                print('Ghost populated')
                return row_index, column_index
        else:
            print('Invalid Indices found')

# This function will call get_ghost_cell_index() to create ghosts based on number of ghosts received.
def place_ghosts(num_ghosts):
    global invalid_indices
    for i in range(num_ghosts):
        row_ind, col_ind = get_ghost_cell_index()
        my_grid[row_ind][col_ind] = my_grid[row_ind][col_ind] - 10
        print(my_grid)
        # invalid_indices = np.append(invalid_indices, [[row_ind, col_ind]], axis=0)
        # invalid_indices = invalid_indices.tolist()
    #print('Invalid Indices : ' + str(invalid_indices))
    return my_grid   

def set_invalid_indices():
    invalid_indices = np.argwhere(my_grid == 1)
    invalid_indices = np.append(invalid_indices, [[0,0]], axis=0)
    invalid_indices = np.append(invalid_indices, [[grid_size-1, grid_size-1]], axis=0)
    return invalid_indices

# Depth First Search algorithm
def depth_first_search(my_grid, goal_x, goal_y):
    start = [0,0]
    fringe = [start]
    #print('Fringe : '+ str(fringe) + str(type(fringe)))
    #print('Start : '+ str(start) + str(type(start)))
    explored = [start]
    i=0     # can be deleted later, just a safety mechanism to analyze infinite loops
    try:
        while len(fringe) > 0:
            currCell = fringe.pop()
            #print('Fringe : '+str(fringe))
            #print('currcell : ' + str(currCell) + str(type(currCell)))
            if currCell not in explored:            # to solve the issue where code was revisiting already explored cells
                explored.append(currCell)
            #explored.append(nextCell)      # when was this appended? Unsure
            if currCell == [goal_x, goal_y]:
                print('Path exists')
                print('Fringe : '+str(fringe))
                print('Explored Path : '+str(explored))
                return True
            # write code to check each side : LUDR and check if not going array out of bounds
            # Code to select nextCell as Left
            if currCell[1] != 0:
                if (my_grid[currCell[0], (currCell[1] - 1)] % 10) == 0:
                    nextCell = [currCell[0], (currCell[1] - 1)]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    #print('In first loop')
            # Code to select nextCell as Up
            if currCell[0] != 0:
                if (my_grid[(currCell[0] - 1), currCell[1]] % 10) == 0:
                    nextCell = [(currCell[0] - 1), currCell[1]]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    #print('In sec loop')
            # Code to select nextCell as Down
            if currCell[0] != (grid_size - 1):
                if (my_grid[currCell[0] + 1, currCell[1]] % 10) == 0:
                    nextCell = [(currCell[0] + 1), currCell[1]]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    #print('In third loop')
            # Code to select nextCell as Right
            if currCell[1] != (grid_size - 1):
                if (my_grid[currCell[0], currCell[1] + 1] % 10) == 0:
                    nextCell = [currCell[0], (currCell[1] + 1)]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    #print('In fourth loop')
            if nextCell in explored:
                continue
            if nextCell is None:
                print('nextCell is not defined. Path probably does not exist')
                return False
            explored.append(nextCell)
            #fringe.append(nextCell)        # Dont remember, useful?
            #print('Fringe : '+str(fringe))
            #print('Explored : '+str(explored))
             # can be deleted later, just a safety mechanism to analyze infinite loops
            i=i+1
            if i>200:
                print('Value of i is more than threshold')
                return False
        else:
            print('Path does not exist!')
            return False
    except Exception as error111:
        print('No path present')
        print(error111)
        return False


def print_bfs_path(childToParentMapping, goalCell):
    # childToParentMapping = {(1, 0): {(0, 0)}, (0, 1): {(0, 0)}, (2, 0): {(1, 0)}, (2, 1): {(2, 0)}, (3, 1): {(2, 1)}, (2, 2): {(2, 1)}, (2, 3): {(2, 2)}, (3, 3): {(2, 3)}}
    # goalCell = (3,3)
    curr = goalCell
    path = []
    path.append(goalCell)
    while curr != (0,0):
        val = childToParentMapping[curr]
        curr = list(val)[0]
        path.append(curr)
    return path

# Breadth First Search algorithm
def breadth_first_search(my_grid, goal_x=grid_size-1, goal_y=grid_size-1, start_x=0, start_y=0):
    print('In BFS')
    start = [start_x, start_y]
    fringe = [start]
    print('Fringe : '+ str(fringe) + str(type(fringe)))
    print('Start : '+ str(start) + str(type(start)))
    explored = [start]
    childToParentMap = {}
    # bfs_path = {}
    # pathFwd = {}
    startTuple = (start_x,start_y)
    i=0     # can be deleted later, just a safety mechanism to analyze infinite loops
    # try:
    while len(fringe) > 0:
        currCell = fringe.pop(0)
        print('Fringe : '+str(fringe))
        print('currcell : ' + str(currCell) + str(type(currCell)))
        if currCell not in explored:            # to solve the issue where code was revisiting already explored cells
            explored.append(currCell)
        #explored.append(nextCell)      # when was this appended? Unsure
        if currCell == [goal_x, goal_y]:
            print('Path exists')
            print('Final Fringe : '+str(fringe))
            print('Explored Path : '+str(explored))
            # print('BFS_Path : '+str(bfs_path))
            path_xy = (goal_x, goal_y)
            # while path_xy != startTuple:
                # pathFwd[bfs_path[path_xy]] = path_xy
                # path_xy = bfs_path[path_xy]
            #     print('PathFwd : '+str(pathFwd))
            # return pathFwd
            return print_bfs_path(childToParentMap, (goal_x,goal_y))
        # write code to check each side : LUDR and check if not going array out of bounds
        # Code to select nextCell as Left
        if currCell[1] != 0:
            if (my_grid[currCell[0], (currCell[1] - 1)] % 10) == 0:
                nextCell = [currCell[0], (currCell[1] - 1)]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            val = childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = val
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
                print('In Left loop')
        # Code to select nextCell as Up
        if currCell[0] != 0:
            if (my_grid[(currCell[0] - 1), currCell[1]] % 10) == 0:
                nextCell = [(currCell[0] - 1), currCell[1]]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            val = childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = val
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
                print('In Up loop')
        # Code to select nextCell as Down
        if currCell[0] != (grid_size - 1):
            if (my_grid[currCell[0] + 1, currCell[1]] % 10) == 0:
                nextCell = [(currCell[0] + 1), currCell[1]]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            val = childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = val
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
                print('In Down loop')
        # Code to select nextCell as Right
        if currCell[1] != (grid_size - 1):
            if (my_grid[currCell[0], currCell[1] + 1] % 10) == 0:
                nextCell = [currCell[0], (currCell[1] + 1)]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            val = childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = val
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
                print('In Right loop')
        print('Fringe : '+str(fringe))
        print('Explored : '+str(explored))
        # print('BFS Path : '+str(bfs_path))
        if nextCell in explored:
            print('if nextCell in explored Executed. nextCell : '+str(nextCell))
            continue
        if nextCell is None:
            print('nextCell is not defined. Path probably does not exist')
            return print_bfs_path(childToParentMap, (goal_x,goal_y))
            # return pathFwd
        explored.append(nextCell)
        # bfs_path[tuple(nextCell)] = tuple(currCell)
        #fringe.append(nextCell)        # Dont remember, useful?
        print('Fringe : '+str(fringe))
        print('Explored : '+str(explored))
        # print('BFS Path : '+str(bfs_path))
        # can be deleted later, just a safety mechanism to analyze infinite loops
        i=i+1
        print("VAL" + str(i))
        if i>2000:
            print('Value of i is more than threshold')
            # return pathFwd
            return print_bfs_path(childToParentMap, (goal_x,goal_y))
    else:
        print('Path does not exist!')
        return False
    # except Exception as error111:
    #     print('No path present')
    #     print(error111)
    #     return pathFwd
        

def create_env():
    global my_grid, invalid_indices
    my_grid = create_grid(grid_size)
    invalid_indices = set_invalid_indices()
    invalid_indices = invalid_indices.tolist()
    print('Invalid Indices: ' + str(invalid_indices))
    my_grid = place_ghosts(nr_of_ghosts)
    # print(my_grid)

create_env()
print(breadth_first_search(my_grid))

# print(print_bfs_path('a', 'b'))
