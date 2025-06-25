class Nodo:
    def __init__(self, tipo, props=None, hijos=None):
        self.tipo = tipo
        self.props = props or {}
        self.hijos = hijos or []

    def add_hijo(self, nodo):
        self.hijos.append(nodo)

    def __repr__(self, nivel=0):
        indent = "  " * nivel
        props = []
        for k, v in self.props.items():
            if isinstance(v, list):
                props.append(f"{k}={v}")
            else:
                props.append(f"{k}='{v}'")
        props_str = " " + " ".join(props) if props else ""
        out = f"{indent}{self.tipo}{props_str}\n"
        for hijo in self.hijos:
            out += hijo.__repr__(nivel + 1)
        return out

def calcular_tamano(indices):
    tam = 1
    for idx in indices:
        # Si el índice es vacío (corchetes vacíos), omitirlo
        if len(idx) == 0:
            return None
        if len(idx) == 1 and idx[0].isdigit():
            tam *= int(idx[0])
        else:
            return None  # No es un tamaño fijo (puede ser variable)
    return tam


def parsear(tokens, debug=False):
    i = 0
    stack = []
    root = Nodo("PROGRAMA")
    actual = root

    def show_stack():
        if debug:
            print("  Stack:", [nodo.tipo for nodo in stack])
            print("  Actual:", actual.tipo)
            print("-" * 40)

    while i < len(tokens):
        t = tokens[i]
        if debug:
            print(f"\nToken[{i}]: {t}")

        # CLASE
        if t['tipo'] == 'PALABRA_CLAVE' and t['valor'].lower() == 'clase':
            i += 1
            nombre = tokens[i]['valor']
            nodo = Nodo("CLASE", {'nombre': nombre})
            actual.add_hijo(nodo)
            stack.append(actual)
            actual = nodo
            i += 1
            if debug:
                print(f"Abro CLASE '{nombre}'")
                show_stack()

        # FUNCION
        elif t['tipo'] == 'PALABRA_CLAVE' and t['valor'].lower() == 'funcion':
            i += 1
            nombre = tokens[i]['valor']
            args = []
            if tokens[i+1]['tipo'] == 'PAREN_IZQ':
                i += 2
                while tokens[i]['tipo'] != 'PAREN_DER':
                    if tokens[i]['tipo'] == 'IDENT':
                        args.append(tokens[i]['valor'])
                    i += 1
                    if tokens[i]['tipo'] == 'COMA':
                        i += 1
                i += 1
            nodo = Nodo("FUNCION", {'nombre': nombre, 'args': args})
            actual.add_hijo(nodo)
            stack.append(actual)
            actual = nodo
            if debug:
                print(f"Abro FUNCION '{nombre}' args={args}")
                show_stack()

        # ASIGNACION
        elif t['tipo'] == 'IDENT' and i+1 < len(tokens) and tokens[i+1]['tipo'] == 'ASIGNACION':
            var = t['valor']
            i += 2
            expr = []
            while i < len(tokens) and tokens[i]['tipo'] not in ('NUEVA_LINEA', 'PALABRA_CLAVE', 'PAREN_DER'):
                expr.append(tokens[i]['valor'])
                i += 1
            nodo = Nodo("ASIGNACION", {'var': var, 'expr': expr})
            actual.add_hijo(nodo)
            if debug:
                print(f"ASIGNACION '{var} <- {' '.join(expr)}'")
                show_stack()
                
        # ACCESO, DECLARACION O ASIGNACION DE ARREGLO (SOPORTA MULTIDIMENSIONALES)
        elif t['tipo'] == 'IDENT' and i+1 < len(tokens) and tokens[i+1]['tipo'] == 'CORCHETE_IZQ':
            nombre = t['valor']
            indices = []
            i += 1
            while i < len(tokens) and tokens[i]['tipo'] == 'CORCHETE_IZQ':
                i += 1
                index_expr = []
                while i < len(tokens) and tokens[i]['tipo'] != 'CORCHETE_DER':
                    index_expr.append(tokens[i]['valor'])
                    i += 1
                indices.append(index_expr)
                if i < len(tokens) and tokens[i]['tipo'] == 'CORCHETE_DER':
                    i += 1
            # Si es asignación
            if i < len(tokens) and tokens[i]['tipo'] == 'ASIGNACION':
                i += 1
                # Inicialización con llaves
                if i < len(tokens) and tokens[i]['tipo'] == 'LLAVE_IZQ':
                    i += 1
                    elementos = []
                    while i < len(tokens) and tokens[i]['tipo'] != 'LLAVE_DER':
                        if tokens[i]['tipo'] == 'NUMERO':
                            elementos.append(tokens[i]['valor'])
                        i += 1
                    if i < len(tokens) and tokens[i]['tipo'] == 'LLAVE_DER':
                        i += 1
                    tamano_declarado = calcular_tamano(indices)
                    tamano_elementos = len(elementos)
                    coincide_tamano = None
                    if tamano_declarado is not None:
                        coincide_tamano = (tamano_declarado == tamano_elementos)
                    nodo = Nodo("ASIGNACION_ARREGLO", {
                        'nombre': nombre,
                        'indices': indices,
                        'elementos': elementos,
                        'tamano': tamano_elementos,
                        'coincide_tamano': coincide_tamano
                    })
                    actual.add_hijo(nodo)
                else:
                    # Asignación tradicional
                    expr = []
                    while i < len(tokens) and tokens[i]['tipo'] not in ('NUEVA_LINEA', 'PALABRA_CLAVE', 'PAREN_DER'):
                        expr.append(tokens[i]['valor'])
                        i += 1
                    nodo = Nodo("ASIGNACION_ARREGLO", {
                        'nombre': nombre,
                        'indices': indices,
                        'expr': expr,
                        'tamano': calcular_tamano(indices)
                    })
                    actual.add_hijo(nodo)
            else:
                # Declaración sin asignación
                tamano = calcular_tamano(indices)
                nodo = Nodo("DECLARACION_ARREGLO", {
                    'nombre': nombre,
                    'indices': indices,
                    'tamano': tamano
                })
                actual.add_hijo(nodo)


        # SI
        elif t['tipo'] == 'PALABRA_CLAVE' and t['valor'].lower() == 'si':
            i += 1
            if tokens[i]['tipo'] == 'PAREN_IZQ':
                i += 1
                cond = []
                while tokens[i]['tipo'] != 'PAREN_DER':
                    cond.append(tokens[i]['valor'])
                    i += 1
                i += 1
            else:
                cond = []
                while tokens[i]['valor'].lower() != 'entonces':
                    cond.append(tokens[i]['valor'])
                    i += 1
            if tokens[i]['valor'].lower() == 'entonces':
                i += 1
            nodo = Nodo("SI", {'cond': cond})
            actual.add_hijo(nodo)
            stack.append(actual)
            actual = nodo
            if debug:
                print(f"Abro SI cond={cond}")
                show_stack()

        # SINO
        elif t['tipo'] == 'PALABRA_CLAVE' and t['valor'].lower() == 'sino':
            nodo = Nodo("SINO")
            stack[-1].add_hijo(nodo)
            actual = nodo
            i += 1
            if debug:
                print("Abro SINO")
                show_stack()

        # MIENTRAS
        elif t['tipo'] == 'PALABRA_CLAVE' and t['valor'].lower() == 'mientras':
            i += 1
            if tokens[i]['tipo'] == 'PAREN_IZQ':
                i += 1
                cond = []
                while tokens[i]['tipo'] != 'PAREN_DER':
                    cond.append(tokens[i]['valor'])
                    i += 1
                i += 1
            else:
                cond = []
                while tokens[i]['valor'].lower() != 'hacer':
                    cond.append(tokens[i]['valor'])
                    i += 1
            if tokens[i]['valor'].lower() == 'hacer':
                i += 1
            nodo = Nodo("MIENTRAS", {'cond': cond})
            actual.add_hijo(nodo)
            stack.append(actual)
            actual = nodo
            if debug:
                print(f"Abro MIENTRAS cond={cond}")
                show_stack()

        # PARA
        elif t['tipo'] == 'PALABRA_CLAVE' and t['valor'].lower() == 'para':
            i += 1
            var = tokens[i]['valor']
            i += 1
            if tokens[i]['valor'].lower() == 'desde':
                i += 1
            start = tokens[i]['valor']
            i += 1
            if tokens[i]['valor'].lower() == 'hasta':
                i += 1
            end = tokens[i]['valor']
            i += 1
            if tokens[i]['valor'].lower() == 'hacer':
                i += 1
            nodo = Nodo("PARA", {'var': var, 'desde': start, 'hasta': end})
            actual.add_hijo(nodo)
            stack.append(actual)
            actual = nodo
            if debug:
                print(f"Abro PARA var={var}, desde={start}, hasta={end}")
                show_stack()

        # retornar
        elif t['tipo'] == 'PALABRA_CLAVE' and t['valor'].lower() == 'retornar':
            i += 1
            ret = []
            while i < len(tokens) and tokens[i]['tipo'] not in ('NUEVA_LINEA', 'PALABRA_CLAVE'):
                if tokens[i]['tipo'] != 'COMA':
                    ret.append(tokens[i]['valor'])
                i += 1
            nodo = Nodo("RETORNAR", {'args': ret})
            actual.add_hijo(nodo)
            if debug:
                print(f"RETORNAR {ret}")
                show_stack()

        # LLAMADA_FUNCION
        elif t['tipo'] == 'IDENT' and i+1 < len(tokens) and tokens[i+1]['tipo'] == 'PAREN_IZQ':
            nombre = t['valor']
            i += 2
            args = []
            temp = []
            while tokens[i]['tipo'] != 'PAREN_DER':
                if tokens[i]['tipo'] == 'COMA':
                    if temp:
                        args.append(temp)
                        temp = []
                elif tokens[i]['tipo'] in ('IDENT', 'NUMERO'):
                    temp.append(tokens[i]['valor'])
                i += 1
            if temp:
                args.append(temp)
            i += 1
            nodo = Nodo("LLAMADA_FUNCION", {'nombre': nombre, 'args': args})
            actual.add_hijo(nodo)
            if debug:
                print(f"LLAMADA_FUNCION {nombre} args={args}")
                show_stack()

        # LLAMADA_METODO
        elif (t['tipo'] == 'IDENT' and i+1 < len(tokens) and
              tokens[i+1]['tipo'] == 'PUNTO' and
              tokens[i+2]['tipo'] == 'IDENT' and
              tokens[i+3]['tipo'] == 'PAREN_IZQ'):
            obj = t['valor']
            metodo = tokens[i+2]['valor']
            i += 4
            args = []
            temp = []
            while tokens[i]['tipo'] != 'PAREN_DER':
                if tokens[i]['tipo'] == 'COMA':
                    if temp:
                        args.append(temp)
                        temp = []
                elif tokens[i]['tipo'] in ('IDENT', 'NUMERO'):
                    temp.append(tokens[i]['valor'])
                i += 1
            if temp:
                args.append(temp)
            i += 1
            nodo = Nodo("LLAMADA_METODO", {'obj': obj, 'metodo': metodo, 'args': args})
            actual.add_hijo(nodo)
            if debug:
                print(f"LLAMADA_METODO {obj}.{metodo} args={args}")
                show_stack()

        # CIERRE DE BLOQUE
        elif t['tipo'] == 'PALABRA_CLAVE' and t['valor'].lower().startswith('f'):
            if debug:
                print(f"Cierro bloque '{t['valor']}' y regreso de {actual.tipo} a {stack[-1].tipo if stack else 'VACIO'}")
            actual = stack.pop()
            i += 1
            if debug:
                show_stack()

        else:
            i += 1

    return root

# === Prueba ===
if __name__ == "__main__":
    from pseudogrammar import tokenizar

    pseudocodigo = '''
Clase Prueba
    Funcion inicializar()
        arreglo1[5]
        arreglo2[] <- {1, 2, 3, 4, 5}
        matriz[3][4] <- 0
        datos[8] <- {2, 4, 6, 8, 10, 12, 14, 16}
        x <- 7
        y <- arreglo2[2]
        matriz[1][2] <- x + y
        Para i desde 1 hasta 5 hacer
            suma <- suma + arreglo2[i]
        fPara
        Mientras (x < 10) hacer
            x <- x + 1
        fMientras
        Si (x > y) Entonces
            resultado <- x - y
        Sino
            resultado <- y - x
        fSi
        retornar resultado
    fFuncion

    Funcion operar(a, b)
        temp <- self.inicializar()
        Si (a > b) Entonces
            res <- temp + a
        Sino
            res <- temp + b
        fSi
        retornar res
    fFuncion
fClase

obj <- Prueba()
resultado <- obj.operar(10, 5)
arregloGlobal[3] <- 99
'''
    tokens = tokenizar(pseudocodigo)
    arbol = parsear(tokens, False)
    print(arbol)

#for t in tokens:
#    print(t)
