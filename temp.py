def subtract(variable,num=1):
    variable = variable - num
    if variable<0 :
        variable=0
    return variable
print("Please input N :") 
N =int(input())
I = 0
sum = 0
tempI = 0
while N != 0:
    I += 1
    sum += I
    tempI += I
    I = 0
    I += tempI
    tempI = 0
    N = subtract(N)
print("Value of  I : " + str(I)) 
print("Value of  sum : " + str(sum)) 
print("Value of  tempI : " + str(tempI)) 
print("Value of  N : " + str(N)) 
