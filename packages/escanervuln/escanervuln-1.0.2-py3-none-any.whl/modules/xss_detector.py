# modules/xss_detector.py

import ast

class Detector(ast.NodeVisitor):
    def __init__(self):
        self.vulnerabilities = []  # Lista para almacenar vulnerabilidades encontradas
        self.user_inputs = set()   # Variables que contienen entrada del usuario
        self.parents = {}          # Referencias al nodo padre de cada nodo

    def visit_Call(self, node):
        # Detectar request.args.get() para registrar variables como entrada del usuario
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'get':
            value = node.func.value
            if isinstance(value, ast.Attribute) and value.attr == 'args':
                if isinstance(value.value, ast.Name) and value.value.id == 'request':
                    parent = self.parents.get(node)
                    if isinstance(parent, ast.Assign):
                        target = parent.targets[0]
                        if isinstance(target, ast.Name):
                            self.user_inputs.add(target.id)  # Registrar variable de entrada del usuario

        # Detectar render_template_string() con f-strings, .format(), o variables peligrosas
        if isinstance(node.func, ast.Name) and node.func.id == 'render_template_string':
            for arg in node.args:
                if self.is_user_input(arg):
                    self.vulnerabilities.append((
                        node.lineno,
                        node.col_offset,
                        "Posible XSS: entrada del usuario sin escapar en render_template_string."
                    ))
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Rastrear asignaciones para detectar propagación de variables con entrada del usuario
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            value = node.value
            if self.is_user_input(value):
                self.user_inputs.add(var_name)
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        # Detectar f-strings que usan variables de entrada del usuario
        for value in node.values:
            if isinstance(value, ast.FormattedValue) and self.is_user_input(value.value):
                self.vulnerabilities.append((
                    node.lineno,
                    node.col_offset,
                    "Posible XSS: entrada del usuario sin escapar en f-string."
                ))

    def visit_BinOp(self, node):
        # Detectar concatenación de cadenas que involucra entrada del usuario
        if isinstance(node.op, ast.Add):
            if self.is_user_input(node.left) or self.is_user_input(node.right):
                self.vulnerabilities.append((
                    node.lineno,
                    node.col_offset,
                    "Posible XSS: concatenación de cadenas con entrada del usuario."
                ))

    def is_user_input(self, node):
        """ Verifica si un nodo contiene una variable de entrada del usuario """
        if isinstance(node, ast.Name):
            return node.id in self.user_inputs
        elif isinstance(node, ast.BinOp):  # Concatenación
            return self.is_user_input(node.left) or self.is_user_input(node.right)
        elif isinstance(node, ast.JoinedStr):  # f-strings
            return any(self.is_user_input(v.value) for v in node.values if isinstance(v, ast.FormattedValue))
        return False

    def visit(self, node):
        # Añadir referencias al nodo padre
        for child in ast.walk(node):
            for child_node in ast.iter_child_nodes(child):
                self.parents[child_node] = child
        super().visit(node)
        return self.vulnerabilities
