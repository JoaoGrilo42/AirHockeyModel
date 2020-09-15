import sys, pygame as pg
import numpy as np
import time
from math import pi
from Puck import Puck
from PlayerPlotter import Player

pg.init()

mm2pixel = 2.5
m2pixel = .0025
size = width, height = int(1219/mm2pixel), int(2134/mm2pixel) #size of table in mm
armLen1 = int(((1219**2 + (2134/2)**2)**.5)/2)
armLen2 = armLen1
screen = pg.display.set_mode(size)

dt = .005 # update interval in seconds

rad = 42
pos = np.array(size)*mm2pixel/2
mass=42
mu=1
dt_impact=.01
dt_interval=.01
pad_rad = 50
gamePuck = Puck(rad, pos, mass, mu, dt_impact, dt_interval,mm2pixel,screen)
autoPlayer = Player(1219, 2134/2, [0,0], 500, dt_interval)

HITPUCK = pg.USEREVENT+1

autoPlayer.goToPos([1219/2, 2134/2], [500,500])
#pg.time.set_timer(HITPUCK, 2000)
while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        if event.type == HITPUCK:
            print("*******Should hit puck now**********")
            gamePuck.collision(gamePuck.pos+2, -3*pi/4, 200000)

    if gamePuck.pos[0]+gamePuck.radius > width*mm2pixel :
        gamePuck.pos[0] = width*mm2pixel-gamePuck.radius
        gamePuck.collision(gamePuck.pos + [gamePuck.radius, 0], pi + np.arctan2(*gamePuck.v[::-1]), 2*gamePuck.m*np.linalg.norm(gamePuck.v)/gamePuck.dt_impact)
    if gamePuck.pos[0]-gamePuck.radius < 0:
        gamePuck.pos[0] = gamePuck.radius
        gamePuck.collision(gamePuck.pos - [-gamePuck.radius, 0], pi+np.arctan2(*gamePuck.v[::-1]), 2*gamePuck.m*np.linalg.norm(gamePuck.v)/gamePuck.dt_impact)
    if gamePuck.pos[1]-gamePuck.radius < 0:
        gamePuck.pos[1] = gamePuck.radius
        gamePuck.collision(gamePuck.pos - [0, -gamePuck.radius], pi + np.arctan2(*gamePuck.v[::-1]), 2*gamePuck.m*np.linalg.norm(gamePuck.v)/gamePuck.dt_impact)
    if gamePuck.pos[1]+gamePuck.radius > height*mm2pixel:
        gamePuck.pos[1] = height*mm2pixel-gamePuck.radius
        gamePuck.collision(gamePuck.pos + [0, gamePuck.radius], pi +np.arctan2(*gamePuck.v[::-1]), 2*gamePuck.m*np.linalg.norm(gamePuck.v)/gamePuck.dt_impact)
    
    colDist = rad+pad_rad
    padPos, padV = autoPlayer.getPaddleState()
    print("padPos: {}, puckPos: {}".format(padPos, gamePuck.pos))
    print("{}".format((gamePuck.pos - padPos)[::-1]))
    print("Len puck: {}".format(len(gamePuck.pos)))
    d = np.linalg.norm(gamePuck.pos-padPos)
    theta = np.arctan2(*(gamePuck.pos-padPos)[::-1])
    if d <= colDist :
        gamePuck.collision(padPos, theta, 200000)
    screen.fill((0, 0, 0))
    gamePuck.update()
    autoPlayer.update(screen, mm2pixel)
    
    #pg.draw.circle(screen, )
    #screen.fill(pg.Color('black'))
    #screen.blit(screen, screen)
    pg.display.flip()
    time.sleep(dt)