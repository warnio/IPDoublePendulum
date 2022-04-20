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
    ignace_theta = np.array([(0.18785238812682503, 1.6456561745056635), (3.6822500791473463, 3.1669037027326414),
                             (-0.5406464119980261, 1.3639223778151535), (0.20856260832903684, 2.304516405709915),
                             (-0.35021995486593327, 2.8712673072111268), (-1.2915822569254067, -0.40964610862483797),
                             (0.6461892743611717, 2.4668517113662407), (1.2366691103291862, -1.2451547414516102),
                             (1.2032444926166803, 3.8181786121699965), (1.1221176595477609, -0.20202515640359242),
                             (0.4932247800060494, 1.4653070182698058), (0.5198015295221645, 1.392003271991975),
                             (0.797423485652458, 3.4975503917577786), (0.4932247800060494, -0.2536740961386428),
                             (1.950803577420135, -0.3256415853432868), (0.230356183303001, 2.662073361597197),
                             (0.2968594306923411, 1.371112441419795), (0.3413719116653715, 3.141592653589793),
                             (-0.35986767656927365, 0.36292577101173285), (-0.5184990745438727, 0.6270706625890182),
                             (1.1551944894782895, 3.7054620123704933), (-0.49494382916885415, 2.4316810351262683),
                             (1.3775848429470905, 3.4099588644957), (0.4613056929075765, -1.2908465042711055),
                             (1.9863981641115036, 0.6652894278305354), (1.9767355987303898, 4.651488772106702),
                             (0.12964507579873796, 2.793825665732778), (0.5989112617302315, 0.5685245477310399),
                             (0.3522909538467338, 1.8850282258792348), (0.37583121432417577, -0.3893167218331408),
                             (0.583050105862505, -0.8461927192722372), (2.199400471796612, -0.44179316551744385),
                             (0.36587561496297716, -0.7853981633974483), (-0.5779508199851331, 1.6559557194146033),
                             (-0.1573549404393042, 1.323442371223073), (0.24720017645111425, 2.245537269018449),
                             (1.1813248397418317, -0.024686342055599386), (1.1394903779752457, 0.48995732625372823),
                             (0.08019653541567218, 2.2119050956546022), (0.6648021214162277, 0.5713374798336267),
                             (1.1010138254362147, 2.0183163019520665), (3.3910058774478404, 0.26299473168091936),
                             (1.8481873907383886, -0.5914390161375551), (-0.014491739065500164, 1.9914596759279315),
                             (-0.04484171507888379, 2.238102461773251), (1.0276495605588427, -0.04758310327698356),
                             (0.2699025006519573, 2.635642254318717), (0.33499747117246437, 1.97568811307998),
                             (0.7130879581233178, 3.833249275442993), (0.40089667118474837, 1.964664937531258)])

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
