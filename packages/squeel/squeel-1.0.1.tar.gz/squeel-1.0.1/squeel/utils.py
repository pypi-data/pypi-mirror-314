def find_current_line_whitespace(data: bytes, position: int) -> bytes:
    """
    Finds the leading whitespace on the current line containing the given position.

    :param data: The multiline bytes string.
    :param position: The byte position in the string.
    :return: The leading whitespace on the current line as bytes.
    """
    if position < 0 or position > len(data):
        raise ValueError("Position is out of bounds")

    line_start = data.rfind(b"\n", 0, position) + 1
    current_line = data[line_start:position]

    return current_line[: len(current_line) - len(current_line.lstrip())]
