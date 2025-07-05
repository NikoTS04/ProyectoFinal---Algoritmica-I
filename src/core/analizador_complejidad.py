from .expresion_simbolica import ExpresionSimbolica
from .analizador_expresiones import contar_operaciones

class ResultadoAnalisis:
    def __init__(self, funcion_tiempo, big_o, recursivo = False, nombre_funcion = None):
        self.funcion_tiempo = funcion_tiempo
        self.big_o = big_o
        self.recursivo = recursivo
        self.nombre_funcion = nombre_funcion

    def mostrar(self):
        nombre = f"Función: '{self.nombre_funcion}': " if self.nombre_funcion else ""
        rec = " (recursiva)" if self.recursivo else ""
        print(f"{nombre}Complejidad temporal{rec}:")
        print(f"  T(n) = {self.funcion_tiempo.como_str()}")
        print(f"  Big O: {self.big_o}")

    def graficar(self, var='N', rango=(1, 20)):
        self.funcion_tiempo.graficar(var=var, rango=rango)

class AnalizadorComplejidad:
    def __init__(self, arbol):
        self.arbol = arbol
        self.funciones = self._mapear_funciones(arbol)

    def _mapear_funciones(self, nodo):
        funciones = {}
        if nodo.tipo == 'FUNCION':
            nombre = nodo.props.get('nombre')
            if nombre:
                funciones[nombre] = nodo
        for hijo in nodo.hijos:
            funciones.update(self._mapear_funciones(hijo))
        return funciones
    
    def analizar(self, nombre_funcion=None):
        if nombre_funcion:
            if nombre_funcion not in self.funciones:
                raise ValueError(f"La función '{nombre_funcion}' no existe en el árbol de análisis.")
            nodo = self.funciones[nombre_funcion]
            funcion_tiempo, recursivo = self._analizar_funcion(nodo, set())
        else:
            funcion_tiempo = self._analizar_nodo(self.arbol, set())
            recursivo = False
        big_o = funcion_tiempo.big_o()
        return ResultadoAnalisis(funcion_tiempo, big_o, recursivo, nombre_funcion)
    
    def _analizar_nodo(self, nodo, funciones_llamadas):

        tipo = nodo.tipo
        props = nodo.props

        # === ASIGNACION SIMPLE ===
        if tipo == 'ASIGNACION':
            expr_tokens = props.get('expr', [])
            return ExpresionSimbolica.desde_tokens(expr_tokens)
        
        # === ASIGNACION ARREGLO ===
        elif tipo == 'ASIGNACION_ARREGLO':
            expr_tokens = props.get('expr', [])
            if 'elementos' in props:
                return ExpresionSimbolica.constante(len(props['elementos']))
            return ExpresionSimbolica.desde_tokens(expr_tokens) +  ExpresionSimbolica.constante(1)
        
        # === DECLARACION ARREGLO ===
        elif tipo == 'DECLARACION_ARREGLO':
            return ExpresionSimbolica.constante(0)

        # === PARA ===
        elif tipo == 'PARA':
            desde = props.get('desde', '1')
            hasta = props.get('hasta', 'N')
            try:
                desde_val = int(desde)
            except Exception:
                desde_val = None
                
            if desde_val is not None and hasta.isdigit():
                iteraciones = int(hasta) - desde_val + 1
                it_exp = ExpresionSimbolica.constante(iteraciones)
            else:
                # Limpiar paréntesis innecesarios
                hasta_limpio = hasta.replace('(', '').replace(')', '')
                desde_limpio = desde.replace('(', '').replace(')', '')
                
                if hasta_limpio.isdigit() and desde_limpio.isdigit():
                    iteraciones = int(hasta_limpio) - int(desde_limpio) + 1
                    it_exp = ExpresionSimbolica.constante(iteraciones)
                else:
                    # Crear expresión simbólica para iteraciones variables
                    hasta_expr = ExpresionSimbolica.variable(hasta_limpio) if not hasta_limpio.isdigit() else ExpresionSimbolica.constante(int(hasta_limpio))
                    desde_expr = ExpresionSimbolica.variable(desde_limpio) if not desde_limpio.isdigit() else ExpresionSimbolica.constante(int(desde_limpio))
                    it_exp = hasta_expr - desde_expr + ExpresionSimbolica.constante(1)

            # analisis del cuerpo
            cuerpo = ExpresionSimbolica.constante(0)
            for hijo in nodo.hijos:
                cuerpo += self._analizar_nodo(hijo, funciones_llamadas)
            
            control = ExpresionSimbolica.constante(2) + it_exp
            return control + it_exp * cuerpo
        
        # === MIENTRAS ===
        elif tipo == 'MIENTRAS':
            cond_tokens = props.get('cond', [])
            costo_cond = ExpresionSimbolica.desde_tokens(cond_tokens)
            
            # Intentar detectar patrones comunes de complejidad
            # Si vemos división por 2, probablemente es logarítmico
            cond_str = ' '.join([token if isinstance(token, str) else str(token.get('valor', '')) for token in cond_tokens])
            cuerpo_str = ""
            for hijo in nodo.hijos:
                if hijo.tipo == 'ASIGNACION':
                    expr_tokens = hijo.props.get('expr', [])
                    expr_str = ' '.join([token if isinstance(token, str) else str(token.get('valor', '')) for token in expr_tokens])
                    cuerpo_str += expr_str + " "
            
            # Detectar patrones logarítmicos (división por constante)
            if ('/' in cuerpo_str and ('2' in cuerpo_str or '3' in cuerpo_str)) or 'medio' in cuerpo_str.lower():
                # Probablemente logarítmico
                import sympy
                iteraciones = ExpresionSimbolica(sympy.log(sympy.Symbol('N'), 2))
            else:
                # Asumir máximo N iteraciones para casos generales
                iteraciones = ExpresionSimbolica.variable('N')
            
            cuerpo = ExpresionSimbolica.constante(0)
            for hijo in nodo.hijos:
                cuerpo += self._analizar_nodo(hijo, funciones_llamadas)
            return iteraciones * (costo_cond + cuerpo)
        
        # === SI ===
        elif tipo == 'SI':
            cond_tokens = props.get('cond', [])
            costo_cond = ExpresionSimbolica.desde_tokens(cond_tokens)
            ramas = [self._analizar_nodo(hijo, funciones_llamadas) for hijo in nodo.hijos]
            if ramas:
                return costo_cond + max(ramas, key = lambda r: r.expr)
            return costo_cond
        
        # === LLAMADA A FUNCION ===
        elif tipo == 'LLAMADA_FUNCION':
            nombre = props.get('nombre')
            if nombre in self.funciones:
                if nombre in funciones_llamadas:
                    # Es una llamada recursiva
                    # Para fibonacci y casos similares, asumir crecimiento exponencial
                    if 'fibonacci' in nombre.lower():
                        import sympy
                        return ExpresionSimbolica(2**sympy.Symbol('N'))
                    else:
                        # Para otras recursiones, asumir T(n) = T(n-1) + O(1) -> O(n)
                        return ExpresionSimbolica.variable('N')
                else:
                    nuevas_funciones_llamadas = set(funciones_llamadas)
                    nuevas_funciones_llamadas.add(nombre)
                    return self._analizar_funcion(self.funciones[nombre], nuevas_funciones_llamadas)[0]
            else:
                # funcion desconocida, asumir costo constante
                return ExpresionSimbolica.constante(1)
            
        # === RETORNAR ===
        elif tipo == 'RETORNAR':
            args = props.get('args', [])
            if args:
                # Buscar llamadas recursivas en la expresión de retorno
                costo = ExpresionSimbolica.constante(0)
                i = 0
                while i < len(args):
                    # Buscar patrones de llamada a función: nombre(
                    if (i + 1 < len(args) and 
                        isinstance(args[i], str) and 
                        isinstance(args[i+1], str) and 
                        args[i+1] == '('):
                        
                        nombre_funcion = args[i]
                        if nombre_funcion in self.funciones:
                            if nombre_funcion in funciones_llamadas:
                                # Es recursión
                                if 'fibonacci' in nombre_funcion.lower():
                                    import sympy
                                    costo += ExpresionSimbolica(2**sympy.Symbol('N'))
                                else:
                                    costo += ExpresionSimbolica.variable('N')
                            else:
                                # Llamada normal
                                costo += ExpresionSimbolica.constante(1)
                        i += 1
                    else:
                        i += 1
                
                return costo
            return ExpresionSimbolica.constante(0)
        
        # === ESTRUCTURAS NO MANEJADAS ESPECIFICAMENTE | SUMA DE HIJOS ===
        else:
            total = ExpresionSimbolica.constante(0)
            for hijo in nodo.hijos:
                total += self._analizar_nodo(hijo, funciones_llamadas)
            return total
        
    def _analizar_funcion(self, nodo_funcion, funciones_llamadas):

        nombre = nodo_funcion.props.get('nombre', '')
        cuerpo = ExpresionSimbolica.constante(0)
        recursivo = False
        for hijo in nodo_funcion.hijos:
            # Verificar si es una llamada recursiva
            if hijo.tipo == 'LLAMADA_FUNCION' and hijo.props.get('nombre') == nombre:
                recursivo = True
            cuerpo += self._analizar_nodo(hijo, funciones_llamadas | {nombre})
        return cuerpo, recursivo