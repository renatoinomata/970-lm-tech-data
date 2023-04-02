# Importanto a função do arquivo calculadora/__init__.py
import os
import sys
sys.path.insert(0, os.getcwd())
from projetos.calculadora import calcule

# Executando a aplicação
resultado = calcule()
print(f'O resultado é {resultado}')

# Executar o código no terminal com python .../app.py