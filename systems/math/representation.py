from graphviz import Digraph
from IPython.display import Markdown

import systems.math as math

COLORS = ["lightgrey", "pink", "lightgreen", "cyan"]


class Tree:
    def __init__(self, value, left_tree=None, right_tree=None, comment=None):
        self.value = value
        self.left_tree = left_tree
        self.right_tree = right_tree
        self.comment = comment

    def __add__(self, obj):
        if isinstance(obj, int) or isinstance(obj, float):
            return math.ops.add(self, Scalar(obj))
        else:
            return math.ops.add(self, obj)

    def __sub__(self, obj):
        if isinstance(obj, int) or isinstance(obj, float):
            return math.ops.sub(self, Scalar(obj))
        else:
            return math.ops.sub(self, obj)

    def __mul__(self, obj):
        if isinstance(obj, int) or isinstance(obj, float):
            return math.ops.mul(self, Scalar(obj))
        else:
            return math.ops.mul(self, obj)

    def __truediv__(self, obj):
        if isinstance(obj, int) or isinstance(obj, float):
            return math.ops.div(self, Scalar(obj))
        else:
            return math.ops.div(self, obj)

    def __neg__(self):
        return math.ops.sub(Scalar(0), self)

    def __lshift__(self, obj):
        self.comment = obj
        return self

    def is_leaf(self):
        if isinstance(self, Operation):
            return False
        elif isinstance(self, Scalar):
            return True
        elif isinstance(self, Reference):
            return True

    def node(self, dot):
        color = None
        fillcolor = None
        style = None
        fontcolor = None
        if isinstance(self, Operation):
            color = "blue"
        # elif isinstance(self, Stock):
        #     style = "filled"
        #     fillcolor = "orange"
        # elif isinstance(self, Flow):
        #     style = "filled"
        #     fillcolor = "purple"
        #     fontcolor = "white"
        # elif isinstance(self, Variable):
        #     style = "filled"
        #     fillcolor = "green"
        #     fontcolor = "white"

        dot.node(
            name=str(id(self)),
            label=str(self.value),
            color=color,
            fillcolor=fillcolor,
            style=style,
            fontcolor=fontcolor,
        )

    def visualize(self, dot=None, comments=False, comment_colors_used=[]):
        if dot is None:
            dot = Digraph()

        # TODO: it would be convenient if it was possible to only draw the comment block around leaves and parent, I need to figure out a way to define the boundaries that a comment actually applies to.

        if comments and self.comment is not None:
            sub_color = None
            for color in COLORS:
                if color not in comment_colors_used:
                    sub_color = color
                    break
            if sub_color is None:
                comment_colors_used = []
                sub_color = COLORS[0]
            comment_colors_used.append(sub_color)

            with dot.subgraph(
                name=f"cluster_commented{id(self)}",
                body=[
                    "style=filled\n",
                    f"fillcolor={sub_color}\n",
                    f'label="{self.comment}"\n',
                    "labelloc=b\n",
                ],
            ) as g:

                self._visualize_inner(g, comments, comment_colors_used)

        else:
            self._visualize_inner(dot, comments, comment_colors_used)

        return dot

    def _visualize_inner(self, g, comments, comment_colors_used):
        self.node(g)

        if self.left_tree:
            g.edge(str(id(self.left_tree)), str(id(self)))
            g = self.left_tree.visualize(g, comments, comment_colors_used)

        if self.right_tree:
            g.edge(str(id(self.right_tree)), str(id(self)))
            g = self.right_tree.visualize(g, comments, comment_colors_used)

        return g


class Operation(Tree):
    def __init__(self, op, left_tree=None, right_tree=None):
        self.op = op
        super().__init__(op, left_tree, right_tree, None)

    def __repr__(self):
        return f"({self.op} {self.left_tree.__repr__()} {self.right_tree.__repr__()})"

    def latex(self, annotations=False):  # recursive
        return Markdown(f"${self.latex_str(annotations)}$")

    def latex_repr(self, latex_left: str, latex_right: str) -> str:
        """Make the latex to represent how this operation relates
        the left and right sides.

        This should be overriden in all subclasses.

        Args:
            latex_left (str): The latex string from the left tree.
            latex_right (str): The latex string from the right tree.
        """
        # needs to be overriden in subclasses
        return f"{latex_left} NOOP {latex_right}"

    def latex_str(self, annotations: bool = False, top: bool = False) -> str:
        """Recursively construct the latex string for the equation
        from this point in the tree.

        Args:
            annotations (bool): Whether the over/under brace comments
                are being included.
            top (bool): Used to alternate over/under comments each
                level of recursion.
        """
        if annotations and self.comment is not None:
            top = not top

        latex_left = (
            self.left_tree.latex_str(annotations, top)
            if self.left_tree is not None
            else ""
        )
        latex_right = (
            self.right_tree.latex_str(annotations, top)
            if self.right_tree is not None
            else ""
        )
        if (
            self.right_tree is not None
            and isinstance(self.right_tree, Scalar)
            and self.right_tree.scalar == 0
        ):
            latex_right = "0"

        core = self.latex_repr(latex_left, latex_right)

        if annotations and self.comment is not None:
            if top:
                core = f"\\overbrace{{{core}}}^{{\\texttt{{{self.comment}}}}}"
            else:
                core = f"\\underbrace{{{core}}}_{{\\texttt{{{self.comment}}}}}"

        return core


class Scalar(Tree):
    def __init__(self, scalar):
        self.scalar = scalar
        super().__init__(scalar, None, None, None)

    def __repr__(self):
        return str(self.scalar)

    def __eq__(self, obj):
        if not isinstance(obj, Scalar):
            return False
        return self.scalar == obj.scalar

    def latex_str(self, annotations=False, top=False):
        if self.scalar == 0:
            return ""  # so that negated vals don't always show a 0-
        else:
            return str(self.scalar)


class Reference(Tree):
    """A reference to a flow, stock, or variable."""

    def __init__(self, name):
        self.name = name
        self.latex_shorthand = ""
        self.description = ""  # different from comment?
        super().__init__(name, None, None, None)

    def __repr__(self):
        return f'"{self.name}"'

    def latex_str(self, annotations=False, top=False):
        return f"\\mathit{{{self.name}}}"
