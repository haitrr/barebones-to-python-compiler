ENDMARK = "\0"
from Character import *
class Character(object):
    def __init__(self, char, line_index, column_index, source_index, source_text):
        self.char = char
        self.source_index = source_index
        self.column_index = column_index
        self.line_index = line_index
        self.source_text = source_text

    def __str__(self):
        result = self.char
        if result == " ":
            result = "    space"
        elif result == "\n":
            result = "    new_line"
        elif result == "\t":
            result = "    tab"
        elif result == ENDMARK:
            result = "    end_of_file"
        return str(self.line_index).rjust(6) + str(self.column_index).rjust(4) + "    " + result