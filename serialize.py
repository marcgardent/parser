import formula
from formula import TokenType

def default_registry():
    return {
        TokenType.T_NUM: render_value,
        TokenType.T_FLOAT: render_value,
        TokenType.T_PLUS: render_left_right,
        TokenType.T_MINUS: render_left_right,
        TokenType.T_MULT: render_left_right,
        TokenType.T_DIV: render_left_right,
        TokenType.T_SYMBOL: render_value,
        TokenType.G_FUNCTION: render_function,
        TokenType.T_SEPARATOR: render_left_right,
        TokenType.T_POW: render_left_right,
        TokenType.G_PARENTHESIS: render_parenthesis,
        TokenType.U_SIGN: render_unaire,
        TokenType.B_SUM: render_bag,
        TokenType.B_PRODUCT: render_bag,
    }

def serializer(render_registry):
    render_registry = render_registry

    def serialize(node):
        if node.token_type in render_registry:
            return render_registry[node.token_type](serialize, node)
        else:
            raise Exception(f"not implemented yet: {node.token_type}")
    return serialize


def render_left_right(
    serialize, node): return f'{serialize(node.left())}{node.value}{serialize(node.right())}'

def render_value(serialize, node): return node.value

def render_function(
    serialize, node): return f"{node.value}({serialize(node.unique())})"

def render_parenthesis(serialize, node): return f"({serialize(node.unique())})"

def render_unaire(
    serialize, node): return f"{node.value}{serialize(node.unique())}"

def render_custom_left_right(prefix='', suffix='?', separator=''):
    return lambda serialize, node: f"{prefix}{serialize(node.left())}{separator}{serialize(node.right())}{suffix}"

def render_bag(serialize, node): return node.value.join(
    [serialize(c) for c in node.children])

if __name__ == '__main__':
    import sys
    string = sys.argv[1]
    ast = formula.parse(string)
    print("------- TREE -----------")
    print()
    ast.print()
    print()
    print("----- SERIALIZED -------")
    print()
    serialize=serializer(default_registry())
    print(serialize(ast))