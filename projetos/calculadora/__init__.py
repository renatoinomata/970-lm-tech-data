# Arquivo __init__

import funcoes as fun

def calcule():
    # Recebendo os inputs de 'a' e 'b'
    input_a = input('Digite um número para "a": ')
    input_b = input('Digite um número para "b": ')

    try:
        a = float(input_a)
        b = float(input_b)
    except:
        return 'Não foi possível converter algum dos valores para numérico.'
    
    # Definindo um dicionário para as operações
    funcoes_dict = {'soma': fun.soma,
                'subtracao': fun.subtracao,
                'divisao': fun.divisao,
                'multiplicacao': fun.multiplicacao,
                '+': fun.soma,
                '-': fun.subtracao,
                '/': fun.divisao,
                '*': fun.multiplicacao,}
    
    # Recebendo o input da operação
    print('Ecolha a operação desejada. Opções válidas:')
    print('soma, subtracao, divisao, multiplicacao, +, -, /, *')
    input_operacao = input('Digite a operação desejada:')

    if input_operacao not in funcoes_dict:
        return 'Operação inválida.'
    
    return funcoes_dict[input_operacao](a, b)