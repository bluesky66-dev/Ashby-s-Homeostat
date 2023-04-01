import sys
# relative path to folder which contains the Sandbox module
sys.path.insert(1, '../../Sandbox_v1_2')
sys.path.insert(1, '../lab6_part1')
from Sandbox import *

import copy as cp

# this simulates the needle on a Unit being physically pushed out of viable limits
class ImpulseDisturbanceSource(DisturbanceSource):

    # construct disturbance source
    def __init__(self, unit, start_times, mag=1):
        super().__init__(start_times, [], False) # call DisturbanceSource constructor
        self.unit = unit # the object which will be disturbed
        self.mag = mag # magnitude of disturbance

    # step disturbance source
    def step(self, dt):
        super().step(dt) # call DisturbanceSource step
        if self.enabled:  # if the disturbance source is enabled, disturb the homeostat essential variable
            self.unit.thetas[-1] = self.mag # apply the disturbance to the unit state

            self.enabled = False  # unlike a generic DisturbanceSource, this is a one-shot disturbance, and so is automatically disabled immediately after being applied

    # no need to implement reset in this class, as the unit's parameters/attributes
    # are not disturbed

class SquareWaveDisturbanceSource(DisturbanceSource):

    def __init__(self, unit, start_times, stop_times, freq=0.01, offset=0, amp=3, phase_shift=0):
        super().__init__(start_times, stop_times, False) # call DisturbanceSource constructor
        self.unit = unit # the object which will be disturbed
        self.sq_wave = SignalGenerator(freq=freq, form='square', offset=offset, amp=amp, phase_shift=phase_shift) # a square wave generator, which is used to drive one unit

    # step disturbance source
    def step(self, dt):
        o = self.sq_wave.step(dt) # always step the signal generator
        super().step(dt) # call DisturbanceSource step
        if self.enabled:  # if the disturbance source is enabled, disturb the homeostat essential variable
            self.unit.thetas[-1] = o # only use the signal when disturbance is enabled

    # no need to implement reset in this class, as the unit's parameters/attributes
    # are not disturbed
