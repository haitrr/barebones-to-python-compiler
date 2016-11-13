ASSIGNMENT = ":="
BEGIN = "begin"
CALL = "call"
COMMA = ","
CONST = "const"
DO = "do"
END = "end"
EQ = "=="
GE = ">="
GT = ">"
IF = "if"
LE = "<="
LPAREN = "("
LT = "<"
MINUS = "-"
MULTIPLY = "*"
NE = "!="
ODD = "odd"
PERIOD = "."
PLUS = "+"
PROC = "proc"
RPAREN = ")"
SEMICOLON = ";"
SLASH = "/"
THEN = "then"
VAR = "var"
WHILE = "while"

IDENTIFIER = "IDENTIFIER"
NUMBER = "NUMBER"


class ParserException(Exception):
    pass


class Parser():
    def __init__(self):
        self.token = ""

    def error(self, msg):
        quoted_token = '"%s"' % self.token
        msg = msg + " while processing token " + quoted_token
        raise ParserException("\n\n" + msg)

    def found(self, arg_token):
        if (self.token == arg_token):
            self.get_token()
            return True
        return False

    def expect(self, arg_token):
        if self.found(self.arg_token):
            return  # no problem
        else:
            quoted_token = '"%s"' % arg_token
            self.error("I was self.expecting to find token "
                       + quoted_token
                       + "\n  but I self.found something else")

    def factor(self):
        """
        factor = IDENTIFIER | NUMBER | "(" expression ")"
        .
        """
        if self.found(IDENTIFIER):
            pass
        elif self.found(NUMBER):
            pass
        elif self.found(LPAREN):
            self.expression()
            self.expect(RPAREN)
        else:
            self.error("factor: syntax self.error")
            self.get_token()

    def term(self):
        """
        term = factor {("*"|"/") factor}
        .
        """
        self.factor()
        while self.found(MULTIPLY) or self.found(SLASH):
            self.factor()

    def expression(self):
        """
        expression = ["+"|"-"] term {("+"|"-") term}
        .
        """
        if self.found(PLUS) or self.found(MINUS):
            pass
        self.term()
        while self.found(PLUS) or self.found(MINUS):
            self.term()

    def condition(self):
        """
        condition =
            "odd" expression
            | expression ("="|"#"|"<"|"<="|">"|">=") expression
        .
        """
        if self.found(ODD):
            self.expression()
        else:
            self.expression()
            if (self.found(EQ) or self.found(NE) or self.found(LT)
                or self.found(LE) or self.found(GT) or self.found(GE)):
                self.expression()
            else:
                self.error("condition: self.found invalid operator")
                self.get_token()

    def statement(self):
        """
        statement =
            [IDENTIFIER ":=" expression
            | "call" IDENTIFIER
            | "begin" statement {";" statement} "end"
            | "if" condition "then" statement
            | "while" condition "do" statement
            ]
        .
        """
        if self.found(IDENTIFIER):
            self.expect(ASSIGNMENT)
            self.expression()

        elif self.found(CALL):
            self.expect(IDENTIFIER)

        elif self.found(BEGIN):
            self.statement()
            while self.found(SEMICOLON):
                self.statement()
            self.expect(END)

        elif self.found(IF):
            self.condition()
            self.expect(THEN)
            self.statement()

        elif self.found(WHILE):
            self.condition()
            self.expect(DO)
            self.statement()

    def block(self):
        """
        block =
            ["const" IDENTIFIER "=" NUMBER {"," IDENTIFIER "=" NUMBER} ";"]
            ["var" IDENTIFIER {"," IDENTIFIER} ";"]
            {"procedure" IDENTIFIER ";" block ";"} statement
        .
        """
        if self.found(CONST):
            self.expect(IDENTIFIER)
            self.expect(EQ)
            self.expect(NUMBER)

            while self.found(COMMA):
                self.expect(IDENTIFIER)
                self.expect(EQ)
                self.expect(NUMBER)
            self.expect(SEMICOLON)

        if self.found(VAR):
            self.expect(IDENTIFIER)
            while self.found(COMMA):
                self.expect(IDENTIFIER)
            self.expect(SEMICOLON)

        while self.found(PROC):
            self.expect(IDENTIFIER)
            self.expect(SEMICOLON)
            self.block()
            self.expect(SEMICOLON)

        self.statement()

    def getToken(self):
        if verbose:
            if self.token:
                # print the current token, before we get the next one
                # print (" "*40 ) + token.show()
                print(("  " * self.indent) + "   (" + self.token.show(align=False) + ")")
        self.token = self.lexer.get()

    def program(self):
        """
        program = block "."
        .
        """
        self.get_token()
        self.block()
        self.expect(PERIOD)
