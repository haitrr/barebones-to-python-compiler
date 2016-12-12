input_variables = []
all_variable = []

import Parser

# -------------------------------------------------------------------
#                       Get all the variable and input variable
# -------------------------------------------------------------------
def get_variable(node):

    # If meet a variable return it
    if node.token is not None and node.token.type == "variable":
        return node.token.cargo

    # If the node have no children nodes return nothing
    elif node.children == []:
        return None
    else:

        # Get variable from children nodes of the node
        for i in node.children:
            temp = get_variable(i)
            if temp is not None:

                # If the variable is not declare with clear statement
                # it is the variable that need input
                if node.token.type != "clear":
                    if temp not in all_variable:
                        input_variables.append(temp)

                # Else
                if temp not in all_variable:
                    all_variable.append(temp)


# -------------------------------------------------------------------
#                       Subtract function for barebones
# -------------------------------------------------------------------
def define_subtract():
    subtract = "def subtract(variable,num=1):\n" \
               "    variable = variable - num\n" \
               "    if variable<0 :\n" \
               "        variable=0\n" \
               "    return variable\n"
    return subtract


# -------------------------------------------------------------------
#                       Compile
# -------------------------------------------------------------------
def compile(ast, level=-1):

    # Clear the variable from last compile
    input_variables.clear()
    all_variable.clear()
    result = ""

    # Compile each node of the tree
    if ast.token is not None:
        if ast.token.type == "incr":
            result += level * "    " + incr(ast) + "\n"
        elif ast.token.type == "decr":
            result += level * "    " + decr(ast) + "\n"
        elif ast.token.type == "clear":
            result += level * "    " + clear(ast) + "\n"
        elif ast.token.type == "while":
            result += level * "    " + while_loop(ast) + "\n"
        else:
            pass

    for i in ast.children:
        # Increase the level by 1
        # and compile all children nodes
        result += compile(i, level + 1)

    # Return result
    return result


# -------------------------------------------------------------------
#                       INCR
# -------------------------------------------------------------------
def incr(node):
    variable = node.children[0].token.cargo

    # Checking for optimize
    if len(node.children) > 1:
        result = variable + " += " + node.children[1].token.cargo
    else:
        result = variable + " += 1"

    return result


# -------------------------------------------------------------------
#                       DECR
# -------------------------------------------------------------------
def decr(node):
    variable = node.children[0].token.cargo

    # Checking for optimize
    if len(node.children) > 1:
        result = variable + " = " + "subtract(" + variable + ", " + node.children[1].token.cargo + ")"
    else:
        result = variable + " = " + "subtract(" + variable + ")"

    return result


# -------------------------------------------------------------------
#                       CLEAR
# -------------------------------------------------------------------
def clear(node):

    variable = node.children[0].token.cargo
    result = variable + " = 0"

    return result


# -------------------------------------------------------------------
#                       WHILE
# -------------------------------------------------------------------
def while_loop(node):

    variable = node.children[0].token.cargo
    result = "while " + variable + " != 0:"

    return result


# -------------------------------------------------------------------
#                  Generate require output code
# -------------------------------------------------------------------
def require_input():

    input_code = ""

    # Generate input code for all variables in input_variables
    for i in input_variables:
        input_code += "print(\"Please input " + i + " :\") \n"
        input_code += i + " =int(input())" + "\n"

    return input_code


# -------------------------------------------------------------------
#            Print all variables after finish running
# -------------------------------------------------------------------
def output_variables():

    output_code = ""

    # Output all variable the declared in the code
    for i in all_variable:
        output_code += "print(\"Value of  " + i + " : \" + str(" + i + ")) \n"

    return output_code


# -------------------------------------------------------------------
#            Safely pre-declare all variable
# -------------------------------------------------------------------

def pre_declare_variables():
    code = ""

    # Pre declare all the variable in the code
    # to avoid unwanted error cause by while loops
    for i in all_variable:
        code += i + " = 0\n"

    return code

