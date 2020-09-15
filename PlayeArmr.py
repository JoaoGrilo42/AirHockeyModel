import pygame as pg
from math import pi
from math import sqrt
from numpy import arccos
from numpy import arctan2
import numpy as np

class Player:
    def __init__(self, r1, r2, theta1, theta2, dTheta1, dTheta2, theta1_max, theta1_min, theta2_max, theta2_min, dOmega1_max, dOmega2_max, dt):
        #2 DOF arm
        self.r1 = r1 # Length of first arm segment, between first and second actuator
        self.r2 = r2 # Length of second arm segment, between second acuator and paddle.
        self.theta1 = theta1 # Angle of first actuator
        self.theta2 = theta2 # angle of second actuator
        self.dTheta1 = dTheta1 # Angular speed  of first actuator
        self.dTheta2 = dTheta2 # Angular speed of second actuator
        self.theta1_max = theta1_max # Maximum angle of actuator 1
        self.theta1_min = theta1_min # minimum angle of actuator 1
        self.theta2_max = theta2_max # Maximum angle of actuator 2
        self.theta2_min = theta2_min # Minimum angle of actuator 2
        self.omega1_max = dOmega1_max # Maximum rotational speed of actuator 1
        self.omega2_max = dOmega2_max # Maximum ratational speed of actuator 2
        self.pos_des = np.array([0,0]) # desired position of paddle
        self.v_des = np.array([0,0]) # desired velocity of paddle at pos_des
        self.dt = dt # discrete time interval

    def goToPos(self, x, y):
        self.pos_des = [x,y]

    def getPaddleState(self):
        R_01 = [[np.cos(self.theta1), -np.sin(self.theta1)],[np.sin(self.theta1), np.cos(self.theta1)]]
        R_12 = [[np.cos(self.theta2), -np.sin(self.theta2)],[np.sin(self.theta2), np.cos(self.theta2)]]
        
        d_01 = [[self.r1*np.cos(self.theta1)],[self.r1*np.sin(self.theta1)]]
        d_12 = [[self.r2*np.cos(self.theta2)],[self.r2*np.sin(self.theta2)]]

        H_01 = np.concatenate((R_01, d_01), 1)
        H_12 = np.concatenate((R_12, d_12), 1)
        H_01 = np.concatenate((H_01, [[0, 0, 1]]), 0)
        H_12 = np.concatenate((H_12, [[0, 0, 1]]), 0)

        H_02 = np.dot(H_01, H_12)

        pos = [H_02[0,2],H_02[1,2]]

        Rv_01 = [[-np.sin(self.theta1)*self.dTheta1, -np.cos(self.theta1)*self.dTheta1],[np.cos(self.theta1)*self.dTheta1, -np.sin(self.theta1)*self.dTheta1]]
        Rv_12 = [[-np.sin(self.theta2)*self.dTheta2, -np.cos(self.theta2)*self.dTheta2],[np.cos(self.theta2)*self.dTheta2, -np.sin(self.theta2)*self.dTheta2]]
        
        #### Not sure about the math for V shoudl it be dTheta or dTheta/dt
        v_01 = [[-self.r1*np.sin(self.theta1)*self.dTheta1],[self.r1*np.cos(self.theta1)*self.dTheta1]]
        v_12 = [[-self.r2*np.sin(self.theta2)*self.dTheta2],[self.r2*np.cos(self.theta2)*self.dTheta2]]

        Hv_01 = np.concatenate((Rv_01, v_01), 1)
        Hv_12 = np.concatenate((Rv_12, v_12), 1)
        Hv_01 = np.concatenate((Hv_01, [[0, 0, 1]]), 0)
        Hv_12 = np.concatenate((Hv_12, [[0, 0, 1]]), 0)

        Hv_02 = np.dot(Hv_01, Hv_12)

        pos = [H_02[0,2],H_02[1,2]]
        v = [Hv_02[0,2], Hv_02[1,2]]
        return pos, v

    def update(self, screen, mm2pixel):
        h = np.linalg.norm(self.pos_des)
        print("h: {}".format(h))
        arg = (h**2 + self.r1**2 - self.r2**2)/(2*h*self.r1)
        if arg > 1:
            arg = 1
        elif arg < -1:
            arg = -1      
        phi1 = arccos(arg)
        print("{} = arccos(({} + {} -{})/(2*{}*{}))".format(phi1, h**2, self.r1**2, self.r2**2, h, self.r1))
        theta1 = arctan2(*self.pos_des[::-1])-phi1
        print("{} = arctan({}/{})-{}".format(theta1, self.pos_des[1], self.pos_des[0], phi1))
        arg = (self.r1**2+self.r2**2-h**2)/(2*self.r1*self.r2)
        if arg > 1:
            arg = 1
        elif arg < -1:
            arg = -1      
        phi2 = arccos(arg)
        print("arg: {}, phi2: {}".format(arg, phi2))
        theta2 = pi - phi2
        omega1 = (theta1 - self.theta1)/self.dt
        omega2 = (theta2 - self.theta2)/self.dt
        print("theta1: {}, self.theta1: {}, theta2: {}, self.theta2: {}, omega1: {}, omega2: {}".format(theta1, self.theta1, theta2, self.theta2, omega1, omega2))
        if omega1 > self.omega1_max:
            self.dTheta1 = self.omega1_max*self.dt
        elif omega1 < -self.omega1_max:
            self.dTheta1 = -self.omega1_max*self.dt
        else:
            self.dTheta1 = (theta1 - self.theta1)
        if omega2 > self.omega2_max:
            self.dTheta2 = self.omega2_max*self.dt
        elif omega2 < -self.omega2_max:
            self.dTheta2 = -self.omega2_max*self.dt
        else:
            self.dTheta2 = (theta2 - self.theta2)
        self.theta1 += self.dTheta1
        self.theta2 += self.dTheta2
        print("dTheta1: {}, dTheta2: {}".format(self.dTheta1, self.dTheta2))
        RED = pg.Color("red")
        BLUE = pg.Color("blue")
        r1_start = pg.math.Vector2(0, 0)
        r1_end = pg.math.Vector2(int(self.r1/mm2pixel), 0)

        print("Theta1: {}, Theta2: {}".format(self.theta1, self.theta2))
        r1_end = r1_start + r1_end.rotate(self.theta1*180/pi)
        r2_start = pg.math.Vector2(0,0) + r1_end
        r2_end = pg.math.Vector2(int(self.r2/mm2pixel), 0)
        #r2_end = pg.math.Vector2(int(r1_end.x+self.r2/mm2pixel), int(r1_end.y))
        r2_end = r2_start + r2_end.rotate((self.theta2+self.theta1)*180/pi)

        pg.draw.line(screen, RED, r1_start, r1_end, 2)
        pg.draw.line(screen, BLUE, r2_start, r2_end, 2)
        pg.draw.circle(screen, RED, [int(r2_end.x), int(r2_end.y)], int(50/mm2pixel), 2)
