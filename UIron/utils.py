from math import floor, ceil


class UtilsError(Exception):
    ...


def pretty_dict(dictionary: dict, indent: int=0, tab: str='    ') -> str:
    """Formats a dictionary to be printed with tabs"""
    result = '{\n'
    for key, value in dictionary.items():
        result += f'{tab*indent+tab}{key}: {prettify(value, indent=indent+1)}\n'
    result += tab*indent + '}'
    return result


def pretty_list(list_: list, indent: int=0, tab: str='    ') -> str:
    """Formats a list, tuple or set to be printed with tabs"""
    result = '[\n'
    for value in list_:
        result += f'{tab*indent+tab}{value}\n'
    result += tab*indent + ']'
    return result


def prettify(object_: object, indent: int=0) -> str:
    """Formats an object to be printed with tabs"""
    if isinstance(object_, dict): return pretty_dict(object_, indent=indent)
    elif isinstance(object_, (list, tuple, set)): return pretty_list(object_, indent=indent)
    return str(object_)


def table(table_: list[list[str]], alignment: str='center', headers: list[str]=[], separator: str='|', padding: int=1) -> str:
    def align(word: str, length: int) -> str:
        diff = length - len(word)
        match alignment:
            case 'center': return ' '*ceil(diff/2)+word+' '*floor(diff/2)
            case 'left': return word + ' '*diff
            case 'right': return ' '*diff + word

    left_separator = separator + ' '*padding
    right_separator = ' '*padding + separator
    separator = ' '*padding + separator + ' '*padding

    rows, columns = len(table_), max([len(row) for row in table_])
    if headers:
        table_.insert(0, headers)
        rows, columns = rows+1, max(columns, len(headers))

    string_table = [[str(element) for element in row] for row in table_]
    filled_table = [row + ['']*(columns-len(row)) for row in string_table]
    column_lengths = [max([len(filled_table[j][i]) for j in range(rows)]) for i in range(columns)]
    padded_table = [[align(row[i], length) for i, length in enumerate(column_lengths)] for row in filled_table]
    row_table = [left_separator + separator.join(row) + right_separator for row in padded_table]
    return '\n'.join(row_table)