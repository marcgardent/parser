import formula
from formula import TokenType
from serialize import serialize


class Javascript:
    DECLARE_FUNCTION = 'function %s(%s){\n%s%s}\n'
    DECLARE_ARG = '%s:number'
    ARG_SEPARATOR = ', '
    DECLARE_VAR = '  const %s=%s;\n'
    DECLARE_RESULT = '  return %s;\n'
    EMPTY_RESULT = 'null'


class Speudocode:
    DECLARE_FUNCTION = '%s(%s)->{%s%s}'
    DECLARE_ARG = '%s'
    ARG_SEPARATOR = ','
    DECLARE_VAR = '%s=%s;'
    DECLARE_RESULT = '%s'
    EMPTY_RESULT = 'None'


class ExpresionBuilder:
    def __init__(self, language):
        self.__lang = language
        self.__args = []
        self.__vars = []
        self.__res = language.EMPTY_RESULT

    def args(self, kargs): self.__args.extend(kargs); return self
    def var(self, k, v): self.__vars.append((k, v)); return self
    def result(self, r): self.__res = r; return self

    def template_args(self):
        return self.__lang.ARG_SEPARATOR.join((self.__lang.DECLARE_ARG % (arg) for arg in self.__args))

    def template_vars(self):
        return ''.join([self.__lang.DECLARE_VAR % (k, v) for (k, v) in self.__vars])

    def template_result(self):
        return self.__lang.DECLARE_RESULT % (self.__res)

    def to_string(self, name):
        args = self.template_args()
        vars = self.template_vars()
        res = self.template_result()
        return self.__lang.DECLARE_FUNCTION % (name, args, vars, res)


def flat(node, ignore=lambda n: False):
    if not ignore(node):
        yield node
        for child in node.children:
            for flatten in flat(child, ignore):
                yield flatten


def find_first(flatten, criteria):
    for child in flatten:
        if criteria(child):
            return child
    return None


def validate(flatten, criteria):
    return None == find_first(flatten, criteria)

def compress_from_ast(ast, vars=list()):
    index = dict()
    compressed = True
    for n in flat(ast):
        if len(n.children) > 1:
            s = serialize(n)
            if s in index:
                index[s].append(n)
            else:
                print("new index:", s)
                index[s] = [n]

    for (k, v) in index.items():
        if len(v) > 1:
            var_label = f"v{len(vars)}"
            print("compress", var_label, k)
            vars.append((var_label, k))
            for n in v:
                n.token_type = TokenType.T_SYMBOL
                n.remove_all()
                n.value = var_label
            compressed = False
            break
    return (compressed, ast, vars)

def collapse(node, type):
   
    if node.parent:
        parent = node.parent
        parent.token_type = type 
        left=node.left()
        right=node.right()
        node.detach() # --> GC  free
        left.detach()
        right.detach()
        parent.append(left,right)

    else: raise Exception()

def collapse_all(node):
    if node.token_type == TokenType.T_PLUS:
        if node.left().token_type== TokenType.T_PLUS: collapse(node.left(), TokenType.B_SUM)
    elif node.token_type == TokenType.T_MULT:
        if node.left().token_type== TokenType.T_PLUS: collapse(node.left(), TokenType.B_PRODUCT)
    for child in node.children:
        collapse_all(child)

def compress(string, language=Speudocode):
    b = ExpresionBuilder(language)
    ast = formula.parse(string)
    collapse_all(ast)
    print("------- TREE -----------")
    print()
    ast.print()
    print()
    print("----- COMPRESSED -------")
    print()

    b.args(set((n.value for n in flat(ast) if n.token_type == TokenType.T_SYMBOL)))

    (compressed, ast, vars) = compress_from_ast(ast)
    while not compressed:
        (compressed, ast, vars) = compress_from_ast(ast, vars)
    
    for (k,v) in vars:
        b.var(k,v)

    b.result(serialize(ast))
    return b.to_string("f")

if __name__ == '__main__':
    import sys
    string = sys.argv[1]
    result = compress(string)
    print(result)