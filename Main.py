#!/usr/bin/env python3

"""Maze solver program visualizing different pathfinding algorithms.

This was a project for my portfolio to show competency using pathfinding
algorithms. Google's style guide was used throughout this doc, reference:
http://google.github.io/styleguide/pyguide.html
"""
import sys
import pygame
import numpy as np
import random as rand
from typing import Optional, List, Tuple


# ------------
#   Classes
# ------------
class mem:

    def __init__(self, value) -> None:
        self.val = value


class cell:

    def __init__(self, x_offset: int, y_offset: int, x: int, y: int,
                 size: Tuple[int, int], margin: int, state: int) -> None:
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

    def update(self) -> None:
        # start (can only have 1)
        # exit = 3
        # shift + left mouse click

        if not solver_running:

            if self.obj.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] == 1:
                    if (pygame.key.get_pressed()[pygame.K_RSHIFT] == 1
                    or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1):

                        if mazeStart.val != False:
                            startCell = maze[mazeStart.val[0]][mazeStart.val[1]]
                            startCell.state = 1
                            startCell.color = valid_path_color

                        self.state = 2
                        self.color = start_color
                        mazeStart.val = (np.where(np.isin(maze, self))[0][0],
                                         np.where(np.isin(maze, self))[1][0])
                    else:
                        if self.state == 2:
                            mazeStart.val = False

                        self.state = 0
                        self.color = wall_color

                if pygame.mouse.get_pressed()[2] == 1:
                    if self.state == 2:
                        mazeStart.val = False

                    if (pygame.key.get_pressed()[pygame.K_RSHIFT] == 1
                    or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1):

                        self.state = 3
                        self.color = exit_color
                    else:

                        self.state = 1
                        self.color = valid_path_color

        pygame.draw.rect(screen, self.color, self.obj)


class btn:

    def __init__(self, listOfLabel: List[str], x: int, y: int, w: int,  h: int,
                 margin: int) -> None:
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


    def update(self) -> None:
        for i in range(len(self.labels)):
            fontW = self.labels[i].get_rect().width
            fontH = self.labels[i].get_rect().height
            pygame.draw.rect(screen, self.colors[i], self.objs[i])
            screen.blit(
                self.labels[i], (self.x + (self.w - fontW) // 2,
                (self.y + i*(self.h + self.margin) + self.h // 2) - fontH // 2)
                )



# ------------
#  Functions
# ------------
def critical_event_handler() -> bool:
    """Handles critcal events in pygame.

    Pygame events need to be handeled during function loops or recursion
    otherwise the game will freeze and/or crash. This function handels the
    most critical events during those cases.

    Returns:
        A bool, with False meaning all events where handled and no other action
        is needed.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return True

    return False


def screen_update(fps: int) -> None:
    """Updates pygame screen and clock.

    Draws objects on the pygame screen in order of execution. Also updates
    pygame clock.

    Args:
        fps: Frames per second.
    """
    screen.fill(screen_bg_color)
    screen.blit(instructions_header, (maze_bg_padding, 5))
    screen.blit(instructions_wall, (maze_bg_padding, 27))
    screen.blit(instructions_path, (maze_bg_padding, 49))
    screen.blit(instructions_start, (maze_bg_padding, 71))
    screen.blit(instructions_exit, (maze_bg_padding, 93))
    screen.blit(instructions_run, (maze_bg_padding, 115))
    screen.blit(instructions_reset, (maze_bg_padding, 137))
    screen.blit(instructions_clear, (maze_bg_padding, 159))
    algoBtn.update()
    pygame.draw.rect(screen, maze_bg_color, maze_bg)
    for row in maze:
        for cell in row:
            cell.update()

    pygame.display.flip()
    clock.tick(fps)


def reset(reset_maze: List[List[cell]]) -> List[List[cell]]:
    """Resets maze to before a solver was run.

    Resets each cell in the maze, clearing visited status and changing
    color back to default state color.

    Args:
        reset_maze: 2D list of "cell" class objects to be reset.

    Returns:
        2D list of "cell" class objects with their attributes reset.
    """
    for row in reset_maze:
        for cell in row:
            cell.visited = 0
            if cell.state == 3:
                cell.color = exit_color
            elif cell.state == 1:
                cell.color = valid_path_color

    return reset_maze


def clear(new_maze: List[List[cell]]) -> List[List[cell]]:
    """Clears all cells in maze except start and exit.

    Args:
        new_maze: 2D list of "cell" class objects to be cleared.

    Returns:
        2D list of "cell" class objects with their attributes cleared.
    """
    for row in new_maze:
        for cell in row:
            if cell.state == 3:
                cell.color = exit_color
            elif cell.state != 2:
                cell.visited = 0
                cell.state = 1
                cell.color = valid_path_color

    return new_maze


def popup(msg: str, bg_color: Tuple[int, int, int]) -> None:
    """Draws a popup on the pygame screen.

    Creates a pygame "Rect" and "Font" object and draws them on the screen.

    Args:
        msg: string to be displayed in popup.
        bg_color: color of pygame "Rect" object.
    """
    text = font.render(msg, True, text_color)
    popup = pygame.Rect(screen_w // 2 - 75, screen_h // 2 + 50, 150, 50)
    pygame.draw.rect(screen, bg_color, popup)
    screen.blit(text, (screen_w // 2 - text.get_rect().width // 2,
                       screen_h // 2 + 62))
    pygame.display.flip()
    pygame.time.wait(1250)


def backTrackSol(maze: List[List[cell]], row: int, col: int) -> bool:
    """Pathfinding algorithm using backtracking recursion.

    This algorithm checks if the current cell (row, col) is the exit of "maze"
    and if not randomly chooses one of the 8 adjacent cells (up, down, left,
    right and the 4 diagonals) to check next. Will call itself recursively
    passing the randomly selected row and col. Once it reaches a deadend or
    a cell that has already been visited it backtracks to the previous
    recursive call and and chooses another adjacent cell randomly but not one
    it has already chosen. Once it finds the exit returns True elif all valid
    cells have been visited returns False.

    Args:
        maze: 2D list of "cell" class objects.
        row: Row of cell to check.
        col:  Column of cell to check.

    Returns:
        Once it finds the exit returns True elif all valid cells have been
        visited returns False.
    """
    if critical_event_handler():
        # exit recursion by setting all cells.visited = inf
        for row in maze:
            for cell in row:
                cell.visited = float('inf')
        return False

    if (row >= 0 and row < maze_size and col >= 0 and col < maze_size
    and maze[row][col].visited == 0 and maze[row][col].state > 0):

        maze[row][col].visited = 1
        maze[row][col].color = start_color
        screen_update(30)

        if maze[row][col].state == 3:
            return True

        else:

            dir = [[0, 1], [0, -1], [1, 0], [-1, 0],
                   [1, 1], [1, -1], [-1, 1], [-1, -1]]

            rand.shuffle(dir)

            for i in range(len(dir)):
                if backTrackSol(maze, row + dir[i][0], col + dir[i][1]):
                    return True

                if maze[row][col].visited == float('inf'):
                    return False

            maze[row][col].color = exit_color
            screen_update(20) # flash red to show backtracking
            maze[row][col].color = valid_path_color
            screen_update(30) # then return to valid_path_color

            return False

    return False


def breadthFirst(maze: List[List[cell]]) -> bool:
    """Uses Breadth First Search algorithm to find the exit to maze.

    Continues to loop through BFS while there is no flag(False) from
    critical_event_handler() function.

    Args:
        maze: 2D list of "cell" class objects.

    Returns:
        Once it finds the exit returns True elif all valid cells have been
        visited returns False.
    """
    queue: List[List[str]] = [[]]
    path: List[str] = []
    cell = getPathCell(maze, path)

    while not critical_event_handler():

        if not queue:
            return False

        path = queue[0]
        queue.pop(0) # Dequeue

        for i in ['UL', 'UR', 'DL', 'DR', 'R', 'L', 'U', 'D']:
            path = path + [i]
            cell = getPathCell(maze, path)

            if checkCell(maze, cell) == 'exit':
                colorPath(maze, path, start_color)
                return True

            elif checkCell(maze, cell) == 'valid':
                queue.append(path) # Enqueue
                cell.color = search_color
                cell.visited = 1

            path = path[:-1]

        screen_update(120)

    return False


def colorPath(maze: List[List[cell]], path: List[str],
              color: Tuple[int, int, int]) -> None:
    """Colors each cell along path.

    Starts at the location of 'maze_start' and moves each direction in path
    till the end of path. Along the way it colors each cell to the arg "color".

    Args:
        maze: 2D list of "cell" class objects.
        path: List of strings indicating next direction to move in maze.
        color: RGB to color each cell in path.
    """
    pos = mazeStart.val

    for i in path:

        screen_update(45)

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


def getPathCell(maze: List[List[cell]], path: List[str]) -> Optional[cell]:
    """Moves through each cell in maze following path.

    Starts at the location of 'maze_start' and moves each direction in path
    till the end of path.

    Args:
        maze: 2D list of "cell" class objects.
        path: List of strings indicating next direction to move in maze.

    Returns:
        If path leads out of bounds for maze then None is returned. Otherwise
        returns the cell Class object at the end of path in maze.
    """
    pos = mazeStart.val

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
        return None


def checkCell(maze: List[List[cell]], cell: Optional[cell]) -> str:
    """Checks the cell class object passed to it.

    First checks if a cell object was passed to it then checks its visited value
    and state value.

    Args:
        maze: 2D list of "cell" class objects.
        cell: cell Class object.

    Returns:
        A string corresponding to the state of cell.
    """
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


def AStar(maze: List[List[cell]]) -> bool:
    """Uses A* algorithm to find the exit to maze.

    !!!!!!!!!!!!!!!!!!docString!!!!!!!!!!!!!!!!!!!!!!!!

    Args:
        maze: 2D list of "cell" class objects.

    Returns:

    """
    pass


# ------------
#  Constants
# ------------
algo = ['A*', 'Breadth First', 'Random Backtracking']
maze_size = 30
cell_size = (20, 20)
cell_margin = 2
top_padding = 160
maze_bg_padding = 25
maze_bg_w = maze_size * (cell_size[0] + cell_margin) + cell_margin
maze_bg_h = maze_size * (cell_size[1] + cell_margin) + cell_margin
cellOffsetX = maze_bg_padding + cell_margin
cellOffsetY = maze_bg_padding + cell_margin + top_padding
screen_w = maze_bg_w + 2 * maze_bg_padding
screen_h = maze_bg_h + 2 * maze_bg_padding + top_padding
screen_bg_color = (0, 0, 0)
maze_bg_color = (100, 100, 100)
valid_path_color = (200, 200, 200)
search_color = (115, 155, 255)
start_color = (50, 200, 50)
exit_color = (200, 50, 50)
wall_color = (0, 0, 0)
not_selected = (190, 190, 190)
selected = (0, 222, 20)
text_color = (220, 220, 220)
font_size = 20
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


# ------------
#  Variables
# ------------
mazeStart = mem((0, 14))
solver_running = False
maze = []
temp = []
for row in range(maze_size):
    for col in range(maze_size):
        temp.append(cell(cellOffsetX, cellOffsetY, col, row, cell_size,
                         cell_margin, starting_maze[row][col]))
    maze.append(temp)
    temp = []


# ------------
# Init Program
# ------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Solver")
screen = pygame.display.set_mode((screen_w, screen_h))
font = pygame.font.SysFont("arial", font_size, True)
instructions_header = font.render("Instructions:", True, (220, 220, 10))
instructions_wall = font.render("Left Click = Maze Wall", True, text_color)
instructions_path = font.render("Right Click = Maze Path", True, text_color)
instructions_start = font.render("Shift + Left Click = Maze Start (Only 1)",
                                 True, text_color)
instructions_exit = font.render("Shift + Right Click = Maze Exit (Any #)",
                                True, text_color)
instructions_run = font.render("Space = Start/Stop Maze Solver",
                               True, text_color)
instructions_reset = font.render("R = Reset Maze", True, text_color)
instructions_clear = font.render("C = Clear Maze", True, text_color)
maze_bg = pygame.Rect(maze_bg_padding, maze_bg_padding + top_padding,
                      maze_bg_w, maze_bg_h)
algoBtn = btn(algo, screen_w - 225, 5, 200, 45, 5)
algoBtn.states[2] = True
algoBtn.colors[2] = selected


# ------------
#  Main Loop
# ------------
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                maze = reset(maze)

            if event.key == pygame.K_c:
                maze = clear(maze)

            if event.key == pygame.K_SPACE:
                solver_running = True

                if mazeStart.val == False:
                    popup('No Maze Start!', exit_color)

                elif algoBtn.states[algo.index('Random Backtracking')]:
                    if (backTrackSol(maze, mazeStart.val[0], mazeStart.val[1])):
                        popup('DONE!', start_color)
                    else:
                        popup('No Exit Found!', exit_color)

                elif algoBtn.states[algo.index('Breadth First')]:
                    if breadthFirst(maze):
                        popup('DONE!', start_color)
                    else:
                        popup('No Exit Found!', exit_color)

                else:
                    # A* by default
                    popup('A* Not Done!', exit_color)

                solver_running = False

        if (event.type == pygame.MOUSEBUTTONDOWN
        and pygame.mouse.get_pressed()[0] == 1):
                for i in range(len(algoBtn.states)):
                    if algoBtn.objs[i].collidepoint(pygame.mouse.get_pos()):
                        for x in range(len(algoBtn.states)):
                            algoBtn.states[x] = False
                            algoBtn.colors[x] = not_selected

                        algoBtn.states[i] = True
                        algoBtn.colors[i] = selected

    screen_update(60)
