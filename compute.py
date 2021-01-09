import sys
import operator
import formula

class NotImplementedException(Exception):
  pass

operations = {
    formula.TokenType.T_PLUS: operator.add,
    formula.TokenType.T_MINUS: operator.sub,
    formula.TokenType.T_MULT: operator.mul,
    formula.TokenType.T_DIV: operator.truediv,
    formula.TokenType.T_POW: operator.pow
    
}



def compute(node):
    if node.type_in(formula.TokenType.G_PARENTHESIS):
        return compute(node.unique())
    elif node.type_in(formula.TokenType.T_NUM):
        return node.asInteger()
    elif node.type_in(formula.TokenType.U_SIGN):
        f = -1 if node.value =='-' else 1
        return compute(node.unique())*f
    elif not node.token_type in operations:
        raise NotImplementedException(f"token {node.token_type} not implemented for computing")

    left_result = compute(node.left())
    right_result = compute(node.right())
    
    operation = operations[node.token_type]
    return operation(left_result, right_result)


if __name__ == '__main__':
    ast = formula.parse(sys.argv[1])
    result = compute(ast)
    print(result)
