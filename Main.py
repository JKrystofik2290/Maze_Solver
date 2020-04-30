import sys
import pygame


# ------------
#   classes
# ------------
class cell():
    def __init__(self, state, x, y):
        self.state = state
        self.size = 20
        self.margin = 2
        # 0 = wall
        if self.state == 0:
            self.color = (0, 0, 0)
        # 1 = vaild path
        if self.state == 1:
            self.color = (200, 200, 200)
        # 2 = starting point
        if self.state == 2:
            self.color = (50, 200, 50)
        # 3 = exit point
        if self.state == 3:
            self.color = (200, 50, 50)
        # cell rect obj
        self.obj = pygame.Rect(x, y, self.size, self.size)
    def update(self):
        # 0 = wall
        if self.state == 0:
            self.color = (0, 0, 0)
        # 1 = vaild path
        if self.state == 1:
            self.color = (200, 200, 200)
        # 2 = starting point
        if self.state == 2:
            self.color = (50, 200, 50)
        # 3 = exit point
        if self.state == 3:
            self.color = (200, 50, 50)


# -----------------------
# init variables
# -----------------------
screen_w = 750
screen_h = 850
screen_bg = (0, 0, 0)
maze_w = 662
maze_h = 662
maze_size = 30
maze_bg = (100, 100, 100)
found = False


# ------------
# init program & objects
# ------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Solver")
screen = pygame.display.set_mode((screen_w, screen_h))
maze_area = pygame.Rect(50, 150, maze_w, maze_h)
# maze_grid = [[1 for x in range(maze_size)] for y in range(maze_size)]
maze_sol = [[0 for x in range(maze_size)] for y in range(maze_size)]
maze = [[cell(1, 22 * x + 52, 22 * y + 152)
        for x in range(maze_size)]
        for y in range(maze_size)]


# ------------
#  functions
# ------------
def event_handler(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if pygame.mouse.get_pressed()[0] == 1:
        found = False
        for row in maze:
            if found:
                break
            for cell in row:
                if cell.obj.collidepoint(pygame.mouse.get_pos()):
                    cell.state = 0
                    cell.update()
                    found = True
                    break

def screen_update():
    screen.fill(screen_bg)
    pygame.draw.rect(screen, maze_bg, maze_area)
    for row in maze:
        for cell in row:
            pygame.draw.rect(screen, cell.color, cell.obj)
    pygame.display.flip()


# ------------
#  Main Loop
# ------------
while True:

    # event handler
    for event in pygame.event.get():
        event_handler(event)

    # screen update
    screen_update()
    clock.tick(60)

# todo:
    # make backtrack move diaginal? maybe not but we will see
    # flash red when backtracking
    # can only place 1 start and exit
    # maybe add other path finding methods (A*)
        # for each method display rules i.e. can/cannot move diaginal
