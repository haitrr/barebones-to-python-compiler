import Compiler

def check_semantic_error(ast):
     check_self_terminate(ast)



def check_self_terminate(ast):
    for i in ast.children:
        if i.token.type == "while":
            if check_terminate(i,i.children[0].token.cargo,False) is True:
                i.token.abort("Detected infinite loop")
            check_self_terminate(i)


def check_terminate(ast,variable,exist):
    loops=[]
    if exist == False:
        for i in ast.children:
            if i.token.type in ["clear","decr"]:
                    return False
            if i.token.type == "while":
                 loops.append(i)
        if loops == []:
            return True
        else:
            for l in loops:
                return check_self_terminate(l,ast.children[0].token.cargo,True)
    else:
        Compiler.get_variable(ast)
        if variable in Compiler.all_variable:
            return False
        else:
            return True
