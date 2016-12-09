#--------Redefine subtract function--------

def subtract(variable,num=1):
    variable = variable - num
    if variable<0 :
        variable=0
    return variable

#--------Safe pre declare variables--------

Z = 0
i = 0
n = 0
Z1 = 0
tmpZ = 0
tmpZ1 = 0
tmpI = 0

#-----------Input requirer code------------

print("Please input n :") 
n =int(input())

#-----------Compiled code------------

Z = 0
Z += 1
i = 0
while n != 0:
    i += 1
    Z1 = 0
    tmpZ = 0
    Z1 += Z
    tmpZ += Z
    Z = 0
    Z = 0
    tmpZ1 = 0
    while Z1 != 0:
        tmpI = 0
        Z += i
        tmpI += i
        i = 0
        Z1 = subtract(Z1)
        tmpZ1 += 1
        i += tmpI
        tmpI = 0
    Z1 += tmpZ1
    tmpZ1 = 0
    i += tmpI
    tmpI = 0
    n = subtract(n)

#-----------Output variables code------------

print("Value of  Z : " + str(Z)) 
print("Value of  i : " + str(i)) 
print("Value of  n : " + str(n)) 
print("Value of  Z1 : " + str(Z1)) 
print("Value of  tmpZ : " + str(tmpZ)) 
print("Value of  tmpZ1 : " + str(tmpZ1)) 
print("Value of  tmpI : " + str(tmpI)) 

#-----------End-------------