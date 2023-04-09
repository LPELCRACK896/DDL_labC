
class Instruction():

    def __init__(self, type, name, dicc_data, list_data) -> None:
        self.type = type
        self.name = name
        self.dicc_data = dicc_data
        self.list_data = list_data

def read_yalex(yalex_file):
    instructions = {}
    
    prelines = ["let", "rule"]
    special_prelines = ["|"]
    other_prelines = ["", " ", "\n", "\t"]
    waiting_first_rule = False 
    expects_rule = False
    pending_rule = None
    tokens = []
    rules = {}
    with open(yalex_file, 'r') as file:
        i = 0
        lines = file.readlines()
        error = None
        while not error and i<len(lines):
            line = lines[i]
            line_split = line.split(" ")
            pref = line_split[0]
            accepted_pref = False
            pref_disp = None
            j = 0
            while not accepted_pref and j<len(line_split) and not error:
                pref = line_split[j]
                if not (pref==" " or pref==" " or pref=="\t"):
                    if pref=="\n":
                        accepted_pref = True
                        pref_disp = "skip"
                    elif pref=="let" or pref=="rule":
                        accepted_pref = True
                        pref_disp = pref
                    else:
                        if waiting_first_rule:
                            accepted_pref = True
                            pref_disp = "first_rule"
                        elif expects_rule:
                            if pref=="|":
                                accepted_pref = True
                                pref_disp = "extra_rule"
                j += 1
            
            if not error:
                if accepted_pref:
                    if pref_disp != "skip":
                        rest_line = line_split[j:]
                        if pref_disp == "let":
                            
                            print(0)
                        elif pref_disp == "rule":
                            pass
                        elif pref_disp == "first_rule":
                            pass
                        elif pref_disp == "extra_rule":
                            pass

                else: 
                    error = f"Syntaxis error: Unexpected line format ln: {i}. \"{line}\""
            i += 1
        if error:
            print(error)


def yalex_let():
    pass

def yalex_rule():
    pass

def yalex_to_regex(yalex, equivalencias_actuales):
    forbidden_simbols = [
        '+',
        '*',
        '|',
        '?'
    ]
    equivalencias = equivalencias_actuales
    for char in yalex: 
        pass


if __name__ == "__main__":
    filename = "yalex.txt"
    read_yalex(filename)    

