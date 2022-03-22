# See https://web.mit.edu/jorloff/www/chaosTalk/double-pendulum/double-pendulum-en.html

import numpy as np


def normalize_angle(angle):
    return angle % (2 * np.pi)


dt = 1e-4

g = 9.81

m1 = 1
m2 = 1

l1 = 1
l2 = 1

t = 0

theta1 = 0
theta2 = np.pi/2

omega1 = 0
omega2 = 0

alpha1 = 0
alpha2 = 0


while t < np.inf:

    next_theta1 = normalize_angle(theta1 + omega1 * dt)
    next_theta2 = normalize_angle(theta2 + omega2 * dt)

    next_omega1 = normalize_angle(omega1 + alpha1 * dt)
    next_omega2 = normalize_angle(omega2 + alpha2 * dt)

    next_alpha1 = normalize_angle(
            (
                    - g * (2*m1 + m2) * np.sin(theta1)
                    - m2 * g * np.sin(theta1 - 2*theta2)
                    - 2 * np.sin(theta1 - theta2) * m2 * (
                            + omega2 ** 2 * l2
                            + omega1 ** 2 * l1 * np.cos(theta1 - theta2)
                    )
            ) / (l1 * (2*m1 + m2 - m2 * np.cos(2*theta1 - 2*theta2)))
    )

    next_alpha2 = normalize_angle(
            (
                    2 * np.sin(theta1 - theta2) * (
                            + omega1**2 * l1 * (m1 + m2)
                            + g * (m1 + m2) * np.cos(theta1)
                            + omega2**2 * l2 * m2 * np.cos(theta1 - theta2)
                    )
            ) / (l2 * (2*m1 + m2 - m2 * np.cos(2*theta1 - 2*theta2)))
    )

    theta1 = next_theta1
    theta2 = next_theta2

    omega1 = next_omega1
    omega2 = next_omega2

    alpha1 = next_alpha1
    alpha2 = next_alpha2

    print(theta1, theta2)

    t += dt


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
