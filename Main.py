import sys
import pygame
import numpy as np


# ------------
#   classes
# ------------
class cell():
    def __init__(self, x_offset, y_offset, x, y, size, margin):
        self.size = size
        self.margin = margin
        self.state = 1
        self.solution = 0
        self.color = (200, 200, 200)
        self.obj = pygame.Rect((self.size[0] + self.margin) * x + x_offset,
                               (self.size[1] + self.margin) * y + y_offset,
                               self.size[0], self.size[1])

    def update(self):
        global maze_start, maze_start_exist
        if self.obj.collidepoint(pygame.mouse.get_pos()):
            # left mouse click
            if pygame.mouse.get_pressed()[0] == 1:
                # shift + left mouse click
                if (pygame.key.get_pressed()[pygame.K_RSHIFT] == 1
                or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1):
                    # start (can only have 1)
                    for row in maze:
                        for cell in row:
                            if cell.state == 2:
                                cell.state = 1
                                cell.color = (200, 200, 200)
                    self.state = 2
                    self.color = (50, 200, 50)
                    maze_start = (np.where(np.isin(maze, self))[0][0],
                                  np.where(np.isin(maze, self))[1][0])
                    maze_start_exist = True
                else:
                    if self.state == 2:
                        maze_start_exist = False
                    # wall
                    self.state = 0
                    self.color = (0, 0, 0)

            # right mouse click
            if pygame.mouse.get_pressed()[2] == 1:
                if self.state == 2:
                    maze_start_exist = False
                # shift + right mouse click
                if (pygame.key.get_pressed()[pygame.K_RSHIFT] == 1
                or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1):
                    # exit
                    self.state = 3
                    self.color = (200, 50, 50)
                else:
                    # valid path
                    self.state = 1
                    self.color = (200, 200, 200)

        pygame.draw.rect(screen, self.color, self.obj)


# -----------------------
# init variables
# -----------------------
top_padding = 100
cell_size = (20, 20)
cell_margin = 2
maze_bg_padding = 25
maze_size = 30
maze_bg_w = maze_size * (cell_size[0] + cell_margin) + cell_margin
maze_bg_h = maze_size * (cell_size[1] + cell_margin) + cell_margin
maze_bg_color = (100, 100, 100)
screen_w = maze_bg_w + 2 * maze_bg_padding
screen_h = maze_bg_h + 2 * maze_bg_padding + top_padding
screen_bg_color = (0, 0, 0)
maze_start = (0, 0)
maze_start_exist = True


# ------------
# init program & objects
# ------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Solver")
screen = pygame.display.set_mode((screen_w, screen_h))
maze_bg = pygame.Rect(maze_bg_padding,
                      maze_bg_padding + top_padding,
                      maze_bg_w, maze_bg_h)
maze = [[cell(maze_bg_padding + cell_margin,
              maze_bg_padding + cell_margin + top_padding,
              x, y, cell_size, cell_margin)
          for x in range(maze_size)]
          for y in range(maze_size)]
maze[maze_start[0]][maze_start[1]].state = 2
maze[maze_start[0]][maze_start[1]].color = (50, 200, 50)
maze[maze_size - 1][maze_size - 1].state = 3
maze[maze_size - 1][maze_size - 1].color = (200, 50, 50)


# ------------
#  functions
# ------------
def event_handler(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if maze_start_exist:
                # add algorithm selector logic here
                # if backtracking == selected:
                if backtracking_solver(maze, maze_start[0], maze_start[1]):
                    print('done!')
                else:
                    print('No Exit Found!')
            else:
                # add erro/popup here
                print('No Maze Start!')

def screen_update():
    screen.fill(screen_bg_color)
    pygame.draw.rect(screen, maze_bg_color, maze_bg)
    for row in maze:
        for cell in row:
            cell.update()
    pygame.display.flip()
    clock.tick(60)

def backtracking_solver(maze, row, col):
    # at exit?
    if (row >= 0 and row < maze_size
    and col >= 0 and col < maze_size
    and maze[row][col].state == 3):
        print('issue')
        maze[row][col].solution = 1
        maze[row][col].color = (50, 200, 50)
        screen_update()
        return True

    # is current spot valid and not already visited?
    if (row >= 0 and row < maze_size
    and col >= 0 and col < maze_size
    and maze[row][col].state > 0
    and maze[row][col].solution == 0):

        maze[row][col].solution = 1
        maze[row][col].color = (50, 200, 50)
        screen_update()

        # check if col + 1 is valid
        if backtracking_solver(maze, row, col + 1):
            return True

        # check if row + 1 is valid
        if backtracking_solver(maze, row + 1, col):
            return True

        # check if col - 1 is valid
        if backtracking_solver(maze, row, col - 1):
            return True

        # check if row - 1 is valid
        if backtracking_solver(maze, row - 1, col):
            return True

        # set current spot to not valid
        maze[row][col].solution = 10
        maze[row][col].color = (200, 200, 200)
        screen_update()
        return False

    return False


# ------------
#  Main Loop
# ------------
while True:
    # event handler
    for event in pygame.event.get():
        event_handler(event)

    # screen update
    screen_update()

# todo:
    # clear all or reset button!!!
        # reset .solution and any others
    # indicator or popup when done and color/text based off if it found the exit + time took
    # instructions on how to make maze and start/stop/select Solver
    # make backtrack move diaginal? maybe not but we will see
    # flash red when backtracking
    # maybe add other path finding methods (A*)
        # for each method display rules i.e. can/cannot move diaginal
        # selector to switch between them
