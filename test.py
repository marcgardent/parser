import unittest
import compute
from  compress import compress, sequences
from formula import lexical_analysis, TokenType, cleanup, parse, UnexpectedTokenException,InvalidTokenException
import serialize

class TestStringMethods(unittest.TestCase):

    def test_cleanup(self):
        for string in ["A+A", "A + A", " A+A", "A+A "]:
            with self.subTest("Checking if string is cleaned", string=string):
                r = cleanup(string)
                self.assertEqual("A+A", r)

    def test_scalar(self):
        cases= [
            ("0.0", TokenType.T_FLOAT),
            (".1", TokenType.T_FLOAT),
            ("1", TokenType.T_NUM)
        ]
        
        for (number, tokenType) in cases:
            with self.subTest("Checking if number is tokenized", number=number, tokenType=tokenType):
                result = lexical_analysis(number)
                self.assertListEqual([t.token_type for t in result], [
                                     tokenType, TokenType.T_END])
                self.assertListEqual([t.value for t in result], [number, None])

    def test_symbol(self):
        for number in ["a", "A", "aaa", "a.a", "a_ass", "a1", "a1_z.x"]:
            with self.subTest("Checking if number is tokenized", number=number):
                result = lexical_analysis(number)
                self.assertListEqual([t.token_type for t in result], [
                                     TokenType.T_SYMBOL, TokenType.T_END])
                self.assertListEqual([t.value for t in result], [number, None])

    def test_simple_tokens(self):
        for (exp, tokenType) in [("+", TokenType.T_PLUS), ("*", TokenType.T_MULT), ("/", TokenType.T_DIV), ("-", TokenType.T_MINUS), (",", TokenType.T_SEPARATOR)]:
            with self.subTest("Checking if exp is tokenType", exp=exp, tokenType=tokenType):
                result = lexical_analysis("1"+exp+"1")
                self.assertListEqual([t.token_type for t in result], [
                                     TokenType.T_NUM, tokenType, TokenType.T_NUM, TokenType.T_END])
                self.assertListEqual([t.value for t in result], [
                                     '1', exp, '1', None])

    def test_parenthesis(self):
        result = lexical_analysis("(1)")
        self.assertListEqual([t.token_type for t in result], [
                             TokenType.T_LPAR, TokenType.T_NUM, TokenType.T_RPAR, TokenType.T_END])
        self.assertListEqual([t.value for t in result], ['(', '1', ')', None])

    def test_function(self):
        result = lexical_analysis("fn(1)")
        self.assertListEqual([t.token_type for t in result], [
                             TokenType.T_SYMBOL, TokenType.T_LPAR, TokenType.T_NUM, TokenType.T_RPAR, TokenType.T_END])
        self.assertListEqual([t.value for t in result], [
                             'fn', '(', '1', ')', None])

    def test_computation(self):
        cases = [('1+1', 2), ('1-1', 0), ('3-2+1', 2), ('8/4/2', 1),
                ('1*2', 2), ('(1+7)*(9+2)', 88), ('(2+7)/4', 2.25),
                ('7/4', 1.75), ('2*3+4', 10), ('2*(3+4)', 14),
                ('2+3*4', 14), ('2+(3*4)', 14), ('2-(3*4+1)', -11),
                ('2*(3*4+1)', 26), ('8/((1+3)*2)', 1), ('101', 101),  ('1+2^2+1',6)]
        for (exp, value) in cases:
                with self.subTest("Checking if exp is computed", exp=exp, value=value):
                    actual_result = compute.compute(parse(exp))
                    self.assertEqual(value, actual_result)

    def test_parsing_failed(self):
        for exp in ["1+1)", "fun(1", '((1)']:
                with self.subTest("Checking if the parse() raise UnexpectedTokenException", exp=exp):
                    x = lambda : parse(exp)
                    self.assertRaises(UnexpectedTokenException, x)

    def test_tokenizing_failed(self):
        for exp in ["1+1$", "fun 1", ' 0+.aa']:
            with self.subTest("Checking if the lexical_analysis() raise InvalidTokenException", exp=exp):
                x = lambda : lexical_analysis(exp)
                self.assertRaises(InvalidTokenException, x)
                    
    def test_computing_failed(self):
        for exp in ["fn(1)", "1+a", '1+1.2']:
            with self.subTest("Checking if the compute() raise NotImplementedException", exp=exp):
                x = lambda : compute.compute(parse(exp))
                self.assertRaises(compute.NotImplementedException, x)
    
    def test_serialize(self):
        cases = [
            '1',
            'a',
            '1-1', 
            '1+(1-1)-1',
            '(1+1)/2'
        ]
        for exp in cases:
            with self.subTest("Checking if exp is computed", exp=exp):
                actual_result = serialize.serialize(parse(exp))
                self.assertEqual(exp, actual_result)

    def test_compression(self):
        cases = [
            ('1', 'f()->{1}'), # constant
            ('a', 'f(a)->{a}'), # identity
            ('a*a', 'f(a)->{a*a}'), # identity
            ('-1+2*(1/2)^2-func(x)', 'f(x)->{-1+(1/2)*2^2-func(x)}'), # sample with all operators
            # ('(a+a)*(a+a)', 'f(a)->{v0=(a+a);v0*v0}'), # factorization
            # ('(a+b)*(a+b)-a+b', 'f(a)->{v0=(a+b);v0*v0-a+b}'), # factorization
        ]
        for (exp, compressed) in cases:
            with self.subTest("Checking if exp is computed", exp=exp, compressed=compressed):
                actual_result = compress(exp)
                self.assertEqual(compressed, actual_result)

    def test_sequences_limit(self):
        actual=list(sequences(['A','B','C']))
        self.assertEqual(3,len(actual))
        self.assertTupleEqual(actual[0], (('A','B'),('C',)))
        self.assertTupleEqual(actual[1],(('A','C'),('B',)))
        self.assertTupleEqual(actual[2],(('B','C'),('A',)))

    def test_sequences(self):
        actual=list(sequences(['A','B','C','D']))
        self.assertEqual(7,len(actual))

        self.assertTupleEqual(actual[0], (('A','B'),('C','D',)),"at 0")
        self.assertTupleEqual(actual[1],(('A','C',),('B','D',)),"at 1")
        self.assertTupleEqual(actual[2],(('A','D',),('B','C')),"at 2")

        self.assertTupleEqual(actual[3],(('A', 'B', 'C'), ('D',)), "at 3")
        self.assertTupleEqual(actual[4],(('A', 'B', 'D'), ('C',)), "at 4")
        self.assertTupleEqual(actual[5],(('A', 'C', 'D'), ('B',)), "at 5")
        self.assertTupleEqual(actual[6], (('B', 'C', 'D'), ('A',)), "at 6")
        


        



if __name__ == '__main__':
    unittest.main()
