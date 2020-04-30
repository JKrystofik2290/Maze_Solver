import pygame


# ------------
#   classes
# ------------


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
cell_size = 20
cell_margin = 2
cell_path = (200, 200, 200)


# ------------
# init program & objects
# ------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Solver")
screen = pygame.display.set_mode((screen_w, screen_h))
maze_area = pygame.Rect(50, 150, maze_w, maze_h)
maze_grid = [[1 for x in range(maze_size)] for y in range(maze_size)]
maze = [[pygame.Rect(52 + (cell_size + cell_margin) * x,
                    152 + (cell_size + cell_margin) * y,
                    cell_size, cell_size)
                    for x in range(maze_size)]
                    for y in range(maze_size)]

# =====================================================
# 2 list or 1 like [state: cell.obj]
# =====================================================




# ------------
#  functions
# ------------
def event_handler(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

def screen_update():
    screen.fill(screen_bg)
    pygame.draw.rect(screen, maze_bg, maze_area)
    for row in maze:
        for cell in row:
            pygame.draw.rect(screen, cell_path, cell)
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

# rules:
    # 0 = wall
    # 1 = vaild path
    # 2 = starting point
    # 3 = exit point

# todo:
    # flash red when backtracking
    # can only place 1 start and exit
    # maybe add other path finding methods
