import random
import settings
import physics

class Sun():
    def __init__(self, x, y, r, m):
        self.x = x
        self.y = y
        self.r = r
        self.m = m

class Planet():
    def __init__(self, name, x, y, r, m, vx, vy, color):
        self.name = name
        self.x = x
        self.y = y
        self.r = r
        self.m = m
        self.vx = vx
        self.vy = vy
        self.color = color
        self.xr = [x]
        self.yr = [y]
        self.vxr = [vx]
        self.vyr = [vy]

