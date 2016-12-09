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

# List of symbols

OneCharacterSymbols = """
;
"""

OneCharacterSymbols = OneCharacterSymbols.split()

import string

IDENTIFIER_STARTCHARS = string.ascii_letters

IDENTIFIER_CHARS = string.ascii_letters + string.digits + "_"

ZERO_CHAR='0'

STRING_STARTCHARS = "'" + '"'
WHITESPACE_CHARS = " \t\n"

# -----------------------------------------------------------------------
# TokenTypes for things other than symbols and keywords
# -----------------------------------------------------------------------
IDENTIFIER = "Identifier"
ZERO = "Zero"
WHITESPACE = "Whitespace"
COMMENT = "Comment"
EOF = "Eof"
