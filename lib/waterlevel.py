# MicroPython Water Level Detector.
# Using TouchPad pin on ESP32 board.
#
# Copyright (c) 2020 ks-tec
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to dealin the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sellcopies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE NOT LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS INTHE SOFTWARE.


from micropython import const
from machine import TouchPad


# water level sensing thresholds
WATER_LEVEL_SENSE_MAX      = const(530)
WATER_LEVEL_SENSE_MIN      = const(170)
WATER_LEVEL_SENSE_MULTIPLY = const(1)

class WaterLevelSensor:
  """
  This class is detecting water level using Touch Pin.
  And, this class have a property to get readings with the @values.
  """

  def __init__(self, tp=None, sense_max=WATER_LEVEL_SENSE_MAX, sense_min=WATER_LEVEL_SENSE_MIN):
    """
    Constructor of WaterLevelSensor

    Args:
      tp : machin.TouchPin object
      sense_max : Max capacitance
      sense_min : Min capacitance
    """
    if tp is None:
      raise ValueError('A TouchPad object is required.')
    if sense_max < sense_min:
      raise ValueError('Min threshold must be less than Max threshold.')

    self.sensor  = tp
    self.inverse = True
    self.sense_max = sense_max
    self.sense_min = sense_min
    self.cap_size  = sense_max - sense_min

  @property
  def values(self):
    """
    human readable values

    Return:
      tupple of read values.
    """
    values = []

    wlevel_raw = self.sensor.read()
    if wlevel_raw < self.sense_min:
      wlevel_raw = self.sense_min
    elif self.sense_max < wlevel_raw:
      wlevel_raw = self.sense_max
    wlevel_raw -= self.sense_min

    wlevel_per = wlevel_raw / self.cap_size * 100
    if self.inverse == True:
      wlevel_per = 100 - wlevel_per
    values.append("{:3.1f}%".format(wlevel_per))

    return tuple(values)
