# ----------------------------------------------------------
# a list of keywords
# ----------------------------------------------------------
Keywords = """
while
incr
do
decr
clear
end
not
0
"""
Keywords = Keywords.split()

# fragment start snippet1
# ----------------------------------------------------------
# a list of symbols that are one character long
# ----------------------------------------------------------
OneCharacterSymbols = """
;
"""
# fragment stop snippet1
OneCharacterSymbols = OneCharacterSymbols.split()
# fragment start snippet1

# ----------------------------------------------------------
# a list of symbols that are two characters long
# ----------------------------------------------------------
TwoCharacterSymbols = """
"""
# fragment stop snippet1
TwoCharacterSymbols = TwoCharacterSymbols.split()

# fragment start constants
import string

IDENTIFIER_STARTCHARS = string.ascii_letters
IDENTIFIER_CHARS = string.ascii_letters + string.digits + "_"

NUMBER_STARTCHARS = string.digits
NUMBER_CHARS = string.digits + "."

STRING_STARTCHARS = "'" + '"'
WHITESPACE_CHARS = " \t\n"
# fragment stop constants

# -----------------------------------------------------------------------
# TokenTypes for things other than symbols and keywords
# -----------------------------------------------------------------------
STRING = "String"
IDENTIFIER = "Identifier"
NUMBER = "Number"
WHITESPACE = "Whitespace"
COMMENT = "Comment"
EOF = "Eof"
