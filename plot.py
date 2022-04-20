# See https://web.mit.edu/jorloff/www/chaosTalk/double-pendulum/double-pendulum-en.html

# Press the green button in the gutter to run the script.
import numpy as np
from matplotlib import pyplot as plt

from simulation import TigoDoublePendulumSimulation

if __name__ == '__main__':
    sim = TigoDoublePendulumSimulation(
        dt=1e-4,
        g=9.81,
        m1=1,
        m2=1,
        l1=np.full(1000, 1),
        l2=np.full(1000, 1),
        I1=1,
        I2=1,
        c1=1,
        c2=1,
        t=0,
        theta1=np.full(1000, np.pi),
        theta2=np.linspace(0, np.pi, 1000),
    )

    run_simulation = True

    plot_x_list = []
    plot_y_list2d = []

    for t in np.arange(0, 120, 0.1):
        sim.step_until(t)

        theta1_array = np.array(sim.theta1).reshape((-1))
        theta2_array = np.array(sim.theta2).reshape((-1))

        plot_y_list2d += [theta2_array]
        plot_x_list += [sim.get_time()]

        print(f't = {t}')

    plot_x_list = np.array(plot_x_list)
    plot_y_list2d = np.array(plot_y_list2d)
    for plot_y_list in plot_y_list2d.transpose():
        plt.plot(plot_x_list, plot_y_list)
    plt.show()
    plt.plot(plot_x_list, np.std(plot_y_list2d, axis=1))
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
