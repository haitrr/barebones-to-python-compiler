import string

keywords = """
while
do
end
incr
decr
clear
not
if
then
else
elif
endif
loop
endloop
print
return
exit
"""
keywords = keywords.split()
one_charater_symbol = """
=
( )
< >
/ * + -
! &
.  ;
"""
one_charater_symbol = one_charater_symbol.split()
two_character_symbol = """
==
<=
>=
<>
!=
++
**
--
+=
-=
||
"""
two_character_symbol = two_character_symbol.split()
IDENTIFIER_STARTCHARS = string.ascii_letters
IDENTIFIER_CHARS = string.ascii_letters + string.digits + "_"

NUMBER_STARTCHARS = string.digits
NUMBER_CHARS = string.digits + "."

STRING_STARTCHARS = "'" + '"'
WHITESPACE_CHARS = " \t\n"

STRING = "String"
IDENTIFIER = "Identifier"
NUMBER = "Number"
WHITESPACE = "Whitespace"
COMMENT = "Comment"
EOF = "Eof"
