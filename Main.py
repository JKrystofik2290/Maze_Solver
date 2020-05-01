import sys
import pygame
import numpy as np
import random as rand


# ------------
#   classes
# ------------
class cell:
    def __init__(self, x_offset, y_offset, x, y, size, margin):
        self.size = size
        self.margin = margin
        self.state = 1
        self.solution = 0
        self.color = valid_path_color
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


# ------------
#  functions
# ------------
def screen_update(t):
    screen.fill(screen_bg_color)
    pygame.draw.rect(screen, maze_bg_color, maze_bg)
    for row in maze:
        for cell in row:
            cell.update()
    pygame.display.flip()
    clock.tick(t)

def reset(new_maze):
    new_maze = [[cell(maze_bg_padding + cell_margin,
                 maze_bg_padding + cell_margin + top_padding,
                 x, y, cell_size, cell_margin)
              for x in range(maze_size)]
              for y in range(maze_size)]
    new_maze[maze_start[0]][maze_start[1]].state = 2
    new_maze[maze_start[0]][maze_start[1]].color = start_color
    new_maze[maze_size - 1][maze_size - 1].state = 3
    new_maze[maze_size - 1][maze_size - 1].color = exit_color
    return new_maze

def backtracking_solver(maze, row, col):
    # at exit?
    if (row >= 0 and row < maze_size
    and col >= 0 and col < maze_size
    and maze[row][col].state == 3):

        maze[row][col].solution = 1
        maze[row][col].color = start_color
        screen_update(60)
        return True

    # is current spot valid and not already visited?
    if (row >= 0 and row < maze_size
    and col >= 0 and col < maze_size
    and maze[row][col].state > 0
    and maze[row][col].solution == 0):

        maze[row][col].solution = 1
        maze[row][col].color = start_color
        screen_update(60)

        # all 8 possible moves randomized each call
        dir = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        rand.shuffle(dir)

        for i in range(len(dir)):
            # pygame.time.wait(10)
            if backtracking_solver(maze, row + dir[i][0], col + dir[i][1]):
                return True

        # set current spot to not valid & been visited
        maze[row][col].solution = 10
        maze[row][col].color = valid_path_color
        screen_update(60)
        return False

    return False


# -----------------------
# init variables
# -----------------------
maze_size = 30
maze_start = (0, 0)
maze_start_exist = True
cell_size = (20, 20)
cell_margin = 2
valid_path_color = (200, 200, 200)
start_color = (50, 200, 50)
exit_color = (200, 50, 50)
wall_color = (0, 0, 0)
top_padding = 100
maze_bg_padding = 25
maze_bg_w = maze_size * (cell_size[0] + cell_margin) + cell_margin
maze_bg_h = maze_size * (cell_size[1] + cell_margin) + cell_margin
maze_bg_color = (100, 100, 100)
screen_w = maze_bg_w + 2 * maze_bg_padding
screen_h = maze_bg_h + 2 * maze_bg_padding + top_padding
screen_bg_color = (0, 0, 0)


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
maze[maze_start[0]][maze_start[1]].color = start_color
maze[maze_size - 1][maze_size - 1].state = 3
maze[maze_size - 1][maze_size - 1].color = exit_color


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
                    # add algorithm selector logic here
                    # if backtracking == selected:
                    if backtracking_solver(maze, maze_start[0], maze_start[1]):
                        print('done!')
                    else:
                        print('No Exit Found!')
                else:
                    # add erro/popup here
                    print('No Maze Start!')

            if event.key == pygame.K_r:
                maze = reset(maze)

    # screen update
    screen_update(60)

# todo:
    # check cpu usage
    # when adding to website get like to online python runner
    # random direction list for backtracking
    # indicator or popup when done and color/text based off if it found the exit + time took
    # instructions on how to make maze and start/stop/select Solver
    # add other path finding methods (A*)
        # for each method display rules i.e. can/cannot move diaginal
        # selector to switch between them
