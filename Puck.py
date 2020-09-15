import numpy as np
from math import pi
import pygame as pg


class Puck :
    def __init__(self, rad, pos, mass, mu, dt_impact, dt_interval, mm2pixel, screen):
        self.radius = rad
        self.pos = pos
        self.m = mass
        self.v = np.array([0,0]) #mm/s
        self.mu_F = mu
        self.g = 9.8 # gravity m/s^2
        self.dt_impact = dt_impact
        self.dt = dt_interval
        if mm2pixel <= 0 :
            self.mm2pixel = 1
        else :
            self.mm2pixel = mm2pixel
        self.screen = screen
        self.puck = pg.draw.circle(self.screen, pg.Color('red'), np.multiply(1/self.mm2pixel, self.pos).astype(int), int(self.radius/self.mm2pixel) ,2)

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
        print("v(t) = {} * [{}, {}] + {} * [{}, {}]".format(V_n, *np.array([np.cos(theta_n), np.sin(theta_n)]),  V_p, *np.array([np.cos(theta_n - pi/2), np.sin(theta_n - pi/2)])))
        self.v = V_n*np.array([np.cos(theta_n), np.sin(theta_n)]) + V_p*np.array([np.cos(theta_n + pi/2), np.sin(theta_n + pi/2)])
        print("v(t): {}, {}".format(self.v, np.linalg.norm(self.v)))
    
    def friction(self) :
        theta = np.arctan2(*self.v[::-1])
        print("Theta: {}".format(theta))
        print("dv of Friction {}".format(self.mu_F*self.g*np.array([np.cos(theta + pi), np.sin(theta + pi)])*self.dt))
        dv_f = self.mu_F*self.g*np.array([np.cos(theta + pi), np.sin(theta + pi)])*self.dt
        print("v: {}, v_f: {}".format(np.linalg.norm(self.v), np.linalg.norm(dv_f)))
        if (np.linalg.norm(self.v) - np.linalg.norm(dv_f)) < 0 :
            self.v = np.array([0,0])
        else :
            self.v = self.v + dv_f
        print("v after friction: {}".format(self.v))
        
    def update(self):
        print("pos ({}, {})".format(*self.pos))
        print("dpos ({}, {})".format(*np.multiply(self.dt, self.v)))
        print("v ({}, {})".format(*self.v))
        
        self.screen.fill(pg.Color('black'), self.puck)
                
        self.friction()
        
        self.pos = self.pos + self.dt * self.v
        
        self.puck = pg.draw.circle(self.screen, pg.Color('red'), np.multiply(1/self.mm2pixel, self.pos).astype(int), int(self.radius/self.mm2pixel), 2)
