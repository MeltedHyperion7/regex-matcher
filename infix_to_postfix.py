from nfa import State, NFA
from InvalidRegexException import InvalidRegexException

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

def create_nfa_from_postfix(regex: str):
    """ Creates an NFA from a postfix regex as created by [infix_to_postifix]. """

    nfa_stack = []

    for char in regex:
        if char == '.':
            # to concat two nfas, add an epsilon arrow from every accepting state
            # of the first to the start state of the second and turn all accepting states
            # of the first into non accepting states

            if len(nfa_stack) < 2:
                raise InvalidRegexException()

            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()

            if nfa2.is_one_character_nfa:
                nfa2_matched_character, nfa2_accept_state = nfa2.start_state.transitions[0]
                for accept_state in nfa1.accept_states:
                    accept_state.add_transition(nfa2_matched_character, nfa2_accept_state)
                    accept_state.is_accepting = False

            else:
                for accept_state in nfa1.accept_states:
                    accept_state.add_transition('eps', nfa2.start_state)
                    accept_state.is_accepting = False


            nfa1.accept_states = nfa2.accept_states
            nfa1.is_one_character_nfa = False
            nfa_stack.append(nfa1)

            # for garbage collection
            nfa2.start_state = None
            nfa2.accept_states = None
        elif char == '*':
            # to apply a kleene star to an nfa, add a new start state, which is also an accept state,
            # to the nfa with an epsilon arrow going into the original start state.
            # add epsilon arrows from every accept state to the original start state

            if len(nfa_stack) < 1:
                raise InvalidRegexException()

            nfa = nfa_stack.pop()
            new_start_state = State([('eps', nfa.start_state)], True)
            for accept_state in nfa.accept_states:
                accept_state.add_transition('eps', nfa.start_state)

            nfa.accept_states.append(new_start_state)
            nfa.start_state = new_start_state
            nfa.is_one_character_nfa = False
            nfa_stack.append(nfa)

        elif char == '+':
            # TODO try this out on paper
            # we add epsilon arrows from every accept state to the start state

            if len(nfa_stack) < 1:
                raise InvalidRegexException()

            nfa = nfa_stack.pop()
            for accept_state in nfa.accept_states:
                accept_state.add_transition('eps', nfa.start_state)

            nfa.is_one_character_nfa = False
            nfa_stack.append(nfa)
        elif char == '|':
            # we apply the union operation by adding a new non accepting start state with
            # epsilon arrows going into the start state of each operand nfa

            if len(nfa_stack) < 2:
                raise InvalidRegexException()

            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()

            new_start_state = State([('eps', nfa1.start_state), ('eps', nfa2.start_state)], False)

            nfa1.start_state = new_start_state
            nfa1.accept_states.extend(nfa2.accept_states)
            nfa1.is_one_character_nfa = False
            nfa_stack.append(nfa1)

            # for garbage collection
            nfa2.start_state = None
            nfa2.accept_states = None
        else:
            # character from the alphabet
            accept_state = State([], True)
            start_state = State([(char, accept_state)], False)
            nfa_stack.append(NFA(start_state, [accept_state], True))

    if len(nfa_stack) != 1:
        raise InvalidRegexException()

    return nfa_stack[0]

def input_string_to_nfa(string: str, nfa: NFA):
    """ Pass [string] as input to [nfa] and return True if [nfa] reaches an accept state, else return False. """

    # ? is it possible to get a loop of epsilon transitions

    # we store a list of all current active states in the nfa
    # as each character is read, we follow all transition(including all series of epsilon transitions) to get a new set of active states

    # begin with the start state as the only active state
    active_states = [nfa.start_state]

    # mark all states as active that can be reached by following epsilon arrows from the start state
    i = 0
    while i < len(active_states):
        for transition_char, transition_state in active_states[i].transitions:
            if transition_char == 'eps':
                active_states.append(transition_state)
        i += 1

    string_index = 0
    while string_index < len(string) and len(active_states) > 0:
        character = string[string_index]
        new_active_states = []
        for active_state in active_states:
            # make active all states that can be reached from this state by reading [character]
            next_states = [transition_state for transition_char, transition_state in active_state.transitions if transition_char == character]

            # now make active all states that can be reached by epsilon arrows from these states
            i = 0
            while i < len(next_states):
                for transition_char, transition_state in next_states[i].transitions:
                    if transition_char == 'eps':
                        next_states.append(transition_state)
                i += 1
                
            new_active_states.extend(next_states)

        active_states = new_active_states
        string_index += 1

    for active_state in active_states:
        if active_state.is_accepting:
            return True

    return False

def match_regex(regex: str, string: str):
    """ Match [string] against the regular expression [regex]. """
    postfix_regex = infix_to_postfix(regex)
    nfa = create_nfa_from_postfix(postfix_regex)
    return input_string_to_nfa(string, nfa)
