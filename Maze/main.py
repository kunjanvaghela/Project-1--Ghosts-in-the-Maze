from queue import Empty, PriorityQueue
import numpy as np
import math

# Variable Declare
my_grid=[]              # To store grid, changes when ghost traverses will happen in this directly.
my_grid_original=[]     # To store original grid, with original position of ghosts
invalid_indices=[]      # To store indices which are blocked, and where ghost cannot pop up
grid_size=6            # Size of the grid
nr_of_ghosts=1          # Number of the ghosts to conjure
start_pos = (0,0)
final_pos = (grid_size-1, grid_size-1)
a1Survivability=dict()

# To create the grid
def create_grid(grid_size, blocked_cell=0.28):
    while True:
        my_grid = np.random.rand(grid_size,grid_size)
        # Populates grid with 1 (Blocked cell) and 0 (Unblocked cell) based on probability given by blocked_cell.        
        my_grid = np.where(my_grid<=blocked_cell, 1, 0)
        # Start position and goal must be unblocked
        my_grid[0][0]=0
        my_grid[grid_size-1, grid_size-1] = 0
        # print(my_grid)
        # To check using Depth First Search if grid has a path to reach from the start to the goal
        if (depth_first_search(my_grid, grid_size-1, grid_size-1)):
            break
    return my_grid


# To get randomly generated coordinates to spawn ghosts.
def get_ghost_cell_index():
    while True:
        row_index = np.random.randint(0, grid_size)
        column_index = np.random.randint(0, grid_size)
        # print('Random coordinate of Ghost populated : '+str(row_index)+','+str(column_index))
        # Checks if the randomly generated coordinates is not within invalid_indices, and then returns the coordinates. 
        if [row_index,column_index] not in invalid_indices:
            #print('Indices are valid.')
            if row_index==0 and column_index==0:
                print('row_index==0 and column_index==0; invalid_indices : '+ str(invalid_indices))
                continue
            if my_grid[row_index,column_index]==1:
                print('Generated ghost on Blocked wall : '+str(row_index)+','+str(column_index))
            if (depth_first_search(my_grid, row_index, column_index)):
                # print('Ghost populated')
                return row_index, column_index
        else:
            # print('Invalid Indices found')
            continue    # Can remove this in final code

# This function will call get_ghost_cell_index() to create ghosts based on number of ghosts received.
def place_ghosts(num_ghosts):
    global invalid_indices
    for i in range(num_ghosts):
        row_ind, col_ind = get_ghost_cell_index()
        my_grid[row_ind][col_ind] = my_grid[row_ind][col_ind] - 10
        # print(my_grid)
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
                # print('Path exists')
                # print('Fringe : '+str(fringe))
                # print('Explored Path : '+str(explored))
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
            # print('Path does not exist!')
            return False
    except Exception as error111:
        print('No path present')
        print(error111)
        return False

# For retrieving Path found from BFS Algo
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


# Heuristic of Manhattan Distance
def h(cell1, cell2):
    x1,y1 = cell1       # Represents cell1 coordinates
    x2,y2 = cell2       # Represents cell2 coordinates
    return abs(x1-x2) + abs(y1-y2)      # Maanhattan distance between cell1 and cell2

# A Star Algorithm with Heuristic of Manhattan Distance     -- Returns Forward Path determined as part of the Algo in the grid
def aStar(gridd, start_x=0, start_y=0, goal_x=grid_size-1, goal_y=grid_size-1):
    start=(start_x,start_y)
    gridPos=[]
    a=0
    for i in gridd:
        for j in range(len(i)):
            gridPos.append((a,j))
        a=a+1
    print('gridPos = '+str(gridPos))
    g_score={cell: float('inf') for cell in gridPos}
    g_score[start]=0
    f_score={cell: float('inf') for cell in gridPos}
    f_score[start] = h(start, (goal_x, goal_y))     # Heuristic cost of start cell + g_score of the start cell. Since g_score of start cell is 0, only heuristic cost is assigned
    print('g_score : ' + str(g_score))
    print('f_score : ' + str(f_score))
    openQueue = PriorityQueue()             # Assigned Priority Queue
    openQueue.put(((h(start, (goal_x, goal_y)) + 0), h(start, (goal_x, goal_y)), start))      # Priority Queue contains tuple in order: 1) Heuristic Cost + g_score, 2) Heuristic cost, and 3) start cell
    aPath = {}
    #print('openQueue : '+str(openQueue.get()))
    while not openQueue.empty():
        currCell = openQueue.get()[2]           # Cell value in the Priority Queue is selected as the current cell for this loop
        print('currCell : '+ str(currCell))
        if currCell == (goal_x,goal_y):
            print('currCell reached to goalCell : '+str(currCell))
            break
        # write code to check each side : LUDR and check if not going array out of bounds
        # Code to select nextCell as Left
        if currCell[1] != 0:
            if (my_grid[currCell[0], (currCell[1] - 1)] % 10) == 0:
                nextCell = (currCell[0], (currCell[1] - 1))
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                # print('In Left loop')
        # Code to select nextCell as Up
        if currCell[0] != 0:
            if (my_grid[(currCell[0] - 1), currCell[1]] % 10) == 0:
                nextCell = ((currCell[0] - 1), currCell[1])
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                # print('In Up loop')
        # Code to select nextCell as Down
        if currCell[0] != (grid_size - 1):
            if (my_grid[currCell[0] + 1, currCell[1]] % 10) == 0:
                nextCell = ((currCell[0] + 1), currCell[1])
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                print('f1 : '+str(f1)+'; type:'+ str(type(f1)))
                print('f_score : '+str(f_score)+'; type:'+ str(type(f_score)))
                print(f_score[nextCell])
                print('f_score[nextCell] : '+str(f_score[nextCell])+'; type:'+ str(type(f_score[nextCell])))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                # print('In Down loop')
        # Code to select nextCell as Right
        if currCell[1] != (grid_size - 1):
            if (my_grid[currCell[0], currCell[1] + 1] % 10) == 0:
                nextCell = (currCell[0], (currCell[1] + 1))
                print(nextCell)
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                # print('In Right loop')
    print(openQueue)
    print('aPath : '+str(aPath))
    fwdPath={}
    goal_xy=(goal_x,goal_y)
    while goal_xy!=start:
        fwdPath[aPath[goal_xy]] = goal_xy
        goal_xy = aPath[goal_xy]
    print('fwdPath : '+ str(fwdPath))
    return fwdPath


def create_env():
    global my_grid, invalid_indices
    my_grid = create_grid(grid_size)
    invalid_indices = set_invalid_indices()
    invalid_indices = invalid_indices.tolist()
    # print('Invalid Indices: ' + str(invalid_indices))
    my_grid = place_ghosts(nr_of_ghosts)
    # print(my_grid)

#MANAN-START
# Method for Random movements for ghosts, 
# It accounts for Ghosts position at call [spawn if Timestamp=0] considers the probability of moving to LUDR
# Or Stay at the same place.

# Kunjan Edits:
#   1) Changing argument - removing my_grid as argument and implementing global my_grid to avoid copying my_grid after ghost movement.
#   2) Changed hardcoded 3 to 'gridsize-1'
#   3) Possible if-else error. Changing to if-elif-else:
# def ghostmovement(my_grid):
def ghostmovement():
    global my_grid
    #ghostPositionList=[[1,1],[2,3],[3,0],[3,1]]
    ghostPositionList=np.argwhere(my_grid < 0)
    for index in ghostPositionList:
        no_of_ghosts=abs(math.ceil(my_grid[index[0],index[1]]/10))
        while no_of_ghosts>1:
            ghostPositionList.__add__(index)
            no_of_ghosts=no_of_ghosts-1

    #ghostPositionList=[[1,1],[2,3]]
    print('OG GRID',my_grid)
    for list in ghostPositionList:              #for element in list:
            #L=(1) U=(2) D=(3) R=(4)
            print(list)
            if(list[0]==0 and list[1]==0): #START :CANT GO UP AND LEFT
                    direction=np.random.choice([3,4])
                    print('5')
            elif(list[0]==0 and list[1]==(grid_size - 1)): #RIGHT TOP :CANT GO UP AND RIGHT
                    direction=np.random.choice([1,3])
                    print('6')
            elif(list[0]==(grid_size - 1) and list[1]==0): #BOTTOM LEFT :CANT GO DOWN AND LEFT
                    direction=np.random.choice([2,4])
                    print('7')
            elif(list[1]==(grid_size - 1) and list[1]==(grid_size - 1)): #GOAL :CANT GO DOWN AND RIGHT
                    direction=np.random.choice([1,2])
                    print('8')
            elif(list[1]==0):
                    direction=np.random.choice([2,3,4])     # If ghost is on the left most cell, can only go Up, Down and Right
                    print('1')
            elif(list[0]==0):
                    direction=np.random.choice([1,3,4])     # If ghost is on the top most cell, can only go Left, Down and Right
                    print('2')
            elif(list[0]==(grid_size - 1)):
                    direction=np.random.choice([1,2,4])     # If ghost is on the bottom most cell, can only go Left, Up and Right
                    print('3')
            elif(list[1]==(grid_size - 1)):
                    direction=np.random.choice([1,2,3])     # If ghost is on the right most cell, can only go Left, Up and Down
                    print('4')
            else:
                direction=np.random.randint(low=1, high=5)
                print('9')
            print('GHOST POSITION',list) 
            print('Random Direction:L=(1) U=(2) D=(3) R=(4)::',direction)
            
            
            #L=(1) U=(2) D=(3) R=(4)
            if direction==1 : #GO-LEFT
                           
                if (my_grid[list[0]][list[1]-1]==0 or my_grid[list[0]][list[1]-1]%10==0) and (list[1]>0) : #OPEN CELL
                    #print('LEFT',my_grid[list[0]][list[1]-1]) 
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]][list[1]-1]=my_grid[list[0]][list[1]-1]-10
                    list[1]=list[0]-1
                elif (my_grid[list[0]][list[1]-1]==1 or my_grid[list[0]][list[1]-1]%10!=0) and (list[1]>0): #BLOCKED CELL
                    #print('LEFT',my_grid[list[0]][list[1]-1])
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]][list[1]-1]=my_grid[list[0]][list[1]-1]-10
                        list[1]=list[0]-1
                    else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED
                    
            elif direction==2 :#GO-UP
                if (my_grid[list[0]-1][list[1]]==0 or my_grid[list[0]-1][list[1]]%10==0) and (list[0]>0) : #OPEN CELL
                    #print('UP',my_grid[list[0]-1][list[1]])
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]-1][list[1]]=my_grid[list[0]-1][list[1]]-10
                    list[1]=list[1]-1
                elif (my_grid[list[0]-1][list[1]]==1 or my_grid[list[0]-1][list[1]]%10!=0) and (list[0]>0): #BLOCKED CELL
                    print('UP',my_grid[list[0]-1][list[1]])
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]-1][list[1]]=my_grid[list[0]-1][list[1]]-10
                        list[1]=list[1]-1
                    else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED

            # KV: Check for possible bugs as written in comment below - Ref:Bug01
            elif direction==3 : #GO-DOWN
                if (my_grid[list[0]+1][list[1]]==0 or my_grid[list[0]+1][list[1]]%10==0) and (list[0]<grid_size) : #OPEN CELL   #KV: Changed from 'my_grid[list[0]][list[1]+1]==0' to 'my_grid[list[0]+1][list[1]]==0'  - Ref:Bug01
                    #print('DOWN',my_grid[list[0]+1][list[1]])
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]+1][list[1]]=my_grid[list[0]+1][list[1]]-10
                    list[1]=list[1]+1
                elif (my_grid[list[0]+1][list[1]]==1 or my_grid[list[0]+1][list[1]]%10!=0) and (list[0]<grid_size): #BLOCKED CELL   #KV: Changed from 'my_grid[list[0]][list[1]+1]==0' to 'my_grid[list[0]+1][list[1]]==0' - Ref:Bug01
                    #print('DOWN',my_grid[list[0]+1][list[1]])
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]+1][list[1]]=my_grid[list[0]+1][list[1]]-10
                        list[1]=list[1]+1
                    else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED


            else :#GO-RIGHT 
                if (my_grid[list[0]][list[1]+1]==0 or my_grid[list[0]][list[1]+1]%10==0) and (list[1]<grid_size) : #OPEN CELL
                    #print('RIGHT',my_grid[list[0]][list[1]+1])
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]][list[1]+1]=my_grid[list[0]][list[1]+1]-10
                    list[1]=list[0]+1
                elif (my_grid[list[0]][list[1]+1]==1 or my_grid[list[0]][list[1]+1]%10!=0) and (list[1]<grid_size): #BLOCKED CELL
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]][list[1]+1]=my_grid[list[0]][list[1]+1]-10
                        list[1]=list[0]+1
                    else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED
    print('--------------------')        

    print('GRID MOVEMENT',my_grid)

    #MANAN-END


def agentOneTraversal():
    a1 = start_pos          # Agent 1 coordinates denoted by this variable
    aStarPathDetermined = aStar(my_grid)
    print('aStarPathDetermined for Agent 1 : '+str(aStarPathDetermined))
    while (a1 != final_pos):
        nextLocA1 = aStarPathDetermined[a1]
        ghostmovement()
        print(nextLocA1)
        if my_grid[nextLocA1] == 1:
            print('Agent is in Blocked Cell. Some Serious Error !!!!!!!!!!!!!!')
        if my_grid[nextLocA1] != 0:
            print('Agent not in Open Cell. Ghost Encountered ????????????')
            print(my_grid[nextLocA1])
            return False
        a1 = nextLocA1
        # break
    return True


if __name__=='__main__':
    create_env()
    print('Original Grid generated : ')
    print(my_grid)
    my_grid_original = my_grid                  # To have a backup of original grid
    print('Copied above grid to my_grid_original :')

    # Agent 1 Traversing
    agentOneReached = agentOneTraversal()
    print('Agent One Reached : ' + str(agentOneReached))
    print(my_grid)

    # Agent 1 Traversing
    nr_of_ghosts=1
    while True:                 # Loop to check till what number can the Agent survive
        for i in range(1,10):
            create_env()            # New Env everytime
            agentOneReached = agentOneTraversal()       # Agent 1 Traversal path with A* Algorithm
            print('Agent One Reached : ' + str(agentOneReached))
            if nr_of_ghosts in a1Survivability:         # Dictionary containing results of Agent 1's Traversal success
                a1Survivability[nr_of_ghosts].append(agentOneReached)
            else:
                a1Survivability[nr_of_ghosts] = [agentOneReached]
            print(my_grid)
        print(a1Survivability)
        if True not in a1Survivability[nr_of_ghosts]:       # Loop must break if Agent 1's survivability is no more.
            break
        if nr_of_ghosts>30:         # A check to limit how many times loop will go on, safety mechanism
            break
        nr_of_ghosts+=1



    # print('----------------- BFS Output -----------------')
    # print(breadth_first_search(my_grid))
    # aStar(my_grid)