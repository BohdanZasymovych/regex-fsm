"""Visualization of Regex FSM"""
from regex import RegexFSM, State, AsciiState, DotState, StartState


def visualize_regex_fsm(fsm: RegexFSM, output_file: str = "regex_fsm"):
    """
    Visualizes a RegexFSM as a directed graph.
    
    Args:
        fsm: The compiled RegexFSM object
        output_file: The filename to save the visualization (without extension)
    """
    # Create a directed graph
    dot = graphviz.Digraph(comment='Regex FSM')
    
    # Track visited states to avoid duplicates and infinite recursion
    visited_states = set()
    
    def add_state_to_graph(state: State):
        """Recursively add states and transitions to the graph"""
        if state in visited_states:
            return
        visited_states.add(state)
        
        # Create label based on state type
        if isinstance(state, AsciiState):
            label = f"{state._State__id}: '{state.char}'"
        elif isinstance(state, DotState):
            label = f"{state._State__id}: '.'"
        elif isinstance(state, StartState):
            label = f"{state._State__id}: START"
        else:
            label = f"{state._State__id}"
        
        # Mark accept states with double circle
        shape = "doublecircle" if state.is_accept_state else "circle"
        
        # Add the state to the graph
        dot.node(str(state._State__id), label, shape=shape)
        
        # Add normal transitions
        for next_state in state.next_states:
            dot.edge(str(state._State__id), str(next_state._State__id))
            add_state_to_graph(next_state)
        
        # Add epsilon transitions (with ε label)
        for eps_state in state.epsilon_transition_states:
            dot.edge(str(state._State__id), str(eps_state._State__id), label="ε")
            add_state_to_graph(eps_state)
    
    # Start from the start state
    add_state_to_graph(fsm.start_state)
    
    # Render the graph
    dot.render(output_file, format='png', cleanup=True)
    print(f"FSM visualization saved to {output_file}.png")
    
    return dot
