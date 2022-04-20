# See https://web.mit.edu/jorloff/www/chaosTalk/double-pendulum/double-pendulum-en.html

# Press the green button in the gutter to run the script.
import numpy as np
from matplotlib import pyplot as plt

from simulation import OurDoublePendulumSimulation


should_show_plots = True
should_save_plots = True


def new_plot():
    plt.figure()


def show_plot():
    if should_show_plots:
        plt.show()


def save_plot(fname):
    if should_save_plots:
        plt.savefig(f'plots/{fname}')
        plt.savefig(f'plots/{fname}.eps')


def close_plot():
    plt.close()


if __name__ == '__main__':
    ignace_theta = np.array([(0.48268159796618915, 1.4075560440100592),
                             (0.4771841570626947, 1.2827408797442708),
                             (0.797423485652458, 3.4975503917577786),
                             (3.357118838185478, 1.7380502642571576),
                             (4.122481617235922, 2.9639964863063053),
                             (-0.08784918948192133, 1.4587673643689087),
                             (0.6648021214162277, 0.5713374798336267),
                             (4.648814292435869, -0.5532943253222928),
                             (3.3910058774478404, 0.26299473168091936),
                             (-1.3365411132006457, 3.4552133058064918),
                             (0.7039845880278921, 3.823909208464541)])

    sim = OurDoublePendulumSimulation(
        dt=1e-4,
        t=0,
        theta1=np.pi - ignace_theta[:, 0],
        theta2=np.pi - ignace_theta[:, 1],
    )

    run_simulation = True

    plot_t_list = []
    plot_theta1_list2d = []
    plot_theta2_list2d = []

    for t in np.arange(0, 15, 0.02):
        sim.step_until(t)

        theta1_array = np.array(sim.theta1).reshape((-1))
        theta2_array = np.array(sim.theta2).reshape((-1))

        plot_theta1_list2d += [theta1_array]
        plot_theta2_list2d += [theta2_array]
        plot_t_list += [sim.get_time()]

        print(f't = {t:.3f}')

    plot_t_list = np.array(plot_t_list)
    plot_theta1_list2d = np.array(plot_theta1_list2d).transpose()
    plot_theta2_list2d = np.array(plot_theta2_list2d).transpose()

    plot_x1_list2d = sim.l1 * np.cos(plot_theta1_list2d)
    plot_y1_list2d = sim.l1 * np.sin(plot_theta1_list2d)
    plot_r1_list2d = np.sqrt(plot_x1_list2d ** 2 + plot_y1_list2d ** 2)
    plot_x2_list2d = sim.l2 * np.cos(plot_theta2_list2d) + plot_x1_list2d
    plot_y2_list2d = sim.l2 * np.cos(plot_theta2_list2d) + plot_y1_list2d
    plot_r2_list2d = np.sqrt(plot_x2_list2d ** 2 + plot_y2_list2d ** 2)

    for i in range(len(sim.theta1)):
        print(f'Saving case {i}')

        new_plot()
        plt.title(f'Case #{i}: $\\theta_1$ vs $t$')
        plt.plot(plot_t_list, plot_theta1_list2d[i])
        plt.xlabel('$t$ (s)')
        plt.ylabel('$\\theta_1$ (rad)')
        save_plot(f'case-{i}-theta1')
        # show_plot()
        close_plot()

        new_plot()
        plt.title(f'Case #{i}: $\\theta_2$ vs $t$')
        plt.plot(plot_t_list, plot_theta2_list2d[i])
        plt.xlabel('$t$ (s)')
        plt.ylabel('$\\theta_2$ (rad)')
        save_plot(f'case-{i}-theta2')
        # show_plot()
        close_plot()

        new_plot()
        plt.title(f'Case #{i}: $x_1$ vs $t$')
        plt.plot(plot_t_list, plot_x1_list2d[i])
        plt.xlabel('$t$ (s)')
        plt.ylabel('$x_1$ (m)')
        save_plot(f'case-{i}-x1')
        # show_plot()
        close_plot()

        new_plot()
        plt.title(f'Case #{i}: $y_1$ vs $t$')
        plt.plot(plot_t_list, plot_y1_list2d[i])
        plt.xlabel('$t$ (s)')
        plt.ylabel('$y_1$ (m)')
        save_plot(f'case-{i}-y1')
        # show_plot()
        close_plot()

        new_plot()
        plt.title(f'Case #{i}: $x_2$ vs $t$')
        plt.plot(plot_t_list, plot_x2_list2d[i])
        plt.xlabel('$t$ (s)')
        plt.ylabel('$x_2$ (m)')
        save_plot(f'case-{i}-x2')
        # show_plot()
        close_plot()

        new_plot()
        plt.title(f'Case #{i}: $y_2$ vs $t$')
        plt.plot(plot_t_list, plot_y2_list2d[i])
        plt.xlabel('$t$ (s)')
        plt.ylabel('$y_2$ (m)')
        save_plot(f'case-{i}-y2')
        # show_plot()
        close_plot()

        print(f'Saved case {i}')

    new_plot()
    plt.title('All $\\theta_1$ vs. $t$')
    for plot_theta1_list in plot_theta1_list2d:
        plt.plot(plot_t_list, plot_theta1_list)
    plt.xlabel('$t$ (s)')
    plt.ylabel('$\\theta_1$ (rad)')
    save_plot(f'all-theta1')
    show_plot()
    close_plot()

    new_plot()
    plt.title('$\\sigma(\\theta_1)$ vs. $t$')
    plt.plot(plot_t_list, np.std(plot_theta2_list2d, axis=0))
    plt.xlabel('$t$ (s)')
    plt.ylabel('$\\sigma(\\theta_1)$ (rad)')
    save_plot(f'sigma-theta1')
    show_plot()
    close_plot()

    new_plot()
    plt.title('$\\sigma(r_1)$ vs. $t$')
    plt.plot(plot_t_list, np.std(plot_r1_list2d, axis=0))
    plt.xlabel('$t$ (s)')
    plt.ylabel('$\\sigma(r_1)$ (m)')
    save_plot(f'sigma-r1')
    show_plot()
    close_plot()

    new_plot()
    plt.title('All $\\theta_2$ vs. $t$')
    for plot_theta2_list in plot_theta2_list2d:
        plt.plot(plot_t_list, plot_theta2_list)
    plt.xlabel('$t$ (s)')
    plt.ylabel('$\\theta_2$ (rad)')
    save_plot(f'all-theta2')
    show_plot()
    close_plot()

    new_plot()
    plt.title('$\\sigma(\\theta_2)$ vs. $t$')
    plt.plot(plot_t_list, np.std(plot_theta2_list2d, axis=0))
    plt.xlabel('$t$ (s)')
    plt.ylabel('$\\sigma(\\theta_2)$ (rad)')
    save_plot(f'sigma-theta2')
    show_plot()
    close_plot()

    new_plot()
    plt.title('$\\sigma(r_2)$ vs. $t$')
    plt.plot(plot_t_list, np.std(plot_r2_list2d, axis=0))
    plt.xlabel('$t$ (s)')
    plt.ylabel('$\\sigma(r_2)$ (m)')
    save_plot(f'sigma-r2')
    show_plot()
    close_plot()

    # stop_t = 10
    #
    # anim_time = 0
    # anim_dt = 0.1
    # for i in range(10):
    #     sim.step_until(anim_time)
    #     print(sim.__dict__)
    #     anim_time += anim_dt

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
