# See https://web.mit.edu/jorloff/www/chaosTalk/double-pendulum/double-pendulum-en.html

import numpy as np


def normalize_angle(angle):
    return angle % (2 * np.pi)


class DoublePendulumSimulation:

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

        self.omega1 = normalize_angle(omega1 + alpha1 * dt)
        self.omega2 = normalize_angle(omega2 + alpha2 * dt)

        self.alpha1 = normalize_angle(
            (
                    - g * (2 * m1 + m2) * np.sin(theta1)
                    - m2 * g * np.sin(theta1 - 2 * theta2)
                    - 2 * np.sin(theta1 - theta2) * m2 * (
                            + omega2 ** 2 * l2
                            + omega1 ** 2 * l1 * np.cos(theta1 - theta2)
                    )
            ) / (l1 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))
        )

        self.alpha2 = normalize_angle(
            (
                    2 * np.sin(theta1 - theta2) * (
                            + omega1 ** 2 * l1 * (m1 + m2)
                            + g * (m1 + m2) * np.cos(theta1)
                            + omega2 ** 2 * l2 * m2 * np.cos(theta1 - theta2)
                    )
            ) / (l2 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))
        )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sim = DoublePendulumSimulation(
        dt=1e-4,
        g=9.81,
        m1=1,
        m2=1,
        l1=1,
        l2=2,
        t=0,
        theta1=0,
        theta2=1,
    )

    while sim.t <= 0.1:
        print(sim.theta1, sim.theta2)
        sim.do_step()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
