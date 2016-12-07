print("Please input X :") 
X =int(input())
Y = 0
Temp = 0
while X != 0:
    Y += 1
    Temp += 1
    X -= 1
while Temp != 0:
    X += 1
    Temp -= 1
print("Value of  Y : " + str(Y)) 
print("Value of  Temp : " + str(Temp)) 
print("Value of  X : " + str(X)) 
