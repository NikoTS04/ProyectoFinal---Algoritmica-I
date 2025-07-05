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
        self.cache_analisis = {}  # Cache para evitar re-análisis

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
            recursivo = self._detectar_recursion_global(self.arbol)
        big_o = funcion_tiempo.big_o()
        return ResultadoAnalisis(funcion_tiempo, big_o, recursivo, nombre_funcion)
    
    def _detectar_recursion_global(self, nodo):
        """Detecta si hay recursión en todo el árbol"""
        for nombre_func, nodo_func in self.funciones.items():
            if self._tiene_llamada_recursiva(nodo_func, nombre_func):
                return True
        return False
    
    def _tiene_llamada_recursiva(self, nodo, nombre_funcion):
        """Verifica si un nodo contiene llamadas recursivas"""
        if nodo.tipo == 'LLAMADA_FUNCION':
            if nodo.props.get('nombre') == nombre_funcion:
                return True
        
        for hijo in nodo.hijos:
            if self._tiene_llamada_recursiva(hijo, nombre_funcion):
                return True
        return False
    
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
            
            # Análisis mejorado para detectar patrones logarítmicos
            patron_log = self._detectar_patron_logaritmico(nodo)
            
            if patron_log:
                # Detectamos patrón logarítmico
                import sympy
                iteraciones = ExpresionSimbolica(sympy.log(sympy.Symbol('N'), 2))
            else:
                # Análisis más inteligente para otros patrones
                patron_iteraciones = self._analizar_patron_iteraciones(nodo, cond_tokens)
                iteraciones = patron_iteraciones
            
            cuerpo = ExpresionSimbolica.constante(0)
            for hijo in nodo.hijos:
                cuerpo += self._analizar_nodo(hijo, funciones_llamadas)
            return iteraciones * (costo_cond + cuerpo)
        
        # Continuar con el resto de casos
        else:
            return self._continuar_analisis_nodo(nodo, funciones_llamadas)
    
    def _detectar_patron_logaritmico(self, nodo_mientras):
        """Detecta patrones logarítmicos en bucles Mientras"""
        
        # Verificar condición del bucle
        cond_tokens = nodo_mientras.props.get('cond', [])
        cond_str = ' '.join([str(token.get('valor', token)) if isinstance(token, dict) 
                           else str(token) for token in cond_tokens]).lower()
        
        # Variables que aparecen en la condición (como inicio, fin)
        variables_condicion = set()
        for token in cond_tokens:
            if isinstance(token, dict) and token.get('tipo') == 'VARIABLE':
                variables_condicion.add(token.get('valor', '').lower())
            elif isinstance(token, str) and token.isalpha():
                variables_condicion.add(token.lower())
        
        # Analizar el cuerpo del bucle para detectar patrones logarítmicos
        asignaciones_encontradas = []
        
        def buscar_asignaciones_recursivo(nodo_actual):
            """Busca asignaciones de forma recursiva en todo el árbol"""
            if nodo_actual.tipo == 'ASIGNACION':
                var_name = nodo_actual.props.get('var', '').lower()
                expr_tokens = nodo_actual.props.get('expr', [])
                expr_str = ' '.join([str(token.get('valor', token)) if isinstance(token, dict) 
                                  else str(token) for token in expr_tokens]).lower()
                
                asignaciones_encontradas.append({
                    'variable': var_name,
                    'expresion': expr_str,
                    'tokens': expr_tokens
                })
            
            # Buscar recursivamente en todos los hijos
            for hijo in nodo_actual.hijos:
                buscar_asignaciones_recursivo(hijo)
        
        # Aplicar búsqueda recursiva a todos los hijos del bucle MIENTRAS
        for hijo in nodo_mientras.hijos:
            buscar_asignaciones_recursivo(hijo)
        
        # Detectar patrones específicos de búsqueda binaria
        patron_busqueda_binaria = self._es_busqueda_binaria(variables_condicion, asignaciones_encontradas)
        if patron_busqueda_binaria:
            return True
        
        # Detectar otros patrones logarítmicos
        for asignacion in asignaciones_encontradas:
            expr_str = asignacion['expresion']
            var_name = asignacion['variable']
            
            # Patrones logarítmicos comunes
            patrones_log = [
                # División por 2 o medio
                ('/' in expr_str and '2' in expr_str),
                ('medio' in expr_str),
                ('//' in expr_str),  # División entera
                ('div' in expr_str and '2' in expr_str),
                # Actualización de límites (búsqueda binaria)
                (var_name in variables_condicion and ('medio' in expr_str or '+' in expr_str or '-' in expr_str))
            ]
            
            if any(patrones_log):
                return True
        
        return False
    
    def _es_busqueda_binaria(self, variables_condicion, asignaciones):
        """Detecta específicamente el patrón de búsqueda binaria"""
        # Buscar variables típicas de búsqueda binaria
        vars_inicio = {'inicio', 'left', 'low', 'start'}
        vars_fin = {'fin', 'right', 'high', 'end'}
        vars_medio = {'medio', 'mid', 'middle'}
        
        tiene_inicio = bool(vars_inicio & variables_condicion)
        tiene_fin = bool(vars_fin & variables_condicion)
        
        # Buscar cálculo de medio y actualización de límites
        tiene_medio = False
        actualiza_limites = False
        
        for asignacion in asignaciones:
            var_name = asignacion['variable']
            expr_str = asignacion['expresion']
            tokens = asignacion.get('tokens', [])
            
            # Verificar cálculo de medio - versión más flexible
            if var_name in vars_medio or 'medio' in var_name:
                # Buscar patrón de suma de límites (incluso si falta la división)
                if ('+' in expr_str and 
                    any(var in expr_str for var in ['inicio', 'fin', 'left', 'right'])):
                    tiene_medio = True
                # Verificar también en tokens
                elif ('+' in tokens and 
                      any(token in vars_inicio | vars_fin for token in tokens if isinstance(token, str))):
                    tiene_medio = True
            
            # Verificar actualización de límites - versión mejorada
            if var_name in vars_inicio | vars_fin:
                # Actualización típica de búsqueda binaria
                if ('medio' in expr_str or 
                    ('+' in expr_str and '1' in expr_str) or
                    ('-' in expr_str and '1' in expr_str)):
                    actualiza_limites = True
        
        # Patrón específico de búsqueda binaria:
        # - Tiene variables inicio y fin en condición
        # - Calcula un punto medio (suma de límites)
        # - Actualiza los límites usando el medio
        if tiene_inicio and tiene_fin and tiene_medio and actualiza_limites:
            return True
        
        # Patrón alternativo más relajado para casos con parsing incompleto
        if tiene_inicio and tiene_fin and tiene_medio:
            # Si hay actualización de límites con +1 o -1, probablemente es búsqueda binaria
            for asignacion in asignaciones:
                expr_str = asignacion['expresion']
                if ('+' in expr_str and '1' in expr_str) or ('-' in expr_str and '1' in expr_str):
                    return True
        
        return False
    
    def _extraer_variable_control(self, nodo_mientras):
        """Extrae la variable de control del bucle Mientras"""
        cond_tokens = nodo_mientras.props.get('cond', [])
        
        # Buscar variables en la condición
        variables = []
        for token in cond_tokens:
            if isinstance(token, dict) and token.get('tipo') == 'VARIABLE':
                variables.append(token.get('valor', ''))
            elif isinstance(token, str) and token.isalpha():
                variables.append(token)
        
        # Retornar la primera variable encontrada (heurística simple)
        return variables[0] if variables else None
    
    def _analizar_patron_iteraciones(self, nodo_mientras, cond_tokens):
        """Analiza el patrón de iteraciones para bucles no logarítmicos"""
        # Por defecto, asumir O(N) para bucles mientras
        # Se puede mejorar con análisis más sofisticado
        return ExpresionSimbolica.variable('N')
    
    def _continuar_analisis_nodo(self, nodo, funciones_llamadas):
        """Continuación del análisis de nodos para mantener la estructura"""
        tipo = nodo.tipo
        props = nodo.props
        
        # === SI ===
        if tipo == 'SI':
            cond_tokens = props.get('cond', [])
            costo_cond = ExpresionSimbolica.desde_tokens(cond_tokens)
            ramas = [self._analizar_nodo(hijo, funciones_llamadas) for hijo in nodo.hijos]
            if ramas:
                return costo_cond + max(ramas, key = lambda r: r.expr)
            return costo_cond
        
        # === LLAMADA A FUNCION ===
        elif tipo == 'LLAMADA_FUNCION':
            return self._analizar_llamada_funcion(nodo, funciones_llamadas)
            
        # === RETORNAR ===
        elif tipo == 'RETORNAR':
            return self._analizar_retorno(nodo, funciones_llamadas)
        
        # === ESTRUCTURAS NO MANEJADAS ESPECIFICAMENTE ===
        else:
            total = ExpresionSimbolica.constante(0)
            for hijo in nodo.hijos:
                total += self._analizar_nodo(hijo, funciones_llamadas)
            return total
    
    def _analizar_llamada_funcion(self, nodo, funciones_llamadas):
        """Análisis mejorado de llamadas a función"""
        props = nodo.props
        nombre = props.get('nombre')
        
        if nombre in self.funciones:
            if nombre in funciones_llamadas:
                # Es una llamada recursiva - análisis mejorado
                return self._analizar_recursion(nombre, nodo, funciones_llamadas)
            else:
                # Llamada normal a función conocida
                nuevas_funciones_llamadas = set(funciones_llamadas)
                nuevas_funciones_llamadas.add(nombre)
                return self._analizar_funcion(self.funciones[nombre], nuevas_funciones_llamadas)[0]
        else:
            # Función desconocida, asumir costo constante
            return ExpresionSimbolica.constante(1)
    
    def _analizar_recursion(self, nombre_funcion, nodo_llamada, funciones_llamadas):
        """Análisis mejorado de recursión"""
        # Obtener la función recursiva para análisis más profundo
        funcion_nodo = self.funciones.get(nombre_funcion)
        if funcion_nodo:
            patron_recursion = self._detectar_patron_recursion(funcion_nodo, nombre_funcion)
            return self._calcular_complejidad_por_patron(patron_recursion)
        
        # Fallback a detección simple por nombre
        if 'fibonacci' in nombre_funcion.lower():
            import sympy
            return ExpresionSimbolica(2**sympy.Symbol('N'))
        elif 'factorial' in nombre_funcion.lower():
            return ExpresionSimbolica.variable('N')
        else:
            return ExpresionSimbolica.variable('N')
    
    def _detectar_patron_recursion(self, funcion_nodo, nombre_funcion):
        """Detecta el patrón de recursión analizando la estructura de la función"""
        llamadas_recursivas = []
        
        # Buscar todas las llamadas recursivas y sus argumentos
        self._encontrar_llamadas_recursivas(funcion_nodo, nombre_funcion, llamadas_recursivas)
        
        if not llamadas_recursivas:
            return {'tipo': 'constante', 'factor': 1}
        
        # Primero, verificar si es recursión condicional (como potencia rápida)
        patron_condicional = self._detectar_recursion_condicional(funcion_nodo, nombre_funcion)
        if patron_condicional:
            return patron_condicional
        
        # Analizar los argumentos de las llamadas recursivas
        patrones = []
        for llamada in llamadas_recursivas:
            patron = self._analizar_argumentos_recursion(llamada)
            patrones.append(patron)
        
        return self._clasificar_patron_recursion(patrones)
    
    def _encontrar_llamadas_recursivas(self, nodo, nombre_funcion, llamadas_encontradas):
        """Encuentra todas las llamadas recursivas en la función"""
        if nodo.tipo == 'LLAMADA_FUNCION' and nodo.props.get('nombre') == nombre_funcion:
            llamadas_encontradas.append(nodo)
        
        # Buscar en expresiones de retorno
        elif nodo.tipo == 'RETORNAR':
            args = nodo.props.get('args', [])
            i = 0
            while i < len(args):
                if (i + 1 < len(args) and 
                    isinstance(args[i], str) and args[i] == nombre_funcion and
                    isinstance(args[i+1], str) and args[i+1] == '('):
                    
                    # Crear un nodo virtual para la llamada recursiva
                    nodo_llamada = type('NodoLlamada', (), {
                        'tipo': 'LLAMADA_FUNCION',
                        'props': {'nombre': nombre_funcion, 'args': args[i+2:]}
                    })()
                    llamadas_encontradas.append(nodo_llamada)
                i += 1
        
        # Buscar recursivamente en hijos
        for hijo in nodo.hijos:
            self._encontrar_llamadas_recursivas(hijo, nombre_funcion, llamadas_encontradas)
    
    def _analizar_argumentos_recursion(self, nodo_llamada):
        """Analiza los argumentos de una llamada recursiva para detectar el patrón"""
        args = nodo_llamada.props.get('args', [])
        
        # Convertir argumentos a string para análisis
        args_str = ' '.join([str(arg) for arg in args])
        
        # Detectar patrones comunes
        if '/2' in args_str or '/ 2' in args_str:
            return {'tipo': 'division', 'factor': 2}
        elif '/3' in args_str or '/ 3' in args_str:
            return {'tipo': 'division', 'factor': 3}
        elif 'N-1' in args_str or 'n-1' in args_str or '- 1' in args_str:
            return {'tipo': 'decremental', 'factor': 1}
        elif 'N-2' in args_str or 'n-2' in args_str or '- 2' in args_str:
            return {'tipo': 'decremental', 'factor': 2}
        else:
            # Analisis más detallado
            if any(op in args_str for op in ['/', 'div']):
                return {'tipo': 'division', 'factor': 2}  # Asumir división por 2 por defecto
            elif any(op in args_str for op in ['-', 'menos']):
                return {'tipo': 'decremental', 'factor': 1}
            else:
                return {'tipo': 'constante', 'factor': 1}
    
    def _clasificar_patron_recursion(self, patrones):
        """Clasifica el patrón general de recursión basado en todos los patrones encontrados"""
        if not patrones:
            return {'tipo': 'constante', 'factor': 1}
        
        # Contar tipos de patrones
        divisiones = [p for p in patrones if p['tipo'] == 'division']
        decrementales = [p for p in patrones if p['tipo'] == 'decremental']
        
        # Si hay múltiples llamadas recursivas con decrementos (como Fibonacci)
        if len(decrementales) >= 2:
            return {'tipo': 'exponencial', 'llamadas': len(decrementales)}
        
        # Si hay divisiones, es logarítmico
        elif divisiones:
            return {'tipo': 'logaritmico', 'factor': divisiones[0]['factor']}
        
        # Si hay decrementos simples, es lineal
        elif decrementales:
            return {'tipo': 'lineal', 'factor': decrementales[0]['factor']}
        
        # Por defecto
        else:
            return {'tipo': 'lineal', 'factor': 1}
    
    def _calcular_complejidad_por_patron(self, patron):
        """Calcula la complejidad basada en el patrón de recursión detectado"""
        import sympy
        
        if patron['tipo'] == 'exponencial':
            # T(n) = a^n donde a es el número de llamadas recursivas
            llamadas = patron.get('llamadas', 2)
            return ExpresionSimbolica(llamadas**sympy.Symbol('N'))
        
        elif patron['tipo'] == 'logaritmico':
            # T(n) = log_factor(n)
            factor = patron.get('factor', 2)
            return ExpresionSimbolica(sympy.log(sympy.Symbol('N'), factor))
        
        elif patron['tipo'] == 'logaritmico_promedio':
            # Para algoritmos como potencia rápida: caso promedio O(log n)
            factor = patron.get('factor', 2)
            return ExpresionSimbolica(sympy.log(sympy.Symbol('N'), factor))
        
        elif patron['tipo'] == 'lineal':
            # T(n) = n
            return ExpresionSimbolica.variable('N')
        
        else:  # constante
            return ExpresionSimbolica.constante(1)
    
    def _analizar_retorno(self, nodo, funciones_llamadas):
        """Análisis mejorado de declaraciones de retorno"""
        props = nodo.props
        args = props.get('args', [])
        
        if not args:
            return ExpresionSimbolica.constante(0)
        
        # Buscar llamadas recursivas en la expresión de retorno
        costo = ExpresionSimbolica.constante(0)
        i = 0
        llamadas_recursivas = []
        
        while i < len(args):
            # Buscar patrones de llamada a función: nombre(
            if (i + 1 < len(args) and 
                isinstance(args[i], str) and 
                isinstance(args[i+1], str) and 
                args[i+1] == '('):
                
                nombre_funcion = args[i]
                if nombre_funcion in self.funciones:
                    if nombre_funcion in funciones_llamadas:
                        # Es recursión - recopilar información para análisis conjunto
                        llamadas_recursivas.append({
                            'nombre': nombre_funcion,
                            'posicion': i,
                            'args': self._extraer_argumentos_llamada(args, i+2)
                        })
                    else:
                        # Llamada normal
                        costo += ExpresionSimbolica.constante(1)
                i += 1
            else:
                i += 1
        
        # Analizar llamadas recursivas encontradas
        if llamadas_recursivas:
            costo += self._analizar_llamadas_recursivas_multiples(llamadas_recursivas, funciones_llamadas)
        
        return costo
    
    def _extraer_argumentos_llamada(self, args, inicio):
        """Extrae los argumentos de una llamada a función desde la posición dada"""
        argumentos = []
        nivel_parentesis = 1
        i = inicio
        
        while i < len(args) and nivel_parentesis > 0:
            token = args[i]
            if token == '(':
                nivel_parentesis += 1
            elif token == ')':
                nivel_parentesis -= 1
            
            if nivel_parentesis > 0:
                argumentos.append(token)
            i += 1
        
        return argumentos
    
    def _analizar_llamadas_recursivas_multiples(self, llamadas_recursivas, funciones_llamadas):
        """Analiza múltiples llamadas recursivas en una expresión de retorno"""
        if len(llamadas_recursivas) == 1:
            # Una sola llamada recursiva
            llamada = llamadas_recursivas[0]
            return self._analizar_recursion(llamada['nombre'], 
                                          self._crear_nodo_llamada(llamada), 
                                          funciones_llamadas)
        
        elif len(llamadas_recursivas) >= 2:
            # Múltiples llamadas recursivas (como Fibonacci)
            # Analizar el patrón de argumentos para determinar complejidad
            patrones = []
            for llamada in llamadas_recursivas:
                args_str = ' '.join([str(arg) for arg in llamada['args']])
                if '-1' in args_str or '- 1' in args_str:
                    patrones.append('decremental_1')
                elif '-2' in args_str or '- 2' in args_str:
                    patrones.append('decremental_2')
                elif '/2' in args_str or '/ 2' in args_str:
                    patrones.append('division_2')
            
            # Clasificar patrón
            if 'decremental_1' in patrones and 'decremental_2' in patrones:
                # Patrón Fibonacci: T(n) = T(n-1) + T(n-2) -> O(2^n)
                import sympy
                return ExpresionSimbolica(2**sympy.Symbol('N'))
            elif len([p for p in patrones if 'decremental' in p]) >= 2:
                # Múltiples decrementos -> exponencial
                import sympy
                return ExpresionSimbolica(len(llamadas_recursivas)**sympy.Symbol('N'))
            else:
                # Análisis individual de la primera llamada
                llamada = llamadas_recursivas[0]
                return self._analizar_recursion(llamada['nombre'], 
                                              self._crear_nodo_llamada(llamada), 
                                              funciones_llamadas)
        
        return ExpresionSimbolica.constante(0)
    
    def _crear_nodo_llamada(self, info_llamada):
        """Crea un nodo virtual para una llamada recursiva"""
        return type('NodoLlamada', (), {
            'tipo': 'LLAMADA_FUNCION',
            'props': {
                'nombre': info_llamada['nombre'],
                'args': info_llamada['args']
            }
        })()
    
    def _analizar_funcion(self, nodo_funcion, funciones_llamadas):
        """Análisis mejorado de funciones"""
        nombre = nodo_funcion.props.get('nombre', '')
        cuerpo = ExpresionSimbolica.constante(0)
        recursivo = False
        
        # Verificar recursión de manera más completa
        recursivo = self._detectar_recursion_en_funcion(nodo_funcion, nombre)
        
        for hijo in nodo_funcion.hijos:
            cuerpo += self._analizar_nodo(hijo, funciones_llamadas | {nombre})
        
        return cuerpo, recursivo
    
    def _detectar_recursion_en_funcion(self, nodo_funcion, nombre_funcion):
        """Detecta recursión de manera más completa en una función"""
        return self._buscar_llamada_recursiva(nodo_funcion, nombre_funcion)
    
    def _buscar_llamada_recursiva(self, nodo, nombre_funcion):
        """Busca llamadas recursivas en cualquier parte del árbol"""
        # Verificar si el nodo actual es una llamada recursiva
        if nodo.tipo == 'LLAMADA_FUNCION':
            if nodo.props.get('nombre') == nombre_funcion:
                return True
        
        # Verificar en expresiones de retorno
        if nodo.tipo == 'RETORNAR':
            args = nodo.props.get('args', [])
            for i, arg in enumerate(args):
                if isinstance(arg, str) and arg == nombre_funcion:
                    # Verificar si el siguiente token es '(' para confirmar que es una llamada
                    if i + 1 < len(args) and args[i + 1] == '(':
                        return True
        
        # Buscar recursivamente en hijos
        for hijo in nodo.hijos:
            if self._buscar_llamada_recursiva(hijo, nombre_funcion):
                return True
        
        return False

    def _detectar_recursion_condicional(self, funcion_nodo, nombre_funcion):
        """Detecta patrones de recursión condicional (como potencia rápida)"""
        llamadas_en_ramas = []
        
        # Buscar llamadas recursivas en diferentes ramas de condiciones
        self._buscar_llamadas_en_ramas(funcion_nodo, nombre_funcion, llamadas_en_ramas, [])
        
        if len(llamadas_en_ramas) >= 2:
            # Analizar patrones en las diferentes ramas
            patrones_ramas = []
            for rama in llamadas_en_ramas:
                patron = self._analizar_argumentos_recursion_simple(rama['llamada'])
                patrones_ramas.append({
                    'patron': patron,
                    'condicion': rama['condicion'],
                    'rama': rama['tipo_rama']
                })
            
            # Determinar complejidad basada en el mejor caso común
            if self._es_patron_potencia_rapida(patrones_ramas):
                return {'tipo': 'logaritmico_promedio', 'factor': 2}
            elif any(p['patron']['tipo'] == 'division' for p in patrones_ramas):
                return {'tipo': 'logaritmico', 'factor': 2}
        
        return None
    
    def _buscar_llamadas_en_ramas(self, nodo, nombre_funcion, llamadas_encontradas, ruta_condicion):
        """Busca llamadas recursivas en diferentes ramas condicionales"""
        if nodo.tipo == 'LLAMADA_FUNCION' and nodo.props.get('nombre') == nombre_funcion:
            llamadas_encontradas.append({
                'llamada': nodo,
                'condicion': ruta_condicion.copy(),
                'tipo_rama': 'directo'
            })
        
        elif nodo.tipo == 'RETORNAR':
            # Buscar llamadas en expresiones de retorno
            args = nodo.props.get('args', [])
            i = 0
            while i < len(args):
                if (i + 1 < len(args) and 
                    isinstance(args[i], str) and args[i] == nombre_funcion and
                    isinstance(args[i+1], str) and args[i+1] == '('):
                    
                    nodo_llamada = type('NodoLlamada', (), {
                        'tipo': 'LLAMADA_FUNCION',
                        'props': {'nombre': nombre_funcion, 'args': args[i+2:]}
                    })()
                    
                    llamadas_encontradas.append({
                        'llamada': nodo_llamada,
                        'condicion': ruta_condicion.copy(),
                        'tipo_rama': 'retorno'
                    })
                i += 1
        
        elif nodo.tipo == 'SI':
            # Analizar rama entonces
            nueva_ruta = ruta_condicion + [('si', nodo.props.get('cond', []))]
            for i, hijo in enumerate(nodo.hijos):
                if i == 0 or not self._es_rama_sino(hijo):  # Primera rama es "entonces"
                    self._buscar_llamadas_en_ramas(hijo, nombre_funcion, llamadas_encontradas, nueva_ruta)
                else:  # Rama "sino"
                    nueva_ruta_sino = ruta_condicion + [('sino', nodo.props.get('cond', []))]
                    self._buscar_llamadas_en_ramas(hijo, nombre_funcion, llamadas_encontradas, nueva_ruta_sino)
        
        else:
            # Continuar búsqueda en hijos
            for hijo in nodo.hijos:
                self._buscar_llamadas_en_ramas(hijo, nombre_funcion, llamadas_encontradas, ruta_condicion)
    
    def _es_rama_sino(self, nodo):
        """Determina si un nodo es parte de la rama 'sino'"""
        # Heurística simple: si el nodo anterior fue analizado, este es sino
        return False  # Simplificación por ahora
    
    def _analizar_argumentos_recursion_simple(self, nodo_llamada):
        """Versión simplificada de análisis de argumentos para recursión condicional"""
        args = nodo_llamada.props.get('args', [])
        args_str = ' '.join([str(arg) for arg in args])
        
        if '/2' in args_str or '/ 2' in args_str:
            return {'tipo': 'division', 'factor': 2}
        elif '-1' in args_str or '- 1' in args_str:
            return {'tipo': 'decremental', 'factor': 1}
        else:
            return {'tipo': 'constante', 'factor': 1}
    
    def _es_patron_potencia_rapida(self, patrones_ramas):
        """Detecta si el patrón corresponde a potencia rápida o similar"""
        # Buscar si hay una rama con división por 2 y otra con decremento
        tiene_division = any(p['patron']['tipo'] == 'division' for p in patrones_ramas)
        tiene_decremento = any(p['patron']['tipo'] == 'decremental' for p in patrones_ramas)
        
        return tiene_division and tiene_decremento