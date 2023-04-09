from regex_to_posfix import infix_to_posfix
from regex_to_afn import generate_afn_from_posfix
def main():
    finish = False
    while not finish:
        regex = input("Ingresa expresion regex: ")
        posfix, err, alphabet = infix_to_posfix(regex)
        if(err):
            print(err.name)
            print(err.details)
        else:
            print(f"Posfix: {posfix}")
            generate_afn_from_posfix(posfix, alphabet).draw_afn()
        finish = input("¿Desea salir? (s/n)").lower()=="s" 
if __name__ == "__main__": 
    main()