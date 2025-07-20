import lexer


class ProgramNode:
    def __init__(self, statements: list):
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode(statements={self.statements})"

    def eval(self, env):
        env['data_local'] = []
        env['data'] = []
        env["stack"] = []
        for statement in self.statements:
            statement.eval(env)


class MainNode:
    def __init__(self, statements: list):
        self.statements = statements

    def __repr__(self):
        return f"MainNode(statements={self.statements})"

    def eval(self, env):
        env['stack'] = ['Principal']
        for statement in self.statements:
            statement.eval(env)


class FuncNode:
    def __init__(self, datatypes: list[str], ID: str,
                 params: list[tuple[list, str]], body: list):
        self.datatypes = datatypes
        self.ID = ID
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FuncNode(datatypes={self.datatypes}, ID={self.ID}, params={self.params}, body={self.body})"

    def eval(self, env):
        """
        Adds the function to the environment.
        """
        if self.ID in env:
            raise ValueError(f"'{self.ID}' already defined. Can't define function with the same ID (name)")
        func_dict = {
            "datatypes": self.datatypes,
            "params": self.params,
            "body": self.body
        }
        env[self.ID] = func_dict


class PrintNode:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"PrintNode(expression={self.expression})"

    def eval(self, env):
        """
        Evaluates the expression and prints the result.
        """
        value = self.expression.eval(env)
        print(value)  # Assuming the expression has an eval method


class StringNode:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"StringNode(value={self.value})"

    def eval(self, env):
        return self.value
