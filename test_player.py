import unittest
from Player import Player
from math import pi
import numpy as np
import pygame as pg

class TestPuck(unittest.TestCase):
    def test_getPaddleState(self):
        p = Player(10, 10, 0, pi, 0, 0, pi, 0, pi, 0, 2*pi, 2*pi, 1)
        p.theta1 = 0
        p.theta2 = 0
        pos, v = p.getPaddleState()
        self.assertListEqual(pos, [20, 0])
        p.theta1 = pi/4
        pos, v = p.getPaddleState()
        self.assertListEqual(pos, [20*np.cos(p.theta1), 20*np.sin(p.theta1)])
        p.theta1 = 0
        p.theta2 = pi/2
        pos, v = p.getPaddleState()
        self.assertListEqual(pos, [10, 10])
        p.theta2 = pi/4
        pos, v = p.getPaddleState()
        self.assertListEqual(pos, [10+10*np.cos(p.theta2), 10*np.sin(p.theta2)])
        
    def test_update(self):
        mm2pixel = 2.5
        size = width, height = int(1219/mm2pixel), int(2134/mm2pixel) #size of table in mm

        screen = pg.display.set_mode(size)
        
        p = Player(10, 10, 0, pi, 0, 0, pi, 0, pi, 0, 2*pi, 2*pi, 2)
        p.pos_des = [0,20]
        p.update(screen, mm2pixel)
        p.update(screen, mm2pixel)
        self.assertAlmostEqual(p.theta1, pi/2)
        self.assertAlmostEqual(p.theta2, 0)
        