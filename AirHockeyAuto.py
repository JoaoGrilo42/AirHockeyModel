import sys, pygame as pg
import numpy as np
import time
import math

pg.init()

mm2pixel = 2.5
m2pixel = .0025
size = width, height = int(1219/mm2pixel), int(2134/mm2pixel) #size of table in mm

screen = pg.display.set_mode(size)

dt = .005 # update interval in seconds

class Puck :
    def __init__(self):
        self.radius = 42
        self.pos = np.array([width/2*mm2pixel, height/2*mm2pixel])
        self.puck = pg.draw.circle(screen, pg.Color('red'), np.multiply(1/mm2pixel, self.pos).astype(int), int(self.radius/mm2pixel) ,2)
        self.m = 42 # grams
        self.v = np.array([0,0]) #mm/s
        self.mu_F = 5 # Coefficient of friction of puck on table
        self.g = 9.8 # gravity m/s^2
        self.dt_impact = .5# time duration of impact


    def collision(self, pos, theta, F) :
        print("Collision")
        print("Position:\nPuck: ({}, {}), Object: ({}, {})".format(*self.pos, *pos))
        theta_n = np.arctan2(*np.array(self.pos - pos)[::-1])
        theta_puck = np.arctan2(*self.v[::-1])
        print("Theta_n: {}, Theta_puck: {}, Theta: {}".format(theta_n, theta_puck, theta))
        V_n = (np.linalg.norm(self.v) * np.cos(theta_puck - theta_n))+(self.dt_impact * F / self.m * np.cos(theta-theta_n))        
        V_p = (np.linalg.norm(self.v) * np.sin(theta_puck - theta_n))
        print("V_n: {} = {} * {} + {} * {}".format(V_n, np.linalg.norm(self.v),np.cos(theta_puck - theta_n), self.dt_impact / self.m * F, np.cos(theta-theta_n)))
        print("V_p: {} = {} * {}".format(V_p, np.linalg.norm(self.v), np.sin(theta_puck - theta_n)))
        print("v(t-1): {}, {}".format(self.v, np.linalg.norm(self.v)))
        print("v(t) = {} * [{}, {}] + {} * [{}, {}]".format(V_n, *np.array([np.cos(theta_n), np.sin(theta_n)]),  V_p, *np.array([np.cos(theta_n - math.pi/2), np.sin(theta_n - math.pi/2)])))
        self.v = V_n*np.array([np.cos(theta_n), np.sin(theta_n)]) + V_p*np.array([np.cos(theta_n + math.pi/2), np.sin(theta_n + math.pi/2)])
        print("v(t): {}, {}".format(self.v, np.linalg.norm(self.v)))
    
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
        
        if self.pos[0]+self.radius > width*mm2pixel :
            self.pos[0] = width*mm2pixel-self.radius
            self.collision(self.pos + [self.radius, 0], math.pi + np.arctan2(*self.v[::-1]), 2*self.m*np.linalg.norm(self.v)/self.dt_impact)
        if self.pos[0]-self.radius < 0:
            self.pos[0] = self.radius
            self.collision(self.pos - [-self.radius, 0], math.pi+np.arctan2(*self.v[::-1]), 2*self.m*np.linalg.norm(self.v)/self.dt_impact)
        if self.pos[1]-self.radius < 0:
            self.pos[1] = self.radius
            self.collision(self.pos - [0, -self.radius], math.pi + np.arctan2(*self.v[::-1]), 2*self.m*np.linalg.norm(self.v)/self.dt_impact)
        if self.pos[1]+self.radius > height*mm2pixel:
            self.pos[1] = height*mm2pixel-self.radius
            self.collision(self.pos + [0, self.radius], math.pi +np.arctan2(*self.v[::-1]), 2*self.m*np.linalg.norm(self.v)/self.dt_impact)
        
        self.friction()
        
        self.pos = self.pos + dt * self.v
        
        self.puck = pg.draw.circle(screen, pg.Color('red'), np.multiply(1/mm2pixel, self.pos).astype(int), int(self.radius/mm2pixel), 2)

gamePuck = Puck()

HITPUCK = pg.USEREVENT+1

pg.time.set_timer(HITPUCK, 2000)
while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        if event.type == HITPUCK:
            print("*******Should hit puck now**********")
            gamePuck.collision(gamePuck.pos+2, -3*math.pi/4, 200000)

    gamePuck.update()
    #pg.draw.circle(screen, )
    #screen.fill(pg.Color('black'))
    #screen.blit(screen, screen)
    pg.display.flip()
    time.sleep(dt)