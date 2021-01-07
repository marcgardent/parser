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
    T_SEPARATOR = 9
    T_EXP = 10
    T_END = 11

def tokenize_constant(tokenType, match):
    length = len(match)    
    def t(ctx):
        buffer=ctx.read(length)
        return (buffer == match, tokenType, match, len(buffer))
    return t

def tokenize_regex(tokenType, regex, buffer_size=16):
    def t(ctx):
        buffer=ctx.read(buffer_size)
        r = re.match(regex,buffer)
        success =r!=None
        return (success, tokenType, r.group(1) if success else None, len(buffer))
    return t

###################################################################################
# Modeling
###################################################################################
CLEANUP_REGEX = r'\s+'

TOKENIZERS = [
    tokenize_constant(TokenType.T_PLUS, '+'),
    tokenize_constant(TokenType.T_EXP, '^'),
    tokenize_constant(TokenType.T_MINUS, '-'),
    tokenize_constant(TokenType.T_MULT, '*'),
    tokenize_constant(TokenType.T_DIV, '/'),
    tokenize_constant(TokenType.T_LPAR, '('),
    tokenize_constant(TokenType.T_RPAR, ')'),
    tokenize_constant(TokenType.T_SEPARATOR, ','),
    tokenize_regex(TokenType.T_FLOAT, r'(\d*\.\d+)'),
    tokenize_regex(TokenType.T_NUM, r'(\d+)'),
    tokenize_regex(TokenType.T_SYMBOL, r'([a-zA-Z][a-zA-Z0-9_\.]*)'),
    ]

LEAF_BEHAVIOR = (TokenType.T_NUM, TokenType.T_FLOAT, TokenType.T_SYMBOL)
PRIORITY_BEHAVIOR = (TokenType.T_MULT, TokenType.T_DIV, TokenType.T_EXP)
DEFAULT_BEHAVIOR = (TokenType.T_PLUS, TokenType.T_MINUS,TokenType.T_SEPARATOR)
FLOAT_CAST_BEHAVIOR = (TokenType.T_NUM,  TokenType.T_FLOAT)
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
        self.children = []

    def print(self, padding=''):
        print(f"{padding}{self.token_type.name}={self.value}")

        padding=padding.replace('├', '|').replace('└', ' ').replace('─', ' ')
        for child in self.children[:-1]:
            child.print(padding+'   ├───')
        if len(self.children)>0: self.children[-1].print(padding+'   └───')

    def asInteger(self):
        if not self.token_type == TokenType.T_NUM: raise InvalidCastOperationException(f"can't cast the node {self.token_type} into int()")
        return int(self.value)

    def asFloat(self):
        if not self.token_type in (FLOAT_CAST_BEHAVIOR): raise InvalidCastOperationException(f"can't cast the node {self.token_type} into int()")
        return float(self.value)
        

def lexical_analysis(s):

    tokens = []

    length=len(s)
    
    ctx = io.StringIO(s)
    while ctx.tell() < length:
        token = None
        logging.debug("tokenize at char %s", ctx.tell())
        
        for tokenizer in TOKENIZERS:
            
            (success, tokenType, content, buffer) = tokenizer(ctx)
            logging.debug("tokenizer result: success=%s, tokenType=%s, content=%s, buffer=%s", success, tokenType, content, buffer)
            if success and len(content)==0:
                    logging.error(f"the token '{tokenType}' accepted but no char consumed: check the tokenizer() for the '{tokenType}'")
            elif success:
                token=Node(tokenType, value=content)
                logging.debug(f"token '{tokenType}' accepted with the value '{content}'")
                ctx.seek(ctx.tell()-(buffer-len(content)))
                break
            ctx.seek(ctx.tell()-buffer)
        if token: tokens.append(token)
        else: raise InvalidTokenException(f'unexpected token at char {ctx.tell()}: { ctx.read(16)}')
    
    tokens.append(Node(TokenType.T_END))
    return tokens

def match(tokens, *accepted):
    if tokens[0].token_type in accepted:
        return tokens.pop(0)
    else:
        raise UnexpectedTokenException('Invalid syntax on token {}: excepted ({})'.format(tokens[0].token_type, ','.join([str(t) for t in accepted])))

def parse_e(tokens):
    left_node = parse_e2(tokens)

    while tokens[0].token_type in DEFAULT_BEHAVIOR:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e2(tokens))
        left_node = node

    return left_node

def parse_e2(tokens):
    left_node = parse_e3(tokens)

    while tokens[0].token_type in PRIORITY_BEHAVIOR:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e3(tokens))
        left_node = node
    return left_node

def parse_e3(tokens):
    if tokens[0].token_type == TokenType.T_SYMBOL and tokens[1].token_type == TokenType.T_LPAR:
        node = tokens.pop(0)
        match(tokens, TokenType.T_LPAR)
        node.children.append(parse_e(tokens))
        match(tokens, TokenType.T_RPAR, TokenType.T_SEPARATOR)
        return node

    elif tokens[0].token_type in LEAF_BEHAVIOR:
        return tokens.pop(0)

    match(tokens, TokenType.T_LPAR)
    expression = parse_e(tokens)
    match(tokens, TokenType.T_RPAR)

    return expression

def cleanup(inputstring):
    return re.sub(CLEANUP_REGEX, '', inputstring)

def parse(inputstring):
    tokens = lexical_analysis(cleanup(inputstring))
    ast = parse_e(tokens)
    match(tokens, TokenType.T_END)
    return ast

if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG)
    inputstring = sys.argv[1]
    ast = parse(inputstring)
    print(f"expresion parsed: {cleanup(inputstring)}")
    ast.print()