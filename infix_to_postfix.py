precedence = {
    # TODO add '?' operator
    '(': 1,
    '|': 2,
    '.': 3,
    '*': 4,
    '+': 5
}

def add_concat(infix_regex: str):
    """
    Adds the '.' concatenation operator explicitly
    to an infix regular expression.
    """

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

def infix_to_postfix(infix_regex: str):
    result = ""
    stack = []

    postfix_regex = add_concat(infix_regex)

    for char in postfix_regex:
        if char == '(':
            stack.append(char)
        elif char == ')':
            # TODO add error check
            while stack[-1] != '(':
                result += stack.pop()

            # remove opening parentheses
            stack.pop()
        else:
            while len(stack) > 0:
                stack_top_char = stack[-1]
                stack_top_char_precedence = precedence.get(stack_top_char, len(precedence)+1)
                char_precedence = precedence.get(char, len(precedence)+1)

                if stack_top_char_precedence >= char_precedence:
                    result += stack.pop()
                else:
                    break
            
            stack.append(char)

    while len(stack) > 0:
        result += stack.pop()

    return result

print(infix_to_postfix('a((ab)+c)+'))