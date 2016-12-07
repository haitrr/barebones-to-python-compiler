import Compiler
import Parser as parser

outputFilename = "barebones_to_python_ouput.py"
sourceFilename = "barebones_source_code.txt"
source_text = open(sourceFilename).read()
ast = parser.parse(source_text, verbose=False)
print(50 * "~")
print(ast.to_string())
print(50 * "~")
result = Compiler.compile(ast)
Compiler.get_variable()
input_code = Compiler.require_input()
output_code = Compiler.output_variables()
result = Compiler.define_subtract() + input_code + result + output_code
f = open(outputFilename, "w")
f.write(result)
f.close()
print(result)
