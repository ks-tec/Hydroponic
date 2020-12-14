# MicroPython Water Level Detector.
# Using GPIO pin on ESP32 board.
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


SUPPLY_START  = const(5)
SUPPLY_FINISH = const(100)

class Relay:
  """
  This class is switching relay using GPIO Pin.
  And, this class have a property to get readings with the @values.
  """

  def __init__(self, pin=None, supply_start=SUPPLY_START, supply_finish=SUPPLY_FINISH):
    """
    Constructor of WaterLevelSensor

    Args:
      pin : Pin object
      supply_start : switching water level
    """
    if pin is None:
      raise ValueError("A Pin object is required.")

    self.relay_pin = pin
    self.supply_start  = supply_start
    self.supply_finish = supply_finish

  def on(self):
    """
    Set the relay pin status to high.
    """
    self.relay_pin.on()

  def off(self):
    """
    Set the relay pin status to low.
    """
    self.relay_pin.off()
