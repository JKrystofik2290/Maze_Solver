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
from typing import Optional, List, Tuple, Any, Iterator


# ------------
#  Type Alias
# ------------
MazeType = List[List["Cell"]] # "Cell" refers to a Cell class object
MazeRowType = List["Cell"]
DefaultMaze = List[List[int]]
ColorType = Tuple[int, int, int]


# ------------
#   Classes
# ------------
class Mem(object):
    """Memory class to help avoid global variables.

    Use sparingly, only to avoid global variables or corner cases.

    Attributes:
        val: Value to store. Can be any type.
    """

    def __init__(self, value: Any) -> None:
        """Inits Mem with value."""
        self.val = value


class Cell(object):
    """Used to create each "cell" in the maze.

    Keeps track of all the attributes a cell has and that needs to be know
    by the pathfinding algorithms. Example: Is the cell a wall, vaild path,
    been visited, the exit and so on. Also evenly postisions each cell and
    handles drawing each cell with the update() method.

    Correlation table for state and color:
        Start of maze:
            state = 2
            color = START_COLOR
        Exit of maze:
            state = 3
            color = EXIT_COLOR
        Maze wall:
            state = 0
            color = WALL_COLOR
        Valid path:
            state = 1
            color = VALID_PATH_COLOR

    Attributes:
        size: Tuple containing width and height of the cell.
        margin: Spacing to have between cells.
        visited: Value indicating if a cell has been previously checked by a
            pathfinding algorithm.
        state: Used to determine if a cell is a wall, valid path, the exit,
            or the start of the maze.
        color: The color to fill the cell with. This should be tied to the
            state of the cell.
        obj: Contains the pygame "Rect" object reference for the cell.
    """
    def __init__(self, x_offset: int, y_offset: int, x: int, y: int,
                 size: Tuple[int, int], margin: int, state: int) -> None:
        """Inits Cell with values need to create Cell objects."""
        self.size = size
        self.margin = margin
        self.visited = 0
        self.state = state
        if state == 0:
            self.color = WALL_COLOR
        elif state == 1:
            self.color = VALID_PATH_COLOR
        elif state == 2:
            self.color = START_COLOR
        elif state == 3:
            self.color = EXIT_COLOR

        self.obj = pygame.Rect((self.size[0] + self.margin) * x + x_offset,
                               (self.size[1] + self.margin) * y + y_offset,
                               self.size[0], self.size[1])

    def update(self) -> None:
        """Handles user inputs and pygame drawing of cells.

        Will skip user inputs if a pathfinding algorithm is running. When
        drawing the maze start, will clear previous maze start since only one
        is allowed. Any number of exits are allowed.

        Controls for cells:
            Left mouse click = Draw maze wall
            Right mouse click = Draw maze path
            Shift + Left mouse click = Draw maze start
            Shift + Right mouse click = Draw maze exit
        """
        if not solver_running.val:

            if self.obj.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] == 1:
                    if (pygame.key.get_pressed()[pygame.K_RSHIFT] == 1
                    or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1):

                        if maze_start.val != False:
                            start_cell = (maze[maze_start.val[0]]
                                              [maze_start.val[1]])

                            start_cell.state = 1
                            start_cell.color = VALID_PATH_COLOR

                        self.state = 2
                        self.color = START_COLOR
                        maze_start.val = (np.where(np.isin(maze, self))[0][0],
                                          np.where(np.isin(maze, self))[1][0])

                    else:

                        if self.state == 2: maze_start.val = False

                        self.state = 0
                        self.color = WALL_COLOR

                if pygame.mouse.get_pressed()[2] == 1:

                    if self.state == 2: maze_start.val = False

                    if (pygame.key.get_pressed()[pygame.K_RSHIFT] == 1
                    or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1):

                        self.state = 3
                        self.color = EXIT_COLOR

                    else:
                        self.state = 1
                        self.color = VALID_PATH_COLOR

        pygame.draw.rect(screen, self.color, self.obj)


class Btn(object):
    """Creates a group of buttons.

    The group of buttons are tied to gether in that only one button can be
    selected at a time. The number of buttons in the group is determined by
    the number of labels in "lables" passed to it.

    Attributes:
        labels: list of strings. Used to label each button.
        x: The x position of the button in the pygame screen.
        y: The y position of the button in the pygame screen.
        w: The width of the button.
        h: The height of the button.
        margin: Space between buttons.
        objs: A list of the pygame "Rect" obj for each button.
        state: List of bool state of each button.
        colors: List of fill colors of each button.
    """
    def __init__(self, labels: List[str], x: int, y: int,
                 w: int, h: int, margin: int) -> None:
        """Inits Btn with the values need to build the button group."""
        self.labels = []
        self.objs = []
        self.states = []
        self.colors = []
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.margin = margin

        for i in range(len(labels)):
            self.labels.append(font.render(labels[i], True, (33, 33, 33)))
            self.objs.append(pygame.Rect(x, y + (h + margin)*i, w, h))
            self.states.append(False)
            self.colors.append(NOT_SELECTED)


    def update(self) -> None:
        """Updates the pygame object for each button in the group."""
        for i in range(len(self.labels)):
            font_w = self.labels[i].get_rect().width
            font_h = self.labels[i].get_rect().height
            pygame.draw.rect(screen, self.colors[i], self.objs[i])
            screen.blit(
                self.labels[i], (self.x + (self.w - font_w) // 2,
                (self.y + i*(self.h + self.margin) + self.h // 2) - font_h // 2)
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


def maze_maker(size: int, default_maze: DefaultMaze) -> Iterator[MazeRowType]:
    """Makes a maze row by row.

    Could have returned whole maze but since this program is a portfolio
    project I wanted practice with yield.

    Args:
        size: Sets the number of rows and Cells per row.
        default_maze: Gives each Cell its starting state.

    Yields:
        Each row of the maze
    """
    for y in range(size):
        maze_row = []
        for x in range(size):
            maze_row.append(Cell(CELL_OFFSET_X, CELL_OFFSET_Y, x, y, CELL_SIZE,
                                 CELL_MARGIN, default_maze[y][x]))

        yield maze_row


def screen_update(fps: int) -> None:
    """Updates pygame screen and clock.

    Draws objects on the pygame screen in order of execution. Also updates
    pygame clock.

    Args:
        fps: Frames per second.
    """
    screen.fill(SCREEN_BG_COLOR)
    screen.blit(instructions_header, (MAZE_BG_PADDING, 5))
    screen.blit(instructions_wall, (MAZE_BG_PADDING, 27))
    screen.blit(instructions_path, (MAZE_BG_PADDING, 49))
    screen.blit(instructions_start, (MAZE_BG_PADDING, 71))
    screen.blit(instructions_exit, (MAZE_BG_PADDING, 93))
    screen.blit(instructions_run, (MAZE_BG_PADDING, 115))
    screen.blit(instructions_reset, (MAZE_BG_PADDING, 137))
    screen.blit(instructions_clear, (MAZE_BG_PADDING, 159))
    algo_btn.update()
    pygame.draw.rect(screen, MAZE_BG_COLOR, maze_bg)
    for row in maze:
        for cell in row:
            cell.update()

    pygame.display.flip()
    clock.tick(fps)


def reset(reset_maze: MazeType) -> MazeType:
    """Resets maze to before a solver was run.

    Resets each Cell in the maze, clearing visited status and changing
    color back to default state color.

    Args:
        reset_maze: 2D list of Cell class objects to be reset.

    Returns:
        2D list of Cell class objects with their attributes reset.
    """
    for row in reset_maze:
        for cell in row:
            cell.visited = 0

            if cell.state == 3:
                cell.color = EXIT_COLOR

            elif cell.state == 1:
                cell.color = VALID_PATH_COLOR

    return reset_maze


def clear(new_maze: MazeType) -> MazeType:
    """Clears all Cells in maze except start and exit.

    Args:
        new_maze: 2D list of Cell class objects to be cleared.

    Returns:
        2D list of Cell class objects with their attributes cleared.
    """
    for row in new_maze:
        for cell in row:

            if cell.state == 3:
                cell.color = EXIT_COLOR

            elif cell.state != 2:
                cell.visited = 0
                cell.state = 1
                cell.color = VALID_PATH_COLOR

    return new_maze


def popup(msg: str, bg_color: ColorType) -> None:
    """Draws a popup on the pygame screen.

    Creates a pygame "Rect" and "Font" object and draws them on the screen.

    Args:
        msg: string to be displayed in popup.
        bg_color: color of pygame "Rect" object.
    """
    text = font.render(msg, True, TEXT_COLOR)
    popup = pygame.Rect(SCREEN_W // 2 - 75, SCREEN_H // 2 + 50, 150, 50)
    pygame.draw.rect(screen, bg_color, popup)
    screen.blit(text, (SCREEN_W // 2 - text.get_rect().width // 2,
                       SCREEN_H // 2 + 62))
    pygame.display.flip()
    pygame.time.wait(1250)


def color_path(maze: MazeType, path: List[str], color: ColorType) -> None:
    """Colors each Cell along path.

    Starts at the location of 'maze_start' and moves each direction in path
    till the end of path. Along the way it colors each Cell to the arg "color".

    Args:
        maze: 2D list of Cell class objects.
        path: List of strings indicating next direction to move in maze.
        color: RGB to color each Cell in path.
    """
    pos = maze_start.val

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


def get_path_cell(maze: MazeType, path: List[str]) -> Optional[Cell]:
    """Moves through each Cell in maze following path.

    Starts at the location of 'maze_start' and moves each direction in path
    till the end of path.

    Args:
        maze: 2D list of Cell class objects.
        path: List of strings indicating next direction to move in maze.

    Returns:
        If path leads out of bounds for maze then None is returned. Otherwise
        returns the Cell class object at the end of path in maze.
    """
    pos = maze_start.val

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

    if (pos[0] >= 0 and pos[0] < MAZE_SIZE
    and pos[1] >= 0 and pos[1] < MAZE_SIZE):

        return maze[pos[0]][pos[1]]

    else:
        return None


def check_cell(maze: MazeType, cell: Optional[Cell]) -> str:
    """Checks the Cell class object passed to it.

    First checks if a Cell object was passed to it then checks its visited
    value and state value.

    Args:
        maze: 2D list of Cell class objects.
        cell: Cell class object.

    Returns:
        A string corresponding to the state of Cell.
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


def backtrack_solver(maze: MazeType, row: int, col: int) -> bool:
    """Pathfinding algorithm using backtracking recursion.

    This algorithm checks if the current Cell (row, col) is the exit of "maze"
    and if not randomly chooses one of the 8 adjacent Cells (up, down, left,
    right and the 4 diagonals) to check next. Will call itself recursively
    passing the randomly selected row and col. Once it reaches a deadend or
    a Cell that has already been visited it backtracks to the previous
    recursive call and and chooses another adjacent Cell randomly but not one
    it has already chosen. Once it finds the exit returns True elif all valid
    Cells have been visited returns False.

    Args:
        maze: 2D list of Cell class objects.
        row: Row of Cell to check.
        col:  Column of Cell to check.

    Returns:
        Once it finds the exit, returns True, otherwise if all valid Cells
        have been visited, returns False.
    """
    if critical_event_handler():
        solver_running.val = False
        return False

    if (row >= 0 and row < MAZE_SIZE and col >= 0 and col < MAZE_SIZE
    and maze[row][col].visited == 0 and maze[row][col].state > 0):

        maze[row][col].visited = 1
        maze[row][col].color = START_COLOR
        screen_update(30)

        if maze[row][col].state == 3:
            return True

        else:

            DIR = [[0, 1], [0, -1], [1, 0], [-1, 0],
                   [1, 1], [1, -1], [-1, 1], [-1, -1]]

            rand.shuffle(DIR)

            for i in range(len(DIR)):
                if backtrack_solver(maze, row + DIR[i][0], col + DIR[i][1]):
                    return True

                if not solver_running.val:
                    return False

            maze[row][col].color = EXIT_COLOR
            screen_update(20) # Flash red to show backtracking.
            maze[row][col].color = VALID_PATH_COLOR
            screen_update(30) # Then return to VALID_PATH_COLOR.

            return False

    return False


def breadth_first(maze: MazeType) -> bool:
    """Uses Breadth First Search algorithm to find the exit to maze.

    This algorithm is allowed to move diagonal thus it prioritizes moving
    diagonal since in any square grid style maze moving diagonal will always be
    faster then not doing so.

    Args:
        maze: 2D list of Cell class objects.

    Returns:
        Once it finds the exit, returns True, otherwise if all valid Cells
        have been visited, returns False.
    """
    queue = [[]]
    path = []
    cell = get_path_cell(maze, path)

    while not critical_event_handler():

        if not queue:
            return False

        path = queue[0]
        queue.pop(0) # Dequeue

        for i in ['UL', 'UR', 'DL', 'DR', 'R', 'L', 'U', 'D']:
            path = path + [i]
            cell = get_path_cell(maze, path)

            if check_cell(maze, cell) == 'exit':
                color_path(maze, path, START_COLOR)
                return True

            elif check_cell(maze, cell) == 'valid':
                queue.append(path) # Enqueue
                cell.color = SEARCH_COLOR
                cell.visited = 1

            path = path[:-1]

        screen_update(120)

    return False


def a_star(maze: MazeType) -> bool:
    """Uses A* algorithm to find the exit to maze.

    This algorithm is allowed to move diagonal thus it prioritizes moving
    diagonal since in any square grid style maze moving diagonal will always be
    faster then not doing so.

    Args:
        maze: 2D list of Cell class objects.

    Returns:
        Once it finds the exit, returns True, otherwise if all valid Cells
        have been visited, returns False.
    """
    pass


def main(maze: MazeType) -> None:
    """Handels the main execution of this program, pygame and user inputs.

    Loops infinitely, only way to exit is pygame window exit("x" button),
    a system exit or if a critical error occurs.

    Args:
        maze: 2D list of Cell class objects.
    """
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r: maze = reset(maze)

                if event.key == pygame.K_c: maze = clear(maze)

                if event.key == pygame.K_SPACE:
                    solver_running.val = True

                    if maze_start.val == False:
                        popup('No Maze Start!', EXIT_COLOR)

                    elif algo_btn.states[ALGO.index('Random Backtracking')]:

                        if (backtrack_solver(maze, maze_start.val[0],
                                             maze_start.val[1])):

                            popup('DONE!', START_COLOR)

                        else:
                            popup('No Exit Found!', EXIT_COLOR)

                    elif algo_btn.states[ALGO.index('Breadth First')]:

                        if breadth_first(maze):
                            popup('DONE!', START_COLOR)

                        else:
                            popup('No Exit Found!', EXIT_COLOR)

                    else:
                        # A* is choosen by default though should never be
                        # possible to not have a button selected.
                        popup('A* Not Done!', EXIT_COLOR)

                    solver_running.val = False

            if (event.type == pygame.MOUSEBUTTONDOWN
            and pygame.mouse.get_pressed()[0] == 1):

                    for i in range(len(algo_btn.states)):

                        if algo_btn.objs[i].collidepoint(pygame.mouse.get_pos()):

                            for x in range(len(algo_btn.states)):
                                algo_btn.states[x] = False
                                algo_btn.colors[x] = NOT_SELECTED

                            algo_btn.states[i] = True
                            algo_btn.colors[i] = SELECTED

        screen_update(60)


# ------------
#  Constants
# ------------
ALGO = ['A*', 'Breadth First', 'Random Backtracking']
MAZE_SIZE = 30
CELL_SIZE = (20, 20)
CELL_MARGIN = 2
TOP_PADDING = 160
MAZE_BG_PADDING = 25
MAZE_BG_W = MAZE_SIZE * (CELL_SIZE[0] + CELL_MARGIN) + CELL_MARGIN
MAZE_BG_H = MAZE_SIZE * (CELL_SIZE[1] + CELL_MARGIN) + CELL_MARGIN
CELL_OFFSET_X = MAZE_BG_PADDING + CELL_MARGIN
CELL_OFFSET_Y = MAZE_BG_PADDING + CELL_MARGIN + TOP_PADDING
SCREEN_W = MAZE_BG_W + 2 * MAZE_BG_PADDING
SCREEN_H = MAZE_BG_H + 2 * MAZE_BG_PADDING + TOP_PADDING
SCREEN_BG_COLOR = (0, 0, 0)
MAZE_BG_COLOR = (100, 100, 100)
VALID_PATH_COLOR = (200, 200, 200)
SEARCH_COLOR = (115, 155, 255)
START_COLOR = (50, 200, 50)
EXIT_COLOR = (200, 50, 50)
WALL_COLOR = (0, 0, 0)
NOT_SELECTED = (190, 190, 190)
SELECTED = (0, 222, 20)
TEXT_COLOR = (220, 220, 220)
FONT_SIZE = 20
STARTING_MAZE = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
maze_start = Mem((0, 14))
solver_running = Mem(False)
maze = [row for row in maze_maker(MAZE_SIZE, STARTING_MAZE)]


# ------------
# Init Program
# ------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Solver")
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
font = pygame.font.SysFont("arial", FONT_SIZE, True)
instructions_header = font.render("Instructions:", True, (220, 220, 10))
instructions_wall = font.render("Left Click = Maze Wall", True, TEXT_COLOR)
instructions_path = font.render("Right Click = Maze Path", True, TEXT_COLOR)
instructions_start = font.render("Shift + Left Click = Maze Start (Only 1)",
                                 True, TEXT_COLOR)
instructions_exit = font.render("Shift + Right Click = Maze Exit (Any #)",
                                True, TEXT_COLOR)
instructions_run = font.render("Space = Start/Stop Maze Solver",
                               True, TEXT_COLOR)
instructions_reset = font.render("R = Reset Maze", True, TEXT_COLOR)
instructions_clear = font.render("C = Clear Maze", True, TEXT_COLOR)
maze_bg = pygame.Rect(MAZE_BG_PADDING, MAZE_BG_PADDING + TOP_PADDING,
                      MAZE_BG_W, MAZE_BG_H)
algo_btn = Btn(ALGO, SCREEN_W - 225, 5, 200, 45, 5)
algo_btn.states[2] = True
algo_btn.colors[2] = SELECTED

if __name__ == '__main__': main(maze)
