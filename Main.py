import pygame


# ------------
#   classes
# ------------


# ------------
# init program
# ------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Solver")
screen = pygame.display.set_mode((750, 900))
game_font = pygame.font.Font("freesansbold.ttf", 24)


# -----------------------
# init variables
# -----------------------
maze_area = pygame.Rect(50, 200, 650, 650)


# ------------
#  functions
# ------------
def event_handler(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

def screen_update():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (100, 100, 100), maze_area)
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
