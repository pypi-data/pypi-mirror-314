# modules/sql_injection_detector.py

import ast

class Detector(ast.NodeVisitor):
    def __init__(self):
        self.vulnerabilities = []
        self.assignments = {}

    def visit_Assign(self, node):
        # Almacenar asignaciones de variables
        if len(node.targets) > 0 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            self.assignments[var_name] = node.value
        self.generic_visit(node)

    def visit_Call(self, node):
        # Verificar si es una llamada a cursor.execute()
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr.lower()
            if func_name in ('execute', 'executemany', 'callproc'):
                if node.args:
                    query_arg = node.args[0]
                    query, has_variable = self.resolve_value(query_arg)
                    params = node.args[1] if len(node.args) > 1 else None
                    if params:
                        # Se están usando parámetros, es más seguro
                        is_safe = True
                    else:
                        is_safe = False

                    if has_variable and not is_safe:
                        self.vulnerabilities.append((
                            node.lineno,
                            node.col_offset,
                            'Posible Inyección SQL detectada.'
                        ))
        self.generic_visit(node)

    def resolve_value(self, node):
        # Resuelve el valor de una expresión y detecta si contiene variables
        if isinstance(node, ast.Str):
            return node.s, False
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value, False
        elif isinstance(node, ast.Name):
            var_name = node.id
            if var_name in self.assignments:
                return self.resolve_value(self.assignments[var_name])
            else:
                # Variable cuyo valor no se conoce, marcar como variable
                return f"<{var_name}>", True
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left_value, left_has_var = self.resolve_value(node.left)
            right_value, right_has_var = self.resolve_value(node.right)
            value = ''
            has_variable = left_has_var or right_has_var
            if left_value is not None and right_value is not None:
                value = left_value + right_value
            return value, has_variable
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            # Manejar métodos de formato de cadenas como format()
            if node.func.attr == 'format':
                format_string, has_var = self.resolve_value(node.func.value)
                return format_string, True  # Asumimos que puede ser inseguro
            else:
                # Otros métodos de cadena, asumimos que pueden ser inseguros
                return None, True
        elif isinstance(node, ast.Call):
            # Otras llamadas a funciones, asumimos que pueden ser inseguras
            return None, True
        elif isinstance(node, ast.JoinedStr):
            # Manejar f-strings
            return '', True  # Asumimos que puede ser inseguro
        else:
            return None, True  # Nodo desconocido, asumir que tiene variable

    def visit(self, node):
        # No reinicializar self.vulnerabilities aquí
        super().visit(node)
        return self.vulnerabilities
