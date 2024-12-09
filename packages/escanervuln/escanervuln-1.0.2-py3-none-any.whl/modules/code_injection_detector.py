# modules/code_injection_detector.py

import ast

class Detector(ast.NodeVisitor):
    def __init__(self):
        self.dangerous_functions = ['eval', 'exec', 'execfile', 'compile']
        self.user_input_functions = [
            'input', 'raw_input',
            'request.args.get', 'request.form.get',
            'request.values.get', 'request.get_json',
            'request.cookies.get', 'request.headers.get',
            'self.get_argument',  # Para frameworks como Tornado
            'cgi.FieldStorage',   # Para aplicaciones CGI
        ]
        self.user_input_sources = ['sys.argv', 'os.environ']
        self.vulnerabilities = []
        self.user_inputs = set()
        self.assignments = {}
        self.function_defs = {}
        self.user_input_params = {}
        self.parents = {}
        self.safe_functions = ['sanitize_input', 'escape', 'clean']  # Ejemplo

    def collect_info(self, node):
        # Primera pasada: recopilar información
        for child in ast.walk(node):
            for child_node in ast.iter_child_nodes(child):
                child_node.parent = child

            if isinstance(child, ast.FunctionDef):
                self.function_defs[child.name] = child

            elif isinstance(child, ast.Call):
                func_name = self.get_full_name(child.func)
                # Detectar funciones de entrada del usuario
                if func_name in self.user_input_functions:
                    parent = getattr(child, 'parent', None)
                    if isinstance(parent, ast.Assign):
                        targets = parent.targets
                        for target in targets:
                            if isinstance(target, ast.Name):
                                var_name = target.id
                                self.user_inputs.add(var_name)
                    elif isinstance(parent, ast.Expr):
                        # Manejar casos donde la llamada está sola (por efectos secundarios)
                        pass  # Puedes agregar lógica adicional aquí si es necesario
                    else:
                        # Manejar argumentos tainted en llamadas a funciones
                        grandparent = getattr(parent, 'parent', None)
                        if isinstance(grandparent, ast.Assign):
                            targets = grandparent.targets
                            for target in targets:
                                if isinstance(target, ast.Name):
                                    var_name = target.id
                                    self.user_inputs.add(var_name)
                # Mapear argumentos de llamadas a funciones definidas
                elif func_name in self.function_defs:
                    func_def = self.function_defs[func_name]
                    arg_names = [arg.arg for arg in func_def.args.args]
                    call_arg_values = child.args
                    for param, arg in zip(arg_names, call_arg_values):
                        if self.is_user_input(arg):
                            if func_name not in self.user_input_params:
                                self.user_input_params[func_name] = set()
                            self.user_input_params[func_name].add(param)
                # Detectar asignación de funciones peligrosas a variables (alias)
                elif func_name in self.dangerous_functions:
                    parent = getattr(child, 'parent', None)
                    if isinstance(parent, ast.Assign):
                        if isinstance(parent.targets[0], ast.Name):
                            alias_name = parent.targets[0].id
                            self.dangerous_functions.append(alias_name)

            elif isinstance(child, ast.Assign):
                targets = child.targets
                value = child.value
                # Verificar si la asignación proviene de una entrada del usuario
                if self.is_user_input(value):
                    for target in targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            self.user_inputs.add(var_name)
                # Manejar asignaciones de funciones peligrosas a variables
                if isinstance(value, ast.Name) and value.id in self.dangerous_functions:
                    for target in targets:
                        if isinstance(target, ast.Name):
                            alias_name = target.id
                            self.dangerous_functions.append(alias_name)

            elif isinstance(child, ast.Subscript):
                value = self.get_full_name(child.value)
                if value in self.user_input_sources:
                    parent = getattr(child, 'parent', None)
                    if isinstance(parent, ast.Assign):
                        target = parent.targets[0]
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            self.user_inputs.add(var_name)

    def analyze(self, node):
        # Segunda pasada: detectar vulnerabilidades
        self.visit(node)

    def visit_FunctionDef(self, node):
        # Añadir parámetros que son entradas del usuario
        original_user_inputs = self.user_inputs.copy()
        if node.name in self.user_input_params:
            self.user_inputs.update(self.user_input_params[node.name])

        self.generic_visit(node)

        # Restaurar self.user_inputs
        self.user_inputs = original_user_inputs

    def visit_Call(self, node):
        func_name = self.get_full_name(node.func)
        # Detectar uso de funciones peligrosas
        if func_name in self.dangerous_functions:
            # Verificar si los argumentos son tainted
            for arg in node.args:
                if self.is_user_input(arg):
                    if not self.is_sanitized(arg):
                        self.vulnerabilities.append((
                            node.lineno,
                            node.col_offset,
                            f'Posible Inyección de Código usando {func_name} con entrada del usuario.'
                        ))
        self.generic_visit(node)

    def is_sanitized(self, node):
        if isinstance(node, ast.Call):
            func_name = self.get_full_name(node.func)
            return func_name in self.safe_functions
        return False

    def is_user_input(self, node):
        if isinstance(node, ast.Name):
            return node.id in self.user_inputs
        elif isinstance(node, ast.Call):
            func_name = self.get_full_name(node.func)
            if func_name in self.user_input_functions:
                return True
            # Verificar si la función retorna un valor tainted
            elif func_name in self.function_defs:
                if func_name in self.user_input_params:
                    return True
            # Analizar los argumentos de la llamada
            return any(self.is_user_input(arg) for arg in node.args)
        elif isinstance(node, ast.Attribute):
            full_name = self.get_full_name(node)
            if full_name in self.user_input_sources:
                return True
            else:
                return self.is_user_input(node.value)
        elif isinstance(node, ast.Subscript):
            return self.is_user_input(node.value) or self.is_user_input(node.slice)
        elif isinstance(node, ast.BinOp):
            return self.is_user_input(node.left) or self.is_user_input(node.right)
        elif isinstance(node, ast.UnaryOp):
            return self.is_user_input(node.operand)
        elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            return any(self.is_user_input(elt) for elt in node.elts)
        elif isinstance(node, ast.Dict):
            return any(
                self.is_user_input(key) or self.is_user_input(value)
                for key, value in zip(node.keys, node.values)
            )
        else:
            return False

    def get_full_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value = self.get_full_name(node.value)
            return f"{value}.{node.attr}"
        else:
            return ''

    def visit(self, node):
        super().visit(node)
        return self.vulnerabilities

    def run(self, node):
        # Método principal para ejecutar el detector
        self.collect_info(node)
        self.analyze(node)
        return self.vulnerabilities
