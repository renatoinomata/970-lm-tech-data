# Arquivo de funções:

def soma(a, b):
    try:
        soma = a + b
        return soma
    except TypeError:
        print(f'O input "a" e "b" devem ser numéricos, recebido a = {a}, tipo = {type(a)} e b = {b}, tipo = {type(b)}')
    
