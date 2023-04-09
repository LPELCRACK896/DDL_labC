from AFD import AFD
from AFN import AFN
class AFD_TEMP():
    def __init__(self, alphabet, states, start_state, transitions, accepting_states):
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.transitions = transitions
        self.accepting_states = accepting_states
    

    def to_AFD(self):
        new_transitions = {}
        
        for state, transitions in self.transitions.items():
            new_state_transitions = {}
            
            for transition, next_state in transitions.items():
                new_transition = str(transition)
                
                new_state_transitions[new_transition] = next_state
            
            new_transitions[state] = new_state_transitions
        
        return AFD(self.start_state, self.alphabet, self.states, self.accepting_states, new_transition)
def regex_to_afd(regex) -> AFD:
    """Converts a regular expression to an AFD"""
    # Define a node class for the syntax tree
    class Node():
        def __init__(self, value=None, left=None, right=None):
            self.value = value
            self.left = left
            self.right = right
            self.followpos = set()

    # Define the nullable, firstpos, lastpos, and followpos functions
    def nullable(node):
        if node.value == None:
            return False
        elif node.value == "epsilon":
            return True
        elif node.value == "|":
            return nullable(node.left) or nullable(node.right)
        elif node.value == ".":
            return nullable(node.left) and nullable(node.right)
        elif node.value == "*":
            return True

    def firstpos(node):
        if node.value == None:
            return set()
        elif node.value.isalpha():
            return {node}
        elif node.value == ".":
            if nullable(node.left):
                return firstpos(node.left) | firstpos(node.right)
            else:
                return firstpos(node.left)
        elif node.value == "|":
            return firstpos(node.left) | firstpos(node.right)
        elif node.value == "*":
            return firstpos(node.left)

    def lastpos(node):
        if node.value == None:
            return set()
        elif node.value.isalpha():
            return {node}
        elif node.value == ".":
            if nullable(node.right):
                return lastpos(node.left) | lastpos(node.right)
            else:
                return lastpos(node.right)
        elif node.value == "|":
            return lastpos(node.left) | lastpos(node.right)
        elif node.value == "*":
            return lastpos(node.left)

    def followpos(node):
        if node.value == "*":
            for pos in lastpos(node.left):
                pos.followpos |= firstpos(node.left)
        elif node.value == ".":
            for pos in lastpos(node.left):
                pos.followpos |= firstpos(node.right)
        return

    # Build the syntax tree using the Shunting Yard algorithm
    precedence = {"*": 3, ".": 2, "|": 1}
    stack = []
    output = []
    for c in regex:
        if c.isalpha():
            output.append(Node(c))
        elif c == "(":
            stack.append(c)
        elif c == ")":
            while stack and stack[-1] != "(":
                output.append(Node(stack.pop()))
            stack.pop()
        else:
            while stack and stack[-1] != "(" and precedence[c] <= precedence[stack[-1]]:
                output.append(Node(stack.pop()))
            stack.append(c)
    while stack:
        output.append(Node(stack.pop()))

    # Set the followpos for each position in the syntax tree
    root = output.pop()
    for node in reversed(list(output)):
        if node.value == "*":
            node.left.followpos = set()
            followpos(node)
        elif node.value == ".":
            followpos(node)
        elif node.value == "|":
            followpos(node)

    # Convert the syntax tree to an AFD
    alphabet = set()
    states = []
    state_index = {}
    start_state = frozenset(firstpos(root))
    states.append(start_state)
    state_index[start_state] = 0
    next_index = 1
    unmarked_states = [start_state]
    transitions = {}
    while len(unmarked_states) > 0:
        state = unmarked_states.pop()
        for node in state:
            if node.value.isalpha():
                alphabet.add(node.value)
                for pos in node.followpos:
                    next_state = frozenset(firstpos(pos))
                    if next_state not in state_index:
                        states.append(next_state)
                        state_index[next_state] = next_index
                        next_index += 1
                        unmarked_states.append(next_state)
                    if (state_index[state], node.value) not in transitions:
                        transitions[(state_index[state], node.value)] = set()
                    transitions[(state_index[state], node.value)].add(state_index[next_state])
    accepting_states = set(state_index[state] for state in states if any(node.value == "end" for node in state))
    afd: AFD = AFD_TEMP(alphabet, states, start_state, transitions, accepting_states)
    return afd
from regex_to_posfix import infix_to_posfix
from regex_to_afn import generate_afn_from_posfix
def regex_to__afd(regex)-> AFD:
    posfix, error, alphabet = infix_to_posfix(regex)
    if  error:
       return "Error on regex" 
    afn: AFN = generate_afn_from_posfix(posfix, alphabet)
    afn.find_cerradura()
    afd = afn.to_afd()
    afd.rename_states()
    return afd