from Token import *
from Symbols import *


class LexerError(Exception): pass


class Lexer:
    # enclose string s in double quotes
    def dq(self, s):
        return '"%s"' % s

    # fragment start snippet1
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
        Construct and return the next token in the source text.
        """

        # --------------------------------------------------------------------------------
        # read past and ignore any whitespace characters or any comments -- START
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

        if self.c1 == ENDMARK:
            token.type = EOF
            return token

        if self.c1 in IDENTIFIER_STARTCHARS:
            token.type = IDENTIFIER
            self.get_char()

            while self.c1 in IDENTIFIER_CHARS:
                token.cargo += self.c1
                self.get_char()

            if token.cargo in Keywords:
                token.type = token.cargo
            return token

        if self.c1 in NUMBER_STARTCHARS:
            token.type = NUMBER
            self.get_char()

            while self.c1 in NUMBER_CHARS:
                token.cargo += self.c1
                self.get_char()
            return token

        # fragment start getstring
        if self.c1 in STRING_STARTCHARS:
            # remember the quoteChar (single or double quote)
            # so we can look for the same self.character to terminate the quote.
            quoteChar = self.c1

            self.get_char()

            while self.c1 != quoteChar:
                if self.c1 == ENDMARK:
                    token.abort("Found end of file before end of string literal")

                token.cargo += self.c1  # append quoted self.character to text
                self.get_char()

            token.cargo += self.c1  # append close quote to text
            self.get_char()
            token.type = STRING
            return token
        # fragment stop getstring


        # fragment start getsymbols
        if self.c2 in TwoCharacterSymbols:
            token.cargo = self.c2
            token.type = token.cargo  # for symbols, the token type is same as the cargo
            self.get_char()  # read past the first  self.character of a 2-self.character token
            self.get_char()  # read past the second self.character of a 2-self.character token
            return token

        if self.c1 in OneCharacterSymbols:
            token.type = token.cargo  # for symbols, the token type is same as the cargo
            self.get_char()  # read past the symbol
            return token
        # fragment stop getsymbols

        # else.... We have encountered something that we don't recognize.
        token.abort("Found a character or symbol that I do not recognize: " + self.dq(self.c1))

    # fragment stop snippet1

    # fragment start getchar1
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

        # fragment stop getchar1
