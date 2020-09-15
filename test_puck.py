import unittest
from Puck import Puck
from math import pi
import numpy as np
import pygame as pg

class TestPuck(unittest.TestCase):
    def test_collision(self):
        mm2pixel = 2.5
        size = width, height = int(1219/mm2pixel), int(2134/mm2pixel) #size of table in mm

        screen = pg.display.set_mode(size)
        rad = 42
        pos = pos=np.array([420,420])
        mass=42
        mu=1
        dt_impact=.01
        dt_interval=.01
        test_puck = Puck(rad, pos, mass, mu, dt_impact, dt_interval,0,screen)
        test_puck.collision(test_puck.pos + [2,0], pi, 100)
        self.assertAlmostEqual(np.arctan2(*test_puck.v[::-1]), pi)
        self.assertAlmostEqual(np.linalg.norm(test_puck.v), 100 * dt_impact/mass)

        test_puck.collision(test_puck.pos + [-2,0], 0, 100)
        self.assertAlmostEqual(np.linalg.norm(test_puck.v), 0)

        test_puck.collision(test_puck.pos + [0, 2], pi/2, 100)
        self.assertAlmostEqual(np.arctan2(*test_puck.v[::-1]), pi/2)
        self.assertAlmostEqual(np.linalg.norm(test_puck.v), 100 * dt_impact/mass)

        test_puck.collision(test_puck.pos + [0, -2], 3*pi/2, 100)
        self.assertAlmostEqual(np.linalg.norm(test_puck.v), 0)

        test_puck.collision(test_puck.pos + [2,2], pi/4, 100)
        self.assertAlmostEqual(np.arctan2(*test_puck.v[::-1]), pi/4)
        self.assertAlmostEqual(np.linalg.norm(test_puck.v), 100 * dt_impact/mass)

        #Test collision at perpendicular angle (should cause no change)
        test_puck.collision(test_puck.pos + [2,-2], 5*pi/4, 100)
        self.assertAlmostEqual(np.arctan2(*test_puck.v[::-1]), pi/4)
        self.assertAlmostEqual(np.linalg.norm(test_puck.v), 100 * dt_impact/mass)

        #Test Change in direction
        test_puck.collision(test_puck.pos +[2,0], pi, np.cos(pi/4)*2*np.linalg.norm(test_puck.v)*test_puck.m/test_puck.dt_impact)
        self.assertAlmostEqual(np.arctan2(*test_puck.v[::-1]), 3*pi/4)
        self.assertAlmostEqual(np.linalg.norm(test_puck.v), 100 * dt_impact/mass)
    def test_friction(self):
        mm2pixel = 2.5
        size = width, height = int(1219/mm2pixel), int(2134/mm2pixel) #size of table in mm

        screen = pg.display.set_mode(size)
        rad = 42
        pos = pos=np.array([420,420])
        mass=42
        mu=10000
        dt_impact=.01
        dt_interval=1
        test_puck = Puck(rad, pos, mass, mu, dt_impact, dt_interval,0, screen)
        test_puck.v = np.array([500000,500000])
        theta = np.arctan2(*test_puck.v[::-1])
        v_expected = test_puck.v + mu*test_puck.g*np.array([np.cos(theta + pi), np.sin(theta + pi)])*dt_interval
        test_puck.friction()
        
        self.assertAlmostEqual(test_puck.v[0], v_expected[0])
        self.assertAlmostEqual(test_puck.v[1], v_expected[1])

        test_puck.v = np.array([0,0])
        test_puck.friction()
        
        self.assertAlmostEqual(test_puck.v[0], 0)
        self.assertAlmostEqual(test_puck.v[1], 0)

        test_puck.v = np.array([1,1])
        test_puck.friction()

        self.assertAlmostEqual(test_puck.v[0], 0)
        self.assertAlmostEqual(test_puck.v[1], 0)

    def test_update(self):
        mm2pixel = 2.5
        size = width, height = int(1219/mm2pixel), int(2134/mm2pixel) #size of table in mm

        screen = pg.display.set_mode(size)
        rad = 42
        pos = pos=np.array([0,0])
        mass=42
        mu=0
        dt_impact=.01
        dt_interval=2
        test_puck = Puck(rad, pos, mass, mu, dt_impact, dt_interval,0, screen)

        test_puck.update()
        self.assertEqual(test_puck.pos[0], pos[0])
        self.assertEqual(test_puck.pos[1], pos[1])

        test_puck.v = np.array([100,100])
        test_puck.update()
        self.assertEqual(test_puck.pos[0], 200)
        self.assertEqual(test_puck.pos[1], 200)

if __name__ == '__main__':
    unittest.main()