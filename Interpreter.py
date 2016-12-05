input_variables = []
all_variable = []

def get_variable(node):
    if node.token is not None and node.token.type == "variable":
        return node.token.cargo
    elif node.children == []:
        return None
    else:
        for i in node.children:
            temp = get_variable(i)
            if temp is not None:
                if node.token.type != "clear":
                    if temp not in all_variable:
                        input_variables.append(temp)
                if temp not in all_variable:
                    all_variable.append(temp)

def define_subtract():
    subtract = "def subtract(i):\n    if i>0 :\n        i-=1\n    return i\n"
    return subtract

def interpreter(ast, level=-1):
    input_variables.clear()
    all_variable.clear()
    result = ""
    if ast.token is not None:
        if ast.token.type == "incr":
            result += level * "    " + incr(ast, level) + "\n"
        elif ast.token.type == "decr":
            result += level * "    " + decr(ast, level) + "\n"
        elif ast.token.type == "clear":
            result += level * "    " + clear(ast, level) + "\n"
        elif ast.token.type == "while":
            result += level * "    " + while_loop(ast, level) + "\n"
        elif ast.token.type == "do":
            pass
    for i in ast.children:
        result += interpreter(i, level + 1)
    return result


def do(node, level):
    return ""


def incr(node, level):
    variable = node.children[0].token.cargo
    result = variable + " += 1"
    return result


def decr(node, level):
    variable = node.children[0].token.cargo
    result = variable + " = "+"subtract("+ variable +")"
    return result


def clear(node, level):
    variable = node.children[0].token.cargo
    result = variable + " = 0"
    return result


def while_loop(node, level):
    variable = node.children[0].token.cargo
    result = "while " + variable + " != 0:"
    return result


def end(node, level):
    return (level - 1) * "    "

def require_input():
    input_code = ""
    for i in input_variables:
        input_code += "print(\"Please input " + i + " :\") \n"
        input_code += i + " =int(input())" + "\n"
    return input_code

def output_variables():
    output_code=""
    for i in all_variable:
        output_code += "print(\"Value of  " + i + " : \" + str(" + i + ")) \n"
    return output_code