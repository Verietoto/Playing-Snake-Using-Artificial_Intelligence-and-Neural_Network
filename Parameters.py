"""Some Libraries to Import"""
import numpy as np
import sys
import os
import pygame
import random
from itertools import permutations
import multiprocessing
import copy
import concurrent.futures
from joblib import Parallel, delayed
from pygame import gfxdraw
import sys
from numba import jit
"""Arena Grid Color"""
GRID_COLOR_1 = (238,235,206)
GRID_COLOR_2 = (29,238,232)

"""Screen Option"""
GRID_SIZE = 20
SCREEN_WIDTH, SCREEN_HEIGHT = (800,600)
SCREEN_WIDTH2, SCREEN_HEIGHT2 = (300,700)
VISION_LENGTH = 5


"""Snake Direction"""
RIGHT = (GRID_SIZE, 0)
LEFT = (-GRID_SIZE, 0)
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)

"""Genetic Params"""
shape = (24, 24, 16, 4)
popNumb = 1000
parentNumber = int(0.6*popNumb)
mutationRate = 0.1

xObstacle = np.arange(5*GRID_SIZE, SCREEN_WIDTH-5*GRID_SIZE,20)
yObstackle = np.arange(5*GRID_SIZE, SCREEN_HEIGHT-5*GRID_SIZE,20)
OBSTACLE = [(x,3*GRID_SIZE) for x in xObstacle] + [(SCREEN_WIDTH-3*GRID_SIZE,y) for y in yObstackle] + [(x,SCREEN_WIDTH-5*GRID_SIZE) for x in xObstacle]