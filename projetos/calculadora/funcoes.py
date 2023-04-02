# Arquivo de funções:

def soma(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a + b
    else:
        raise TypeError(f'O input "a" e "b" devem ser numéricos, recebido a = {a}, tipo = {type(a)} e b = {b}, tipo = {type(b)}')
    
def subtracao(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a - b
    else:
        raise TypeError(f'O input "a" e "b" devem ser numéricos, recebido a = {a}, tipo = {type(a)} e b = {b}, tipo = {type(b)}')
    
def divisao(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError(f'O input "a" e "b" devem ser numéricos, recebido a = {a}, tipo = {type(a)} e b = {b}, tipo = {type(b)}')  
    
    if b != 0:
        return a / b
    else:
        raise ZeroDivisionError(f'O input "b" deve ser diferente de zero')