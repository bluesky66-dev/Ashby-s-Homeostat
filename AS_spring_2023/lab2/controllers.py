import sys
# relative path to folder which contains the Sandbox module
sys.path.insert(1, '../../../Sandbox_v1_2')
from Sandbox import *

# A "broken" aggressor method. Fix it by editing the speed_command lines
def aggressor(dt, inputs, params, state=[]) -> List[float]:

    # set left motor speed
    left_speed_command = math.sin(4) + params[0]
    # set right motor speed
    right_speed_command = left_speed_command * params[0]

    # return motor speeds to robot's controller
    return [left_speed_command, right_speed_command]

aggressor_controller = BraitenbergController(step_fun=aggressor, gain=1)

# A "broken" coward method. Fix it by editing the speed_command lines
def coward(dt, inputs, params, state=[]) -> List[float]:

    # set left motor speed
    left_speed_command = math.sin(params[0]) - inputs[0]
    # set right motor speed
    right_speed_command = left_speed_command * params[0]

    # return motor speeds to robot's controller
    return [left_speed_command, right_speed_command]

coward_controller = BraitenbergController(step_fun=coward, gain=10)

# A "broken" lover method. Fix it by editing the speed_command lines
def lover(dt, inputs, params, state=[]) -> List[float]:

    # set left motor speed
    left_speed_command = math.sin(params[0]) - inputs[0]
    # set right motor speed
    right_speed_command = left_speed_command * params[0]

    # return motor speeds to robot's controller
    return [left_speed_command, right_speed_command]

lover_controller = BraitenbergController(step_fun=lover, gain=2)

# A "broken" monocular method. Fix it by editing the speed_command lines
def monocular(dt, inputs, params, state=[]) -> List[float]:

    # set left motor speed
    left_speed_command = params[0] - inputs[0]
    # set right motor speed
    right_speed_command = left_speed_command * inputs[1]

    # return motor speeds to robot's controller
    return [left_speed_command, right_speed_command]

monocular_controller = BraitenbergController(step_fun=monocular, gain=0.35)
