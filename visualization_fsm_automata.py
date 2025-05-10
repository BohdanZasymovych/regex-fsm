"""Visualization of Regex FSM"""
import graphviz
from regex import RegexFSM, State


def visualize_regex_fsm(fsm: RegexFSM, output_file: str = "regex_fsm"):
    """
    Visualizes a RegexFSM as a directed graph.
    
    Args:
        fsm: The compiled RegexFSM object
        output_file: The filename to save the visualization (without extension)
    """
    # Create a directed graph with horizontal layout (left to right)
    dot = graphviz.Digraph(comment='Regex FSM')
    dot.attr(rankdir='LR')  # Set direction to Left-to-Right
    
    # Track visited states to avoid duplicates and infinite recursion
    visited_states = set()
    
    def add_state_to_graph(state: State):
        """Recursively add states and transitions to the graph"""
        if state in visited_states:
            return
        visited_states.add(state)
        
        # Create label based on state type
        state_class = state.__class__.__name__
        
        if state_class == "AsciiState":
            label = f"{state._State__id}: '{state.char}'"
        elif state_class == "DotState":
            label = f"{state._State__id}: '.'"
        elif state_class == "StartState":
            label = f"{state._State__id}: START"
        else:
            label = f"{state._State__id}"
        
        # Mark accept states with double circle
        shape = "doublecircle" if state.is_accept_state else "circle"
        
        # Add the state to the graph
        dot.node(str(state._State__id), label, shape=shape)
        
        # Add normal transitions with appropriate labels
        for next_state in state.next_states:
            # Check class name instead of using isinstance
            next_class = next_state.__class__.__name__
            
            if next_class == "AsciiState":
                trans_label = f"'{next_state.char}'"
            elif next_class == "DotState":
                trans_label = "any ascii"
            else:
                trans_label = "transition"
                
            dot.edge(str(state._State__id), str(next_state._State__id), label=trans_label)
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
