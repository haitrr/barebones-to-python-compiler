from tkinter import *
from tkinter.scrolledtext import ScrolledText
import Parser
import Interpreter
from subprocess import call
from tkinter import filedialog
import os


def interpreter():
    interpretered_code_text_box.config(state=NORMAL)
    try:
        ast = Parser.parse(source_code_text_box.get(1.0,END), verbose=False)
    except Exception as e:
        interpretered_code_text_box.delete(1.0, END)
        interpretered_code_text_box.insert(INSERT,e )
        run_button.config(state=DISABLED)
    else:
        result = Interpreter.interpreter(ast)
        Interpreter.get_variable(ast)
        input_code = Interpreter.require_input()
        output_code = Interpreter.output_variables()
        subtract_function = Interpreter.define_subtract()
        result =subtract_function+ input_code + result + output_code
        interpretered_code_text_box.delete(1.0,END)
        interpretered_code_text_box.insert(INSERT,result)
        save_result(result)
        run_button.config(state=NORMAL)
    finally:
        interpretered_code_text_box.config(state=DISABLED)

def save_result(text):
    file = open("temp.py",'w')
    file.write(text)
    file.close()

def get_input():
    file_path = filedialog.askopenfilename()
    file = open(file_path,'r')
    source_code_text_box.delete(1.0,END)
    source_code_text_box.insert(INSERT,file.read())
    file.close()
def run():
    os.system("python temp.py")
root = Tk()
root.resizable(width=False, height=False)
root.grid()
open_file_button = Button(root,text = "Open",command = get_input)
open_file_button.grid(row=0, column=0)
run_button = Button(root,text = "Run",command=run)
run_button.config(state=DISABLED)
run_button.grid(row=3,column=0,columnspan=2)
interpreter_button = Button(root,text = "Interpreter",command = interpreter)
interpreter_button.grid(row=0, column=1)
source_code_lable=Label(root,text="Source code")
source_code_lable.grid(row=1,column=0)
interpretered_code_lable = Label(root,text="Result")
interpretered_code_lable.grid(row =1 ,column=1)
source_code_text_box = ScrolledText(root,width = 50,height=30)
source_code_text_box.grid(row =2,column = 0)
interpretered_code_text_box = ScrolledText(root,width = 50,height=30,state=DISABLED)
interpretered_code_text_box.grid(row =2 ,column = 1)
#root.geometry('{}x{}'.format(500, 500))
root.title("BareBones Interpreter")
root.mainloop()