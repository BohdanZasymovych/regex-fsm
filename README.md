# Regular Expression Finite State Machine

A Python implementation of a Finite State Machine (FSM) for processing regular expressions. The implementation creates a non-deterministic finite automaton (NFA) from a regex pattern and checks whether input strings match that pattern.

## Features

This regex engine supports:

- Basic character matching (e.g., "abc" matches exactly "abc")
- Wildcard character "." (matches any single character)
- Repetition operators:
  - "*" (zero or more occurrences)
  - "+" (one or more occurrences)
- Character classes:
  - Basic sets: `[abc]` (matches any of a, b, or c)
  - Character ranges: `[a-z]` (matches any lowercase letter)
  - Negated classes: `[^abc]` (matches any character except a, b, or c)

## How It Works

The FSM implementation uses several state types:
- **StartState**: The initial state of the automaton
- **AsciiState**: Accepts a specific ASCII character
- **DotState**: Accepts any ASCII character (implements the "." wildcard)
- **CharClassState**: Accepts characters based on inclusion or exclusion from a set

The matching algorithm follows standard NFA principles with epsilon transitions, allowing for powerful pattern matching capabilities.

## Project Structure

- **regex.py**: Core implementation of the RegexFSM class
- **visualization_fsm_automata.py**: Visualization utilities for the finite state machine
- **test_regex.py**: Unit tests for the regex implementation
