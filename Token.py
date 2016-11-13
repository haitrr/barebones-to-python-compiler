from Character import *
class LexerError(Exception): pass

class Token:
    def __init__(self,start_char):
        self.char = start_char.char
        self.source_text=start_char.source_text
        self.line_index=start_char.line_index
        self.column_index = start_char.column_index
        self.type = None
    def show(self,show_line_number=False,**kwargs):
        align = kwargs.get("align",True)
        if align:
            token_type_length=12
            space = " "
        else:
            token_type_length=0
            space=""
        if show_line_number:
            s = str(self.line_index).rjust(6)+str(self.column_index).rjust(4)+"     "
        else:
            s=""
        if self.type == self.char:
            s = s+"Symbol".ljust(token_type_length,".")+":"+space+self.type
        elif self.type=="white_space":
            s = s+ "WhiteSpace".ljust(token_type_length,".")+":"+space+repr(self.char)
        else:
            s = s+ self.type.ljust(token_type_length,".")+":"+space+self.char
        return s
    guts= property(show)
    def abort(self,message):
        lines = self.source_text.split("\n")
        source_line = lines[self.line_index]
        raise LexerError("\nIn line " + str(self.line_index + 1)
                         + " near column " + str(self.column_index + 1) + ":\n\n"
                         + source_line.replace("\t", " ") + "\n"
                         + " " * self.column_index
                         + "^\n\n"
                         + message)