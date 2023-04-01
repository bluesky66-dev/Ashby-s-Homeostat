import sys
# relative path to folder which contains the Sandbox module
sys.path.insert(1, '../../../Sandbox_v1_2')
from Sandbox import *

'''
	An init_conditions method for setting the initial conditions of the robot's pose.

	This method places the robot at a different position on the radius of a circle
	every time. The robot's orientation is set to point roughly (using a small
	degree of randomness) towards the centre of the circle, which is where the
	light source is).

	As this method will be set to the init_conditions method of a robot, the only
	parameter to the method is "self", which will be a reference to that robot.
'''
def init_fun1(self):

	# coordinates will be randomly generated on the circumference of a circle with this radius
    rad = 7

	# angle of line from origin to robot's position
    alpha = random_in_interval(minimum=-math.pi, maximum=math.pi)
	# random value to add to robot's orientation, so that it is not always the same
    n = random_in_interval(minimum=-math.pi/5, maximum=math.pi/5)

	# alter the robot's pose: [x, y, theta]
	# - it is important to use the push method for this, so that the histories
	#	of the adjusted variables get updated correctly
    self.push(x=rad*math.cos(alpha), y=rad*math.sin(alpha), theta=alpha+math.pi+n)

'''
	An init_conditions method for setting the initial conditions of the robot's pose.

	In this case, this function generates a fixed number of robot poses.

	As this method will be set to the init_conditions method of a robot, the only
	parameter to the method is "self", which will be a reference to that robot.
'''
def init_fun2(self):

	# circle radius
    rad = 7
	# number of points
    n = 10

	# generate angles
    thetas = np.linspace(0, 2*np.pi, num=n, endpoint=False)
	# get angle index. by using the modulo operator, we ensure that this index
	# will always be valid, even if the function is used for more than n runs
    ind = self.init_ind % n
	# get angle
    angle = thetas[ind]

	# use angle to generate the robot's pose: [x, y, theta]
	# - it is important to use the push method for this, so that the histories
	#	of the adjusted variables get updated correctly
    self.push(x=rad * np.cos(angle), y=rad * np.sin(angle), theta=angle + np.pi)

'''
	A perturb function for perturbing the robot's pose. If this method is used in conjunction
	with init_fun2, then we will have robot poses which are generated on the
	radius of a circle, but have some degree of randomness added to them.

	We could use this method in conjunction with any init_conditions method we like.
	For example, we may ge generating initial poses for the robot on a square
	instead of a circle, or on any set of initial locations & orientations which
	we want to evaluate the robot's behaviour from. 

	As this method will be set to the perturb method of a robot, the only
	parameter to the method is "self", which will be a reference to that robot.
'''
def perturb2(self):
    x = self.x + random_in_interval(minimum=-1, maximum=1)
    y = self.y + random_in_interval(minimum=-1, maximum=1)
    theta = self.theta + random_in_interval(minimum=-math.pi/4, maximum=math.pi/4)

    self.push(x=x, y=y, theta=theta)
