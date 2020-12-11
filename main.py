# This is Hydroponic project in MicroPython with the ESP32 board.
# Using devices are SSD1306 OLED, DS18B20, BME280, and Touch Pin.


from machine import I2C, Pin, TouchPad
import os, sys, machine, onewire, ubinascii, ujson, utime, _thread

from lib import ssd1306, bme280, ds18, waterlevel
from resource import splashicon


# application setting file
CONFIG_FILE = "hydroponic.json"


# ==================== Main Functions ====================

def main():
  """
  Main function.
  """
  splash_screen()
  utime.sleep_ms(DISPLAY_WAITING_SPLASH)

  check_platform()
  utime.sleep_ms(DISPLAY_WAITING_PLATFORM)

  # thread start
  _thread.start_new_thread(display_callback, (1, DISPLAY_TIMER_PERIOD - ds18.reading_wait))


# ==================== Callback Functions ====================

def display_callback(id, delay_ms):
  """
  Callback function for read values from BME280 and DS18x20, water level detector.
  After that, bellow showing values to OLED.

  Args:
    id : thread id
    delay_ms : delay time is repeat waiting time for function
  """
  while True:
    oled.fill(0)
    oled.text("[air]", 0, 0)                            # [atmospheric]
    oled.text("T=" + bme.values[0],  0, 10)             # - temperature
    oled.text("H=" + bme.values[2], 64, 10)             # - humidity
    oled.text("P=" + bme.values[1],  0, 20)             # - pressure
    oled.text("[water]", 0, 30)                         # [water]
    oled.text("W=" + ds18.values[0],    0, 40)          # - temperature
    oled.text("L=" + wlevel.values[0], 64, 40)          # - raw water level
    oled.show()

    for cnt in range(3600):         # max waiting 1hour = 60min = 3600sec
      utime.sleep_ms(1000)

      oled.text(".", 8*cnt, 55)
      oled.show()

      waiting = (cnt + 1) * 1000
      if delay_ms <= waiting:       # waiting limit has exceeded delay_ms
        break
      cnt += 1


# ==================== Configuration Functions ====================

def load_settings(filename):
  """
  Load application setting values from specified file.
  The contents of the file must be in json format, and keywords are fixed.

  Ars:
    filename : file name of setting file
  """
  global DISPLAY_SPLASH_ICON, DISPLAY_WAITING_SPLASH, DISPLAY_WAITING_PLATFORM, DISPLAY_TIMER_PERIOD
  global OLED_PIN_SCL, OLED_PIN_SDA, OLED_ADDRESS, OLED_WIDTH, OLED_HEIGHT
  global BME280_PIN_SCL, BME280_PIN_SDA, BME280_ADDRESS
  global DS18_PIN_DQ, DS18_ADDRESS, DS18_READING_WAIT
  global WATER_LEVEL_PIN, WATER_LEVEL_SENSE_MAX, WATER_LEVEL_SENSE_MIN

  if filename is None or len(filename) == 0:
    raise ValueError("An application setting file is required.")
  elif filename not in os.listdir():
    raise OSError("An application setting file is NOT exists.")

  with open(filename) as f:
    settings = ujson.load(f)

  # COMMON settings
  DISPLAY_SPLASH_ICON      = settings["COMMON"]["SPLASH_ICON"]
  DISPLAY_WAITING_SPLASH   = int(str(settings["COMMON"]["SPLASH_WAITING"]),   0)
  DISPLAY_WAITING_PLATFORM = int(str(settings["COMMON"]["PLATFORM_WAITING"]), 0)
  DISPLAY_TIMER_PERIOD     = int(str(settings["COMMON"]["DISPLAY_TIMER"]),    0)

  # OLED settings
  OLED_PIN_SCL = int(str(settings["OLED"]["PIN_SCL"]), 0)
  OLED_PIN_SDA = int(str(settings["OLED"]["PIN_SDA"]), 0)
  OLED_ADDRESS = int(str(settings["OLED"]["ADDRESS"]), 0)
  OLED_WIDTH   = int(str(settings["OLED"]["WIDTH"]),   0)
  OLED_HEIGHT  = int(str(settings["OLED"]["HEIGHT"]),  0)

  # BME280 settings
  BME280_PIN_SCL = int(str(settings["BME280"]["PIN_SCL"]), 0)
  BME280_PIN_SDA = int(str(settings["BME280"]["PIN_SDA"]), 0)
  BME280_ADDRESS = int(str(settings["BME280"]["ADDRESS"]), 0)

  # DS18B20 settinsgs
  DS18_PIN_DQ       = int(str(settings["DS18X20"]["PIN_DQ"]), 0)
  DS18_ADDRESS      = [int(str(addr), 0) for addr in settings["DS18X20"]["ADDRESS"]]
  DS18_READING_WAIT = int(str(settings["DS18X20"]["READING_WAIT"]), 0)

  # TOUTCH SENSOR settings
  WATER_LEVEL_PIN            = int(str(settings["WATER_LEVEL"]["PIN_DQ"]),    0)
  WATER_LEVEL_SENSE_MAX      = int(str(settings["WATER_LEVEL"]["SENSE_MAX"]), 0)
  WATER_LEVEL_SENSE_MIN      = int(str(settings["WATER_LEVEL"]["SENSE_MIN"]), 0)


# ==================== I2C device Functions ====================

def detect_i2c_device(i2c=None, device=None, address=None):
  """
  I2C device scan and it was found or else, show message.

  Args:
    i2c : machine.I2C object
    device : name of I2C device to display
    address : address of I2C device
  """
  if i2c is None:
    raise ValueError("An I2C object is required.")
  if address is None:
    raise ValueError("A device address is required.")
  if device is None or len(device) == 0:
    raise ValueError("A device name is required.")

  print("Detecting {} ...".format(device))
  i2cDevs = i2c.scan()
  for idx, dev in enumerate(i2cDevs):
    if dev == address:
      print("  Found {} device: ['{}']".format(device, hex(dev)))
      break
  else:
    print("  NOT Found I2C device, check wiring of device !")


# ==================== SPI device Functions ====================

def detect_ow_device(ow=None, device=None, address=None):
  """
  1-Wire device scan and it was found, show message.

  Args:
    ow : machine.OneWire object
    device : name of 1-Wire device to display
    address : list of address for 1-Wire deviece address
  """
  if ow is None:
    raise ValueError("An ow object is required.")
  if address is None:
    raise ValueError("A device address is required.")
  if device is None or len(device) == 0:
    raise ValueError("A device name is required.")

  print("Detecting {} ...".format(device))
  owDevs = ow.scan()
  for idx, dev in enumerate(owDevs):
    addr_int = [int(r) for r in dev]
    if addr_int == address:
      print("  Found {} device: {}".format(device, [hex(r) for r in dev]))
      break
  else:
    print("  NOT Found 1-Wire device, check wiring of device !")


# ==================== Platform Functions ====================

def check_platform():
  """
  Check running platform, and show result to OLED.
  """
  platform = sys.platform
  chip_id = str(ubinascii.hexlify(machine.unique_id()))[2:14]
  pclk = machine.freq() // (1000 ** 2)

  supported = " Supported"
  if platform != "esp32":
    raise ValueError("Platform is esp32 board required.")

  oled.fill(0)
  oled.show()

  oled.text(platform, 0, 0)
  oled.text(supported, 0, 10)
  oled.text("UID {}".format(chip_id), 0, 20)
  oled.text("PCLK {}MHz".format(pclk) , 0, 30)
  oled.show()

  print("-" * 20)
  print("PLATFORM : {}".format(platform))
  print("CHIP UID : {}".format(chip_id))
  print("PERIPHERAL CLOCK : {} MHz".format(pclk))
  print("-" * 20)


# ==================== OLED Functions ====================

def splash_screen():
  """
  Splash logo image to OLED from binary array.
  """
  icon = None

  if DISPLAY_SPLASH_ICON == "v":
    icon = splashicon.SplashIcon.logo_v()
  elif DISPLAY_SPLASH_ICON == "h":
    icon = splashicon.SplashIcon.logo_h()
  else:
    raise ValueError("The value of 'DISPLAY_SPLASH_ICON' can specify 'v' or 'h' only.")

  dx = (oled.width  - icon.logo_width)  // 2
  dy = (oled.height - icon.logo_height) // 2

  oled.fill(0)
  oled.show()

  for y, fila in enumerate(icon.logo_icon):
    for x, c in enumerate(fila):
      oled.pixel(x + dx, y + dy, c)
  oled.show()


# ==================== Entry Point ====================

if __name__ == "__main__":
  """
  Entry point at functional execution.
  """
  try:
    # load configuration values
    load_settings(CONFIG_FILE)

    # gobal devices initialization (I2C OLED SSD1306)
    i2c = I2C(scl=Pin(OLED_PIN_SCL), sda=Pin(OLED_PIN_SDA))
    oled = ssd1306.SSD1306_I2C(width=OLED_WIDTH, height=OLED_HEIGHT, i2c=i2c)
    detect_i2c_device(i2c, "SSD1306", OLED_ADDRESS)

    # gobal devices initialization (I2C BME280)
    i2c = I2C(scl=Pin(BME280_PIN_SCL), sda=Pin(BME280_PIN_SDA))
    bme = bme280.BME280(i2c=i2c)
    detect_i2c_device(i2c, "BME280", BME280_ADDRESS)

    # gobal devices initialization (1-Wire DS18B20)
    ow = onewire.OneWire(pin=Pin(DS18_PIN_DQ))
    ds18 = ds18.DS18(ow=ow, reading_wait=DS18_READING_WAIT)
    detect_ow_device(ds18, "DS18X20", DS18_ADDRESS)

    # global devices initialization (Capacitive Sensor)
    tp = TouchPad(Pin(WATER_LEVEL_PIN))
    wlevel = waterlevel.WaterLevelSensor(tp, WATER_LEVEL_SENSE_MAX, WATER_LEVEL_SENSE_MIN)

    # call main routine
    main()

  except Exception as e:
    print("\nAn error has occured !")
    print("-" * 20)
    sys.print_exception(e)
    print("-" * 20)
