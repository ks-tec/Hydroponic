# MicroPython DS18 thermistor driver, 1-wire interface.
# Inherit the DS18X20 driver.
#
# added the return value returned by @property values.
#   << return value >>
#   * The modified return value have unit, it is tuple.
#   * Temperature is up to the first decimal place.


from micropython import const
from ds18x20 import DS18X20
import time


# DS18x20 default waiting time
DS18_READING_WAIT = const(750)


class DS18(DS18X20):

  def __init__(self, ow=None, reading_wait=DS18_READING_WAIT):
    """
    Constructor
    """
    if ow is None:
      raise ValueError('An OneWire object is required.')
    self.ow = ow
    self.reading_wait = reading_wait

    super().__init__(self.ow)

  @property
  def values(self):
    """
    human readable values
    """
    self.convert_temp()
    time.sleep_ms(self.reading_wait)

    values = []
    roms = self.scan()
    for rom in roms:
      # print("Found DS18 devices (raw): ", rom)
      # print("                   (int): ", [int(r) for r in rom])
      # print("                   (hex): ", [hex(r) for r in rom])
      wtemp = self.read_temp(rom)
      values.append("{:3.1f}C".format(wtemp))

    return tuple(values)
