import re

# Palabras clave del pseudocódigo
palabras_clave = [
    "Clase", "Funcion", "Mientras", "hacer", "Para", "desde", "hasta", "Si", "Entonces",
    "Sino", "retornar", "fClase", "fFuncion", "fMientras", "fPara", "fSi"
]

# Operadores y símbolos relevantes
operadores = {
    "<=": "MENOR_IGUAL",
    ">=": "MAYOR_IGUAL",
    "<>": "DIFERENTE",
    "<-": "ASIGNACION",
    "<": "MENOR",
    ">": "MAYOR",
    "=": "IGUAL",
    "+": "SUMA",
    "-": "RESTA",
    "*": "MULTIPLICACION",
    "/": "DIVISION",
    "^": "POTENCIA",
    ".": "PUNTO",
    "&&": "Y",
    "||": "O"
}

# Ordenar operadores por longitud descendente (compuestos primero)
operadores_ordenados = sorted(operadores.keys(), key=lambda x: -len(x))

# Construir la lista de patrones, colocando los operadores primero
token_specification = []
for op in operadores_ordenados:
    token_specification.append( (operadores[op], re.escape(op)) )

token_specification += [
    ('NUMERO',       r'\d+(\.\d+)?'),
    ('IDENT',        r'[A-Za-z_][A-Za-z0-9_]*'),
    ('PAREN_IZQ',    r'\('),
    ('PAREN_DER',    r'\)'),
    ('COMA',         r','),
    ('CORCHETE_IZQ', r'\['),
    ('CORCHETE_DER', r'\]'),
    ('LLAVE_IZQ', r'\{'),
    ('LLAVE_DER', r'\}'),
    ('NUEVA_LINEA',  r'\n'),
    ('ESPACIO',      r'[ \t]+'),
    ('DESCONOCIDO',  r'.'),
]

# Crear el regex maestro
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
palabras_clave_set = set(pc.lower() for pc in palabras_clave)

def tokenizar(texto):
    tokens = []
    for mo in re.finditer(tok_regex, texto):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'ESPACIO':
            continue
        if kind == 'IDENT':
            if value.lower() in palabras_clave_set:
                kind = 'PALABRA_CLAVE'
        tokens.append({'tipo': kind, 'valor': value})
    return tokens
