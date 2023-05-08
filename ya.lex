
let delimitador = [' ''\t''\n']
let espacioEnBlanco = delimitador+
let digito = ['0'-'9']
let numero = '-'?digito+
let letra = ['a'-'Z''A'-'Z']

rule tokens = 
  espacioEnBlanco {}
  | identificador	{ print("Identificador\n") }
  | numero			{ print("Número\n") }
  | '+'				{ print("Operador de suma\n") }
  | '*'				{ print("Operador de multiplicación\n") }
  | '='				{ print("Operador de asignación\n") }