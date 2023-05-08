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
        P = [set(self.estados_de_aceptacion), set(self.estados) - set(self.estados_de_aceptacion)]

        while True:
            P_new = []
            for partition in P:
                partition_dict = {}
                for state in partition:
                    key = tuple(sorted((next_state, symbol) for symbol, next_state in self.transitions[state].items() if next_state is not None))
                    partition_dict.setdefault(key, set()).add(state)
                P_new.extend(partition_dict.values())

            if P_new == P:
                break
            else:
                P = P_new

        new_states = [''.join(sorted(group)) for group in P]
        new_transitions = {}

        for group in P:
            group_key = new_states[P.index(group)]
            for symbol in self.alfabeto:
                next_state = self.transitions[list(group)[0]].get(symbol)
                if next_state:
                    next_group = next((g for g in P if next_state in g), None)
                    new_transitions.setdefault(group_key, {})[symbol] = new_states[P.index(next_group)]

        new_estado_inicial = next(new_states[P.index(g)] for g in P if self.estado_inicial in g)
        new_estados_de_aceptacion = [new_states[P.index(g)] for g in P if set(g) & set(self.estados_de_aceptacion)]

        return AFD(new_estado_inicial, self.alfabeto, new_states, new_estados_de_aceptacion, new_transitions)

    
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
