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
        n = sympy.Symbol(var)
        try:
            # Simplificar la expresión primero
            expr_simplificada = sympy.simplify(self.expr)
            
            # Casos especiales para expresiones exponenciales
            expr_str = str(expr_simplificada)
            if (expr_simplificada.has(2**n) or 
                '2**N' in expr_str or 
                '2**n' in expr_str or
                '2**(' in expr_str or  # Para casos como 2**(N+1)
                expr_simplificada.has(sympy.exp(n))):
                return f"O(2^n)"
            
            # Casos especiales para logarítmicos - detección mejorada
            if (expr_simplificada.has(sympy.log(n)) or 
                'log(N)' in expr_str or 
                'log(n)' in expr_str or
                '/log(' in expr_str):
                return f"O(log(n))"
            
            # Expandir para obtener términos individuales
            expr_expanded = sympy.expand(expr_simplificada)
            
            # Si es una constante, retornar O(1)
            if not expr_expanded.has(n):
                return "O(1)"
            
            # Verificación adicional para logaritmos en expresiones expandidas
            expr_expanded_str = str(expr_expanded)
            if ('log(' in expr_expanded_str and 
                (var in expr_expanded_str or var.lower() in expr_expanded_str)):
                return f"O(log(n))"
            
            # Si es una suma, encontrar el término dominante
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
            # Fallback: buscar la mayor potencia de n
            try:
                degree = sympy.degree(self.expr, n)
                if degree > 0:
                    return f"O(n**{degree})".replace('**1', '')
                else:
                    return "O(1)"
            except:
                return "O(n)"

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