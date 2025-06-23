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
Clase Calculadora
    Funcion suma(a, b)
        resultado <- a + b
        retornar resultado
    fFuncion

    Funcion multiplicar(a, b)
        resultado <- 0
        Para i desde 1 hasta b hacer
            resultado <- resultado + a
        fPara
        retornar resultado
    fFuncion

    Funcion operacionCompuesta(x, y)
        Si (x > 10) Entonces
            Si (y < 5) Entonces
                retornar suma(x, y)
            Sino
                retornar multiplicar(x, y)
            fSi
        Sino
            resultado <- suma(x, y)
            Mientras (resultado < 100) hacer
                resultado <- resultado + x
            fMientras
            retornar resultado
        fSi
    fFuncion
fClase

num1 <- 7
num2 <- 4
calc <- Calculadora()

sumaTotal <- calc.suma(num1, num2)
multiTotal <- calc.multiplicar(num1, num2)
resultadoFinal <- calc.operacionCompuesta(num1, num2)

'''
    tokens = tokenizar(pseudocodigo)
    arbol = parsear(tokens, False)
    print(arbol)

#for t in tokens:
#    print(t)
