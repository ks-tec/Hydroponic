# MicroPython Water Level Detector.
# Using GPIO pin on ESP32 board.

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
