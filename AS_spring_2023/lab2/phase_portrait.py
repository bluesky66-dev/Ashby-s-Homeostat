import sys
# relative path to folder which contains the Sandbox module
sys.path.insert(1, '../../Sandbox_v1_2')
from Sandbox import *

# we use scipy to smooth time series data - this is usually a better choice of
# method than the moving average that I showed you in lab 1
from scipy import signal

# plot a phase portrait of the difference between the robot's sensor measurements
def plot_phase_portrait(x_axis, y_axis, t, margin_size, title, showColorBar):
    x_min = min(x_axis)-margin_size
    x_max = max(x_axis)+margin_size
    fig, ax = plt.subplots()
    tcp.doColourVaryingPlot2d(x_axis, y_axis, t, fig, ax, map_ind=0, showBar=showColorBar)
    ax.set_title(title)
    ax.set_xlabel('Left sensor activation - Right sensor activation')
    ax.set_ylabel('Derivative of x-axis with respect to time')
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([min(y_axis)-margin_size, max(y_axis)+margin_size])
    ax.plot([x_min, x_max], [0, 0], 'g--')
    ax.plot([0, 0], [min(y_axis)-margin_size, max(y_axis)+margin_size], 'g--')

# plot a robot's sensor measurements in vertically arranged subplots
def plot_sensors(t, left, right, title):
    fig, ax = plt.subplots(2, 1)
    plt.suptitle(title)
    ax[0].plot(t, left)
    ax[1].plot(t, right)
    ax[0].set_xlabel('Time')
    ax[1].set_xlabel('Time')
    ax[0].set_ylabel('Activation')
    ax[1].set_ylabel('Activation')
    ax[0].set_title('Left sensor')
    ax[1].set_title('Right sensor')
    fig.tight_layout()

# do phase portrait of sensor data
def do_phase_portraits(ts, robot_data):

	left_sensor_activations = robot_data["sensors"][0]["activations"]
	right_sensor_activations = robot_data["sensors"][1]["activations"]
	# plot an awful phase portrait using noisy raw sensor data
	dt = 0.1
	x = np.array(left_sensor_activations) - np.array(right_sensor_activations)
	x_dot = np.diff(x) / dt
	plot_phase_portrait(x[1:].tolist(), x_dot.tolist(), ts[1:], 0.01, 'A horrible phase portrait', True)
	plt.plot(x[-1], x_dot[-1], 'r*')

	# smooth sensor values
	b, a = signal.butter(1, 0.1) # adjusting the scale of the second parameter controls the degree of smoothing
	zi = signal.lfilter_zi(b, a)
	left_sensor_smoothed = signal.filtfilt(b, a, left_sensor_activations)
	right_sensor_smoothed = signal.filtfilt(b, a, right_sensor_activations)

	# plot smoothed sensor activations
	plot_sensors(ts, left_sensor_smoothed, right_sensor_smoothed, 'Smoothed sensor activations')

	# plot a (potentially) useful phase portrait using smoothed sensor data
	x = np.array(left_sensor_smoothed) - np.array(right_sensor_smoothed)
	x_dot = np.diff(x) / dt
	plot_phase_portrait(x[1:].tolist(), x_dot.tolist(), ts[1:], 0.01, 'A useful phase portrait', True)
	plt.plot(x[-1], x_dot[-1], 'r*')

	# plot rates of change of unsmoothed sensor measurements
	left_diffd = np.diff(left_sensor_activations) / dt
	right_diffd = np.diff(right_sensor_activations) / dt
	plot_sensors(ts[1:], left_diffd, right_diffd, 'Unsmoothed sensor activation rates of change')

	# plot rates of change of smoothed sensor measurements
	left_diffd = np.diff(left_sensor_smoothed) / dt
	right_diffd = np.diff(right_sensor_smoothed) / dt
	plot_sensors(ts[1:], left_diffd, right_diffd, 'Smoothed sensor activation rates of change')
