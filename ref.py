Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore

@JKrystofik2290
JKrystofik2290
/
Box_Game
1
00
 Code
 Issues 0
 Pull requests 0 Actions
 Projects 0
 Wiki
 Security 0
 Insights
 Settings
Box_Game/Main.py /
 Krystofik infinite platform spawning
d427866 3 days ago
160 lines (145 sloc)  5.2 KB

Code navigation is available!
Navigate your code with ease. Click on function and method calls to jump to their definitions or references in the same repository. Learn more

import pygame, sys, random

# ------------
# init program
# ------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Box Game")
game_font = pygame.font.Font("freesansbold.ttf", 24)


# ------------
#   classes
# ------------
class screen():
    def __init__(self, w, h, color):
        self.w = w
        self.h = h
        self.color = color
        self.mid_w = w/2
        self.mid_h = h/2
        self.obj = pygame.display.set_mode((w,h))
class player():
    def __init__(self, start_w, start_h, start_x, start_y, color):
        self.start_w = start_w
        self.start_h = start_h
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        self.obj = pygame.Rect(start_x, start_y, start_w, start_h)
        self.jumping = False
        self.grounded = False
        self.speed_x = 0
        self.speed_y = 0
    def animation(self):
        if start:
            self.obj.x += self.speed_x
            if self.jumping:
                self.obj.y -= self.speed_y
                self.speed_y -= 1
                if self.speed_y <= 0:
                    self.jumping = False
            else:
                # gravity
                self.obj.y += 8
                for plat in platforms:
                    if self.obj.colliderect(plat.obj):
                        if abs(self.obj.bottom - plat.obj.top) < abs(self.obj.top - plat.obj.bottom):
                            self.grounded = True
                            self.jumping = False
                            self.speed_y = 0
                            self.obj.bottom = plat.obj.top + 1
                            self.obj.x -= plat.speed_x
                        elif abs(self.obj.bottom - plat.obj.top) > abs(self.obj.top - plat.obj.bottom):
                            self.jumping = False
                            self.speed_y = 0
                            self.obj.top = plat.obj.bottom
    def jump(self):
        if self.grounded:
            self.grounded = False
            self.jumping = True
            self.speed_y = 24
class platform():
    def __init__(self, start_w, start_h, start_x, start_y, color):
        self.start_w = start_w
        self.start_h = start_h
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        self.speed_x = 4
        self.speed_y = 0
        self.obj = pygame.Rect(start_x, start_y, start_w, start_h)
    def move(self):
        self.obj.x -= self.speed_x


# -----------------------
# init objects/variables
# -----------------------
screen = screen(1000, 500, (0,0,0))
player = player(25, 25, round(screen.mid_w - 300), round(screen.mid_h + 125), (200,200,200))
start = False
platform_color = (50,255,50)
platforms = [platform(400, 25, round(screen.mid_w - 300), round(screen.mid_h + 150),platform_color), platform(200, 25, round(screen.mid_w + 400), round(screen.mid_h + 50),platform_color),platform(400, 25, round(screen.mid_w - 200), round(screen.mid_h),platform_color)]


# ------------
#  functions
# ------------
def event_handler(event):
    global start
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if start:
                player.jump()
            else: start = True
        if start:
            if event.key == pygame.K_LEFT:
                player.speed_x -= 7
            if event.key == pygame.K_RIGHT:
                player.speed_x += 7
    if start:
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.speed_x += 7
            if event.key == pygame.K_RIGHT:
                player.speed_x -= 7
def screen_update():
    screen.obj.fill(screen.color)
    pygame.draw.rect(screen.obj, player.color, player.obj)
    for plat in platforms:
        pygame.draw.rect(screen.obj, plat.color, plat.obj)
    pygame.display.flip()
def spawn_platform(platforms):
    # spawn range 500 - 900
    if random.randint((screen.w - 800),(screen.w - 200)) <= platforms[-1].obj.right <= (screen.w - 200):
        new_plat_w = random.randint(25,300)
        new_plat_y = random.randint(50,screen.h - 25)
        platforms.append(platform(new_plat_w, 25, screen.w, new_plat_y,platform_color))
    if platforms[0].obj.right <= 0:
        platforms.pop(0)
    return platforms


# ------------
#  Main Loop
# ------------
while True:

    # event handler
    for event in pygame.event.get():
        event_handler(event)

    # update animations
    player.animation()
    platforms = spawn_platform(platforms)
    if start:
        for plat in platforms:
            plat.move()

    # screen update
    screen_update()
    clock.tick(60)



# todo:
    # grounded = True if touch side of plat???? able to jump again?????
    # play with different plat speeds
    # keep???? if slide off platform player can still jump once in air
    # figure out y bounds to spawn platforms in and x bounds from previous platform
    # add collision with bottom and sides of platforms
    # player move with platforms when grounded????????
    # add roof for player??????
    # player die and game reset when fall off bottom of screen
    # add score = to time survived
    # add text at start "Press Space to Start" then remove once start
