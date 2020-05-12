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
        self.visited = 0
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
        if solver_running == False:
            if self.obj.collidepoint(pygame.mouse.get_pos()):
                # left mouse click
                if pygame.mouse.get_pressed()[0] == 1:
                    # shift + left mouse click
                    if (pygame.key.get_pressed()[pygame.K_RSHIFT] == 1
                    or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1):
                        # start (can only have 1)
                        if maze[mazeGlobals['maze_start'][0]][mazeGlobals['maze_start'][1]].state == 2:
                            maze[mazeGlobals['maze_start'][0]][mazeGlobals['maze_start'][1]].state = 1
                            maze[mazeGlobals['maze_start'][0]][mazeGlobals['maze_start'][1]].color = valid_path_color
                        self.state = 2
                        self.color = start_color
                        mazeGlobals['maze_start'] = (np.where(np.isin(maze, self))[0][0],
                                                     np.where(np.isin(maze, self))[1][0])
                        mazeGlobals['maze_start_exist'] = True
                    else:
                        if self.state == 2:
                            mazeGlobals['maze_start_exist'] = False
                        # wall
                        self.state = 0
                        self.color = wall_color

                # right mouse click
                if pygame.mouse.get_pressed()[2] == 1:
                    if self.state == 2:
                        mazeGlobals['maze_start_exist'] = False
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
        for i in range(len(self.labels)):
            pygame.draw.rect(screen, self.colors[i], self.objs[i])
            screen.blit(self.labels[i],
                       (self.x + self.w // 2 - self.labels[i].get_rect().width // 2,
                       (self.y + i*(self.h + self.margin) + self.h // 2)
                        - self.labels[i].get_rect().height // 2))


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
    screen.blit(instructions_clear, (maze_bg_padding, 159))
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
            cell.visited = 0
            if cell.state == 3:
                cell.color = exit_color
            elif cell.state == 1:
                cell.color = valid_path_color

    return new_maze

def clear(new_maze):
    for row in new_maze:
        for cell in row:
            if cell.state == 3:
                cell.color = exit_color
            elif cell.state != 2:
                cell.visited = 0
                cell.state = 1
                cell.color = valid_path_color

    return new_maze

def popup(msg, bg_color):
    text = font.render(msg, True, text_color)
    popup = pygame.Rect(screen_w // 2 - 75, screen_h // 2 + 50, 150, 50)
    pygame.draw.rect(screen, bg_color, popup)
    screen.blit(text, (screen_w // 2 - text.get_rect().width // 2,
                       screen_h // 2 + 62))
    pygame.display.flip()
    pygame.time.wait(1500)

def backtracking_solver(maze, row, col):
    # need to handle events during recusion to not freeze/crash pygame
    # also added ability to stop solver
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mazeGlobals['exit_solver'] = True
                return False

    # at maze exit?
    if (row >= 0 and row < maze_size
    and col >= 0 and col < maze_size
    and maze[row][col].state == 3):

        maze[row][col].visited = 1
        maze[row][col].color = start_color
        screen_update(30)
        return True

    # is current spot valid and not already visited?
    if (row >= 0 and row < maze_size
    and col >= 0 and col < maze_size
    and maze[row][col].state > 0
    and maze[row][col].visited == 0):

        maze[row][col].visited = 1
        maze[row][col].color = start_color
        screen_update(30)

        # all 8 possible moves randomized each call
        dir = [[0, 1], [0, -1], [1, 0], [-1, 0],
               [1, 1], [1, -1], [-1, 1], [-1, -1]]
        rand.shuffle(dir)

        for i in range(len(dir)):
            if mazeGlobals['exit_solver']:
                return False
            if backtracking_solver(maze, row + dir[i][0], col + dir[i][1]):
                return True

        # set current spot to not valid & been visited
        maze[row][col].visited = 10

        # flash red to show backtracking
        maze[row][col].color = exit_color
        screen_update(20)
        # then return to valid_path_color
        maze[row][col].color = valid_path_color
        screen_update(30)
        return False

    return False

def breadthFirst(maze):
    queue = [[]]
    path = []
    cell = getPathCell(maze, path)

    while True:

        # if queue empty no exit found
        if queue == []:
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mazeGlobals['exit_solver'] = True
                    return False

        # Dequeue
        path = queue[0]
        queue.pop(0)

        for i in ['UL', 'UR', 'DL', 'DR', 'R', 'L', 'U', 'D']:
            # add to path next direction i
            path = path + [i]
            cell = getPathCell(maze, path)

            if checkCell(maze, cell) == 'exit':
                colorPath(maze, path, start_color)
                return True
            elif checkCell(maze, cell) == 'valid':
                # Enqueue
                queue.append(path)
                cell.color = search_color
                cell.visited = 1

            # remove i from end of path to prep for next iteration i
            path = path[:-1]

        screen_update(120)

    return True

def colorPath(maze, path, color):
    # takes path and colors every node in it
    pos = mazeGlobals['maze_start']

    for i in path:

        screen_update(60)

        if i == 'UL':
            pos = (pos[0] - 1, pos[1] - 1)
            maze[pos[0]][pos[1]].color = color
            continue

        if i == 'UR':
            pos = (pos[0] - 1, pos[1] + 1)
            maze[pos[0]][pos[1]].color = color
            continue

        if i == 'DL':
            pos = (pos[0] + 1, pos[1] - 1)
            maze[pos[0]][pos[1]].color = color
            continue

        if i == 'DR':
            pos = (pos[0] + 1, pos[1] + 1)
            maze[pos[0]][pos[1]].color = color
            continue

        if i == 'R':
            pos = (pos[0], pos[1] + 1)
            maze[pos[0]][pos[1]].color = color
            continue

        if i == 'L':
            pos = (pos[0], pos[1] - 1)
            maze[pos[0]][pos[1]].color = color
            continue

        if i == 'U':
            pos = (pos[0] - 1, pos[1])
            maze[pos[0]][pos[1]].color = color
            continue

        if i == 'D':
            pos = (pos[0] + 1, pos[1])
            maze[pos[0]][pos[1]].color = color
            continue

    screen_update(60)

def getPathCell(maze, path):
    # takes path and returns the corresponding cell
    pos = mazeGlobals['maze_start']

    for i in path:
        if i == 'UL':
            pos = (pos[0] - 1, pos[1] - 1)
            continue

        if i == 'UR':
            pos = (pos[0] - 1, pos[1] + 1)
            continue

        if i == 'DL':
            pos = (pos[0] + 1, pos[1] - 1)
            continue

        if i == 'DR':
            pos = (pos[0] + 1, pos[1] + 1)
            continue

        if i == 'R':
            pos = (pos[0], pos[1] + 1)
            continue

        if i == 'L':
            pos = (pos[0], pos[1] - 1)
            continue

        if i == 'U':
            pos = (pos[0] - 1, pos[1])
            continue

        if i == 'D':
            pos = (pos[0] + 1, pos[1])
            continue

    if (pos[0] >= 0 and pos[0] < maze_size
    and pos[1] >= 0 and pos[1] < maze_size):
        return maze[pos[0]][pos[1]]
    else:
        return False

def checkCell(maze, cell):
    # checks cell and returns one of the following
    # 'exit', 'valid', 'notValid', 'visited'
    if not cell:
        return 'notValid'

    if cell.visited == 0:
        if cell.state == 1:
            return 'valid'
        elif cell.state == 2:
            return 'start'
        elif cell.state == 3:
            return 'exit'
        else:
            return 'notValid'
    else:
        return 'visited'

def AStar(maze):
    pass


# -----------------------
# init variables
# -----------------------
mazeGlobals = {'exit_solver': False,
               'maze_start_exist': True,
               'maze_start': (0, 14)}
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
cell_size = (20, 20)
cell_margin = 2
valid_path_color = (200, 200, 200)
search_color = (100, 220, 255)
start_color = (50, 200, 50)
exit_color = (200, 50, 50)
wall_color = (0, 0, 0)
top_padding = 160
maze_bg_padding = 25
maze_bg_w = maze_size * (cell_size[0] + cell_margin) + cell_margin
maze_bg_h = maze_size * (cell_size[1] + cell_margin) + cell_margin
maze_bg_color = (100, 100, 100)
screen_w = maze_bg_w + 2 * maze_bg_padding
screen_h = maze_bg_h + 2 * maze_bg_padding + top_padding
screen_bg_color = (0, 0, 0)
solver_running = False
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
instructions_header = font.render("Instructions:", True, (220, 220, 10))
instructions_wall = font.render("Left Mouse Click = Maze Wall", True, text_color)
instructions_path = font.render("Right Mouse Click = Maze Path", True, text_color)
instructions_start = font.render("Shift + Left Mouse Click = Maze Start (Only 1)", True, text_color)
instructions_exit = font.render("Shift + Right Mouse Click = Maze Exit (Any #)", True, text_color)
instructions_run = font.render("Space = Start/Stop Maze Solver", True, text_color)
instructions_reset = font.render("R = Reset Maze", True, text_color)
instructions_clear = font.render("C = Clear Maze", True, text_color)
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
algorithms = ['A*', 'Breadth First', 'Random Backtracking']
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

                if mazeGlobals['maze_start_exist']:
                    solver_running = True

                    if algorithmSelectors.states[algorithms.index('Random Backtracking')]:
                        if (backtracking_solver(maze,
                                                mazeGlobals['maze_start'][0],
                                                mazeGlobals['maze_start'][1])):
                            popup('DONE!', start_color)
                        elif mazeGlobals['exit_solver']:
                            popup('Solver Stopped!', exit_color)
                            mazeGlobals['exit_solver'] = False
                        else:
                            popup('No Exit Found!', exit_color)

                    if algorithmSelectors.states[algorithms.index('Breadth First')]:
                        if breadthFirst(maze):
                            popup('DONE!', start_color)
                        elif mazeGlobals['exit_solver']:
                            popup('Solver Stopped!', exit_color)
                            mazeGlobals['exit_solver'] = False
                        else:
                            popup('No Exit Found!', exit_color)

                    if algorithmSelectors.states[algorithms.index('A*')]:
                        popup('A* Not Done!', exit_color)

                    solver_running = False

                else:
                    popup('No Maze Start!', exit_color)

            if event.key == pygame.K_r:
                maze = reset(maze)

            if event.key == pygame.K_c:
                maze = clear(maze)

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

    screen_update(60)


# todo:
    # move event handler to function
    # practice making branches and pull request ect....
    # update to follow PEP8 (or greater) standards
    # create self imposed git standard (lookup some?)
        # crown example: https://crown-confluence.crownlift.net/display/IMMV2/Bitbucket+Guidelines
    # make to Crown python standards
        # https://crown-confluence.crownlift.net/display/IMMV2/Python+Guidelines
    # A*
    # when done update README.txt on github (DOCUMENT WELL!!!!)
        # explain everything as if actual project but dont give excuses
        # Breadth First prioritizes diagonals....explaing why
            # IMPROVMENTS/LOOKING BACK????
            # explaing how it works
            # very in-efficiant especially with larger data sets
            # https://techwithtim.net/tutorials/breadth-first-search/
        # random backtracking explaing how it works
            # essentially depth search First(double check this??)
        # rehash any notes in code in readme
        # improve code comments/add


# https://www.youtube.com/watch?v=umvhVljqWeY
# https://www.youtube.com/watch?v=oHBFD8cfXho
# https://www.youtube.com/watch?v=XEhZFtq0xTk
# https://www.youtube.com/watch?v=II7UCUbxOus
# https://www.youtube.com/watch?v=Pb9UNhfy1U4
