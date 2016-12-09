from tkinter import *
from tkinter.scrolledtext import ScrolledText
import Parser
import Compiler
from subprocess import call
from tkinter import filedialog


# Compile souce code
def compile(ast=None):
    # Set the text box to editable
    compiled_code_text_box.config(state=NORMAL)

    # Try to parse the source
    try:
        if ast is None:
            ast = Parser.parse(source_code_text_box.get(1.0, END), verbose=False)

    # If there are compile errors display them out
    except Exception as e:
        compiled_code_text_box.delete(1.0, END)
        compiled_code_text_box.insert(INSERT, e)
        run_button.config(state=DISABLED)
    # Display compiled code
    else:

        result = Compiler.compile(ast)
        Compiler.get_variable(ast)

        # Combine the code with other parts to create a program
        input_code = Compiler.require_input()
        output_code = Compiler.output_variables()
        subtract_function = Compiler.define_subtract()
        pre_declare = Compiler.pre_declare_variables()
        result = "#--------Redefine subtract function--------\n\n" \
                 + subtract_function \
                 + "\n#--------Safe pre declare variables--------\n\n" \
                 + pre_declare \
                 + "\n#-----------Input requirer code------------\n\n" \
                 + input_code + "\n#-----------Compiled code------------\n\n" \
                 + result + "\n#-----------Output variables code------------\n\n" \
                 + output_code + "\n#-----------End-------------"
        compiled_code_text_box.delete(1.0, END)
        compiled_code_text_box.insert(INSERT, result)

        # Save result code to temp file
        save_result(result)

        # Enable run button
        run_button.config(state=NORMAL)

        # Enable optimize run button
        optimize_button.config(state=NORMAL)
    finally:

        # Set the text box to read only
        compiled_code_text_box.config(state=DISABLED)


        # Optimize code


def optimize():
    # Parse and optimize the syntax tree
    ast = Parser.parse(source_code_text_box.get(1.0, END), verbose=False)
    Parser.optimize(ast)

    # Compile
    compile(ast)

    # Disable optimize button
    optimize_button.config(state=DISABLED)


# Save compiled result code to temp file
def save_result(text):
    file = open("temp.py", 'w')
    file.write(text)
    file.close()


# Load the source code from file
def get_input():
    file_path = filedialog.askopenfilename()
    file = open(file_path, 'r')
    source_code_text_box.delete(1.0, END)
    source_code_text_box.insert(INSERT, file.read())
    file.close()


# Run compiled code
def run():
    call("python temp.py", shell=True)


# Set up UI
root = Tk()
root.resizable(width=False, height=False)
root.grid()
open_file_button = Button(root, text="Open", command=get_input)
open_file_button.grid(row=0, column=0)
run_button = Button(root, text="Run", command=run)
run_button.config(state=DISABLED)
run_button.grid(row=3, column=0)
compiler_button = Button(root, text="Compile", command=compile)
compiler_button.grid(row=0, column=1)
optimize_button = Button(root, text="Optimize", command=optimize)
optimize_button.grid(row=3, column=1)
source_code_lable = Label(root, text="Source code")
source_code_lable.grid(row=1, column=0)
compiled_code_lable = Label(root, text="Result")
compiled_code_lable.grid(row=1, column=1)
source_code_text_box = ScrolledText(root, width=50, height=30)
source_code_text_box.grid(row=2, column=0)
compiled_code_text_box = ScrolledText(root, width=50, height=30, state=DISABLED)
compiled_code_text_box.grid(row=2, column=1)
root.title("BareBones Compiler")
root.mainloop()
