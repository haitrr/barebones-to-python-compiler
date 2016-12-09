from Token import *
from Symbols import *


class LexerError(Exception): pass


class Lexer:
    # enclose string s in double quotes
    def dq(self, s):
        return '"%s"' % s

    # -------------------------------------------------------------------
    #
    # -------------------------------------------------------------------
    def __init__(self, source_text):
        # initialize the scanner with the sourceText
        self.scanner = Scanner(source_text)
        self.c1 = ''
        self.c2 = ''
        self.character = ''

        # use the scanner to read the first self.character from the sourceText
        self.get_char()

    # -------------------------------------------------------------------
    #
    # -------------------------------------------------------------------
    def get(self):
        """
        Return the next token
        """

        # --------------------------------------------------------------------------------
        # Skip any whitespace or comment at start
        # --------------------------------------------------------------------------------
        while self.c1 in WHITESPACE_CHARS or self.c2 == "/*":

            # process whitespace
            while self.c1 in WHITESPACE_CHARS:
                token = Token(self.character)
                token.type = WHITESPACE
                self.get_char()

                while self.c1 in WHITESPACE_CHARS:
                    token.cargo += self.c1
                    self.get_char()

                    # return token  # only if we want the lexer to return whitespace

            # process comments
            while self.c2 == "/*":
                # we found comment start
                token = Token(self.character)
                token.type = COMMENT
                token.cargo = self.c2

                self.get_char()  # read past the first  self.character of a 2-self.character token
                self.get_char()  # read past the second self.character of a 2-self.character token

                while not (self.c2 == "*/"):
                    if self.c1 == ENDMARK:
                        token.abort("Found end of file before end of comment")
                    token.cargo += self.c1
                    self.get_char()

                token.cargo += self.c2  # append the */ to the token cargo

                self.get_char()  # read past the first  self.character of a 2-self.character token
                self.get_char()  # read past the second self.character of a 2-self.character token

                # return token  # only if we want the lexer to return comments
        # --------------------------------------------------------------------------------
        # read past and ignore any whitespace characters or any comments -- END
        # --------------------------------------------------------------------------------

        # Create a new token.  The token will pick up
        # its line and column information from the self.character.
        token = Token(self.character)

        # End of file
        if self.c1 == ENDMARK:
            token.type = EOF
            return token

        # clear,incr,decr,while,do,end
        if self.c1 in IDENTIFIER_STARTCHARS:
            token.type = IDENTIFIER
            self.get_char()

            while self.c1 in IDENTIFIER_CHARS:
                token.cargo += self.c1
                self.get_char()

            if token.cargo in Keywords:
                token.type = token.cargo
            return token

        # 0
        if self.c1 == ZERO_CHAR:
            token.type = ZERO
            self.get_char()
            token.cargo="0"
            return token

        # ;
        if self.c1 in OneCharacterSymbols:

            # for symbols, the token type is same as the cargo
            token.type = token.cargo

            # read past the symbol
            self.get_char()
            return token

        # else.... Encountered something that we don't recognize.
        token.abort("Found a character or symbol that I do not recognize: " + self.dq(self.c1))

    # -------------------------------------------------------------------
    #
    # -------------------------------------------------------------------
    def get_char(self):
        """
        get the next self.character
        """
        self.character = self.scanner.get()
        self.c1 = self.character.char
        # ---------------------------------------------------------------
        # Every time we get a self.character from the scanner, we also
        # lookahead to the next self.character and save the results in c2.
        # This makes it easy to lookahead 2 characters.
        # ---------------------------------------------------------------
        self.c2 = self.c1 + self.scanner.lookahead(1)

