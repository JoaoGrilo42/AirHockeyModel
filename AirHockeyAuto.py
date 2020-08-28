import sys, pygame as pg
import numpy as np
import time
import math

pg.init()

mm2pixel = 2.5
m2pixel = .0025
size = width, height = int(1219/mm2pixel), int(2134/mm2pixel) #size of table in mm

screen = pg.display.set_mode(size)

dt = .01 # update interval in seconds

class Puck :
    def __init__(self):
        self.radius = 42
        self.pos = np.array([width/2*mm2pixel, height/2*mm2pixel])
        self.puck = pg.draw.circle(screen, pg.Color('red'), np.multiply(1/mm2pixel, self.pos).astype(int), int(self.radius/mm2pixel) ,2)
        self.m = 42 # grams
        self.v = np.array([0,0]) #mm/s
        #self.theta = 0 # Direction of velocity (0 = right)
        self.mu_F = 10 # Coefficient of friction of puck on table
        self.g = 9.8 # gravity m/s^2
        self.dt_impact = .5# time duration of impact


    def collisionWall(self, theta_wall) :
        print("Wall Collision")
        self.v = self.v - 2*np.abs(self.v)*[np.cos(theta_wall), np.sin(theta_wall)]

    def collisionArm(self, pos_arm, theta_arm, F_arm) :
        print("Arm Collision")
        print("Position:\nPuck: ({}, {}), Arm: ({}, {})".format(*self.pos, *pos_arm))
        theta_n = np.arctan2(*np.array(self.pos - pos_arm)[::-1])
        theta_puck = np.arctan2(*self.v[::-1])
        print("Theta_n: {}, Theta_puck: {}, Theta_arm: {}".format(theta_n, theta_puck, theta_arm))
        print("{} * {} + {} * {}".format(np.linalg.norm(self.v), np.cos(theta_puck - theta_n),  dt/self.m*F_arm, np.cos(theta_arm-theta_n)))
        V_n = (np.linalg.norm(self.v) * np.cos(theta_puck - theta_n))+(self.dt_impact / self.m * F_arm * np.cos(theta_arm-theta_n))        
        V_p = (np.linalg.norm(self.v) * np.sin(theta_puck - theta_n))
        print("{} * [{}, {}] + [{}, {}]".format(V_n, *np.array([np.cos(theta_n), np.sin(theta_n)]), *self.v))
        self.v = V_n*np.array([np.cos(theta_n), np.sin(theta_n)]) + V_p*np.array([np.cos(math.pi/2 + theta_n), np.sin(math.pi/2 + theta_n)])

    def friction(self) :
         theta = np.arctan2(*self.v[::-1])
         print("Theta: {}".format(theta))
         print("dv of Friction {}".format(self.mu_F*self.g*np.array([np.cos(theta + math.pi), np.sin(theta + math.pi)])*dt))
         self.v = self.v + self.mu_F*self.g*np.array([np.cos(theta + math.pi), np.sin(theta + math.pi)])*dt

    def update(self):
        print("pos ({}, {})".format(*self.pos))
        print("dpos ({}, {})".format(*np.multiply(dt, self.v)))
        print("v ({}, {})".format(*self.v))
        screen.fill(pg.Color('black'), self.puck)
        self.pos = self.pos + dt * self.v
        self.puck = pg.draw.circle(screen, pg.Color('red'), np.multiply(1/mm2pixel, self.pos).astype(int), int(self.radius/mm2pixel), 2)
        if self.pos[0]+self.radius > width*mm2pixel :
            self.collisionWall(0)
        if self.pos[0]-self.radius < 0:
            self.collisionWall(math.pi)
        if self.pos[1]-self.radius < 0:
            self.collisionWall(3*math.pi/2)
        if self.pos[1]+self.radius > height*mm2pixel:
            self.collisionWall(math.pi/2)
        self.friction()
gamePuck = Puck()

gamePuck.v = np.array([100,-100])
#gamePuck.theta = math.pi/4
HITPUCK = pg.USEREVENT+1

pg.time.set_timer(HITPUCK, 10000)
while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        if event.type == HITPUCK:
            print("*******Should hit puck now**********")
            gamePuck.collisionArm(gamePuck.pos+2, -3*math.pi/4, 20000)

    gamePuck.update()
    #pg.draw.circle(screen, )
    #screen.fill(pg.Color('black'))
    #screen.blit(screen, screen)
    pg.display.flip()
    time.sleep(dt)