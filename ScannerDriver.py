from Scanner import Scanner
import Character

# -------------------------------------------
# support for writing output to a file
# -------------------------------------------
def writeln(*args):
    for arg in args:
        f.write(str(arg))
    f.write("\n")


# -----------------------------------------------------------------------
#
#                    main
#
# -----------------------------------------------------------------------
def main(source_text):
    global f
    f = open(output_file_name, "w")  # open the ouput file

    writeln("Here are the characters returned by the scanner:")
    writeln("  line col  character")

    # create a scanner (an instance of the Scanner class)
    scanner = Scanner(source_text)

    # ------------------------------------------------------------------
    #               Scan all character in the source text
    # ------------------------------------------------------------------
    character = scanner.get()
    while True:
        writeln(character)
        if character.char == Character.ENDMARK: break
        character = scanner.get()  # get next character

    f.close()

# -----------------------------------------
#              run
# -----------------------------------------
if __name__ == "__main__":
    output_file_name = "barebones_to_python_ouput.py"
    sourceFilename = "barebones_source_code.txt"
    source_text = open(sourceFilename).read()
    main(source_text)
    print(open(output_file_name).read())
