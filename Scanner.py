# fragment start *
# fragment start 1
from Character import *

"""
A Scanner object reads through the sourceText
and returns one character at a time.
"""


# -------------------------------------------------------------------
#
# -------------------------------------------------------------------
class Scanner:
    def __init__(self, source_text_arg):
        self.source_text = source_text_arg
        self.last_index = len(self.source_text) - 1
        self.source_index = -1
        self.line_index = 0
        self.column_index = -1

    # -------------------------------------------------------------------
    #
    # -------------------------------------------------------------------
    def get(self):
        """
        Return the next character in sourceText.
        """

        self.source_index += 1  # increment the index in sourceText

        # maintain the line count
        if self.source_index > 0:
            if self.source_text[self.source_index - 1] == "\n":
                # -------------------------------------------------------
                # The previous character in sourceText was a newline
                # character.  So... we're starting a new line.
                # Increment lineIndex and reset colIndex.
                # -------------------------------------------------------
                self.line_index += 1
                self.column_index = -1

        self.column_index += 1

        if self.source_index > self.last_index:
            # We've read past the end of sourceText.
            # Return the ENDMARK character.
            char = Character(ENDMARK, self.line_index, self.column_index, self.source_index, self.source_text)
        else:
            c = self.source_text[self.source_index]
            char = Character(c, self.line_index, self.column_index, self.source_index, self.source_text)

        return char

    # fragment stop  1


    # fragment start 2
    # -------------------------------------------------------------------
    #
    # -------------------------------------------------------------------
    def lookahead(self, offset=1):
        """
        Return a string (not a Character object) containing the character
        at position:
                sourceIndex + offset
        Note that we do NOT move our current position in the sourceText.
        That is,  we do NOT change the value of sourceIndex.
        """
        index = self.source_index + offset

        if index > self.last_index:
            # We've read past the end of sourceText.
            # Return the ENDMARK character.
            return ENDMARK
        else:
            return self.source_text[index]
