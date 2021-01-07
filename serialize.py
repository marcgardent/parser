import formula
from formula import TokenType

def serialize(node):
    if node.token_type in render_registry:
        return render_registry[node.token_type](node)
    else:
        raise Exception(f"not implemented yet: {node.token_type}")

def render_left_right(node): return f'{serialize(node.left())}{node.value}{serialize(node.right())}'
def render_value(node): return node.value
def render_function(node): return f"{node.value}({serialize(node.unique())})"
def render_parenthesis(node): return f"({serialize(node.unique())})"
def render_unaire(node): return f"{node.value}{serialize(node.unique())}"

def render_left_right_as_func(node,func_name,arg_begin='(',arg_end=')',arg_separator=','):
    return lambda node: f"{func_name}{arg_begin}{serialize(node.left())}{arg_separator}{serialize(node.right())}{arg_end}"

def render_bag(node): return node.value.join([serialize(c) for c in node.children])

render_registry = {
    TokenType.T_NUM : render_value,
    TokenType.T_FLOAT : render_value,
    TokenType.T_PLUS : render_left_right,
    TokenType.T_MINUS : render_left_right,
    TokenType.T_MULT : render_left_right,
    TokenType.T_DIV : render_left_right,
    TokenType.T_SYMBOL : render_value,
    TokenType.G_FUNCTION : render_function,
    TokenType.T_SEPARATOR : render_left_right,
    TokenType.T_POW : render_left_right,
    TokenType.G_PARENTHESIS : render_parenthesis,
    TokenType.U_SIGN: render_unaire,
    TokenType.B_SUM: render_bag,
    TokenType.B_PRODUCT: render_bag,
}

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
    print(serialize(ast))