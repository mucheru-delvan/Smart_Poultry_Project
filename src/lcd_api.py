import time

class LcdApi:
    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
    def putstr(self, string):
        for char in string: self.putchar(char)
    def putchar(self, char): pass
    def clear(self): pass
    def custom_char(self, location, charmap): pass
    def hal_write_command(self, cmd): pass
    def hal_write_data(self, data): pass