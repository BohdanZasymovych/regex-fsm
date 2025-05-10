"""regex.py"""
from __future__ import annotations


class State:
    """
    Basic class for state in FSM
    """
    def __init__(self, state_id: int) -> None:
        """
        constructor for state
        """
        self.__id = state_id
        self.next_states: set[State] = set()
        self.epsilon_transition_states: set[State] = set()
        self.is_accept_state: bool = False

    def add_loop(self) -> None:
        """
        function adds loop to current state
        """
        self.next_states.add(self)

    def accepts(self, char: str) -> bool:
        """
        function checks whether occured character is handled by the current ctate
        """
        if isinstance(self, AsciiState):
            return self.char == char
        if isinstance(self, DotState):
            return char.isascii()
        return False

    def add_next_state(self, state: State, epsilon_transition: bool=False) -> None:
        """
        function adds next state to current state
        """
        if epsilon_transition:
            self.epsilon_transition_states.add(state)
        else:
            self.next_states.add(state)

    def get_next_states(self, next_char: str) -> set[State]:
        """
        function returns set of next states after transition by given character
        """
        nxt_states = set()
        for next_state in self.next_states:
            if next_state.accepts(next_char):
                nxt_states.add(next_state)
        return nxt_states

    def epsilon_closure(self) -> set[State]:
        """
        function returns set of states reachable from current state by epsilon transitions
        """
        closure = set()
        closure.add(self)
        for state in self.epsilon_transition_states:
            closure.update(state.epsilon_closure())
        return closure

    def __hash__(self):
        return hash(self.__id)

class StartState(State):
    """
    state for start state
    """


class DotState(State):
    """
    state for "." character (any character accepted)
    """


class AsciiState(State):
    """
    state for alphabet letters or numbers
    """
    def __init__(self, state_id: int, char: str) -> None:
        super().__init__(state_id)
        self.char: str = char


class CharClassState(State):
    """
    State for character class [abc], [a-z], etc.
    """
    def __init__(self, state_id: int, chars: set, is_negated: bool):
        super().__init__(state_id)
        self.chars: set = chars
        self.is_negated: bool = is_negated

    def accepts(self, char):
        """
        function checks whether occured character is handled by the current state
        """
        if self.is_negated:
            return char.isascii() and char not in self.chars

        return char in self.chars


class RegexFSM:
    """
    Finite State Machine for regex
    """
    def __init__(self, regex_expr: str) -> None:
        self.start_state = StartState(0)
        self.__init_machine(regex_expr)

        self.__start_states: set[State] = self.start_state.epsilon_closure()
        self.__cur_states: set[State] = self.__start_states

    def __parse_char_class(self, regex_expr: str, i: int) -> tuple[set, bool, int]:
        """
        function parses character class
        """
        char_set = set()
        is_negated = False

        if regex_expr[i] == "^":
            is_negated = True
            i += 1

        while i < len(regex_expr) and regex_expr[i] != "]":

            if i+2 < len(regex_expr) and regex_expr[i+1] == "-":
                start_char = regex_expr[i]
                end_char = regex_expr[i+2]
                char_set.update(chr(c) for c in range(ord(start_char), ord(end_char)+1))
                i += 3
                continue

            char_set.add(regex_expr[i])
            i += 1

        return char_set, is_negated, i

    def __init_machine(self, regex_expr: str) -> None:
        """
        function initializes FSM
        """
        prev_state = self.start_state

        i, state_id = 0, 1
        while i < len(regex_expr):
            char = regex_expr[i]

            if char in ("*", "+"):
                i += 1
                continue

            if char == ".":
                cur_state = DotState(state_id)
                state_id += 1
            elif char == "[":
                char_set, is_negated, i = self.__parse_char_class(regex_expr, i+1)
                cur_state = CharClassState(state_id, char_set, is_negated)
                state_id += 1
            elif char.isascii():
                cur_state = AsciiState(state_id, char)
                state_id += 1
            else:
                raise AttributeError(f"Character '{char}'' is not supported")

            next_char = regex_expr[i+1] if i+1 < len(regex_expr) else None

            match next_char:
                case "*":
                    cur_state.add_loop()
                    if prev_state is not None:
                        prev_state.epsilon_transition_states.add(cur_state)
                case "+":
                    cur_state.add_loop()
                    if prev_state is not None:
                        prev_state.next_states.add(cur_state)
                case _:
                    if prev_state is not None:
                        prev_state.next_states.add(cur_state)

            if i == len(regex_expr)-1 or (i == len(regex_expr)-2 and next_char in ("+", "*")):
                cur_state.is_accept_state = True

            prev_state = cur_state
            i += 1

    def __update_cur_states(self, char: str) -> None:
        """
        function updates current states
        """
        new_states = set()
        for state in self.__cur_states:
            next_states = state.get_next_states(char)

            for next_state in next_states:
                new_states.update(next_state.epsilon_closure())

        self.__cur_states = new_states

    def __reset_machine(self) -> None:
        """
        function resets FSM
        """
        self.__cur_states = self.__start_states

    def check_string(self, string: str) -> bool:
        """
        checks whether string is accepted by FSM
        """
        if self.start_state is None:
            return False

        for char in string:
            self.__update_cur_states(char)

        for state in self.__cur_states:
            if state.is_accept_state:
                self.__reset_machine()
                return True

        self.__reset_machine()
        return False


if __name__ == "__main__":
    regex_pattern = "[a-c]*4.+hi"
    from visualization_fsm_automata import visualize_regex_fsm

    regex_compiled = RegexFSM(regex_pattern)
    visualize_regex_fsm(regex_compiled, regex_pattern+"_automata")

    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))  # True
    print(regex_compiled.check_string("meow"))  # False
