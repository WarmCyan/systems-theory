import systems.math.representation as representation


class add(representation.Operation):
    def __init__(self, a, b):
        super().__init__("+", a, b)

    def latex_repr(self, left, right):
        return f"{left} + {right}"


class sub(representation.Operation):
    def __init__(self, a, b):
        super().__init__("-", a, b)

    def latex_repr(self, left, right):
        return f"{left} - {right}"


class mul(representation.Operation):
    def __init__(self, a, b):
        super().__init__("*", a, b)

    def latex_repr(self, left, right):
        return f"{left} * {right}"


class div(representation.Operation):
    def __init__(self, a, b):
        super().__init__("/", a, b)

    def latex_repr(self, left, right):
        return f"\\frac{{{left}}}{{{right}}}"
