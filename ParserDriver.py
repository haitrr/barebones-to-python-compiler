# fragment start *
import Parser as parser


# -------------------------------------------------
# support for writing output to a file
# -------------------------------------------------
def writeln(*args):
    for arg in args:
        f.write(str(arg))
    f.write("\n")


if __name__ == "__main__":
    outputFilename = "nxxParserDriver_output.txt"
    sourceFilename = "nxx1.txt"
    source_text = open(sourceFilename).read()
    ast = parser.parse(source_text, verbose=False)
    print("~" * 80)
    print("Here is the abstract syntax tree:")
    print("~" * 80)
    f = open(outputFilename, "w")
    f.write(ast.toString())
    f.close()
    print(open(outputFilename).read())
