#!/usr/bin/env python3
import sys

STATE_DIAGRAM_QUERY = 'Which Turing machine (.txt) would you like to run? '
NUMBER_INPUT_QUERY  = 'Argument to Turing machine program (positive ints only): '
OUTPUT_STATEMENT    = 'The final answer is:' 

START_STATE         = 'S1'
END_STATE           = 'Q'
LEFT                = 'L'
RIGHT               = 'R'
STAY                = '-'

class transition:
	# represents transition arrow in state diagram
	def __init__(self, state, symbol, direction):
		self.state = state
		self.symbol = symbol
		self.direction = direction

def read_state_diagram_from_file(f):
	state_diagram = {}
	for line in f:
		x = line.strip().replace(' ', '').split(',')
		state_diagram[(x[0], int(x[1]))] = transition(x[2], int(x[3]), x[4])
	return state_diagram

def load_state_diagram():
	if len(sys.argv) >= 2:
		f = open(sys.argv[1])
	else:
		f = open(input(STATE_DIAGRAM_QUERY))
	state_diagram = read_state_diagram_from_file(f)
	f.close()
	return state_diagram

def initialize_tape():
	number_input = int(input(NUMBER_INPUT_QUERY))
	tape = {}
	for i in range(number_input + 1):
		tape[i] = 1
	return tape

def read_symbol(tape, index):
	return tape.setdefault(index, 0)

def read_output(tape, index):
	print(OUTPUT_STATEMENT, sum(tape.values())) 
	
def move_head(index, direction):
	if direction == LEFT:
		index -= 1
	elif direction == RIGHT:
		index += 1
	else:
		pass 
	return index

def move(tape, state_diagram, state, index):
	current_symbol = read_symbol(tape, index)
	transition_triple = state_diagram.setdefault((state, current_symbol), 
                                                     transition(END_STATE, current_symbol, STAY))
	state = transition_triple.state
	tape[index] = transition_triple.symbol
	index =  move_head(index, transition_triple.direction)	
	return (state, index)

def run(tape, state_diagram):
	state = START_STATE
	index = 0
	while state != END_STATE:
		state, index = move(tape, state_diagram, state, index)
	return index

state_diagram = load_state_diagram()
tape = initialize_tape()
index = run(tape, state_diagram)
read_output(tape, index)
