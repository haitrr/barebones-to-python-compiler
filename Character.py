ENDMARK = "\0"


# -----------------------------------------------------------------------
#
#               Character
#
# -----------------------------------------------------------------------
class Character:
    # -------------------------------------------------------------------
    #               Constructor
    # -------------------------------------------------------------------
    def __init__(self, char, line_index, column_index, source_index, source_text):
        self.char = char
        self.source_index = source_index
        self.line_index = line_index
        self.column_index = column_index
        self.source_text = source_text

    # -------------------------------------------------------------------
    # return a displayable string representation of the Character object
    # -------------------------------------------------------------------
    def __str__(self):
        cargo = self.char
        if cargo == " ":
            cargo = "   space"
        elif cargo == "\n":
            cargo = "   newline"
        elif cargo == "\t":
            cargo = "   tab"
        elif cargo == ENDMARK:
            cargo = "   eof"

        return (
            str(self.line_index).rjust(6)
            + str(self.column_index).rjust(4)
            + "  "
            + cargo
        )
