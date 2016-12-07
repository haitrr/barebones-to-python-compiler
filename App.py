from tkinter import *
from tkinter.scrolledtext import ScrolledText
import Parser
import Compiler
from subprocess import call
from tkinter import filedialog


def compile():
    compiled_code_text_box.config(state=NORMAL)
    try:
        ast = Parser.parse(source_code_text_box.get(1.0, END), verbose=False)
    except Exception as e:
        compiled_code_text_box.delete(1.0, END)
        compiled_code_text_box.insert(INSERT, e)
        run_button.config(state=DISABLED)
    else:
        result = Compiler.compile(ast)
        Compiler.get_variable(ast)
        input_code = Compiler.require_input()
        output_code = Compiler.output_variables()
        subtract_function = Compiler.define_subtract()
        result = subtract_function + input_code + result + output_code
        compiled_code_text_box.delete(1.0, END)
        compiled_code_text_box.insert(INSERT, result)
        save_result(result)
        run_button.config(state=NORMAL)
    finally:
        compiled_code_text_box.config(state=DISABLED)


def save_result(text):
    file = open("temp.py", 'w')
    file.write(text)
    file.close()


def get_input():
    file_path = filedialog.askopenfilename()
    file = open(file_path, 'r')
    source_code_text_box.delete(1.0, END)
    source_code_text_box.insert(INSERT, file.read())
    file.close()


def run():
    call("python temp.py", shell=True)


root = Tk()
root.resizable(width=False, height=False)
root.grid()
open_file_button = Button(root, text="Open", command=get_input)
open_file_button.grid(row=0, column=0)
run_button = Button(root, text="Run", command=run)
run_button.config(state=DISABLED)
run_button.grid(row=3, column=0, columnspan=2)
compiler_button = Button(root, text="Compile", command=compiler)
compiler_button.grid(row=0, column=1)
source_code_lable = Label(root, text="Source code")
source_code_lable.grid(row=1, column=0)
compilered_code_lable = Label(root, text="Result")
compilered_code_lable.grid(row=1, column=1)
source_code_text_box = ScrolledText(root, width=50, height=30)
source_code_text_box.grid(row=2, column=0)
compiled_code_text_box = ScrolledText(root, width=50, height=30, state=DISABLED)
compiled_code_text_box.grid(row=2, column=1)
# root.geometry('{}x{}'.format(500, 500))
root.title("BareBones Compiler")
root.mainloop()
