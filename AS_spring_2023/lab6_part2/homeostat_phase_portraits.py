import sys
# relative path to folder which contains the Sandbox module
sys.path.insert(1, '../../Sandbox_v1_2')
sys.path.insert(1, '../lab6_part1')
from Sandbox import *

import copy as cp

from Homeostat import *

# construct a Homeostat unit. this is the unit which we will study
unit0 = Unit(lower_viability=-np.Inf, upper_viability=np.Inf, test_interval=10, # add a new Unit to the Homeostat
            theta0=0,
            theta_dot0=0,
            adapt_fun = random_val
            )

# unit1 is used as a constant input to unit0 - for this reason, unit1 is not stepped
unit1_output = -12
unit1 = Unit(lower_viability=-np.Inf, upper_viability=np.Inf, test_interval=10, # add a new Unit to the Homeostat
            theta0=unit1_output,
            theta_dot0=0,
            adapt_fun = random_val
            )

# set simulation time step
dt = 0.01

# set the feedback weight
# w00 = -1
# w00 = 0
# w00 = 1
w00 = random_in_interval(minimum=-1, maximum=1)

# set the input weight
# w10 = 0
w10 = random_in_interval(minimum=-1, maximum=1)

# connect units
# note: unit 0 is connected to itself
#       unit 1 is connected to unit 0, but nothing is connected to unit 1
unit0.add_connection(unit0, w00)
unit0.add_connection(unit1, w10)

# set up grids for quiver plot
n = 21
lims = (-15, 15)
plot_angles = np.linspace(*lims, n)
thetas, thetadots = np.meshgrid(plot_angles, plot_angles)

# for each point on the quiver plot, calculate the acceleration
thetadotdots = np.zeros([n, n])
for i in range(len(thetas[0])):
    for j in range(len(thetas[0])):
        theta = thetas[i][j]
        thetadot = thetadots[i][j]
        unit0.thetas[-1] = theta # set unit state variables to values from grid
        unit0.theta_dots[-1] = thetadot
        unit0.step(dt) # step unit to find new acceleration value
        thetadotdots[i][j] = unit0.theta_dotdots[-1] # store acceleration value

# produce quiver plot to show field for unit0
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.quiver(thetas, thetadots, thetadots, thetadotdots)

# plot lines to show where the limits to viability *could* be (in this simulation,
#   the viability region is not defined, so that the unit will not adapt)
ax.plot([10, 10], [-15, 15], 'r--', linewidth='2')
ax.plot([-10, -10], [-15, 15], 'r--', linewidth='2')

# run the simulation 20 times from random initial states
for _ in range(20):
    # randomise essential variable
    theta0 = random_in_interval(minimum=-15, maximum=15)
    # randomise rate of change of essential variable
    theta_dot0 = random_in_interval(minimum=-15, maximum=15)
    # construct unit0 - this is the unit we are studying
    unit0 = Unit(lower_viability=-np.Inf, upper_viability=np.Inf, test_interval=10, # add a new Unit to the Homeostat
                 theta0=theta0,
                 theta_dot0=theta_dot0,
                 adapt_fun = random_val
                 )

    unit1 = Unit(lower_viability=-np.Inf, upper_viability=np.Inf, test_interval=10, # add a new Unit to the Homeostat
                 theta0=unit1_output,
                 theta_dot0=0,
                 adapt_fun = random_val
                 )

    # connect units
    # note: unit 0 is connected to itself
    #       unit 1 is connected to unit 0, but nothing is connected to unit 1
    unit0.add_connection(unit0, w00)
    unit0.add_connection(unit1, w10)

    # run simulation for a fixed number of steps
    for _ in range(1000):
        unit0.step(dt)

    # plot lines of behaviour from simulation run
    # this plots a circle at the *beginning* of the line, so we can tell which direction it is moving in
    plt.plot(unit0.thetas[1], unit0.theta_dots[1], 'bo')
    # this plots the actual line of behaviour
    plt.plot(unit0.thetas[1:], unit0.theta_dots[1:], 'b--')


# set axis limits
ax.set_xlim([-15, 15])
ax.set_ylim([-15, 15])
# label figure axes
font_size = 15
ax.set_xlabel('$\Theta$', fontsize=font_size, fontweight='bold')
ax.set_ylabel('$\dot{\Theta}$', fontsize=font_size, fontweight='bold')
ax.set_title('Homeostat unit phase portrait')

# print out unit0 weights to terminal
print("Weight 0->0 (feedback): " + str(w00))
print("Weight 1->0 (input): " + str(w10))

plt.show()
