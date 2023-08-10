import pygame
import time
import random
from utils import variables, algorithms
from maze import Maze
from ghosts import Ghosts
from agent import Agent

# Maze Variables
grid = []
visited = []
# stack = []
# solution = []
agent_type = 1

# Pygame visualizer variables
window_size = variables.GRID_WIDTH*variables.GRID_SIZE + variables.GRID_WIDTH*2 # 440
fps = 5

# Pygame Initialize
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((window_size, window_size + 40))
pygame.display.set_caption("Ghosts in the Maze")
clock = pygame.time.Clock()

# Import images
IMG_GHOST = pygame.image.load('Images/Ghost.jpeg').convert_alpha()

# Draw Text Function
text_font = pygame.font.SysFont(name=variables.FONT_NAME, size=variables.FONT_SIZE, bold=variables.FONT_BOLD, italic=variables.FONT_ITALIC)
def draw_text(text, x, y):
    img = text_font.render(text, True, variables.FONT_COLOR)
    screen.blit(img, (x, y))

def simulation_stats():
    draw_text("Agent : "+str(agent_type), 20, window_size)
    
# build the gridd
def build_grid(maze):
    screen.fill(variables.CLR_BACKGROUND)        # Coloring the bg black
    x, y, w = variables.START_X, variables.START_Y, variables.GRID_WIDTH
    env_grid = maze.get_my_grid()
    for i in range(variables.GRID_SIZE):            # To draw the lines
        x = w      # to start position
        y += w     # new row
        grid.append([])
        for j in range(variables.GRID_SIZE):
            # Drawing the Walls
            if ((env_grid[i][j] % 10) != 0):
                RECT_WALL = pygame.Rect(x, y, variables.GRID_WIDTH, variables.GRID_WIDTH)
                pygame.draw.rect(screen, variables.CLR_WALL, RECT_WALL)
            # Drawing determined path
            if ((i, j) in path_determined.keys()):
                RECT_PATH = pygame.Rect(x, y, variables.GRID_WIDTH, variables.GRID_WIDTH)
                pygame.draw.rect(screen, variables.CLR_PATH, RECT_PATH)
            # Drawing Agent
            pygame.draw.rect(screen, variables.CLR_CURRCELL, RECT_CURRCELL)
            RECT_CURRCELL.x = variables.GRID_WIDTH * agent_position[1] + variables.GRID_WIDTH
            RECT_CURRCELL.y = variables.GRID_WIDTH * agent_position[0] + variables.GRID_WIDTH
            # Putting ghosts
            if (env_grid[i][j] < 0):
                RECT_GHOST = IMG_GHOST.get_rect(topleft = (x + variables.ADJUSTER1, y))
                screen.blit(IMG_GHOST, RECT_GHOST)
            # Drawing the walls
            pygame.draw.line(screen, variables.CLR_LINE, [x, y], [x+w, y])   # Cell top
            pygame.draw.line(screen, variables.CLR_LINE, [x+w, y], [x+w, y+w])   # Cell right
            pygame.draw.line(screen, variables.CLR_LINE, [x, y], [x, y+w])   # Cell left
            pygame.draw.line(screen, variables.CLR_LINE, [x, y+w], [x+w, y+w])   # Cell top
            grid[i].append((x, y))     # add cell to grid list
            x += w     # move cell to new position


maze = Maze()
ghosts = Ghosts(maze, num_ghosts=8)
agent = Agent(agent_type)
if agent.get_agent_type() == 1:
    path_determined = agent.agent_one_traversal(maze)       # Agemt 1 Path
    print(path_determined)
    agent_position = (variables.START_X, variables.START_Y)
RECT_CURRCELL = pygame.Rect(agent_position[0], agent_position[1], variables.GRID_WIDTH, variables.GRID_WIDTH)       # for Agent
build_grid(maze)
print(maze.get_my_grid())


# RECT_GHOST = IMG_GHOST.get_rect(topleft = (grid[0][0][0] + variables.ADJUSTER1, grid[0][0][1]))
# pos_currcell_x = grid[10][4][0]
# pos_currcell_y = grid[10][4][1]
# RECT_CURRCELL = pygame.Rect(grid[10][4][0], grid[10][4][1], variables.GRID_WIDTH, variables.GRID_WIDTH)

running = True
simulation = True
build_grid(maze)
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if simulation == True:
        simulation_stats()
        if agent_position == (variables.GRID_SIZE - 1, variables.GRID_SIZE - 1) or maze.my_grid[agent_position[0]][agent_position[1]] != 0:
            time.sleep(3)
            simulation = False
            # running = False
            # break
        else:
            nextLocA1 = path_determined[agent_position]
        ghosts.ghostmovement(maze.my_grid)
        
        pygame.display.update()
        print(agent_position)
        agent_position = nextLocA1
        build_grid(maze)     # Building the lines




def agentRun():
    pass
