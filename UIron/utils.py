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