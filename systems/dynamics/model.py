import systems.math.representation as representation


class Model(object):
    def __init__(self):
        self.components = {}
        self.delta_trees = {}
        
    # actually, as long as operations return a new thing, this should just work.
    def __setattr__(self, name, value):
        #if isinstance(value, Tree):
        if isinstance(value, representation.Tree):
            if name not in self.components:
                self.components[name] = value
                self.components[name].model = self
                self.delta_trees[name] = None # don't include self in delta tree (implicit add)
            else:
                # don't actually overwrite, this is returnning a compute graph
                if self.delta_trees[name] is None:
                    self.delta_trees[name] = value
                else:
                    self.delta_trees[name] = self.delta_trees[name] + value
                # TODO: we need the operations to also return a non-compute system symbolic graph? Or can this always be inferred from the compute graph and the list of names/stocks/flows we have in model?
                # the latter. We just need to find all reference nodes, and that means there's an edge from that reference node _to_ the current node.

                # this also means you can define the formula for a value in pieces, and it will assume you're adding them all together. (this also allows documenting specific portions)
        else:
            object.__setattr__(self, name, value)
            
    def __getattr__(self, name):
        if name in self.components:
            return self.components[name]

    def _compile(self):
        """Write optimized jax operation list for computations into python file?"""
        pass
