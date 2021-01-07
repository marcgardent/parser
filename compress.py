import formula
from formula import TokenType
from serialize import serialize, render_registry, render_left_right_as_func
import itertools

render_registry[TokenType.T_POW] = render_left_right_as_func('Math.Pow')

class Javascript:
    DECLARE_FUNCTION = 'function %s(%s): number {\n%s%s}\n'
    DECLARE_ARG = '%s:number'
    ARG_SEPARATOR = ', '
    DECLARE_VAR = '  const %s = %s;\n'
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


def flat(node):
    yield node
    for child in node.children:
        for flatten in flat(child):
            yield flatten
            
def iflat(node, ignore=lambda n: False):
    for child in node.children:
        for flatten in iflat(child):
            yield flatten
    yield node



# def find_first(flatten, criteria):
#     for child in flatten:
#         if criteria(child):
#             return child
#     return None


# def validate(flatten, criteria):
#     return None == find_first(flatten, criteria)

def sequences(iter):
    length=len(iter)
    for window in range(2, length):
        c = list(itertools.combinations(iter, window))
        if window*2==length: c = c[:int(len(c)/2)] #remove symmetric case
        for seq in c:
                yield (seq,tuple(n for n in iter if n not in seq ))

def indexable(node):
    
    if node.token_type in (TokenType.B_PRODUCT, TokenType.B_SUM):
        ret=dict()
        for (sequence,others) in sequences(node.children):
            n1 =formula.Node(node.token_type)
            n1.value = node.value
            n1.append(*sequence)
            n2 = None 
            if len(others)==1:
                n2=others[0]
            elif len(others)>1:
                n2 =formula.Node(node.token_type)
                n2.value = node.value
                n2.append(*others)
            ret[serialize(n1)]=n2 # remove repeat of 1+1+1+1
        for item in ret.items(): yield item
    else:
        s = serialize(node)
        yield (s, None)

def compress_from_ast(ast, vars=list()):
    index = dict()
    compressed = True
    for n in flat(ast):
        if len(n.children) > 1:
            for (s,other) in indexable(n):
                n.print()
                if s in index:
                    index[s].append((n,other))

                else:
                    index[s] = [(n,other)]
    for (k, v) in index.items():
        if len(v) > 1:
            var_label = f"v{len(vars)}"
            vars.append((var_label, k))
            for (n,other) in v:
                if other:
                    n.remove_all()
                    symbol = formula.Node(TokenType.T_SYMBOL)
                    symbol.value = var_label
                    n.append(symbol, other)

                else:
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

def sort_all(node):
    for n in iflat(node):
        if n.token_type in (TokenType.B_SUM,  TokenType.B_PRODUCT,  TokenType.T_MULT, TokenType.T_PLUS):
            n.children = sorted(n.children, key=lambda n: serialize(n))

def compress(string, language=Speudocode):
    b = ExpresionBuilder(language)
    ast = formula.parse(string)
    collapse_all(ast)
    sort_all(ast)
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

    ast.print()
    print()

    b.result(serialize(ast))
    return b.to_string("f")

if __name__ == '__main__':
    import sys
    string = sys.argv[1]
    result = compress(string, language=Javascript)
    print(result)