from __future__ import print_function
import numpy as np
import tifffile
import argparse as ap
from copy import deepcopy
import math

size = 10
radius = 3

zeros = np.zeros((10,10,10))

sphere = deepcopy(zeros)

x0 = 5
y0 = 5
z0 = 5

for x in range(0, 10):
    for y in range(0, 10):
        for z in range(0,10):
            distance = math.sqrt(math.pow(x - x0, 2) + math.pow(y - y0, 2) + math.pow(z - z0, 2))
            if distance <= 5:  sphere[x,y,z] = 100



