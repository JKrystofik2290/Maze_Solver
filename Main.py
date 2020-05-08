import sys
import pygame
import numpy as np
import random as rand


# ------------
#   classes
# ------------
class cell:
    def __init__(self, x_offset, y_offset, x, y, size, margin, state):
        self.size = size
        self.margin = margin
        self.solution = 0
        self.state = state
        if state == 0:
            self.color = wall_color
        elif state == 1:
            self.color = valid_path_color
        elif state == 2:
            self.color = start_color
        elif state == 3:
            self.color = exit_color

        self.obj = pygame.Rect((self.size[0] + self.margin) * x + x_offset,
                               (self.size[1] + self.margin) * y + y_offset,
                               self.size[0], self.size[1])

    def update(self):
        global maze_start, maze_start_exist
        if solver_running == False:
            if self.obj.collidepoint(pygame.mouse.get_pos()):
                # left mouse click
                if pygame.mouse.get_pressed()[0] == 1:
                    # shift + left mouse click
                    if (pygame.key.get_pressed()[pygame.K_RSHIFT] == 1
                    or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1):
                        # start (can only have 1)
                        if maze[maze_start[0]][maze_start[1]].state == 2:
                            maze[maze_start[0]][maze_start[1]].state = 1
                            maze[maze_start[0]][maze_start[1]].color = valid_path_color
                        self.state = 2
                        self.color = start_color
                        maze_start = (np.where(np.isin(maze, self))[0][0],
                                      np.where(np.isin(maze, self))[1][0])
                        maze_start_exist = True
                    else:
                        if self.state == 2:
                            maze_start_exist = False
                        # wall
                        self.state = 0
                        self.color = wall_color

                # right mouse click
                if pygame.mouse.get_pressed()[2] == 1:
                    if self.state == 2:
                        maze_start_exist = False
                    # shift + right mouse click
                    if (pygame.key.get_pressed()[pygame.K_RSHIFT] == 1
                    or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1):
                        # exit
                        self.state = 3
                        self.color = exit_color
                    else:
                        # valid path
                        self.state = 1
                        self.color = valid_path_color

        pygame.draw.rect(screen, self.color, self.obj)

class selectors:
    def __init__(self, listOfLabel, x, y, w, h, margin):
        self.labels = []
        self.objs = []
        self.states = []
        self.colors = []
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.margin = margin

        for i in range(len(listOfLabel)):
            self.labels.append(font.render(listOfLabel[i], True, (33, 33, 33)))
            self.objs.append(pygame.Rect(x, y + (h + margin)*i, w, h))
            self.states.append(False)
            self.colors.append(not_selected)

    def update(self):
        if solver_running == False:
            for i in range(len(self.labels)):
                pygame.draw.rect(screen, self.colors[i], self.objs[i])
                screen.blit(self.labels[i],
                           (self.x + self.w // 2 - self.labels[i].get_rect().width // 2,
                           (self.y + i*(self.h + self.margin)
                            + self.h // 2) - self.labels[i].get_rect().height // 2))


# ------------
#  functions
# ------------
def screen_update(t):
    screen.fill(screen_bg_color)
    screen.blit(instructions_header, (maze_bg_padding, 5))
    screen.blit(instructions_wall, (maze_bg_padding, 27))
    screen.blit(instructions_path, (maze_bg_padding, 49))
    screen.blit(instructions_start, (maze_bg_padding, 71))
    screen.blit(instructions_exit, (maze_bg_padding, 93))
    screen.blit(instructions_run, (maze_bg_padding, 115))
    screen.blit(instructions_reset, (maze_bg_padding, 137))
    algorithmSelectors.update()
    pygame.draw.rect(screen, maze_bg_color, maze_bg)
    for row in maze:
        for cell in row:
            cell.update()

    pygame.display.flip()
    clock.tick(t)

def reset(new_maze):
    for row in new_maze:
        for cell in row:
            cell.solution = 0
            if cell.state == 3:
                cell.color = exit_color
            elif cell.state == 1:
                cell.color = valid_path_color

    return new_maze

def popup(msg, bg_color):
    text = font.render(msg, True, text_color)
    popup = pygame.Rect(screen_w // 2 - 75, screen_h // 2 + 50, 150, 50)
    pygame.draw.rect(screen, bg_color, popup)
    screen.blit(text, (screen_w // 2 - text.get_rect().width // 2, screen_h // 2 + 62))
    pygame.display.flip()
    pygame.time.wait(1500)

def backtracking_solver(maze, row, col):
    global exit_solver

    # need to handle events to not freeze/crash during recusion
    # also added ability to stop solver
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                exit_solver = True
                return False

    # at maze exit?
    if (row >= 0 and row < maze_size
    and col >= 0 and col < maze_size
    and maze[row][col].state == 3):

        maze[row][col].solution = 1
        maze[row][col].color = start_color
        screen_update(30)
        return True

    # is current spot valid and not already visited?
    if (row >= 0 and row < maze_size
    and col >= 0 and col < maze_size
    and maze[row][col].state > 0
    and maze[row][col].solution == 0):

        maze[row][col].solution = 1
        maze[row][col].color = start_color
        screen_update(30)

        # all 8 possible moves randomized each call
        dir = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        rand.shuffle(dir)

        for i in range(len(dir)):
            if exit_solver:
                return False
            if backtracking_solver(maze, row + dir[i][0], col + dir[i][1]):
                return True

        # set current spot to not valid & been visited
        maze[row][col].solution = 10

        # flash red to show backtracking
        maze[row][col].color = exit_color
        screen_update(20)
        # then retrun to valid_path_color
        maze[row][col].color = valid_path_color
        screen_update(30)
        return False

    return False


# -----------------------
# init variables
# -----------------------
maze_size = 30
# need to change starting_maze if maze_size is changed (maze_size = 30 when made)
starting_maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                 [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                 [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                 [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 3, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
# need to change maze_start to match start of starting_maze
maze_start = (0, 14)
maze_start_exist = True
cell_size = (20, 20)
cell_margin = 2
valid_path_color = (200, 200, 200)
start_color = (50, 200, 50)
exit_color = (200, 50, 50)
wall_color = (0, 0, 0)
top_padding = 150
maze_bg_padding = 25
maze_bg_w = maze_size * (cell_size[0] + cell_margin) + cell_margin
maze_bg_h = maze_size * (cell_size[1] + cell_margin) + cell_margin
maze_bg_color = (100, 100, 100)
screen_w = maze_bg_w + 2 * maze_bg_padding
screen_h = maze_bg_h + 2 * maze_bg_padding + top_padding
screen_bg_color = (0, 0, 0)
solver_running = False
exit_solver = False
font_size = 20
text_color = (220, 220, 220)
not_selected = (190, 190, 190)
selected = (0, 222, 20)


# ------------
# init program & objects
# ------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Solver")
screen = pygame.display.set_mode((screen_w, screen_h))
font = pygame.font.SysFont("arial", font_size, True)
instructions_header = font.render("Instructions:", True, text_color)
instructions_wall = font.render("Left Mouse Click = Maze Wall", True, text_color)
instructions_path = font.render("Right Mouse Click = Maze Path", True, text_color)
instructions_start = font.render("Shift + Left Mouse Click = Maze Start (Only 1)", True, text_color)
instructions_exit = font.render("Shift + Right Mouse Click = Maze Exit (Any #)", True, text_color)
instructions_run = font.render("Space = Start/Stop Maze Solver", True, text_color)
instructions_reset = font.render("R = Reset Maze", True, text_color)
maze_bg = pygame.Rect(maze_bg_padding,
                      maze_bg_padding + top_padding,
                      maze_bg_w, maze_bg_h)
maze = [[cell(maze_bg_padding + cell_margin,
              maze_bg_padding + cell_margin + top_padding,
              x, y, cell_size, cell_margin, starting_maze[y][x])
          for x in range(maze_size)]
          for y in range(maze_size)]
# algorithms needs to be updated when adding a new algorithm
# and must correlate index of algorithm name to event call in main loop
algorithms = ['A*', 'Dijkstra', 'Random Backtracking']
algorithmSelectors = selectors(algorithms, screen_w - 225, 5, 200, 45, 5)
# init default selection
algorithmSelectors.states[2] = True
algorithmSelectors.colors[2] = selected


# ------------
#  Main Loop
# ------------
while True:
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if maze_start_exist:
                    solver_running = True
                    if algorithmSelectors.states[algorithms.index('Random Backtracking')]:
                        if backtracking_solver(maze, maze_start[0], maze_start[1]):
                            popup('DONE!', start_color)
                        elif exit_solver:
                            popup('Solver Stopped!', exit_color)
                            exit_solver = False
                        else:
                            popup('No Exit Found!', exit_color)

                    if algorithmSelectors.states[algorithms.index('Dijkstra')]:
                        popup('Dijkstra Not Done!', exit_color)

                    if algorithmSelectors.states[algorithms.index('A*')]:
                        popup('A* Not Done!', exit_color)

                    solver_running = False

                else:
                    popup('No Maze Start!', exit_color)

            if event.key == pygame.K_r:
                maze = reset(maze)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # left mouse click
            if pygame.mouse.get_pressed()[0] == 1:
                for i in range(len(algorithmSelectors.states)):
                    if algorithmSelectors.objs[i].collidepoint(pygame.mouse.get_pos()):
                        for x in range(len(algorithmSelectors.states)):
                            algorithmSelectors.states[x] = False
                            algorithmSelectors.colors[x] = not_selected

                        algorithmSelectors.states[i] = True
                        algorithmSelectors.colors[i] = selected

    # screen update
    screen_update(60)

# todo:
    # move global vars to dict = {'val': 0}
    # add other path finding methods
        # dijkstra's algorithm
        # A*


#  next project: https://www.youtube.com/watch?v=Wo5dMEP_BbI
