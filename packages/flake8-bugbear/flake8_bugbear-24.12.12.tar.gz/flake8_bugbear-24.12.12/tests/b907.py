def foo():
    return "hello"


var = var2 = "hello"

# warnings
f"begin '{var}' end"
f"'{var}' end"
f"begin '{var}'"

f'begin "{var}" end'
f'"{var}" end'
f'begin "{var}"'

f'a "{"hello"}" b'
f'a "{foo()}" b'

# fmt: off
k = (f'"' # Error emitted here on <py312 (all values assigned the same lineno)
     f'{var}'
     f'"'
     f'"')

k = (f'"' # error emitted on this line on <py312
     f'{var}'
     '"'
     f'"')
# fmt: on

f'{"hello"}"{var}"'  # warn for var and not hello
f'"{var}"{"hello"}'  # warn for var and not hello
f'"{var}" and {"hello"} and "{var2}"'  # warn for var and var2
f'"{var}" and "{var2}"'  # warn for both
f'"{var}""{var2}"'  # warn for both

# check that pre-quote & variable is reset if no post-quote is found
f'"{var}abc "{var2}"'  # warn on var2

# check formatting on different contained types
f'"{var}"'
f'"{var.__str__}"'
f'"{var.__str__.__repr__}"'
f'"{3+5}"'
f'"{foo()}"'
f'"{None}"'
f'"{...}"'  # although f'"{...!r}"' == 'Ellipsis'
f'"{True}"'

# alignment specifier
f'"{var:<}"'
f'"{var:>}"'
f'"{var:^}"'
f'"{var:5<}"'

# explicit string specifier
f'"{var:s}"'

# empty format string
f'"{var:}"'

# These all currently give warnings, but could be considered false alarms
# multiple quote marks
f'"""{var}"""'
# str conversion specified
f'"{var!s}"'
# two variables fighting over the same quote mark
f'"{var}"{var2}"'  # currently gives warning on the first one


# ***no warnings*** #

# padding inside quotes
f'"{var:5}"'

# quote mark not immediately adjacent
f'" {var} "'
f'"{var} "'
f'" {var}"'

# mixed quote marks
f"'{var}\""

# repr specifier already given
f'"{var!r}"'

# two variables in a row with no quote mark inbetween
f'"{var}{var}"'

# don't crash on non-string constants
f'5{var}"'
f"\"{var}'"

# sign option (only valid for number types)
f'"{var:+}"'

# integer presentation type specified
f'"{var:b}"'
f'"{var:x}"'

# float presentation type
f'"{var:e%}"'

# alignment specifier invalid for strings
f'"{var:=}"'

# other types and combinations are tested in test_b907_format_specifier_permutations

# don't attempt to parse complex format specs
f'"{var:{var}}"'
f'"{var:5{var}}"'

# even if explicit string type (not implemented)
f'"{var:{var}s}"'
