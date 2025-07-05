OPERADORES_ARITMETICOS = {'+', '-', '*', '/', '^'}
OPERACIOENES_COMPARACION = {'<', '<=', '>', '>=', '=', '<>'}

def contar_operaciones(tokens):
    total = 0
    i = 0
    longitud = len(tokens)

    while i < longitud:
        t = tokens[i]
        if (i+1 < longitud) and tokens[i+1] == '[':
            total += 1
            i += 2

            while i < longitud and tokens[i] != ']':
                subexpr = []
                while i < longitud and tokens[i] != ',' and tokens[i] != ']':
                    subexpr.append(tokens[i])
                    i += 1
                if subexpr:
                    total += contar_operaciones(subexpr)
                if i < longitud and tokens[i] == ',':
                    i += 1
            i += 1  # Saltar el ']'
            continue

        if (i+1 < longitud) and tokens[i+1] == '(':
            total += 1
            i += 2
            paren_level = 1

            while i < longitud and paren_level > 0:
                if tokens[i] == '(':
                    paren_level += 1
                elif tokens[i] == ')':
                    paren_level -= 1
                i += 1
            continue

        if t in OPERADORES_ARITMETICOS:
            total += 1
            i += 1
            continue
        if t in OPERACIOENES_COMPARACION:
            total += 1
            i += 1
            continue

        if t.isidentifier() or t.replace('.', '', 1).isdigit():
            total += 1
            i += 1
            continue
        if t in ('(', ')', '[', ']'):
            total += 1
            i += 1
            continue

        if t == ',':
            i += 1
            continue
        
        i  += 1  # Saltar cualquier otro token desconocido

    return total
