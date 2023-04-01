import sys
# relative path to folder which contains the Sandbox module
sys.path.insert(1, '../../Sandbox_v1_2')
from Sandbox import *

import copy as cp

from Homeostat import *

'''
	4-unit Homeostat with random valued step change adaptation.
	When weights change, they are drawn from the uniform distribution
	[-1, 1]
'''
homie = Homeostat(n_units=4, upper_viability=1, lower_viability=-1, upper_limit=10, lower_limit=-10, adapt_fun=random_val, adapt_enabled=True, test_interval=10)

'''
	As in the first example, but there are no hard limits placed
	on the values that states can take.
'''
# homie = Homeostat(n_units=4, upper_viability=1, lower_viability=-1, adapt_fun=random_val, adapt_enabled=True)


'''
	As in the first example, but the parameters of the individual units are randomised, so that they have different dynamics.
'''
# homie = Homeostat(n_units=4, upper_viability=1, lower_viability=-1, upper_limit=10, lower_limit=-10, adapt_fun=random_val, adapt_enabled=True)
# for u in homie.units:
#     u.randomise_params()

'''
	As in the first example, but the parameters of the individual units are randomised, so that they have different dynamics, and there are only 3 units.
'''
# homie = Homeostat(n_units=3, upper_viability=1, lower_viability=-1, upper_limit=10, lower_limit=-10, adapt_fun=random_val, adapt_enabled=True)
# for u in homie.units:
#     u.randomise_params()

'''
	4-unit Homeostat with random valued step change adaptation.
	When weights change, they are drawn from the uniform distribution
	[-1, 1]

	The parameters of the individual units are randomised, so that they
	have different dynamics.
'''
# homie = Homeostat(n_units=4, upper_viability=1, lower_viability=-1, upper_limit=10, lower_limit=-10, adapt_fun=random_creeper)
# for u in homie.units:
#     u.randomise_params()

'''
	4-unit Homeostat with random valued step change adaptation.
	When weights change, they are drawn from the set of values which
	is created using numpy's linspace.
'''
# weights = np.linspace(-1, 1, 26)
# print(weights)
# homie = Homeostat(n_units=4, upper_viability=1, lower_viability=-1, upper_limit=10, lower_limit=-10, weights_set=weights, adapt_fun=random_selector, adapt_enabled=True)


t = 0
ts = [t]
dt = 0.01
duration = 500

while t < duration:
    # unit.step(dt)
    homie.step(dt)
    t += dt
    ts.append(t)

# PLOT 1: plot system state over time, showing when weights change
plt.figure()
for i, unit in enumerate(homie.units):
    plt.plot(ts, unit.thetas, label='Unit '+str(i))

# plot upper and lower viability boundaries
plt.plot([ts[0], ts[-1]],[homie.units[0].upper_viability, homie.units[0].upper_viability], 'r--', label='Viability boundaries')
plt.plot([ts[0], ts[-1]],[homie.units[0].lower_viability, homie.units[0].lower_viability], 'r--')

# plot upper and lower hard limits
plt.plot([ts[0], ts[-1]],[homie.units[0].upper_limit, homie.units[0].upper_limit], 'g--', label='Hard limits')
plt.plot([ts[0], ts[-1]],[homie.units[0].lower_limit, homie.units[0].lower_limit], 'g--')

# plot times when units start testing new weights
for i, t_t in enumerate(homie.units[0].test_times):
    if i:
        l = None
    else:
        l = 'Weights begin to change'
    plt.plot([t_t, t_t], [homie.units[0].lower_limit, homie.units[0].upper_limit], 'b--', label=l, linewidth=3)

plt.xlabel('t')
plt.ylabel(r'$\theta$')
plt.legend()
plt.title("System state over time")

# PLOT 2: plot system state over time, *without* showing when weights change
plt.figure()
for i, unit in enumerate(homie.units):
    plt.plot(ts, unit.thetas, label='Unit '+str(i))

# plot upper and lower hard limits
plt.plot([ts[0], ts[-1]],[homie.units[0].upper_viability, homie.units[0].upper_viability], 'r--', label='Viability boundaries')
plt.plot([ts[0], ts[-1]],[homie.units[0].lower_viability, homie.units[0].lower_viability], 'r--')

# plot upper and lower hard limits
plt.plot([ts[0], ts[-1]],[homie.units[0].upper_limit, homie.units[0].upper_limit], 'g--', label='Hard limits')
plt.plot([ts[0], ts[-1]],[homie.units[0].lower_limit, homie.units[0].lower_limit], 'g--')

plt.xlabel('t')
plt.ylabel(r'$\theta$')
plt.legend()
plt.title("System state over time")

# PLOT 3: plot all Homeostat unit weights over time
plt.figure()
for i, unit in enumerate(homie.units):
    plt.plot(ts, unit.weights_hist, label='Unit ' + str(i) + ': weight')
plt.title('Homeostat unit weights')
plt.xlabel('t')
plt.ylabel('Weights')
plt.legend()

# PLOT 4: plot when all Homeostat units are adapting
plt.figure()
for i, unit in enumerate(homie.units):
    plt.plot(ts, unit.testing_hist, label='Unit '+str(i))
plt.xlabel('t')
plt.ylabel('Adapting')
plt.title('Units in process of adapting')
plt.legend()

plt.show()
