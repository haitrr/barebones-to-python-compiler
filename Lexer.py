from Scanner import *
from Symbol import *
from Token import *


# enclose string s in double quotes
def dq(s): return '"%s"' % s


class Lexer:
    def __init__(self, source_text):
        self.scanner = Scanner(source_text)
        self.c1 = ""
        self.c2 = ""
        self.character = None
        self.get_char()
    def get(self):
        while self.c1 in WHITESPACE_CHARS or self.c2 == "/*":
            while self.c1 in WHITESPACE_CHARS:
                token = Token(self.character)
                token.type = WHITESPACE
                self.get_char()
            while self.c2 == "/*":
                token = Token(self.character)
                token.type = COMMENT
                token.char = self.c2
                self.get_char()
                self.get_char()
                while not (self.c2 == "*/"):
                    if self.c1 == ENDMARK:
                        token.abort("Found end of file before end of comment")
                    token.char += self.c1
                    self.get_char()
                token.char += self.c2;
                self.get_char()
                self.get_char()
        token = Token(self.character)
        if self.c1 == ENDMARK:
            token.type = EOF
            return token
        if self.c1 in IDENTIFIER_STARTCHARS:
            token.type = IDENTIFIER
            self.get_char()
            while self.c1 in IDENTIFIER_CHARS:
                token.char += self.c1
                self.get_char()
            if token.char in keywords:
                token.type = token.char
            return token
        if self.c1 in NUMBER_STARTCHARS:
            token.type = NUMBER
            self.get_char()
            while self.c1 in NUMBER_CHARS:
                token.char += self.c1
                self.get_char()
            return token
        if self.c1 in STRING_STARTCHARS:
            quote_char = self.c1

            self.get_char()

            while self.c1 != quote_char:
                if self.c1 == ENDMARK:
                    token.abort("Found end of file before end of string literal")

                token.char += self.c1  # append quoted character to text
                self.get_char()

            token.char += self.c1  # append close quote to text
            self.get_char()
            token.type = STRING
            return token
        if self.c2 in two_character_symbol:
            token.char = self.c2
            token.type = token.char  # for symbols, the token type is same as the cargo
            self.get_char()  # read past the first  character of a 2-character token
            self.get_char()  # read past the second character of a 2-character token
            return token
        if self.c1 in one_charater_symbol:
            token.type = token.char  # for symbols, the token type is same as the cargo
            self.get_char()  # read past the symbol
            return token
        token.abort("I found a character or symbol that I do not recognize: " + dq(self.c1))

    def get_char(self):
        self.character = self.scanner.get()
        self.c1 = self.character.char
        self.c2 = self.c1 + self.scanner.look_ahead()


if __name__ == '__main__':
    f = open("source_text.txt", "r")
    print("Here are the tokens returned by the lexer:")
    lexer = Lexer(f.read())
    while True:
        token = lexer.get()
        print(token.show(True))
        if token.type == EOF:
            break
    f.close()
