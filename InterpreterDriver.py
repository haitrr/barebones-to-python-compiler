import Interpreter
import Parser as parser

outputFilename = "barebones_to_python_ouput.py"
sourceFilename = "barebones_source_code.txt"
source_text = open(sourceFilename).read()
ast = parser.parse(source_text, verbose=False)
print(50*"~")
print(ast.to_string())
print(50*"~")
result = Interpreter.interpreter(ast)
input_code = ""
output_code=""
Interpreter.get_variable(ast)
for i in Interpreter.input_variables:
    input_code += "print(\"Please input "+ i+" :\") \n"
    input_code+= i +" =int(input())"+"\n"
for i in Interpreter.all_variable:
    output_code+="print(\"Value of  " +i+" : \" + str("+i+")) \n"
result=input_code+result+output_code
f = open(outputFilename, "w")
f.write(result)
f.close()
print(result)