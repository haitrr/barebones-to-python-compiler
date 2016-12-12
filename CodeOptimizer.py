from Character import Character
from Token import Token
from Node import Node


# Optimize the code
def optimize(node):
    while_loop(node)


# Optimize the while loop
# If in the while loop there are only one decr statement of the while variable
# and only other decr or incr statements
# this mean the while loop is just set the while variable to 0
# and do the incr or decr <value of while variable> times

def while_loop(node,variable=None):
    i = 0
    count = 0
    optmz=False
    decr_node = None

    # Recurse until find the final while loop
    # The most inside while loop
    while i < len(node.children):
        if node.children[i].token.type == "while":

            # Optimize
            if while_loop(node.children[i],node.children[i].children[0].token.cargo):

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