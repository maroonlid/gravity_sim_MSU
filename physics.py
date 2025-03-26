import math
import cosmos
import settings

def kofx(x, y):
    k = settings.g * settings.m / ((((x ** 2) + (y ** 2)) ** 0.5) ** 3) * x
    return k

def kofy(x, y):
    k = settings.g * settings.m / ((((x ** 2) + (y ** 2)) ** 0.5) ** 3) * y
    return k

def gravity(x, y, vx, vy):
    vx1 = vx - kofx(x, y) * settings.t
    vy1 = vy - kofy(x, y) * settings.t
    x1 = x + vx * settings.t - settings.vu * settings.t
    y1 = y + vy * settings.t

    return [vx1, vy1, x1, y1]

def calculate():
    for i in range(settings.n):
        settings.xr.append(gravity(settings.xr[-1], settings.yr[-1], settings.vxr[-1], settings.vyr[-1])[2])
        settings.yr.append(gravity(settings.xr[-1], settings.yr[-1], settings.vxr[-1], settings.vyr[-1])[3])
        settings.vxr.append(gravity(settings.xr[-1], settings.yr[-1], settings.vxr[-1], settings.vyr[-1])[0])
        settings.vyr.append(gravity(settings.xr[-1], settings.yr[-1], settings.vxr[-1], settings.vyr[-1])[1])

    return settings.xr, settings.yr, settings.vxr, settings.vyr
