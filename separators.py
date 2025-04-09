from enum import StrEnum


class Separators(StrEnum):
    list_start = "["
    list_end = "]"
    set_start = "("
    set_end = ")"
    dict_start = "{"
    dict_end = "}"
    dict_key_value = " :"
    value_separator = "\n"
    type_separator = "/"
    indent = "\t"
