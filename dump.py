import logging

from literal import Literal
from last_key_value import LastKeyValue
from separators import Separators
from typeref import TypeRef


def dumps(data, default=None, indent=0):
    result = list()
    data_buffer = [[data]]
    indent_str = ''
    while data_buffer:
        group = data_buffer.pop(0)

        if indent:
            indent_str = Separators.indent * indent * len(data_buffer)
            logging.debug(f"group ({len(data_buffer)}): [{len(indent_str)}] {len(group)}")
        else:
            logging.debug(f"group ({len(data_buffer)}): {len(group)}")

        while group:
            data = group.pop(0)

            logging.debug(f" data ({len(group)}): {data}")

            match data:
                case Literal():
                    logging.debug(f"  Literal: {data.t}")
                    result.append(f"{indent_str}{data.t}")
                case LastKeyValue():
                    logging.debug(f"  LastKeyValue")
                    value = result.pop(-1).lstrip(Separators.indent)
                    key = result.pop(-1).lstrip(Separators.indent)
                    result.append(f"{indent_str}{key}{Separators.dict_key_value}{value}")
                case str():
                    logging.debug(f"  str: {data}")
                    result.append(f"{indent_str}{TypeRef.str}/{data}")
                case bool():
                    logging.debug(f"  bool: {data}")
                    result.append(f"{indent_str}{TypeRef.bool}/{int(data)}")
                case float():
                    logging.debug(f"  float: {data}")
                    result.append(f"{indent_str}{TypeRef.float}/{str(data)}")
                case int():
                    logging.debug(f"  int: {data}")
                    result.append(f"{indent_str}{TypeRef.int}/{str(data)}")
                case list() | tuple() | set():
                    if isinstance(data, set):
                        start_char = Separators.set_start
                        end_char = Separators.set_end
                    else:
                        start_char = Separators.list_start
                        end_char = Separators.list_end

                    logging.debug(f"  list/tuple: {data}")
                    if len(data) == 0:
                        result.append(f"{indent_str}{start_char}{end_char}")
                    else:
                        first_type = type(next(iter(data)))
                        if first_type not in (list, tuple, dict, set) and all((
                            type(item) is first_type
                            for item in data
                        )):
                            data = list(map(Literal, data))

                            cons_type = TypeRef[first_type.__name__]
                            result.append(f"{indent_str}{start_char}{Separators.type_separator}{cons_type}")
                        # TODO: Handle nested lists/tuples
                        else:
                            result.append(f"{indent_str}{start_char}")

                        data_buffer.insert(0, group)
                        group.insert(0, Literal(end_char))
                        new_group = data.copy()
                        data_buffer.insert(0, new_group)
                        break
                case dict():
                    logging.debug(f"  dict: {data}")
                    if len(data) == 0:
                        result.append(f"{indent_str}{Separators.dict_start}{Separators.dict_end}")
                    else:
                        keys = list(data.keys())
                        first_key_type = type(keys[0])
                        is_cons_key_type = (
                            first_key_type not in (list, tuple, dict, set)
                            and all((
                                type(key) is first_key_type
                                for key in keys
                            ))
                        )

                        values = list(data.values())
                        first_value_type = type(values[0])
                        is_cons_value_type = (
                            first_value_type not in (list, tuple, dict, set)
                            and all((
                                type(value) is first_value_type
                                for value in values
                            ))
                        )

                        if is_cons_key_type and is_cons_value_type:
                            cons_key_type = TypeRef[first_key_type.__name__]
                            cons_value_type = TypeRef[first_value_type.__name__]
                            result.append(f"{indent_str}{Separators.dict_start}{cons_key_type}{Separators.type_separator}{cons_value_type}")
                            keys = list(map(Literal, keys))
                            values = list(map(Literal, values))
                        elif is_cons_key_type:
                            cons_key_type = TypeRef[first_key_type.__name__]
                            result.append(f"{indent_str}{Separators.dict_start}{cons_key_type}{Separators.type_separator}")
                            keys = list(map(Literal, keys))
                        elif is_cons_value_type:
                            cons_value_type = TypeRef[first_value_type.__name__]
                            result.append(f"{indent_str}{Separators.dict_start}{Separators.type_separator}{cons_value_type}")
                            values = list(map(Literal, values))
                        else:
                            result.append(f"{indent_str}{Separators.dict_start}")

                        new_group = []
                        for key, value in zip(keys, values):
                            new_group.append(key)
                            new_group.append(value)
                            new_group.append(LastKeyValue())
                        group.insert(0, Literal(Separators.dict_end))
                        data_buffer.insert(0, group)
                        data_buffer.insert(0, new_group)
                        break
                case _:
                    logging.debug(f"  other: {data}")
                    if default is None:
                        raise ValueError(f"Unsupported type: {type(data)}")
                    else:
                        logging.warning(f"Converting {type(data)} to default")
                        group.append(default(data))

    return Separators.value_separator.join(result)


if __name__ == "__main__":
    from pathlib import Path
    # logging.basicConfig(level=logging.DEBUG)

    examples = Path('examples')

    with open(examples / 'single_int.aucff', 'w') as f:
        f.write(dumps(123, indent=1))

    with open(examples / 'single_float.aucff', 'w') as f:
        f.write(dumps(123.456, indent=1))

    with open(examples / 'single_bool.aucff', 'w') as f:
        f.write(dumps(True, indent=1))

    with open(examples / 'single_str.aucff', 'w') as f:
        f.write(dumps("Hello, world!", indent=1))

    with open(examples / 'single_list.aucff', 'w') as f:
        f.write(dumps([1, 2, 3], indent=1))

    with open(examples / 'single_list_of_str.aucff', 'w') as f:
        f.write(dumps(['1', '2', '3'], indent=1))

    with open(examples / 'single_empty_list.aucff', 'w') as f:
        f.write(dumps([], indent=1))

    with open(examples / 'single_dict.aucff', 'w') as f:
        f.write(dumps({"a": '1', "b": 2, "c": 3}, indent=1))

    with open(examples / 'single_dict_with_str_keys.aucff', 'w') as f:
        f.write(dumps({"a": '1', "b": '2', "c": '3'}, indent=1))

    with open(examples / 'single_dict_with_int_keys.aucff', 'w') as f:
        f.write(dumps({"a": 1, 1: 2, "c": 3}, indent=1))

    with open(examples / 'single_dict_with_int_and_str_keys.aucff', 'w') as f:
        f.write(dumps({"a": 1, 1: '2', "c": 3}, indent=1))

    with open(examples / 'single_empty_dict.aucff', 'w') as f:
        f.write(dumps({}, indent=1))

    with open(examples / 'single_set.aucff', 'w') as f:
        f.write(dumps({1, 2, 3, 1}, indent=1))

    with open(examples / 'single_str_set.aucff', 'w') as f:
        f.write(dumps({'1', '2', '3', '1'}, indent=1))

    with open(examples / 'single_empty_set.aucff', 'w') as f:
        f.write(dumps(set(), indent=1))

    with open(examples / 'single_list_of_dicts.aucff', 'w') as f:
        f.write(dumps([{"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 3}], indent=1))
