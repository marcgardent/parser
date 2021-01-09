# Fork
# https://github.com/gnebehay/parser/blob/master/parser.py
#
import enum
import re
import io
import logging


class TokenType(enum.Enum):
    T_NUM = 0
    T_FLOAT = 1
    T_PLUS = 2
    T_MINUS = 3
    T_MULT = 4
    T_DIV = 5
    T_LPAR = 6
    T_RPAR = 7
    T_SYMBOL = 8
    G_FUNCTION = 9
    T_SEPARATOR = 10
    T_POW = 11
    T_END = 12
    G_PARENTHESIS = 13
    U_SIGN = 14
    B_SUM = 15
    B_PRODUCT = 16

###################################################################################

def tokenize_constant(tokenType, match):
    length = len(match)

    def t(ctx):
        buffer = ctx.read(length)
        return (buffer == match, tokenType, match, len(buffer))
    return t


def tokenize_regex(tokenType, regex, buffer_size=16):
    def t(ctx):
        buffer = ctx.read(buffer_size)
        r = re.match(regex, buffer)
        success = r != None
        return (success, tokenType, r.group(1) if success else None, len(buffer))
    return t


###################################################################################
# Modeling
###################################################################################
CLEANUP_REGEX = r'\s+'

TOKENIZERS = [
    tokenize_constant(TokenType.T_PLUS, '+'),
    tokenize_constant(TokenType.T_POW, '^'),
    tokenize_constant(TokenType.T_MINUS, '-'),
    tokenize_constant(TokenType.T_MULT, '*'),
    tokenize_constant(TokenType.T_DIV, '/'),
    tokenize_constant(TokenType.T_LPAR, '('),
    tokenize_constant(TokenType.T_RPAR, ')'),
    tokenize_constant(TokenType.T_SEPARATOR, ','),
    tokenize_regex(TokenType.T_FLOAT, r'((\+|-)?\d*\.\d+)'),
    tokenize_regex(TokenType.T_NUM, r'((\+|-)?\d+)'),
    tokenize_regex(TokenType.T_SYMBOL, r'([a-zA-Z][a-zA-Z0-9_\.]*)'),
]

LEAF_BEHAVIOR = (TokenType.T_NUM, TokenType.T_FLOAT, TokenType.T_SYMBOL)

# PRIORITIES =(
#     (TokenType.T_MULT, TokenType.T_DIV),
#     (TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_SEPARATOR),
#     (TokenType.T_POW,),
# )

FLOAT_CAST_BEHAVIOR = (TokenType.T_NUM,  TokenType.T_FLOAT)
SIGN_BEHAVIOR = (TokenType.T_PLUS,  TokenType.T_MINUS)
EXPRESSION_BEHAVIOR = (TokenType.T_NUM, TokenType.T_FLOAT, TokenType.T_SYMBOL,
                       TokenType.T_LPAR, TokenType.G_FUNCTION, TokenType.G_PARENTHESIS)

###################################################################################


class InvalidCastOperationException(Exception):
    pass


class InvalidTokenException(Exception):
    pass


class UnexpectedTokenException(Exception):
    pass


class Node:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value
        self.parent = None
        self.children = []

    def is_root(self): return self.parent == None

    def append(self, *children):
        for child in children:
            self.children.append(child)
            child.parent = self

    def detach(self):
        if self.parent:
            self.parent.children.remove(self)

    def print(self, padding=''):
        print(f"{padding}{self.token_type.name}={self.value}")

        padding = padding.replace('├', '|').replace('└', ' ').replace('─', ' ')
        for child in self.children[:-1]:
            child.print(padding+'   ├───')
        if len(self.children) > 0:
            self.children[-1].print(padding+'   └───')

    def asInteger(self):
        if not self.token_type == TokenType.T_NUM:
            raise InvalidCastOperationException(
                f"can't cast the node {self.token_type} into int()")
        return int(self.value)

    def asFloat(self):
        if not self.token_type in (FLOAT_CAST_BEHAVIOR):
            raise InvalidCastOperationException(
                f"can't cast the node {self.token_type} into int()")
        return float(self.value)

    def type_in(self, *type):
        return self.token_type in type

    def left(self): assert len(self.children) == 2; return self.children[0]
    def right(self): assert len(self.children) == 2; return self.children[1]
    def unique(self): assert len(self.children) == 1; return self.children[0]

    def remove_all(self):
        for c in self.children:
            c.parent = None
        self.children.clear()


def lexical_analysis(s):

    tokens = []

    length = len(s)

    ctx = io.StringIO(s)
    while ctx.tell() < length:
        token = None
        logging.debug("tokenize at char %s", ctx.tell())

        for tokenizer in TOKENIZERS:

            (success, tokenType, content, buffer) = tokenizer(ctx)
            logging.debug("tokenizer result: success=%s, tokenType=%s, content=%s, buffer=%s",
                          success, tokenType, content, buffer)
            if success and len(content) == 0:
                logging.error(
                    f"the token '{tokenType}' accepted but no char consumed: check the tokenizer() for the '{tokenType}'")
            elif success:
                token = Node(tokenType, value=content)
                logging.debug(
                    f"token '{tokenType}' accepted with the value '{content}'")
                ctx.seek(ctx.tell()-(buffer-len(content)))
                break
            ctx.seek(ctx.tell()-buffer)
        if token:
            tokens.append(token)
        else:
            raise InvalidTokenException(
                f'unexpected token at char {ctx.tell()}: { ctx.read(16)}')

    tokens.append(Node(TokenType.T_END))
    return tokens


def match(tokens, *accepted):
    if tokens[0].token_type in accepted:
        return tokens.pop(0)
    else:
        raise UnexpectedTokenException('Invalid syntax on token {}: excepted ({})'.format(
            tokens[0].token_type, ','.join([str(t) for t in accepted])))


def _parse_left_right_operator(label,accepted, parse_next):
    def _parse(tokens):
        logging.debug(f"{label}...{tokens[0].value}")
        left_node = parse_next(tokens)
        while tokens[0].token_type in accepted:
            logging.debug(f"while {label}...{tokens[0].value}")
            node = tokens.pop(0)
            node.append(left_node, parse_next(tokens))
            left_node = node
        return left_node
    return _parse
 
def _parse_sign(parse_next):
    def _parse(tokens):
        logging.debug(f"parse_sign... {tokens[0].value}")
        left_node = parse_next(tokens)
        if left_node.type_in(TokenType.U_SIGN):
            logging.debug(f"if parse_sign...{tokens[0].value}")
            while tokens[0].type_in(*EXPRESSION_BEHAVIOR):
                logging.debug(f"while parse_sign...{tokens[0].value}")
                node = tokens.pop(0)
                node.append(left_node, parse_expression(tokens))
                left_node = node
            else:
                pass

        return left_node
    return _parse
def _parse_root(parse_next):
    def _parse(tokens):
        logging.debug(f"parse_root... {tokens[0].value}");
        return parse_sum(tokens)
    return _parse

def parse_expression(tokens):
    logging.debug(f"parse_expresion... {tokens[0].value}")
    if tokens[0].type_in(*SIGN_BEHAVIOR): 
        node = tokens.pop(0)
        next=parse_product(tokens)
        node.token_type = TokenType.U_SIGN
        node.append(next)
        return node

    if tokens[0].type_in(TokenType.T_SYMBOL) and tokens[1].type_in(TokenType.T_LPAR):
        node = tokens.pop(0)
        node.token_type = TokenType.G_FUNCTION
        match(tokens, TokenType.T_LPAR)
        node.append(parse_root(tokens))
        match(tokens, TokenType.T_RPAR, TokenType.T_SEPARATOR)
        return node
    elif tokens[0].type_in(*LEAF_BEHAVIOR):
        return tokens.pop(0)

    match(tokens, TokenType.T_LPAR)
    expression = Node(TokenType.G_PARENTHESIS)
    expression.append(parse_root(tokens))
    match(tokens, TokenType.T_RPAR)
    return expression

parse_power=_parse_left_right_operator("parse_power",(TokenType.T_POW,), parse_expression)
parse_product =_parse_left_right_operator("parse_product",(TokenType.T_MULT, TokenType.T_DIV), parse_power)
#parse_sign = _parse_sign(parse_product)
parse_sum = _parse_left_right_operator("parse_sum",(TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_SEPARATOR), parse_product)
parse_root = _parse_root(parse_sum)






def cleanup(inputstring):
    return re.sub(CLEANUP_REGEX, '', inputstring)


def parse(inputstring):
    tokens = lexical_analysis(cleanup(inputstring))
    ast = parse_root(tokens)
    match(tokens, TokenType.T_END)
    return ast


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG)
    inputstring =  sys.argv[1] if len(sys.argv) ==2 else "(-1^2+1)/(-1+2)"
    ast = parse(inputstring)
    print(f"expresion parsed: {cleanup(inputstring)}")
    ast.print()
