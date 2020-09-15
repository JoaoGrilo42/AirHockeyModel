import pygame as pg
from math import pi
from math import sqrt
from numpy import arccos
from numpy import arctan2
import numpy as np

class Player:
    def __init__(self, xmax, ymax, pos_init, vmax, dt):
        #2 DOF arm
        self.XMAX = xmax # Length of first arm segment, between first and second actuator
        self.YMAX = ymax # Length of second arm segment, between second acuator and paddle.
        self.pos = np.array(pos_init)
        self.VMAX = vmax
        self.v = np.array([0,0])
        self.pos_des = np.array([0,0]) # desired position of paddle
        self.v_des = np.array([0,0]) # desired velocity of paddle at pos_des
        self.dt = dt # discrete time interval

    def goToPos(self, desPos, desv):
        self.pos_des = np.array(desPos)
        self.v_des = np.array(desv)
        if desPos[0] > self.XMAX:
            self.pos_des[0] = self.XMAX
        elif desPos[0] < 0:
            self.pos_des[0] = 0
        if desPos[1] > self.YMAX:
            self.pos_des[1] = self.YMAX
        elif desPos[1] < 0:
            self.pos_des[1] = 0
        if self.v_des[0] > self.VMAX:
            self.v_des[0] = self.VMAX
        elif self.v_des[0] < -self.VMAX:
            self.v_des[0] = -self.VMAX
        if self.v_des[1] > self.VMAX:
            self.v_des[1] = self.VMAX
        elif self.v_des[1] < -self.VMAX:
            self.v_des[1] = -self.VMAX
        

    def getPaddleState(self):
        return self.pos, self.v

    def update(self, screen, mm2pixel):
        dpos = self.pos_des - self.pos
        if dpos[0]/self.dt > self.v_des[0] :
            dpos[0] = self.v_des[0]*self.dt
        if dpos[1]/self.dt > self.v_des[1]:
            dpos[1] = self.v_des[1]*self.dt
        self.v = dpos/self.dt
        self.pos = self.pos + dpos
        
        RED = pg.Color("red")
        
        pg.draw.circle(screen, RED, (self.pos/mm2pixel).astype(int), int(50/mm2pixel), 2)
