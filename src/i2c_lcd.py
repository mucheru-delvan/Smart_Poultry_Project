from lcd_api import LcdApi
import time

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.i2c.writeto(self.i2c_addr, bytearray([0]))
        time.sleep_ms(20)
        self.hal_write_init_nibble(0x30)
        self.hal_write_init_nibble(0x30)
        self.hal_write_init_nibble(0x30)
        self.hal_write_init_nibble(0x20)
        super().__init__(num_lines, num_columns)
        self.hal_write_command(0x28)
        self.hal_write_command(0x0C)
        self.hal_write_command(0x06)
        self.clear()

    def hal_write_init_nibble(self, nibble):
        byte = (nibble & 0xF0) | 0x08
        self.i2c.writeto(self.i2c_addr, bytearray([byte | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))

    def hal_write_command(self, cmd):
        self.hal_write_upper_nibble(cmd & 0xF0)
        self.hal_write_upper_nibble((cmd << 4) & 0xF0)

    def hal_write_upper_nibble(self, nibble):
        byte = nibble | 0x08
        self.i2c.writeto(self.i2c_addr, bytearray([byte | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))

    def putchar(self, char):
        char_bin = ord(char)
        self.hal_write_upper_nibble_data(char_bin & 0xF0)
        self.hal_write_upper_nibble_data((char_bin << 4) & 0xF0)

    def hal_write_upper_nibble_data(self, nibble):
        byte = nibble | 0x08 | 0x01
        self.i2c.writeto(self.i2c_addr, bytearray([byte | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))

    def clear(self):
        self.hal_write_command(0x01)
        time.sleep_ms(2)