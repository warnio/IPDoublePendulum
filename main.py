# See https://web.mit.edu/jorloff/www/chaosTalk/double-pendulum/double-pendulum-en.html

import numpy as np
from abc import ABCMeta, abstractmethod
import matplotlib.pyplot as plt


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

    def __init__(self, dt, g, m1, m2, l1, l2, I1, I2, c1, c2, t, theta1, theta2, omega1=0, omega2=0, alpha1=0, alpha2=0, use_angle_normalization=False):
        # Constants
        self.dt = dt
        self.g = g
        self.m1 = m1
        self.m2 = m2
        self.l1 = l1
        self.l2 = l2
        self.I1 = I1
        self.I2 = I2
        self.c1 = c1
        self.c2 = c2

        # Variables
        self.t = t
        self.theta1 = theta1
        self.theta2 = theta2
        self.omega1 = omega1
        self.omega2 = omega2
        self.alpha1 = alpha1
        self.alpha2 = alpha2

        # Other options
        self.use_angle_normalization = use_angle_normalization

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
        I1 = self.I1
        I2 = self.I2
        c1 = self.c1
        c2 = self.c2

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

        self.theta1 = self.simplify_theta(theta1 + omega1 * dt)
        self.theta2 = self.simplify_theta(theta2 + omega2 * dt)

        self.omega1 = omega1 + alpha1 * dt
        self.omega2 = omega2 + alpha2 * dt

#       self.alpha1 = (
#               - g * (2 * m1 + m2) * np.sin(theta1)
#               - m2 * g * np.sin(theta1 - 2 * theta2)
#               - 2 * np.sin(theta1 - theta2) * m2 * (
#                       + omega2 ** 2 * l2
#                       + omega1 ** 2 * l1 * np.cos(theta1 - theta2)
#               )
#       ) / (l1 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))

#       self.alpha2 = (
#               2 * np.sin(theta1 - theta2) * (
#                       + omega1 ** 2 * l1 * (m1 + m2)
#                       + g * (m1 + m2) * np.cos(theta1)
#                       + omega2 ** 2 * l2 * m2 * np.cos(theta1 - theta2)
#               )
#       ) / (l2 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))

        I1_ = m1*l1**2 / 4 + m2*l1**2 + I1
        I2_ = m2*l2**2 / 4 + m2*l2**2 + I2
        k = m2*l1*l2 / 2
        A = (m1 + 2*m2)/2*g*l1
        B = 1/2*m2*g*l2
        Fw1 = c1*omega1**2*l1**2 / I1_ * (omega1 > 0) - c1*omega1**2*l1**2 / I1_ * (omega2 <= 0)
        Fw2 = c2*((omega1*l1*np.cos(theta1) + omega2*l2*np.cos(theta2))**2 + 
                  (omega1*l1*np.sin(theta1) + omega2*l2*np.sin(theta2))**2) * (omega2 > 0) - \
              c2*((omega1*l1*np.cos(theta1) + omega2*l2*np.cos(theta2))**2 + 
                  (omega1*l1*np.sin(theta1) + omega2*l2*np.sin(theta2))**2) * (omega2 <= 0)

        self.alpha1 = - (k*omega2**2 * np.sin(theta1 - theta2) + k*alpha2*np.cos(theta1 - theta2) + A*np.sin(theta1) + Fw1) / I1
        self.alpha2 =   (k*omega1**2 * np.sin(theta1 - theta2) - k*alpha1*np.cos(theta1 - theta2) - B*np.sin(theta2) + \
                         k*omega1**2 * np.sin(theta1 - theta2) - k*alpha1*np.cos(theta1 - theta2) - B*np.sin(theta2) - Fw2) / I2_

#       self.alpha1 = - (m2*alpha2*l1*l2*np.cos(theta1-theta2) \
#                     + 1/2*m2*omega2**2*l1*l2*np.sin(theta1-theta2) \
#                     + (m1+2*m2)/2*g*l1*np.sin(theta1)) \
#                     / (1/4*m1*l1**2+m2*l1**2+I1)
#       self.alpha2 = (-1/2*m2*alpha2*l1*l2*np.cos(theta1-theta2) \
#                     + 1/2*m2*omega1**2*l1*l2*np.sin(theta1-theta2) \
#                     - m2/2*g*l2*np.sin(theta2)) \
#                     / (1/4*m2*l2**2 + I2)

    def simplify_theta(self, theta):
        if self.use_angle_normalization:
            return normalize_angle(theta)
        return theta


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
        I1=1,
        I2=1,
        c1=1,
        c2=1,
        t=0,
        theta1=-np.full(10, np.pi),
        theta2=np.linspace(np.pi * 0.9990, np.pi - 0.0001, 10),
    )

    ### Simulation

    l1_array = np.array(sim.l1).reshape((-1))
    l2_array = np.array(sim.l2).reshape((-1))

    scale = 100
    time_scale = 1

    pygame.init()
    # Create the window, saving it to a variable.
    surface = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Double Pendulum Simulation")

    pygame.font.init()
    # font = pygame.font.SysFont(None, 30)

    time_start = None

    # PLOTTING
    prev_sim_time = 0
    ts = []
    y1s = []
    y2s = []

    run_simulation = False
    while True:
        surface.fill((255, 255, 255))

        if run_simulation:
            time_now = time.time()
            sim.step_until((time_now - time_start) * time_scale)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run_simulation = not run_simulation
                    time_start = time.time()
                elif event.key == pygame.K_EQUALS:
                    time_scale = time_scale * 1.1
                elif event.key == pygame.K_MINUS:
                    time_scale = time_scale / 1.1

        if sim.get_time() - prev_sim_time > 0:
            print(sim.get_time())
            ts += [sim.get_time()]
            y1s += [np.std(theta1_array)]
            y2s += [np.std(theta2_array)]
            prev_sim_time += .1
        if sim.get_time() > 45:
            break

    plt.plot(ts, y1s)
    plt.plot(ts, y2s)
    plt.show()

    # stop_t = 10
    #
    # anim_time = 0
    # anim_dt = 0.1
    # for i in range(10):
    #     sim.step_until(anim_time)
    #     print(sim.__dict__)
    #     anim_time += anim_dt

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
