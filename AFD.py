import graphviz

class AFD():

    def __init__(self, estado_inicial, alfabeto = [], estados = [], estados_de_aceptacion = [], transitions = {}, estado_final = None) -> None:
        
        self.estado_final = estado_final
        self.alfabeto: list = alfabeto #Aceptado como trancisiones (nombre de arista, digamos)
        self.estados: list = estados #Estados (vertices)
        self.estado_inicial = estado_inicial
        self.estados_de_aceptacion: list = [item for item in estados_de_aceptacion if item in self.estados]
        self.transitions: dict = transitions # {state: {symbol: state, ..., symbol: state}}


    def draw_afd(self):
        afn = graphviz.Digraph(format='pdf')
        afn.graph_attr['rankdir'] = 'LR'
        afn.node('start', style='invis')
        nodos = []
        for state in self.estados:
            if state==self.estado_inicial:
                afn.node(state, shape='diamond', color='red')
                nodos.append((state, "inicial"))
            elif state not in self.estados_de_aceptacion:
                afn.node(state)
                nodos.append((state, "normal"))
            else:
                afn.node(state, shape='doublecircle')
                nodos.append((state, "aceptacion"))

        grafo = []
        for state in self.transitions:
            trans = self.transitions.get(state)
            for symbol in trans:
                if symbol !='ε':
                    next_state = trans.get(symbol)
                    afn.edge(state, next_state, label=symbol)

        afn.render('afd', view=True)


    def simulacion(self, w, show_path = False):
        path = []
        curr_state = self.estado_inicial
        for char in w:
            path.append(curr_state)
            if char not in self.alfabeto:
                print("Cadena contiene caracteres que no pertenecen al alfabeto definido")
                return False
            curr_state = self.transitions.get(curr_state).get(char)
        path.append(curr_state)
        if show_path:
            path = "->".join(path)
            print(path)
        return curr_state in self.estados_de_aceptacion

    def minimize(self):
        P = [self.estados_de_aceptacion, list(set(self.estados) - set(self.estados_de_aceptacion))]

        while True:
            P_prime = []

            for group in P:
                d = {}

                for state in group:
                    for symbol in self.alfabeto:
                        next_state = self.transitions[state].get(symbol, None)
                        if next_state is not None:
                            next_group = None
                            for i, g in enumerate(P):
                                if next_state in g:
                                    next_group = i
                                    break
                            if next_group is None:
                                next_group = len(P_prime)
                                P_prime.append([next_state])
                            d.setdefault(next_group, []).append(state)
                for next_group, states in d.items():
                    if len(states) < len(P[next_group]):
                        P[next_group] = states
                    elif len(states) > len(P[next_group]):
                        P[next_group] = states

            for state in self.estados:
                if not any(state in group for group in P_prime):
                    P_prime.append([state])

            if P == P_prime:
                break
            else:
                P = P_prime
        new_states = [f"{''.join(group)}" for group in P]
        new_transitions = {}
        for group in P:
            for symbol in self.alfabeto:
                next_state = None
                for state in group:
                    if next_state is None:
                        next_state = new_states[P.index([self.transitions[state].get(symbol, None) or self.estado_final])]
                    else:
                        assert next_state == new_states[P.index([self.transitions[state].get(symbol, None) or self.estado_final])], \
                            f"Different next states for symbol {symbol} in group {group} and state {state}"
                new_transitions.setdefault(new_states[P.index(group)], {})[symbol] = next_state
        new_estado_inicial = new_states[P.index([self.estado_inicial])]
        new_estado_final = None
        new_estados_de_aceptacion = []
        for group in P:
            if self.estado_final in group:
                new_estado_final = new_states[P.index(group)]
                new_estados_de_aceptacion.append(new_estado_final)
            if set(group) & set(self.estados_de_aceptacion):
                new_estados_de_aceptacion.append(new_states[P.index(group)])
        return AFD(new_estado_inicial, self.alfabeto, new_states, new_estados_de_aceptacion, new_transitions, new_estado_final)
    
    def rename_states(self):
        abcdef = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if len(self.estados)>len(abcdef):
            print("uuu")
            return
        new_names = { self.estados[i] : abcdef[i] for i in range(len(self.estados)) }
        new_acc = [new_names.get(stt) for stt in self.estados_de_aceptacion]
        new_stt = [new_names.get(stt) for stt in self.estados]
        new_trans = {}
        for stt_i in self.transitions:
            trans = {}
            state_transitions = self.transitions.get(stt_i) 
            for symbol in state_transitions: trans[symbol] = new_names.get(state_transitions.get(symbol))
            new_trans[new_names.get(stt_i)] = trans

        self.transitions = new_trans
        self.estados = new_stt
        self.estados_de_aceptacion = new_acc
        self.estado_inicial = new_names.get(self.estado_inicial)
        if self.estado_final: self.estado_final = new_names.get(self.estado_final)
