import logging
from typing import Any

from literal import Literal
from last_key_value import LastKeyValue
from separators import Separators
from typeref import TypeRef
from type_convert import TypeConvert


def loads(data: str) -> Any:
    lines = [
        line.lstrip(Separators.indent)
        for line in data.split(Separators.value_separator)
    ]
    container_stack = []
    converter_stack = []
    curr_container = None
    result = None

    line = None
    for line in lines:
        logging.debug(f"line: {line}")
        if line[0] in (
            Separators.dict_end.value,
            Separators.list_end.value,
            Separators.set_end.value,
        ):
            logging.debug(" container end")
            container_stack.pop()
            converter_stack.pop()
        elif line[0] == Separators.dict_start.value:
            logging.debug(" dict start")
            curr_container = dict()
            container_stack.append(curr_container)
            if len(line) > 2 and line[2] == Separators.type_separator.value:
                if len(line) == 4:
                    key_converter = TypeConvert[line[1]].value
                    value_converter = TypeConvert[line[3]].value
                elif len(line) == 3:
                    if line[2] == Separators.type_separator.value:
                        key_converter = TypeConvert[line[1]].value
                        value_converter = None
                    elif line[1] == Separators.type_separator.value:
                        key_converter = None
                        value_converter = TypeConvert[line[2]].value
                converter_stack.append((key_converter, value_converter))
            else:
                converter_stack.append((None, None))
        elif line[0] == Separators.list_start.value:
            logging.debug(" list start")
            curr_container = list()
            container_stack.append(curr_container)

            if len(line) == 3 and line[1] == Separators.type_separator.value:
                logging.debug("  converter")
                converter_stack.append(TypeConvert[line[2]].value)
            else:
                converter_stack.append(None)
        elif line[0] == Separators.set_start.value:
            logging.debug(" set start")
            curr_container = set()
            container_stack.append(curr_container)

            if len(line) > 1 and line[1] == Separators.type_separator.value:
                logging.debug("  converter")
                converter_stack.append(TypeConvert[line[2]].value)
            else:
                converter_stack.append(None)
        elif isinstance(curr_container, dict):
            logging.debug(" dict entry")
            key, value = line.split(Separators.dict_key_value.value, 1)
            key_converter, value_converter = converter_stack[-1]
            if key_converter is not None:
                key = key_converter(key)
            elif len(key) > 2 and key[1] == Separators.type_separator.value:
                key = TypeConvert[key[0]].value(key[2:])
            if value_converter is not None:
                value = value_converter(value)
            elif len(value) > 2 and value[1] == Separators.type_separator.value:
                value = TypeConvert[value[0]].value(value[2:])
            curr_container[key] = value
        else:
            if len(line) != 1 and line[1] == Separators.type_separator.value:
                logging.debug(" typed value")

                line = TypeConvert[line[0]].value(line[2:])
            else:
                logging.debug(" value")

            if isinstance(curr_container, list):
                if converter_stack[-1] is not None:
                    curr_container.append(converter_stack[-1](line))
                else:
                    curr_container.append(line)
            elif isinstance(curr_container, set):
                if converter_stack[-1] is not None:
                    curr_container.add(converter_stack[-1](line))
                else:
                    curr_container.add(line)
            elif curr_container is None:
                result = line

        if result is None:
            if curr_container is not None:
                result = curr_container
            else:
                result = line

    return result


if __name__ == "__main__":
    from pathlib import Path

    # logging.basicConfig(level=logging.DEBUG)

    examples_folder = Path("examples")
    for example in examples_folder.glob("*.aucff"):
        print(f"## {example}:")
        with open(example, "r") as f:
            data = f.read()
        print(repr(loads(data)))
