

def add_concat(infix_regex: str):
    """ Adds the '.' concatenation operator to an infix regular expression. """

    result = ""

    # we use None to symbolize the start of the string
    cant_concat_from = ['(', '|', None]
    cant_concat_to = ['*', '+', ')', '|']
    last_char = None

    for char in infix_regex:
        if char not in cant_concat_to and last_char not in cant_concat_from:
            result += '.'
        result += char
        last_char = char

    return result


print(add_concat('a+(b*c)|kf'))
