
import numpy as np

dt = 1e-3

g = 9.81

m1 = 1
m2 = 1

l1 = 1
l2 = 1

t = 0

theta1 = 0
theta2 = 0

diff_theta1 = 0
diff_theta2 = 0

diff2_theta1 = 0
diff2_theta2 = 0

while t < 0.1:

    next_theta1 = theta1 + diff_theta1 * dt
    next_theta2 = theta2 + diff_theta2 * dt

    next_diff_theta1 = diff_theta1 + diff2_theta1 * dt
    next_diff_theta2 = diff_theta2 + diff2_theta2 * dt

    next_diff2_theta1 = 4 / (m1 + 4*m2) * (
            + .5 * m2 * l2 / l1 * (
                    + diff_theta1 * (diff_theta1 - diff_theta2) * np.sin(theta1 - theta2)
                    - diff2_theta2 * np.cos(theta1 - theta2)
            )
            + m2 * diff_theta1 * np.cos(theta1) / l1 * (
                    + 1.0 * l1 * diff_theta1 * np.sin(theta1)
                    + 0.5 * l2 * diff_theta2 * np.sin(theta2)
            )
            - m2 * diff_theta1 * np.sin(theta1) * (
                    + 1.0 * l1 * diff_theta1 * np.cos(theta1)
                    + 0.5 * l2 * diff_theta2 * np.sin(theta2)
            )
            - (.5 * m1 + m2) * g / l1
    )

    next_diff2_theta2 = (
            + 2 * l1 / l2 * diff_theta1 * (diff_theta1 - diff_theta2) * np.sin(theta1 - theta2)
            - 2 * l1 / l2 * diff2_theta1 * np.cos(theta1 - theta2)
            + l1 / l2 * diff_theta1 * diff_theta2 * np.sin(theta1 - theta2)
            - 2 * g / l2 * np.sin(theta2)
    )

    diff2_theta1 = next_diff2_theta1
    diff2_theta2 = next_diff2_theta2

    diff_theta1 = next_diff_theta1
    diff_theta2 = next_diff_theta2

    theta1 = next_theta1
    theta2 = next_theta2

    print(theta1, theta2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
