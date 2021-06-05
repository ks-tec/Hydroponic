# MicroPython DS18 thermistor driver, 1-wire interface.
# Inherit the DS18X20 driver.
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
from ds18x20 import DS18X20
import utime

from lib import util


# DS18x20 default waiting time
DS18_READING_WAIT = const(750)


class DS18(DS18X20):
  """
  This class is using DS18x20 with a 1-Wire interface.
  And, this class have a property to get readings with the @values.
  """

  def __init__(self, 
               ow=None, 
               reading_wait=DS18_READING_WAIT, 
               unit="C"):
    """
    Constructor of DS18.

    Args:
      ow : machine.OneWire object
      reading_wait : waiting time to read value
      unit : temperature unit
    """
    if ow is None:
      raise ValueError('An OneWire object is required.')

    self.ow = ow
    self.reading_wait = reading_wait
    self.unit = unit

    super().__init__(self.ow)

  @property
  def values(self):
    """
    human readable values

    Args:
        unit: unit of return value, default = "C"

    Return:
      tupple of read values.
    """
    values = []

    self.convert_temp()
    utime.sleep_ms(self.reading_wait)

    roms = self.scan()
    for rom in roms:
      # print("Found DS18 devices (raw): ", rom)
      # print("                   (int): ", [int(r) for r in rom])
      # print("                   (hex): ", [hex(r) for r in rom])
      wtemp = self.read_temp(rom)
      wtemp = util.conv_temperature_unit(wtemp, self.unit)
      values.append("{:3.1f}{}".format(wtemp, self.unit))

    return tuple(values)
