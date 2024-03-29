import systems.math.representation as representation


class Stock(representation.Reference):
    """Implicit 'dt'. Defined via difference equation made
    up of flows."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None

    def node(self, dot):
        dot.node(
            name=str(id(self)),
            label=str(self.value),
            shape="rect"
        )

    def equation(self):
        delta_tree = self.model.delta_trees[self.value]
        # TODO: how do I replace all stock/flow with 
        pass

class Flow(representation.Reference):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def node(self, dot):
        dot.node(
            name=str(id(self)),
            label=str(self.value),
            shape="ellipse"
        )
