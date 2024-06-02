def read_input_file(input_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    transitions = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith(";"):
            transitions.append(line.split())
        else:
            machine_type = line.split(';')[1]
    
    return transitions, machine_type

def add_transitions(transition, symbols, updated_transitions):
    current_state, current_symbol, new_symbol, direction, new_state = transition
    updated_transitions.add(f"{current_state} # # r shift_{current_state}")
    for i in symbols:
        updated_transitions.add(f"shift_{current_state} {i} _ r {current_state}_aux_W_{i}")
        for j in symbols:
            updated_transitions.add(f"{current_state}_aux_W_{i} {j} {i} r {current_state}_aux_W_{j}")
            updated_transitions.add(f"{current_state}_aux_W_{i} $ {i} r aux_F_{current_state}")
            updated_transitions.add(f"aux_F_{current_state} _ $ l aux_I_{current_state}")
            updated_transitions.add(f"aux_I_{current_state} * * l aux_I_{current_state}")
            updated_transitions.add(f"aux_I_{current_state} # # r {current_state}")

def S_to_I(transitions):

    #antes de comecar o processamento, vai pra esq colocando simbolo pra indicar comeco e retorna com cabecote pra dir
    initial_transitions = ["0 * * l 0", "0 _ # r q0"]

    updated_transitions = set()

    for transition in transitions:
        current_state, current_symbol, new_symbol, direction, new_state = transition

        if current_state == '0' and new_state == current_state:
            updated_transitions.add(f"q0 {current_state} {new_symbol} {direction} q0")

        elif current_state == '0':
            updated_transitions.add(f"q0 {current_symbol} {new_symbol} {direction} {new_state}")

        elif new_state == '0':
            updated_transitions.add(f"{current_state} {current_symbol} {new_symbol} {direction} q0")

        else:
            updated_transitions.add(f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}")

        updated_transitions.add(f"{current_state} # # r {current_state}")
                
    return initial_transitions + list(updated_transitions)

def I_to_S(transitions):

    #antes de comecar o processamento, desloca tudo 1 celula pra dir e insere # a esq e $ a dir, posiciona o cabecote no primeiro simbolo de entrada
    initial_transitions = ["0 0 # r aux0", "0 1 # r aux1", "aux0 0 0 r aux0", "aux0 1 0 r aux1", "aux0 _ 0 r qf", "aux1 0 1 r aux0", "aux1 1 1 r aux1", "aux1 _ 1 r qf", "qf _ $ l qf", "qf * * l qf", "qf # # r q0"]

    updated_transitions = set()
    states = set()
    states.add('q0')
    symbols = set()

    for transition in transitions:
        current_state, current_symbol, new_symbol, direction, new_state = transition
        symbols.add(current_symbol)
        symbols.add(new_symbol)

    for transition in transitions:
        current_state, current_symbol, new_symbol, direction, new_state = transition
        states.add(current_state) 
        states.add(new_state)

        if current_state == '0' and new_state == current_state:
            updated_transitions.add(f"q0 {current_symbol} {new_symbol} {direction} q0")

        elif current_state == '0':
            updated_transitions.add(f"q0 {current_symbol} {new_symbol} {direction} {new_state}")

        elif new_state == '0':
            updated_transitions.add(f"{current_state} {current_symbol} {new_symbol} {direction} q0")

        if current_symbol == '_':
            if direction == 'l' and new_symbol == '_' and current_state == '0':
                updated_transitions.add(f"q0 {current_symbol} {new_symbol} {direction} {new_state}")
                updated_transitions.add(f"q0 $ $ {direction} {new_state}")
            elif direction == 'l' and new_symbol == '_':
                updated_transitions.add(f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}")
                updated_transitions.add(f"{current_state} $ $ {direction} {new_state}")
            elif direction == 'l' and new_symbol != '_':
                updated_transitions.add(f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}")
                updated_transitions.add(f"{current_state} $ _ r qf_{current_state}")
                updated_transitions.add(f"qf_{current_state} _ $ l {current_state}")

            add_transitions(transition, symbols, updated_transitions)

        if current_state != '0' and new_state != '0':
            updated_transitions.add(f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}")

    return initial_transitions + list(updated_transitions)

def write_output_file(output_file, transitions):
    with open(output_file, 'w') as outfile:
        print("traduzido")
        for transition in transitions:
            outfile.write(transition + '\n')

def main(input_file, output_file):
    transitions, machine_type = read_input_file(input_file)
    if machine_type == 'S':
        updated_transitions = S_to_I(transitions)
    else:
        updated_transitions = I_to_S(transitions)

    write_output_file(output_file, updated_transitions)


main('sameamount10.in', 'sameamount10.out')