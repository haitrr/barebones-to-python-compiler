
from Lexer import Lexer
from Symbols import EOF


# -------------------------------------------------
# support for writing output to a file
# -------------------------------------------------
def writeln(*args):
    for arg in args:
        f.write(str(arg))
    f.write("\n")


# fragment start core
# -----------------------------------------------------------------------
#
#                    main
#
# -----------------------------------------------------------------------
def main(source_text):
    global f
    f = open(outputFilename, "w")
    writeln("Here are the tokens returned by the lexer:")

    # create an instance of a lexer
    lexer = Lexer(source_text)

    # ------------------------------------------------------------------
    # use the lexer.getlist() method repeatedly to get the tokens in
    # the sourceText. Then print the tokens.
    # ------------------------------------------------------------------
    while True:
        token = lexer.get()
        writeln(token.show(True))
        if token.type == EOF: break
    f.close()




if __name__ == "__main__":
    outputFilename = "barebones_to_python_ouput.py"
    sourceFilename = "barebones_source_code.txt"
    source_text = open(sourceFilename).read()
    main(source_text)
    print(open(outputFilename).read())
