# See https://web.mit.edu/jorloff/www/chaosTalk/double-pendulum/double-pendulum-en.html

import numpy as np
from abc import ABCMeta, abstractmethod


def normalize_angle(angle):
    return angle % (2 * np.pi)


class Simulation(metaclass=ABCMeta):

    @abstractmethod
    def get_time(self):
        pass

    @abstractmethod
    def do_step(self):
        pass

    def step_until(self, time):
        while self.get_time() < time:
            self.do_step()


class DoublePendulumSimulation(Simulation):

    def __init__(self, dt, g, m1, m2, l1, l2, t, theta1, theta2, omega1=0, omega2=0, alpha1=0, alpha2=0):
        # Constants
        self.dt = dt
        self.g = g
        self.m1 = m1
        self.m2 = m2
        self.l1 = l1
        self.l2 = l2

        # Variables
        self.t = t
        self.theta1 = theta1
        self.theta2 = theta2
        self.omega1 = omega1
        self.omega2 = omega2
        self.alpha1 = alpha1
        self.alpha2 = alpha2

    def get_time(self):
        return self.t

    def do_step(self):
        # Constants
        dt = self.dt
        g = self.g
        m1 = self.m1
        m2 = self.m2
        l1 = self.l1
        l2 = self.l2

        # Variables
        t = self.t
        theta1 = self.theta1
        theta2 = self.theta2
        omega1 = self.omega1
        omega2 = self.omega2
        alpha1 = self.alpha1
        alpha2 = self.alpha2

        # Calculate next values
        self.t = t + dt

        self.theta1 = normalize_angle(theta1 + omega1 * dt)
        self.theta2 = normalize_angle(theta2 + omega2 * dt)

        self.omega1 = omega1 + alpha1 * dt
        self.omega2 = omega2 + alpha2 * dt

        self.alpha1 = (
                - g * (2 * m1 + m2) * np.sin(theta1)
                - m2 * g * np.sin(theta1 - 2 * theta2)
                - 2 * np.sin(theta1 - theta2) * m2 * (
                        + omega2 ** 2 * l2
                        + omega1 ** 2 * l1 * np.cos(theta1 - theta2)
                )
        ) / (l1 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))

        self.alpha2 = (
                2 * np.sin(theta1 - theta2) * (
                        + omega1 ** 2 * l1 * (m1 + m2)
                        + g * (m1 + m2) * np.cos(theta1)
                        + omega2 ** 2 * l2 * m2 * np.cos(theta1 - theta2)
                )
        ) / (l2 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import sys
    import pygame
    import math
    import time

    sim = DoublePendulumSimulation(
        dt=1e-4,
        g=9.81,
        m1=1,
        m2=1,
        l1=np.full(10, 1),
        l2=np.full(10, 1),
        t=0,
        theta1=np.full(10, np.pi),
        theta2=np.linspace(np.pi * 0.9990, np.pi - 0.0001, 10),
    )

    ### Simulation

    l1_array = np.array(sim.l1).reshape((-1))
    l2_array = np.array(sim.l2).reshape((-1))

    scale = 100

    pygame.init()
    # Create the window, saving it to a variable.
    surface = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Double Pendulum Simulation")

    pygame.font.init()
    # font = pygame.font.SysFont(None, 30)

    time_start = None

    start_simulation = False
    while True:
        surface.fill((255, 255, 255))

        if start_simulation:
            time_now = time.time()
            sim.step_until(time_now - time_start)

        theta1_array = np.array(sim.theta1).reshape((-1))
        theta2_array = np.array(sim.theta2).reshape((-1))

        for l1, l2, theta1, theta2 in zip(l1_array, l2_array, theta1_array, theta2_array):
            x1, y1 = surface.get_width() / 2, surface.get_height() / 2
            x2 = x1 + scale * l1 * math.sin(theta1)
            y2 = y1 + scale * l1 * math.cos(theta1)
            x3 = x2 + scale * l2 * math.sin(theta2)
            y3 = y2 + scale * l2 * math.cos(theta2)

            pos1 = (x1, y1)
            pos2 = (x2, y2)
            pos3 = (x3, y3)

            pygame.draw.line(surface, color=(0, 0, 0), start_pos=pos1, end_pos=pos2, width=2)
            pygame.draw.line(surface, color=(0, 0, 0), start_pos=pos2, end_pos=pos3, width=2)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_simulation = True
                time_start = time.time()

    # stop_t = 10
    #
    # anim_time = 0
    # anim_dt = 0.1
    # for i in range(10):
    #     sim.step_until(anim_time)
    #     print(sim.__dict__)
    #     anim_time += anim_dt

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
