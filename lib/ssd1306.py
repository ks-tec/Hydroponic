# MicroPython SSD1306 OLED driver, I2C and SPI interfaces


from micropython import const
import framebuf


# SSD1306 register definitions
SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xa4)
SET_NORM_INV        = const(0xa6)
SET_DISP            = const(0xae)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xa0)
SET_MUX_RATIO       = const(0xa8)
SET_COM_OUT_DIR     = const(0xc0)
SET_DISP_OFFSET     = const(0xd3)
SET_COM_PIN_CFG     = const(0xda)
SET_DISP_CLK_DIV    = const(0xd5)
SET_PRECHARGE       = const(0xd9)
SET_VCOM_DESEL      = const(0xdb)
SET_CHARGE_PUMP     = const(0x8d)


class SSD1306:
    """
    This class is base class for using SSD1306 OLED.
    """

    def __init__(self, width, height, external_vcc):
        """
        Consstructor of SSD1306.

        Args:
            width : Screen width (unit is dot)
            height : Screen height (unit is dot)
            external_vcc : Boolean value is False when using external vcc, or else True using internal vcc
        """
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.framebuf = fb
        # Provide methods for accessing FrameBuffer graphics primitives. This is a
        # workround because inheritance from a native class is currently unsupported.
        # http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
        self.fill = fb.fill
        self.pixel = fb.pixel
        self.hline = fb.hline
        self.vline = fb.vline
        self.line = fb.line
        self.rect = fb.rect
        self.fill_rect = fb.fill_rect
        self.text = fb.text
        self.scroll = fb.scroll
        self.blit = fb.blit
        self.init_display()

    def init_display(self):
        """
        Initialize display.
        """
        for cmd in (
            SET_DISP | 0x00, # off
            # address setting
            SET_MEM_ADDR, 0x00, # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01, # column addr 127 mapped to SEG0
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08, # scan from COM[N] to COM0
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
            SET_VCOM_DESEL, 0x30, # 0.83*Vcc
            # display
            SET_CONTRAST, 0xff, # maximum
            SET_ENTIRE_ON, # output follows RAM contents
            SET_NORM_INV, # not inverted
            # charge pump
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01): # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        """
        Turn off the power of display.
        """
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        """
        Turn on the power of display.
        """
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        """
        Set contrast of display.
        """
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        """
        Invert of display.
        """
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        """
        Buffer data show to display.
        """
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)


class SSD1306_I2C(SSD1306):
    """
    This class is for using SSD1306 OLED with I2C interface.
    """

    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        """
        Constructor of SSD1306_I2C connected with I2C interface.

        Args:
            width : Screen width (unit is dot)
            height : Screen height (unit is dot)
            i2c : machine.I2C object
            addr : I2C address of SSD1306
            external_vcc : Boolean value is False when using external vcc, or else True using internal vcc
        """
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        """
        Command write to SSD1306.

        Args:
            cmd : Command to write
        """
        self.temp[0] = 0x80 # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        """
        Data write to SSD1306.

        Args:
            buf : Data to write
        """
        self.temp[0] = self.addr << 1
        self.temp[1] = 0x40 # Co=0, D/C#=1
        self.i2c.start()
        self.i2c.write(self.temp)
        self.i2c.write(buf)
        self.i2c.stop()


class SSD1306_SPI(SSD1306):
    """
    This class is for using SSD1306 OLED with SPI interface.
    """

    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        """
        Constructor of SSD1306_SPI connected with SPI interface.

        Args:
            width : Screen width (unit is dot)
            height : Screen height (unit is dot)
            spi : machine.SPI object
            dc : machine.Pin object of DC pin
            res : machone.Pin object of RES pin
            cs : machine.Pin object of CS pin
            external_vcc : Boolean value is False when using external vcc, or else True using internal vcc
        """
        self.rate = 10 * 1024 * 1024
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        import time
        self.res(1)
        time.sleep_ms(1)
        self.res(0)
        time.sleep_ms(10)
        self.res(1)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        """
        Command write to SSD1306.

        Args:
            cmd : Command to write
        """
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        """
        Data write to SSD1306.

        Args:
            buf : Data to write
        """
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)
