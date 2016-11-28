# fragment start *
# fragment start 1
from Scanner import *


class LexerError(Exception):
    pass


# -----------------------------------------------------------------------
#
#               Token
#
# -----------------------------------------------------------------------
class Token:
    """
    A Token object is the kind of thing that the Lexer returns.
    It holds:
    - the text of the token (self.cargo)
    - the type of token that it is
    - the line number and column index where the token starts
    """

    # -------------------------------------------------------------------
    #
    # -------------------------------------------------------------------
    def __init__(self, start_char):
        """
        The constructor of the Token class
        """
        self.cargo = start_char.char

        # ----------------------------------------------------------
        # The token picks up information
        # about its location in the sourceText
        # ----------------------------------------------------------
        self.sourceText = start_char.source_text
        self.lineIndex = start_char.line_index
        self.colIndex = start_char.column_index

        # ----------------------------------------------------------
        # We won't know what kind of token we have until we have
        # finished processing all of the characters in the token.
        # So when we start, the token.type is None (aka null).
        # ----------------------------------------------------------
        self.type = None

    # -------------------------------------------------------------------
    #  return a displayable string representation of the token
    # -------------------------------------------------------------------
    def show(self, show_line_numbers=False, **kwargs):
        """
        align=True shows token type left justified with dot leaders.
        Specify align=False to turn this feature OFF.
        """
        align = kwargs.get("align", True)
        if align:
            token_type_len = 12
            space = " "
        else:
            token_type_len = 0
            space = ""

        if show_line_numbers:
            s = str(self.lineIndex).rjust(6) + str(self.colIndex).rjust(4) + "  "
        else:
            s = ""

        if self.type == self.cargo:
            s = s + "Symbol".ljust(token_type_len, ".") + ":" + space + self.type
        elif self.type == "Whitespace":
            s = s + "Whitespace".ljust(token_type_len, ".") + ":" + space + repr(self.cargo)
        else:
            s = s + self.type.ljust(token_type_len, ".") + ":" + space + self.cargo
        return s

    guts = property(show)

    # fragment stop  1


    # fragment start 2
    # -------------------------------------------------------------------
    #
    # -------------------------------------------------------------------
    def abort(self, msg):
        lines = self.sourceText.split("\n")
        source_line = lines[self.lineIndex]
        raise LexerError("\nIn line " + str(self.lineIndex + 1)
                         + " near column " + str(self.colIndex + 1) + ":\n\n"
                         + source_line.replace("\t", " ") + "\n"
                         + " " * self.colIndex
                         + "^\n\n"
                         + msg)

# fragment stop 2
