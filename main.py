import math
import pygame.gfxdraw
import set_settings
import settings
import cosmos
import ctypes
import os
import random
import physics
import time
import numba

pygame.init()
user32 = ctypes.windll.user32

dir = os.path.abspath(os.curdir)
display_width, display_heidth = user32.GetSystemMetrics(78) // 1.3, user32.GetSystemMetrics(79) // 1.3

flags = pygame.SCALED | pygame.DOUBLEBUF
user_screen = pygame.display.set_mode((display_width, display_heidth), flags, vsync=1)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
screen_data = [display_width, display_heidth]

icon_pg = pygame.image.load(dir + "\\icon.ico")#.convert_alpha()
pygame.display.set_icon(icon_pg)

pygame.display.set_caption("Gravity Sim")

screen = pygame.Surface((1920, 1080))
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()

def map_transl_func(file_name):
    txt_file = open(dir + '//data//' + file_name + '.txt')
    data = txt_file.read()
    data_list = data.split("\n")
    txt_file.close()

    answer_list = []

    return answer_list

def rect_collide_func(rect_0, rect_1):
    if ((rect_1[0] + rect_1[2]) / 2 > rect_0[0] and (rect_1[1] + rect_1[3]) / 2 > rect_0[1]):
        if ((rect_1[0] + rect_1[2]) / 2 < rect_0[2] and (rect_1[1] + rect_1[3]) / 2 < rect_0[3]):
            return True

    for i in range(2):
        if (rect_1[0] > rect_0[0] and rect_1[1] > rect_0[1]):
            if (rect_1[0] < rect_0[2] and rect_1[1] < rect_0[3]):
                return True
        if (rect_1[2] > rect_0[0] and rect_1[3] > rect_0[1]):
            if (rect_1[2] < rect_0[2] and rect_1[3] < rect_0[3]):
                return True

        rect_1 = [rect_1[2], rect_1[1], rect_1[0], rect_1[3]]

    return False

def gpu_blit_func(image, x, y):
    screen_rect = [0, 0, 1920, 1080]
    image_rect = [x, y, x + image.get_width(), y + image.get_height()]

    collide = rect_collide_func(screen_rect, image_rect)

    if (collide == True):
        crd_0 = [round(x), round(y)]
        crd_1 = [round(x + image.get_width()) - 1, round(y)]
        crd_2 = [round(x + image.get_width()) - 1, round(y + image.get_height()) - 1]
        crd_3 = [round(x), round(y + image.get_height()) - 1]

        pygame.gfxdraw.textured_polygon(screen, [crd_0,
                                                 crd_1,
                                                 crd_2,
                                                 crd_3], image, crd_0[0], crd_0[1] * -1)

def show_sun():
    pygame.gfxdraw.filled_circle(screen, int(display_width // 2), 700, 9, [155, 155, 155])
    pygame.gfxdraw.aacircle(screen, int(display_width // 2), 700, 9, [255, 255, 255])

def show_planet(x, y, r, color):
    x = x // settings.size + display_width // 2
    y = y // settings.size + 700
    pygame.gfxdraw.filled_circle(screen, int(x), int(y), int(r), color)
    pygame.gfxdraw.aacircle(screen, int(x), int(y), int(r), color)

def distance(x1, y1, x2, y2):
    dist = pow((pow(x2 - x1, 2)+pow(y2 - y1, 2)), 0.5)
    return dist

def update_screen(x, y, vx, vy, fv, frame):

    font_1 = pygame.font.SysFont("Consolas", round(40))
    f3menu3 = font_1.render("FPS: " + str(round(clock.get_fps())), True, [0, 0, 0])
    pygame.gfxdraw.box(screen, [1920 - f3menu3.get_width(), 0, f3menu3.get_width(), f3menu3.get_height()], [255, 255, 255])
    screen.blit(f3menu3, (1920 - f3menu3.get_width(), 0))

    pygame.gfxdraw.box(screen, [0, 0, 510, 343], [0, 0, 0])

    f3menu3 = font_1.render("X - " + str(round(x, 7)), True, [0, 0, 0])
    pygame.gfxdraw.box(screen, [0, 0, f3menu3.get_width(), f3menu3.get_height()], [255, 255, 255])
    screen.blit(f3menu3, (0, 0))

    f3menu3 = font_1.render("Y - " + str(round(y, 7)), True, [0, 0, 0])
    pygame.gfxdraw.box(screen, [0, 60, f3menu3.get_width(), f3menu3.get_height()], [255, 255, 255])
    screen.blit(f3menu3, (0, 60))

    f3menu3 = font_1.render("Vx - " + str(round(vx, 7)), True, [0, 0, 0])
    pygame.gfxdraw.box(screen, [0, 120, f3menu3.get_width(), f3menu3.get_height()], [255, 255, 255])
    screen.blit(f3menu3, (0, 120))

    f3menu3 = font_1.render("Vy - " + str(round(vy, 7)), True, [0, 0, 0])
    pygame.gfxdraw.box(screen, [0, 180, f3menu3.get_width(), f3menu3.get_height()], [255, 255, 255])
    screen.blit(f3menu3, (0, 180))

    f3menu3 = font_1.render("Final V - " + str(round(fv, 6)), True, [0, 0, 0])
    pygame.gfxdraw.box(screen, [0, 240, f3menu3.get_width(), f3menu3.get_height()], [255, 255, 255])
    screen.blit(f3menu3, (0, 240))

    f3menu3 = font_1.render("Frame - " + str(frame), True, [0, 0, 0])
    pygame.gfxdraw.box(screen, [0, 300, f3menu3.get_width(), f3menu3.get_height()], [255, 255, 255])
    screen.blit(f3menu3, (0, 300))

    if user_screen.get_width() != 1920 and user_screen.get_height() != 1080:
        v_screen = pygame.transform.scale(screen, (user_screen.get_width(), user_screen.get_height()))
    else:
        v_screen = screen

    pygame.gfxdraw.textured_polygon(user_screen, [[0, 0], [user_screen.get_width(), 0],
                                                  [user_screen.get_width(), user_screen.get_height()],
                                                  [0, user_screen.get_height()]], v_screen, 0, 0)
    pygame.display.flip()

def run():

    FPS = 60
    keys = pygame.key.get_pressed()
    running = True

    planets_list_x, planets_list_y, vx_list, vy_list = physics.calculate()
    print(planets_list_x)
    print(planets_list_y)

    iterator = 0


    fv = (vx_list[-1] ** 2 + vy_list[-1] ** 2) ** 0.5

    center_planet_x = 0
    center_planet_y = 0

    frame_step = 200

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if keys[pygame.K_s]:
                settings.size *= 0.001
            if keys[pygame.K_w]:
                settings.size *= 1000


        iterator += frame_step
        center_planet_x += frame_step * settings.vu
        center_planet_y += 0

        if iterator >= len(planets_list_x):
            iterator = 0
            center_planet_x = 0
            center_planet_y = 0
            screen.fill([0, 0, 0])

        show_sun()

        show_planet(planets_list_x[int(iterator)], planets_list_y[int(iterator)], 4, [255, 0, 0])

        update_screen(planets_list_x[int(iterator)], planets_list_y[int(iterator)], vx_list[int(iterator)], vy_list[int(iterator)], fv, int(iterator))

        show_planet(planets_list_x[int(iterator)], planets_list_y[int(iterator)], 4, [0, 255, 0])

    exit(0)

run()