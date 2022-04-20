# See https://web.mit.edu/jorloff/www/chaosTalk/double-pendulum/double-pendulum-en.html
import math
import sys
import time

import numpy as np
import pygame

from simulation import OurDoublePendulumSimulation

if __name__ == '__main__':
    sim = OurDoublePendulumSimulation(
        dt=1e-4,
        t=0,
        theta1=np.full(10, np.pi),
        theta2=np.linspace(np.pi*0.99999, np.pi*0.999999, 10),
    )

    ### Rendering

    length_scale = 100
    time_scale = 1

    def draw_pendulum(surface, l1, l2, theta1, theta2):
        x1, y1 = surface.get_width() / 2, surface.get_height() / 2
        x2 = x1 + length_scale * l1 * math.sin(theta1)
        y2 = y1 + length_scale * l1 * math.cos(theta1)
        x3 = x2 + length_scale * l2 * math.sin(theta2)
        y3 = y2 + length_scale * l2 * math.cos(theta2)

        pos1 = (x1, y1)
        pos2 = (x2, y2)
        pos3 = (x3, y3)

        pygame.draw.line(surface, color=(0, 0, 0), start_pos=pos1, end_pos=pos2, width=2)
        pygame.draw.line(surface, color=(0, 0, 0), start_pos=pos2, end_pos=pos3, width=2)

    def draw_pundulums(l1_array, l2_array, theta1_array, theta2_array):
        for l1, l2, theta1, theta2 in zip(l1_array, l2_array, theta1_array, theta2_array):
            draw_pendulum(surface, l1, l2, theta1, theta2)

    def render(sim):
        l1_array = np.array(sim.l1).reshape((-1))
        l2_array = np.array(sim.l2).reshape((-1))
        theta1_array = np.array(sim.theta1).reshape((-1))
        theta2_array = np.array(sim.theta2).reshape((-1))
        surface.fill((255, 255, 255))
        draw_pundulums(l1_array, l2_array, theta1_array, theta2_array)
        pygame.display.update()

    ### Controls

    pygame.init()
    surface = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Double Pendulum Simulation")

    # pygame.font.init()
    # font = pygame.font.SysFont(None, 30)

    time_start = None
    run_simulation = False

    def handle_keydown(event):
        global time_scale
        if event.key == pygame.K_SPACE:
            start_simulation()
        elif event.key == pygame.K_EQUALS:
            time_scale = time_scale * 1.1
        elif event.key == pygame.K_MINUS:
            time_scale = time_scale / 1.1

    def start_simulation():
        global run_simulation, time_start
        run_simulation = True
        if time_start is None:
            time_start = time.time()

    while True:

        if run_simulation:
            time_now = time.time()
            sim.step_until((time_now - time_start) * time_scale)

        render(sim)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                handle_keydown(event)

    # stop_t = 10
    #
    # anim_time = 0
    # anim_dt = 0.1
    # for i in range(10):
    #     sim.step_until(anim_time)
    #     print(sim.__dict__)
    #     anim_time += anim_dt

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
