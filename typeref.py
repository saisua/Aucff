from enum import StrEnum


class TypeRef(StrEnum):
    str = "s"
    bool = "b"
    float = "f"
    int = "i"
    list = "l"
    dict = "d"
    set = "s"
    type = 'T'
    none = 'n'
    nan = 'N'
    inf = 'I'
    bytes = 'B'
