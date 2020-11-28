# This is Hydroponic project in MicroPython with the ESP32 board.
# Using devices are SSD1306 OLED, DS18B20, BME280.


from micropython import const
from machine import I2C, Pin
import sys, time, machine, ubinascii, _thread
import ssd1306, bme280, ds18, onewire
import splashicon


#--- one-time execution settinss ---#
DISPLAY_SPLASH_ICON = "v"
# DISPLAY_SPLASH_ICON = "h"
DISPLAY_WAITING_SPLASH   = const(5000)  # 5.0 sec
DISPLAY_WAITING_PLATFORM = const(2000)  # 2.0 sec

#--- recursive execution settings ---#
TIMER_PERIOD_DISP = const(9000)         # 9.0 sec

#--- device settinss ---#
# OLED settings
OLED_PIN_SCL = const(4)                 # GPIO 4
OLED_PIN_SDA = const(5)                 # GPIO 5
OLED_ADDRESS = 0x3c
OLED_WIDTH   = const(128)
OLED_HEIGHT  = const(64)

# BME280 settings
BME280_PIN_SCL = const(26)              # GPIO 26
BME280_PIN_SDA = const(25)              # GPIO 25
BME280_ADDRESS = 0x76

# DS18B20 settinsgs
DS18_PIN_DQ  = const(16)                # GPIO 16
DS18_ADDRESS = [0x28, 0x82, 0x7d, 0x79, 0x97, 0x09, 0x03, 0x22]


# ==================== Main Functions ====================

def main():
  """
  main function
  """
  splash_screen()
  time.sleep_ms(DISPLAY_WAITING_SPLASH)

  check_platform()
  time.sleep_ms(DISPLAY_WAITING_PLATFORM)

  # thread start
  _thread.start_new_thread(display_callback, (1, TIMER_PERIOD_DISP - ds18.reading_wait))


# ==================== Callback Functions ====================

def display_callback(id, delay_ms):
  """
  callback function: read values from BME280 and DS18x20
  after that, bellow showing values to OLED
  """
  while True:
    oled.fill(0)
    oled.text("[air]", 0, 0)                            # [atmospheric]
    oled.text("T=" + bme.values[0],  0, 10)             # - temperature
    oled.text("H=" + bme.values[2], 64, 10)             # - humidity
    oled.text("P=" + bme.values[1],  0, 20)             # - pressure
    oled.text("[water]", 0, 30)                         # [water]
    oled.text("W=" + ds18.values[0], 0, 40)             # - temperature
    oled.show()

    for cnt in range(3600):         # max waiting 1hour = 60min = 3600sec
      time.sleep_ms(1000)

      oled.text(".", 8*cnt, 55)
      oled.show()

      waiting = (cnt + 1) * 1000
      if delay_ms <= waiting:       # waiting limit has exceeded delay_ms
        break


# ==================== I2C device Functions ====================

def detect_i2c_device(i2c, device, address):
  """
  I2C device scan and it was found or else, show message
  """
  print("Detecting {} ...".format(device))
  i2cDevs = i2c.scan()
  for idx, dev in enumerate(i2cDevs):
    if dev == address:
      print("  Found {} device: ['{}']".format(device, hex(dev)))
      break
  else:
    print("  NOT Found I2C device, check wiring of device !")


# ==================== SPI device Functions ====================

def detect_ow_device(ow, device, address):
  """
  1-Wire device scan and it was found, show message
  """
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
  check running platform, and show result to OLED
  """
  platform = sys.platform
  chip_id = str(ubinascii.hexlify(machine.unique_id()))[2:14]
  pclk = machine.freq() // (1000 ** 2)

  supported = " Supported"
  if platform != "esp32":
    raise ValueError("Platform is esp32 board required.")
  else:
    pass

  oled.fill(0)
  oled.show()

  oled.text(platform, 0, 0)
  oled.text(supported, 0, 10)
  oled.text("UID {}".format(chip_id), 0, 20)
  oled.text("PCLK {}MHz".format(pclk) , 0, 30)
  oled.show()

  print("----------")
  print("PLATFORM : {}".format(platform))
  print("CHIP UID : {}".format(chip_id))
  print("PERIPHERAL CLOCK : {} MHz".format(pclk))
  print("----------")


# ==================== OLED Functions ====================

def splash_screen():
  """
  splash logo image to OLED from binary array
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

if __name__ == '__main__':
  """
  entry point at functional execution
  """
  try:
    # gobal devices initialization (I2C OLED SSD1306)
    i2c = I2C(scl=Pin(OLED_PIN_SCL), sda=Pin(OLED_PIN_SDA))
    oled = ssd1306.SSD1306_I2C(width=OLED_WIDTH, height=OLED_HEIGHT, i2c=i2c)
    detect_i2c_device(i2c, "SSD1306", OLED_ADDRESS)

    # gobal devices initialization (I2C BME280)
    i2c = I2C(scl=Pin(BME280_PIN_SCL), sda=Pin(BME280_PIN_SDA))
    bme = bme280.BME280(i2c=i2c)
    detect_i2c_device(i2c, "BME280", BME280_ADDRESS)

    # gobal devices initialization (1-Wire DS18B20)
    ow = onewire.OneWire(Pin(DS18_PIN_DQ))
    ds18 = ds18.DS18(ow)
    detect_ow_device(ds18, "DS18X20", DS18_ADDRESS)

    # call main routine
    main()

  except Exception as e:
    print(e)
