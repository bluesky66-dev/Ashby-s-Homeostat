import sys
# relative path to folder which contains the Sandbox module
sys.path.insert(1, '../../Sandbox_v1_2')
from Sandbox import *

from controllers import *
from initialisers import *
from phase_portrait import *

#########################################################################
#                           Noise section                               #
#########################################################################

# noise parameters for the robot's left motor
max_white_noise = 0. # try 0.1 and -0.1 at first for white noise params
min_white_noise = -0.
max_brown_noise_step = 0. # try 0.005 at first
spike_noise_prob = 0.025 # try 0.025 at first
pos_spike_size = 1 # if the prob param is 0, there are no spikes, so these params have no effect
neg_spike_size = -1

# construct noise source for robot's left motor
left_motor_noisemaker = NoiseMaker(white_noise_params=[max_white_noise, min_white_noise], brown_noise_step=max_brown_noise_step, spike_noise_params=[spike_noise_prob, pos_spike_size, neg_spike_size])

# we can quickly enable/disable noise by uncommenting or commenting out this line
left_motor_noisemaker = None

#########################################################################
#                      Simulation parameters                            #
#########################################################################

# select controller to use, from this list: [aggressor_controller, coward_controller, lover_controller, monocular_controller]
# - you can also add your own controllers to this list, which you should define in controllers.py
controller = coward_controller
# robot sensor parameters
field_of_view = 0.9 * math.pi
left_sensor_angle = np.pi/6
right_sensor_angle = -np.pi/6

# field_of_view = 0.7 * math.pi
# left_sensor_angle = np.pi/4
# right_sensor_angle = -np.pi/4

# simulation run parameters
screen_width = 700 # height and width of animation window, in pixels
duration = 80 # number of simulation time units to simulate for
n_runs = 10 # number of simulations to run
animate = True # whether or not to animate
animation_frame_delay = 10 # the 10s of milliseconds to pause between frames

#########################################################################
#                       Simulation section                              #
#########################################################################

# set up environment
light_sources = [LightSource(0, 0)]

# set up robot
robot = light_seeking_Robot(x=-5, y=0, theta=0, light_sources=light_sources, controller=controller, left_motor_noisemaker=left_motor_noisemaker, FOV=field_of_view, left_sensor_angle=left_sensor_angle, right_sensor_angle=right_sensor_angle, left_motor_inertia=10, right_motor_inertia=10)

# use these lines to set up ensembles of initial conditions for the robot
# - use init_fun1 with the perturb_fun line comnmented out
# - or use init_fun2 in conjunction with perturb2
# - or comment the init_fun line out and use perturb2 on its own
# - or see what happens if you comment both of these lines out
robot.init_fun = init_fun2 # use init_fun1 or init_fun2
robot.perturb_fun = perturb2

# put robot into list of agents for Simulator
agents=[robot]
# In future labs, this list will not be empty - disturbances are going to be very important
disturbances = []

# get Simulator object - note that agents, environmental systems, and disturbances are all passed to its constructor
sim = Simulator(agents=agents, envs=light_sources, duration=duration, dt=0.1, disturbances=disturbances)
# get SimulationRunner object
sim_runner = SimulationRunner(sim, animate=animate, pause_ani=True, animation_delay=animation_frame_delay, screen_width=screen_width)
# Run simulation n times
sim_data = sim_runner.run_sims(n=10)

#########################################################################
#                     Plotting and analysis section                     #
#########################################################################

# plot agents' trajectories
ax = plot_all_sims_trajectories(sim_data, show_cbar=False, cbar_fig=True)
for light in light_sources:
    light.draw(ax)
# plot robots' basic data (plots of robot's various noisemakers are not produced by this function call)
plot_all_robots_basic_data(sim_data, multiple_plots=False, show_motors=True, show_controllers=True, show_sensors=True)
# plot noise
plot_all_robots_noise(sim_data)

# get simulation data for phase plane plotting
ts = sim_data[0]["ts"]
robot_data = sim_data[0]["agents"][0]
# look at unsmoothed/smoothed data and phase portraits
do_phase_portraits(ts, robot_data)

plt.show()
