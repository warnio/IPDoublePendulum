from abc import ABCMeta, abstractmethod

import numpy as np


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


class IdealDoublePendulumSimulation(Simulation):

    def __init__(self, dt, g, m1, m2, l1, l2, t, theta1, theta2, omega1=0, omega2=0, alpha1=0, alpha2=0,
                 use_angle_normalization=False):
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

    def simplify_theta(self, theta):
        if self.use_angle_normalization:
            return normalize_angle(theta)
        return theta


class TigoDoublePendulumSimulation(Simulation):

    def __init__(self, dt, g, m1, m2, l1, l2, I1, I2, c1, c2, t, theta1, theta2, omega1=0, omega2=0, alpha1=0, alpha2=0,
                 use_angle_normalization=False):
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
        self.I1_ = m1 * l1 ** 2 / 4 + m2 * l1 ** 2 + I1
        self.I2_ = m2 * l2 ** 2 / 4 + m2 * l2 ** 2 + I2
        self.k = m2 * l1 * l2 / 2
        self.A = (m1 + 2 * m2) / 2 * g * l1
        self.B = 1 / 2 * m2 * g * l2

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
        l1 = self.l1
        l2 = self.l2
        I1_ = self.I1_
        I2_ = self.I2_
        c1 = self.c1
        c2 = self.c2
        k = self.k
        A = self.A
        B = self.B

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

        sin_theta1_minus_theta2 = np.sin(theta1 - theta2)
        cos_theta1_minus_theta2 = np.cos(theta1 - theta2)

        Fw1 = np.sign(omega1) * c1 * omega1 ** 2 * l1 ** 2 / I1_
        Fw2 = np.sign(omega2) * \
              c2 * ((omega1 * l1 * np.cos(theta1) + omega2 * l2 * np.cos(theta2)) ** 2 +
                    (omega1 * l1 * np.sin(theta1) + omega2 * l2 * np.sin(theta2)) ** 2)

        self.alpha1 = - (1 * (k * (omega2 ** 2 * sin_theta1_minus_theta2 + alpha2 * cos_theta1_minus_theta2) + A * np.sin(theta1)) + Fw1) / I1_
        self.alpha2 = + (2 * (k * (omega1 ** 2 * sin_theta1_minus_theta2 - alpha1 * cos_theta1_minus_theta2) - B * np.sin(theta2)) - Fw2) / I2_

    def simplify_theta(self, theta):
        if self.use_angle_normalization:
            return normalize_angle(theta)
        return theta


class OurDoublePendulumSimulation(TigoDoublePendulumSimulation):

    def __init__(self, dt, t, theta1, theta2, omega1=0, omega2=0, alpha1=0, alpha2=0, use_angle_normalization=False):
        g = 9.81
        m1 = 131e-3
        m2 = 131e-3
        l = 33.8e-2
        I1 = 1.4e-2
        I2 = 9.9e-3
        c1 = 0
        c2 = 0
        super().__init__(dt, g, m1, m2, l, l, I1, I2, c1, c2, t, theta1, theta2, omega1, omega2, alpha1, alpha2, use_angle_normalization)
