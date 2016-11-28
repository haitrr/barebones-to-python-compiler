# fragment start *
"""
A recursive descent parser for nxx1, 
as defined in nxx1ebnf.txt
"""
from Lexer import Lexer
from Symbols import *
from Node import Node


class ParserError(Exception): pass


def dq(s): return '"%s"' % s


token = None
verbose = False
indent = 0
numberOperator = ["+", "-", "/", "*"]


# -------------------------------------------------------------------
#
# -------------------------------------------------------------------
def get_token():
    global token
    if verbose:
        if token:
            # print the current token, before we get the next one
            # print (" "*40 ) + token.show()
            print(("  " * indent) + "   (" + token.show(align=False) + ")")
    token = lexer.get()


# -------------------------------------------------------------------
#    push and pop
# -------------------------------------------------------------------
def push(s):
    global indent
    indent += 1
    if verbose:
        print(("  " * indent) + " " + s)


def pop(s):
    global indent
    if verbose:
        # print(("  "*indent) + " " + s + ".end")
        pass
    indent -= 1


# -------------------------------------------------------------------
#  decorator track0
# -------------------------------------------------------------------
def track0(func):
    def newfunc():
        push(func.__name__)
        func()
        pop(func.__name__)

    return newfunc


# -------------------------------------------------------------------
#  decorator track
# -------------------------------------------------------------------
def track(func):
    def newfunc(node):
        push(func.__name__)
        func(node)
        pop(func.__name__)

    return newfunc


# -------------------------------------------------------------------
#
# -------------------------------------------------------------------
def error(msg):
    token.abort(msg)


# -------------------------------------------------------------------
#        foundOneOf
# -------------------------------------------------------------------
def found_one_of(arg_token_types):
    """
    argTokenTypes should be a list of argTokenType
    """
    for argTokenType in arg_token_types:
        # print "foundOneOf", argTokenType, token.type
        if token.type == argTokenType:
            return True
    return False


# -------------------------------------------------------------------
#        found
# -------------------------------------------------------------------
def found(arg_token_type):
    if token.type == arg_token_type:
        return True
    return False


# -------------------------------------------------------------------
#       consume
# -------------------------------------------------------------------
def consume(arg_token_type):
    """
    Consume a token of a given type and get the next token.
    If the current token is NOT of the expected type, then
    raise an error.
    """
    if token.type == arg_token_type:
        get_token()
    else:
        error("I was expecting to find "
              + dq(arg_token_type)
              + " but I found "
              + token.show(align=False)
              )


# -------------------------------------------------------------------
#    parse
# -------------------------------------------------------------------
def parse(source_text, **kwargs):
    global lexer, verbose
    verbose = kwargs.get("verbose", False)
    # create a Lexer object & pass it the sourceText
    lexer = Lexer(source_text)
    get_token()
    program()
    if verbose:
        print("~" * 80)
        print("Successful parse!")
        print("~" * 80)
    return ast


# --------------------------------------------------------
#                   program
# --------------------------------------------------------
@track0
def program():
    """
program = statement {statement} EOF.
    """
    global ast
    node = Node()

    statement(node)
    while not found(EOF):
        statement(node)

    consume(EOF)
    ast = node


# --------------------------------------------------------
#                   statement
# --------------------------------------------------------
@track
def statement(node):
    """
statement = printStatement | assignmentStatement .
assignmentStatement = variable "=" expression ";".
printStatement      = "print" expression ";".
    """
    if found("print"):
        print_statement(node)
    else:
        assignment_statement(node)


# --------------------------------------------------------
#                   expression
# --------------------------------------------------------
@track
def expression(node):
    """
expression = stringExpression | numberExpression.

/* "||" is the concatenation operator, as in PL/I */
stringExpression =  (stringLiteral | variable) {"||"            stringExpression}.
numberExpression =  (numberLiteral | variable) { numberOperator numberExpression}.
numberOperator = "+" | "-" | "/" | "*" .
    """

    if found(STRING):
        string_literal(node)
        while found("||"):
            get_token()
            string_expression(node)

    elif found(NUMBER):
        number_literal(node)
        while found_one_of(numberOperator):
            node.add(token)
            get_token()
            number_expression(node)
    else:
        node.add(token)
        consume(IDENTIFIER)

        if found("||"):
            while found("||"):
                get_token()
                string_expression(node)
        elif found_one_of(numberOperator):
            while found_one_of(numberOperator):
                node.add(token)
                get_token()
                number_expression(node)


# --------------------------------------------------------
#                   assignmentStatement
# --------------------------------------------------------
@track
def assignment_statement(node):
    """
assignmentStatement = variable "=" expression ";".
    """
    identifier_node = Node(token)
    consume(IDENTIFIER)

    operator_node = Node(token)
    consume("=")
    node.add_node(operator_node)

    operator_node.add_node(identifier_node)

    expression(operator_node)
    consume(";")


# --------------------------------------------------------
#                   printStatement
# --------------------------------------------------------
@track
def print_statement(node):
    """
printStatement      = "print" expression ";".
    """
    statement_node = Node(token)
    consume("print")

    node.add_node(statement_node)

    expression(statement_node)

    consume(";")


# --------------------------------------------------------
#                   stringExpression
# --------------------------------------------------------
@track
def string_expression(node):
    """
/* "||" is the concatenation operator, as in PL/I */
stringExpression =  (stringLiteral | variable) {"||" stringExpression}.
    """

    if found(STRING):
        node.add(token)
        get_token()

        while found("||"):
            get_token()
            string_expression(node)
    else:
        node.add(token)
        consume(IDENTIFIER)

    while found("||"):
        get_token()
        string_expression(node)


# --------------------------------------------------------
#                   numberExpression
# --------------------------------------------------------
@track
def number_expression(node):
    """
numberExpression =  (numberLiteral | variable) { numberOperator numberExpression}.
numberOperator = "+" | "-" | "/" | "*" .
    """
    if found(NUMBER):
        number_literal(node)
    else:
        node.add(token)
        consume(IDENTIFIER)

    while found_one_of(numberOperator):
        node.add(token)
        get_token()
        number_expression(node)


# --------------------------------------------------------
#                   stringLiteral
# --------------------------------------------------------
def string_literal(node):
    node.add(token)
    get_token()


# --------------------------------------------------------
#                   numberLiteral
# --------------------------------------------------------
def number_literal(node):
    node.add(token)
    get_token()
