# modules/deserialization_detector.py

import ast

class Detector(ast.NodeVisitor):
    dangerous_functions = [
        'pickle.loads', 'pickle.load', 'cPickle.loads', 'cPickle.load',
        'yaml.load', 'dill.loads', 'dill.load', 'eval'
    ]

    def __init__(self):
        self.vulnerabilities = []
        self.user_inputs = set()
        self.aliases = {}

    def visit_Import(self, node):
        # Detectar alias en imports (ej. import pickle as p)
        for alias in node.names:
            if alias.asname:
                self.aliases[alias.asname] = alias.name
            else:
                self.aliases[alias.name] = alias.name
        self.generic_visit(node)

    def visit_Call(self, node):
        # Obtener nombre completo de la función
        func_name = self.get_full_name(node.func)
        if func_name in self.dangerous_functions:
            for arg in node.args:
                if self.is_user_input(arg):
                    self.vulnerabilities.append((
                        node.lineno,
                        node.col_offset,
                        f'Posible Deserialización Insegura usando {func_name} con entrada del usuario.'
                    ))
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Rastrear asignación de entrada del usuario
        if isinstance(node.value, ast.Call):
            func_name = self.get_full_name(node.value.func)
            if func_name in ['request.args.get', 'input']:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.user_inputs.add(target.id)
        self.generic_visit(node)

    def get_full_name(self, node):
        """ Obtiene el nombre completo de una función, considerando alias. """
        if isinstance(node, ast.Attribute):
            value = self.get_full_name(node.value)
            return f"{value}.{node.attr}"
        elif isinstance(node, ast.Name):
            return self.aliases.get(node.id, node.id)
        return ''

    def is_user_input(self, node):
        """ Verifica si un nodo contiene entrada del usuario. """
        if isinstance(node, ast.Name):
            return node.id in self.user_inputs
        elif isinstance(node, ast.Call):
            return self.get_full_name(node.func) in ['request.args.get', 'input']
        return False

    def visit(self, node):
        super().visit(node)
        return self.vulnerabilities
