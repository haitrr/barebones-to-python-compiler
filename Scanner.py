from Character import *


class Scanner:
    def __init__(self, source_text):
        self.source_text = source_text
        self.last_index = len(source_text) - 1
        self.source_index = -1
        self.line_index = 0
        self.column_index = -1

    def get(self):
        self.source_index += 1
        if self.source_index > 0:
            if self.source_text[self.source_index - 1] == "\n":
                self.line_index += 1
                self.column_index = -1
        self.column_index += 1
        if self.source_index > self.last_index:
            char = Character(ENDMARK, self.line_index, self.column_index, self.source_index, self.source_text)
        else:
            c = self.source_text[self.source_index]
            char = Character(c, self.line_index, self.column_index, self.source_index, self.source_text)
        return char

    def look_ahead(self, offset=1):
        index = self.source_index + offset
        if index > self.last_index:
            return ENDMARK
        else:
            return self.source_text[index]


if __name__ == '__main__':
    file = open("source_text.txt", "r")
    print("Here are the characters returned by the scanner:")
    print("     line col  character")
    source_text_file = file.read()
    scanner = Scanner(source_text_file)
    character = scanner.get()
    while True:
        print(character)
        character = scanner.get()
        if character.char == ENDMARK:
            break
    file.close()