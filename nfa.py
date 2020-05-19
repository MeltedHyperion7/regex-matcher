class State:
    def __init__(self, transitions=[], is_accepting=False):
        self.transitions = transitions
        self.is_accepting = is_accepting

    def add_transition(self, character: str, state):

        # check if the transition doesn't already exist
        for transition_char, transition_state in self.transitions:
            if transition_char == character and transition_state is state:
                return

        self.transitions.append((character, state))

class NFA:
    def __init__(self, start_state: State, accept_states: list, is_one_character_nfa=False):
        self.start_state = start_state
        self.accept_states = accept_states
        self.is_one_character_nfa = is_one_character_nfa
