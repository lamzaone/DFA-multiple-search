class DFA:
    def __init__(self, words):
        self.words = words        # list of words
        self.states = {}          # dictionary in the form (state, letter) -> state
        self.final_states = {}    # set of final states, associated with the words
        self.all_states = set()   # set of all states
        self.build_dfa()          # build the DFA

    def build_dfa(self):
        state_id = 1  # Start from 1, because 0 is the universal initial state
        self.all_states.add(0)  # Add the universal initial state

        # Transitions for the initial state (s0) that accepts any character (represented by 'w')
        self.states[(0, 'w')] = 0

        # Build the DFA based on the given words
        for word in self.words:
            current_state = 0
            for letter in word:
                if (current_state, letter) not in self.states:
                    # If there is no transition, add a new state
                    self.states[(current_state, letter)] = state_id
                    self.all_states.add(state_id)
                    state_id += 1

                # Update the current state
                current_state = self.states[(current_state, letter)]

            # Associate the last state with the word and mark it as final
            self.final_states[current_state] = word

    def simulate_complete(self, text):
        current_states = {0}  # Start from the universal initial state (s0)
        path = []  # Keep the complete path for display
        occurrences = {word: [] for word in self.words}  # Keep the locations of occurrences for each word

        # Split the text into lines
        lines = text.split("\n")
        for line_idx, line in enumerate(lines, start=1):
            for col_idx, letter in enumerate(line, start=1):
                new_states = set()

                # Determine all new states based on transitions for each current state
                for state in current_states:
                    if (state, letter) in self.states:
                        new_states.add(self.states[(state, letter)])
                    if (state, 'w') in self.states:  # All ASCII characters
                        new_states.add(self.states[(state, 'w')])

                # Check if we have reached final states and save the locations
                for state in new_states:
                    if state in self.final_states:
                        word = self.final_states[state]
                        occurrences[word].append((line_idx, col_idx - len(word) + 1))  # Start of the word

                path.append((letter, new_states))
                current_states = new_states  # Update the current states

        # Display the complete path of the string
        print("\nComplete path of the string:")
        for letter, states in path:
            print(f"'{letter}' -> {['S'+str(state) for state in states]}")

        # Display the total number of occurrences and locations
        print("\nTotal number of occurrences and locations:")
        for word, locations in occurrences.items():
            print(f"{word}: {len(locations)} occurrences")
            for line, column in locations:
                print(f"  - Line {line}, Column {column}")
        return occurrences


def main():
    # Read words from the user
    words = input("Enter the words, separated by space: ").split()
    filename = 'string.txt'

    # Read file content
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()  # Read the entire string from the file
    except FileNotFoundError:
        print("File not found.")
        return

    # Initialize DFA
    dfa = DFA(words)

    # Display the set of states
    # print("\nSet of states:")
    # print(dfa.all_states)
    
    # Display transitions
    print("\nTransitions:")
    for (state, letter), next_state in dfa.states.items():
        print(f"(S{state}, '{letter}') -> S{next_state}")

    # Display final states
    print("\nFinal states:")
    print('{', end="")
    for finstate in dfa.final_states:
        print(f"S{finstate}", end=",") if finstate != list(dfa.final_states)[-1] else print(f"S{finstate}" + '}')
  
    # Simulate DFA on the string read from the file
    dfa.simulate_complete(content)


if __name__ == "__main__":
    main()
