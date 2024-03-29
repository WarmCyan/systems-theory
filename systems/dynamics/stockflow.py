import systems.math.representation as representation


class Stock(representation.Reference):
    """Implicit 'dt'. Defined via difference equation made
    up of flows."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None
        self.inflow = []
        self.outflow = []

    def node(self, dot):
        dot.node(
            name=str(id(self)),
            label=str(self.value),
            shape="rect"
        )

    def get_compute(self):
        eqn = None
        for flow in self.inflow:
            if eqn is None:
                eqn = flow
            else:
                eqn = eqn + flow
        for flow in self.outflow:
            if eqn is None:
                eqn = -flow
            else:
                eqn = eqn - flow
        return eqn

    def __iadd__(self, obj):
        self.inflow.append(obj)
        return self

    def __isub__(self, obj):
        self.outflow.append(obj)
        return self

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
