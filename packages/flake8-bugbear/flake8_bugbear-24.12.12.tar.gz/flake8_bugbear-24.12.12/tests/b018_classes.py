"""
Should emit:
B018 - on lines 17-26, 30, 33
"""

class Foo1:
    """abc"""


class Foo2:
    """abc"""

    a = 2
    "str"  # Str (no raise)
    f"{int}"  # JoinedStr (no raise)
    1j  # Number (complex)
    1  # Number (int)
    1.0  # Number (float)
    b"foo"  # Binary
    True  # NameConstant (True)
    False  # NameConstant (False)
    None  # NameConstant (None)
    [1, 2]  # list
    {1, 2}  # set
    {"foo": "bar"}  # dict


class Foo3:
    123
    a = 2
    "str"
    1
    (1,)  # bad
    (2, 3)  # bad
    t = (4, 5)  # good
