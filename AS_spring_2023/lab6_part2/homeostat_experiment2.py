import sys
# relative path to folder which contains the Sandbox module
sys.path.insert(1, '../../Sandbox_v1_2')
sys.path.insert(1, '../lab6_part1')
from Sandbox import *

import copy as cp
from tqdm import tqdm

from Homeostat import *

from homeostat_disturbances import *

def run_once(plot_data, n_units=4, dt=0.01, viability_scale=1, k=1, duration=1000, experiment=2):
    # Homeostat parameters
    upper_limit = 20
    lower_limit = -20
    upper_viability = viability_scale
    lower_viability = -viability_scale
    adapt_fun = random_val
    weights_set = None
    test_interval = 10

    # # uncomment to use a discrete weight set
    # adapt_fun = random_selector
    # weights_set = np.linspace(-1, 1, 26)

    # Simulation parameters
    t = 0
    ts = [t]
    # duration = 1000

    # construct Homeostat
    homeostat = Homeostat(n_units=n_units, upper_limit=upper_limit, lower_limit=lower_limit, upper_viability=upper_viability, lower_viability=lower_viability, adapt_fun=adapt_fun, weights_set=weights_set, test_interval=test_interval)

    # manipulate damping parameters of springs
    for unit in homeostat.units:
        unit.k = k

    if experiment > 0:
        # start Homeostat from stable position
        for unit in homeostat.units:
            unit.thetas[-1] = 0
            unit.theta_dots[-1] = 0

    if experiment == 1:
        # create a list of disturbances
        # - positive and negative impulses alternating
        disturbances = [ImpulseDisturbanceSource(unit=homeostat.units[0], start_times=[200, 300, 400, 800], mag=10),
        ImpulseDisturbanceSource(unit=homeostat.units[0], start_times=[250, 350, 450], mag=-10)]
    elif experiment == 2:
    # create a list of disturbances
    # - a square wave disturbance which can be turned on/off
        disturbances = [SquareWaveDisturbanceSource(unit=homeostat.units[0], start_times=[50, 700], stop_times=[450], amp=10, phase_shift=10)]
    else:
        disturbances = []

    # randomise parameters for system equations
    # homeostat.randomise_params()

    # main Homeostat simulation loop
    while t < duration:
        homeostat.step(dt)
        for disturbance in disturbances:
            disturbance.step(dt)
        t += dt
        ts.append(t)

    if plot_data:
        # plot Homeostat essential variables and weights over time
        fig, ax = plt.subplots(2, 1)

        # plot all homeostat unit variables over time
        for i, unit in enumerate(homeostat.units):
            ax[0].plot(ts, unit.thetas, label='Unit ' + str(i) + ': essential variable')
        ax[0].plot([ts[0], ts[-1]], [upper_viability, upper_viability], 'r--', label='upper viable boundary')
        ax[0].plot([ts[0], ts[-1]], [lower_viability, lower_viability], 'g--', label='lower viable boundary')
        ax[0].set_title('Essential variables')
        ax[0].set_xlabel('t')
        ax[0].set_ylabel('Essential variable')
        ax[0].legend()

        # plot all homeostat unit weights over time
        for i, unit in enumerate(homeostat.units):
            ax[1].plot(ts, unit.weights_hist, label='Unit ' + str(i) + ': weight')
        ax[1].set_title('Connection weights')
        ax[1].set_xlabel('t')
        ax[1].set_ylabel('Weight')
        ax[1].legend()

        plt.suptitle("Needle spring damping: " + str(k))

    return homeostat

'''
	In this example, we simulate the Homeostat a number of times, with a
	disturbance to one unit that is repeated many times.

	With the default parameters given below, (e.g. when the Homeostat has only
	2 units, we will typically see that the unit which is not directly disturbed
	will adjust its weights such that the disturbance no longer causes it to lose
	viability, i.e. it typically adapts to the disturbance.

	In the terminal (or command prompt, run window, etc., depending on the
	environment you run the script in) some simple measures of performance are
	printed.
	For an individual run:

		The time each unit was adapting (or attempting to adapt) for is printed,
		as well as the average time for all units.

		The average time for all units over all runs is also printed, at the end.
'''
def basic_analysis(n_units=2, dt=0.01, n_runs=1, k=1, viability_scale=2, duration=1000, experiment=2):
    # n_units = 2 # number of units in Homeostat
    # dt = 0.01 # integration interval
    # n_runs = 1 # number of runs to simulate for per parameter value
    # k = 1 # needle spring damping coefficient
    # viability_scale = 1 # scale of +- viability limits
    sum_of_test_t_sums = 0
    for i in range(n_runs):
        homeostat = run_once(plot_data=i==n_runs-1, n_units=n_units, dt=dt, k=k, viability_scale=viability_scale, duration=duration, experiment=experiment)
        test_t_sum = 0
        print("\nRun ", i, "\n=======")
        for i, unit in enumerate(homeostat.units):
            test_t = sum(unit.testing_hist) * dt
            test_t_sum += test_t
            print("Unit ", i, " was adapting for ", test_t, " units of time")
        print("Average time adapting per unit: ", test_t_sum/n_units, "\n")
        sum_of_test_t_sums += test_t_sum
    print("Average time adapting over all runs: ", sum_of_test_t_sums/(n_runs*n_units))
    print("Average percentage of time adapting over all runs: ", sum_of_test_t_sums/(n_runs*n_units*duration), '%\n')

'''
	An example of a parameter sweep, an important and often informative analysis.

	In a parameter sweep, we run the simulation a number of times for each value
	of the parameter that we wish to test.

	In this case, we are studying how the width of the viability region affects
	the average time the Homeostat units spend adapting (or trying to adapt) their
	weights. For every parameter value (in viability scales) we run the simulation
	for some number of times (specified by n_runs), and then take the average
	of the adapting times.

	We need to run the simulation a number of times for each parameter because
	there is randomness in the simulation. How many times to run the simulation
	is normally determined by compromise - too few, and the results will be too
	subject to randomness, but too many, and the results will take too long to
	obtain.
'''
def param_sweep_1D(n_units=4, n_runs=10, viability_scales=np.linspace(0.2, 1, 5), do_plots=False, experiment=2):
    # do_plots = False # set to True, and one run per parameter value will be plotted
    # n_units = 4 # number of units in Homeostat
    dt = 0.01 # integration interval
    # n_runs = 4 # number of runs to simulate for per parameter value
    # viability_scales = np.linspace(0.2, 1, 5) # parameter values
    average_times = []
    for scale in tqdm(viability_scales):
        adapting_times = 0
        for i in range(n_runs):
            homeostat = run_once(plot_data=(i==n_runs-1) and do_plots, n_units=n_units, dt=dt, viability_scale=scale, experiment=experiment)
            for i, unit in enumerate(homeostat.units):
                adapting_times += sum(unit.testing_hist) * dt
        average_times.append(adapting_times / (n_runs*n_units))
    plt.figure()
    plt.plot(2*(np.array(viability_scales)), average_times)
    plt.xlabel("Width of viability region")
    plt.ylabel("Average time units were adapting")
    plt.title("Parameter sweep over width of viable region, with " + str(n_runs) + " runs")

'''
	Another example of a 1D parameter sweep. This time, it is the damping
	coefficient parameter which is swept over.
'''
def other_param_sweep_1D(n_units=4, n_runs=5, ks = np.linspace(0.1, 10, 20), do_plots=False, experiment=2):
    # do_plots = False # set to True, and one run per parameter value will be plotted
    # n_units = 4 # number of units in Homeostat
    dt = 0.01 # integration interval
    # n_runs = 1 # number of runs to simulate for per parameter value
    # ks = np.linspace(0.1, 10, 20) # damping parameter values
    average_times = []
    for k in tqdm(ks):
        adapting_times = 0
        for i in range(n_runs):
            homeostat = run_once(plot_data=(i==n_runs-1) and do_plots, n_units=n_units, dt=dt, k=k, experiment=experiment)
            for i, unit in enumerate(homeostat.units):
                adapting_times += sum(unit.testing_hist) * dt
        average_times.append(adapting_times / (n_runs*n_units))
    plt.figure()
    plt.plot(ks, average_times)
    plt.xlabel("Needle spring stiffneses")
    plt.ylabel("Average time units were adapting")
    plt.title("Parameter sweep over needle spring damping, with " + str(n_runs) + " runs")


# basic_analysis(n_runs=2, n_units=4, k=1, viability_scale=1, duration=1000, experiment=0)
# param_sweep_1D(n_units=2, n_runs=4, viability_scales=np.linspace(0.2, 1, 10), do_plots=True, experiment=0)
other_param_sweep_1D(n_units=4, n_runs=4, do_plots=True, ks=np.linspace(0.1, 10, 3), experiment=0)

plt.show()
