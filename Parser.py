# fragment start *
"""
A recursive descent parser for Baresbone language
"""
from Lexer import Lexer
from Symbols import *
from Node import Node
from Token import Token
from Character import Character

class ParserError(Exception):
    pass


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
#                       Error
# -------------------------------------------------------------------
def error(msg):
    token.abort(msg)


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
        error("Expecting to find "
              + dq(arg_token_type)
              + " but found "
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

    # Parse for statements until end of file
    while not found(EOF):
        statement(node)

    consume(EOF)
    ast = node


# --------------------------------------------------------
#                   statement
# --------------------------------------------------------
@track
def statement(node):
    if found("clear"):
        clear_statement(node)
    elif found("incr"):
        incr_statement(node)
    elif found("decr"):
        decr_statement(node)
    elif found("while"):
        while_statement(node)
    else:
        # Unexpected
        error("Didn't reconize " + token.show())

# --------------------------------------------------------
#                   clear statement
# --------------------------------------------------------
@track
def clear_statement(node):
    """
    Syntax = clear + variable + ;
    """

    statement_node = Node(token)

    consume("clear")
    node.add_node(statement_node)

    # Parse next variable
    variable(statement_node)

    consume(";")


# --------------------------------------------------------
#                   increase statement
# --------------------------------------------------------
@track
def incr_statement(node):
    """
        Syntax = incr + variable + ;
    """

    statement_node = Node(token)

    consume("incr")
    node.add_node(statement_node)

    #Parse next variable
    variable(statement_node)

    consume(";")

# --------------------------------------------------------
#                   decrease statement
# --------------------------------------------------------
@track
def decr_statement(node):
    """
        Syntax = decr + variable + ;
    """
    statement_node = Node(token)
    consume("decr")
    node.add_node(statement_node)

    # Parse next variable
    variable(statement_node)

    consume(";")

# --------------------------------------------------------
#                   while loop statement
# --------------------------------------------------------
@track
def while_statement(node):
    """
        Syntax = while + variable + not + 0 + do + ;
        + list of statement
        + end + ;
    """

    statement_node = Node(token)
    consume("while")
    node.add_node(statement_node)

    # Parse next variable
    variable(statement_node)

    # Consume keywords
    consume("not")
    consume("Zero")
    consume("do")
    consume(";")

    # Until find end consume all statement
    while not found("end"):

        # If there is no end keyword then raise an error
        if found(EOF):
            error("Expecting \"end\"")

        # Add to children
        statement(statement_node)

    # Consume end keyword
    consume("end")
    consume(";")

# --------------------------------------------------------
#                   variable
# --------------------------------------------------------
def variable(node):

    # Check if first character is degits
    if token.cargo[0] not in string.ascii_letters:
        error("Variable can not start with degits")


    token.type = "variable"
    node.add(token)
    get_token()

# Optimize the code
def optimize(node,variable=None):
    i = 0
    count = 0
    optmz=False
    decr_node = None

    # Recurse until find the final while loop
    # The most inside while loop
    while i < len(node.children):
        if node.children[i].token.type == "while":

            # Optimize
            if optimize(node.children[i],node.children[i].children[0].token.cargo):

                # Take all the children nodes outside of the loop
                for t in range(1,len(node.children[i].children)):
                    node.children.insert(i+t,node.children[i].children[t])

                # Then delete it
                del node.children[i]
            else:
                # Search for next child
                i += 1
        else:
            i += 1

    # Not the root tree
    if variable is not None:

        # Check if there is only one decr statement in the loop that decrease the variable
        # by 1 every loop
        for j in node.children:
            if j.token.type == "variable":
                continue

            # If there are clear and while loop
            # Can not optimize

            if j.token.type == "clear" or j.token.type=="while":
                optmz = False
                break

            # Get the decr node
            if j.children[0].token.cargo==variable:
                if j.token.type == "decr":
                    if count ==0:
                        optmz=True
                        count+=1
                        decr_node=j
                    else:
                        optmz=False
                else:
                    optmz = False
                    break

        # This node can be optimized
        if optmz:

            # Add the variable to decr and incr node
            for j in node.children:
                if j.token.type != "clear":
                    j.children.append(decr_node.children[0])
                j.level -= 1
                j.children[0].level-=1

            # Add clear node to clear the variable of
            # while loop
            temp_char = Character("a",1,1,None,None)
            clear_variable_token = Token(temp_char)
            clear_variable_token.type = "clear"
            clear_variable_token.cargo = "clear"
            clear_variable = Node(clear_variable_token)
            clear_variable.children.append(decr_node.children[0])
            clear_variable.level=decr_node.level
            decr_node.children[0].level+=1
            node.children.append(clear_variable)
            node.children.remove(decr_node)
            return True
        else:
            return False