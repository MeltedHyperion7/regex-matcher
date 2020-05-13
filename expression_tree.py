class ExpressionNode:
    def __init__(self, expression: str):
        self.expression = expression
        self.children = []

    def __len__(self):
        return len(self.expression)

    def __str__(self):
        return self.expression

    def is_subexpression(self):
        return len(self) > 1

def regex_to_node_list(regex: str):
    """ Convert the regex into a list of characters, operators and subexpressions. """

    node_list = []

    # we keep track of subexpressions in parentheses
    # any expression inside one level of nesting will be added to the list as a subexpression
    bracket_nesting_level = 0
    current_node = None
    for character in regex:
        if (character == "*" or character == "+" or character == "|") and bracket_nesting_level == 0:
            current_node = ExpressionNode(character)
            node_list.append(current_node)
            current_node = None

        else:
            if character == "(":
                if bracket_nesting_level != 0:
                    if current_node is None:
                        current_node = ExpressionNode("")
                    current_node.expression += character

                bracket_nesting_level += 1
            elif character == ")":
                if bracket_nesting_level == 1 and current_node is not None:
                    # add the subexpression to the list
                    # pairs of empty parentheses are ignored
                    node_list.append(current_node)
                    current_node = None
                else:
                    if current_node is None:
                        # TODO raise exception
                        current_node = ExpressionNode("")
                    current_node.expression += character

                bracket_nesting_level -= 1
            else:
                if bracket_nesting_level > 0:
                    if current_node is None:
                        # create an [ExpressionNode] for the subexpression
                        current_node = ExpressionNode("")
                    current_node.expression += character
                else:
                    node_list.append(ExpressionNode(character))
                    current_node = None

    if current_node is not None:
        node_list.append(current_node)

    for node in node_list:
        print(node)

def node_list_to_tree(node_list: list):
    i = len(node_list) - 1
    while i >= 0:
        pass

regex_to_node_list("a+ c(a(b*)n)c()+d")