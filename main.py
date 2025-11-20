# IMPORTS
import pygame as pg
import pygame.time

import constants as k
from mysprites import Ball, Paddle#, makeimages

# INITIALIZE THINGS
pg.init()
my_screen = pg.display.set_mode(k.SCREENSIZE)
my_screen.fill(k.BACKGROUNDCOLOR)
clock = pg.time.Clock()
running = True
holdtime = 0
hold = False

# SPRITE CONTAINERS
all = pg.sprite.RenderUpdates()
ballgroup = pg.sprite.RenderUpdates()
Paddle.containers = all
Ball.containers = all, ballgroup

# SPRITES
myball = Ball()
leftpaddle = Paddle(True)
rightpaddle = Paddle(False)

# COMMANDS
# missed ball, set the ball speed to zero
# and wait for reset time to pass
def waitforit(ticks):
    global hold, holdtime
    if ticks - holdtime < k.RESET:
        myball.speed = (0,0)
    else:
        hold = False
        myball.reset()

# LOOP
#startconfig()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    keys = pg.key.get_pressed()
    if keys[pg.K_q] or keys[pg.K_a]:
        direction = keys[pg.K_a] - keys[pg.K_q]
        leftpaddle.move(direction)
    if keys[pg.K_LEFTBRACKET] or keys[pg.K_QUOTE]:
        direction = keys[pg.K_QUOTE] - keys[pg.K_LEFTBRACKET]
        rightpaddle.move(direction)

    # redraw background
    # which clears the screen
    my_screen.fill(k.BACKGROUNDCOLOR)

    # update the sprites
    all.update()
    # ball collides with a paddle
    if pg.sprite.spritecollide(leftpaddle, ballgroup, False) or pg.sprite.spritecollide(rightpaddle, ballgroup, False):
        myball.x = -myball.x
        myball.speed = (myball.x,myball.y)
    # ball exits the playing field
    if hold:
        waitforit(pg.time.get_ticks())
    else:
        if myball.rect.right > k.SCREENWIDE:
            hold = True
            holdtime = pygame.time.get_ticks()
        if myball.rect.left < 0:
            hold = True
            holdtime = pygame.time.get_ticks()




    # redraws all
    dirty = all.draw(my_screen)
    pg.display.update()
    # set frame rate
    dt = clock.tick(30)

# QUIT
pg.quit()