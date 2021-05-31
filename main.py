import csv


class DFA:
    def __init__(self, transition_function, initial_state, final_states, alphabet):
        self.transition_function = transition_function
        self.initial_state = initial_state
        self.final_states = final_states
        self.alphabet = alphabet

    def to_csv(self, csv_path_out=''):
        out_list = []
        for state in self.transition_function:
            row = [state]
            for input_i in self.alphabet:
                if input_i in self.transition_function[state]:
                    row.append(self.transition_function[state][input_i])
                else:
                    row.append('')
            out_list.append(row)
        out_list.sort()
        out_list.insert(0, ['state'] + self.alphabet)
        with open(csv_path_out, "w") as outfile:
            writer = csv.writer(outfile)
            for line in out_list:
                writer.writerow(line)


class NFA:
    def __init__(self, transition_function, initial_state, final_states, alphabet):
        self.transition_function = transition_function
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.alphabet = alphabet

    def get_next_states(self, state, next_input):
        new_states = set([])
        try:
            new_states = new_states.union(self.transition_function[state][next_input])
        except KeyError as e:
            pass
        return new_states


def create_nfa_from_input(input_csv_path):
    with open(input_csv_path, newline='') as f:
        reader = csv.reader(f)
        input_list = list(reader)
        nfa_transition_functions = {}
        for tf in input_list[1:]:
            state_0 = set(tf[1].split(','))
            state_1 = set(tf[2].split(','))
            nfa_transition_functions[tf[0]] = {'0': state_0, '1': state_1}

        nfa_initial_state = input_list[1][0]
        nfa_final_states = [input_list[-1][0]]
        nfa_alphabet = input_list[0][1:]
        new_nfa = NFA(nfa_transition_functions, nfa_initial_state, nfa_final_states, nfa_alphabet)

        return new_nfa


def nfa_2_dfa(nfa: NFA):
    # Step 1: Add q0 to empty initial state
    initial_state = frozenset([nfa.initial_state])
    current_state = {initial_state}
    unvisited_state = current_state.copy()

    dfa_transition_function = {}
    dfa_final_states = []
    dfa_alphabet = nfa.alphabet

    # Step 2: For each unvisited state in current state, find the possible set of states for each input symbol using
    # transition function of NFA. If this set of states is not in current state, add it to current state.
    while len(unvisited_state) > 0:
        this_state = unvisited_state.pop()
        this_state = list(this_state)
        this_state.sort()
        this_state_str = ''
        for s in this_state:
            this_state_str += str(s)
        dfa_transition_function[this_state_str] = {}
        for input_i in dfa_alphabet:
            new_states = set()
            for a_state in this_state:
                new_states = new_states.union(nfa.get_next_states(a_state, input_i))
            new_states = list(new_states)
            new_states.sort()
            new_states_str = ''
            for s in new_states:
                new_states_str += str(s)
            new_states = frozenset(new_states)
            dfa_transition_function[this_state_str][input_i] = new_states_str
            if new_states not in current_state:
                current_state.add(new_states)
                unvisited_state.add(new_states)

    # Step 3: all states contain final states of NFA will be final state of DFA
    for this_state in current_state:
        if len(this_state and nfa.final_states) > 0:
            dfa_final_states.append(this_state)

    new_dfa = DFA(dfa_transition_function, initial_state, dfa_final_states, dfa_alphabet)
    return new_dfa


if __name__ == "__main__":
    input_nfa = create_nfa_from_input(input_csv_path="nfa-page873.csv")

    dfa = nfa_2_dfa(input_nfa)
    dfa.to_csv('output.csv')
