# expresion_simbolica.py

import sympy
from .analizador_expresiones import contar_operaciones

class ExpresionSimbolica:
    def __init__(self, expr):
        self.expr = sympy.sympify(expr)

    @classmethod
    def constante(cls, valor):
        return cls(sympy.Integer(valor))

    @classmethod
    def variable(cls, nombre):
        return cls(sympy.Symbol(nombre))

    @classmethod
    def desde_tokens(cls, tokens):
        """
        Crea una ExpresionSimbolica a partir de una lista de tokens de expresión
        usando el analizador_expresiones para contar operaciones básicas.
        """
        costo = contar_operaciones(tokens)
        return cls.constante(costo)

    def __add__(self, other):
        return ExpresionSimbolica(self.expr + self._to_expr(other))

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return ExpresionSimbolica(self.expr * self._to_expr(other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        return ExpresionSimbolica(self.expr - self._to_expr(other))

    def __rsub__(self, other):
        return ExpresionSimbolica(self._to_expr(other) - self.expr)

    def __truediv__(self, other):
        return ExpresionSimbolica(self.expr / self._to_expr(other))

    def __pow__(self, power):
        return ExpresionSimbolica(self.expr ** self._to_expr(power))

    def __eq__(self, other):
        return sympy.simplify(self.expr - self._to_expr(other)) == 0

    def _to_expr(self, other):
        if isinstance(other, ExpresionSimbolica):
            return other.expr
        return sympy.sympify(other)

    def simplificar(self):
        return ExpresionSimbolica(sympy.simplify(self.expr))

    def como_str(self):
        return str(self.expr)

    def big_o(self, var='N'):
        try:
            # Simplificar la expresión primero
            expr_simplificada = sympy.simplify(self.expr)
            
            # Obtener todas las variables en la expresión
            variables = list(expr_simplificada.free_symbols)
            
            # Si no hay variables, es constante
            if not variables:
                return "O(1)"
            
            # Casos especiales para expresiones exponenciales
            expr_str = str(expr_simplificada)
            for v in variables:
                v_str = str(v)
                if (expr_simplificada.has(2**v) or 
                    f'2**{v_str}' in expr_str or 
                    '2**(' in expr_str):
                    return f"O(2^n)"
            
            # Casos especiales para logarítmicos
            for v in variables:
                v_str = str(v)
                if (expr_simplificada.has(sympy.log(v)) or 
                    f'log({v_str})' in expr_str or
                    '/log(' in expr_str):
                    # Verificar si es N*log(N)
                    if (expr_simplificada.has(v * sympy.log(v)) or
                        f'{v_str}*log({v_str})' in expr_str or
                        f'log({v_str})*{v_str}' in expr_str):
                        return f"O(n log(n))"
                    else:
                        return f"O(log(n))"
            
            # Expandir para obtener términos individuales
            expr_expanded = sympy.expand(expr_simplificada)
            
            # Encontrar el término dominante considerando todas las variables
            max_degree = 0
            degree_info = {}
            
            # Analizar el grado total de la expresión
            for var_sym in variables:
                degree = sympy.degree(expr_expanded, var_sym)
                degree_info[str(var_sym)] = degree
                max_degree = max(max_degree, degree)
            
            # Determinar la complejidad basada en el análisis
            if max_degree == 0:
                return "O(1)"
            elif max_degree == 1:
                # Verificar si es producto de variables (ej: a*b)
                if len(variables) > 1 and expr_expanded.is_Mul:
                    # Contar cuántas variables aparecen en el término principal
                    var_count = sum(1 for v in variables if expr_expanded.has(v))
                    if var_count > 1:
                        return f"O(n*m)"  # Producto de variables
                return "O(n)"
            elif max_degree == 2:
                return "O(n²)"
            elif max_degree == 3:
                return "O(n³)"
            else:
                return f"O(n^{max_degree})"
                
        except Exception as e:
            # Fallback simple
            expr_str = str(self.expr)
            if any(op in expr_str for op in ['**2', '^2', '*N*', '*n*']):
                return "O(n²)"
            elif any(var in expr_str for var in ['N', 'n', 'a', 'b', 'c']):
                return "O(n)"
            else:
                return "O(1)"
            if expr_expanded.is_Add:
                terms = expr_expanded.args
                max_degree = 0
                dominant_term = sympy.Integer(1)
                
                # Verificar si algún término contiene logaritmo
                for term in terms:
                    term_str = str(term)
                    if 'log(' in term_str and (var in term_str or var.lower() in term_str):
                        return f"O(log(n))"
                
                for term in terms:
                    if term.has(n):
                        # Obtener el grado del término respecto a n
                        degree = sympy.degree(term, n)
                        if degree > max_degree:
                            max_degree = degree
                            # Extraer solo la parte que depende de n
                            dominant_term = term
                        if degree > max_degree:
                            max_degree = degree
                            # Extraer solo la parte que depende de n
                            dominant_term = term
                
                # Simplificar el término dominante removiendo constantes
                if dominant_term.is_Mul:
                    factors = []
                    for factor in dominant_term.args:
                        if factor.has(n):
                            factors.append(factor)
                    if factors:
                        result = sympy.Mul(*factors)
                    else:
                        result = n**max_degree if max_degree > 0 else 1
                else:
                    result = dominant_term
            else:
                # Para expresiones no aditivas
                if expr_expanded.has(n):
                    degree = sympy.degree(expr_expanded, n)
                    if degree > 0:
                        result = n**degree
                    else:
                        result = expr_expanded
                else:
                    result = 1
            
            # Limpiar el resultado
            if result == 1:
                return "O(1)"
            else:
                return f"O({result})".replace(var, 'n')
                
        except Exception as e:
            # Fallback simple
            expr_str = str(self.expr)
            if any(op in expr_str for op in ['**2', '^2', '*N*', '*n*']):
                return "O(n²)"
            elif any(var in expr_str for var in ['N', 'n', 'a', 'b', 'c']):
                return "O(n)"
            else:
                return "O(1)"

    def evaluar(self, **kwargs):
        return self.expr.subs(kwargs)

    def graficar(self, var='N', rango=(1, 20)):
        import matplotlib.pyplot as plt
        xs = list(range(rango[0], rango[1] + 1))
        expr_simple = sympy.sympify(self.expr)
        ys = []
        for x in xs:
            try:
                y_val = expr_simple.subs({var: x})
                if y_val.is_number:
                    ys.append(float(y_val))
                else:
                    # Intentar evaluación numérica
                    y_num = y_val.evalf()
                    ys.append(float(y_num))
            except (TypeError, ValueError):
                # Si no se puede convertir, usar el valor x como fallback
                ys.append(x)
        
        plt.plot(xs, ys, marker='o')
        plt.xlabel(var)
        plt.ylabel(str(expr_simple))
        plt.title('Complejidad temporal')
        plt.grid(True)
        plt.show()

    def es_lineal(self):
        """Verifica si la expresión es de complejidad lineal O(n)"""
        try:
            # Expandir la expresión para análisis
            expr_expandida = sympy.expand(self.expr)
            
            # Buscar el término de mayor grado
            variables = list(expr_expandida.free_symbols)
            if not variables:
                return False  # Constante
            
            # Calcular el grado total de la expresión
            grado = sympy.degree(expr_expandida)
            
            # Es lineal si el grado es 1
            return grado == 1
        except:
            # Si hay problemas de análisis, asumir que no es lineal
            return False