import os
from antlr4 import CommonTokenStream, InputStream

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
GENERATED = os.path.join(SRC_DIR, 'gramatica', 'generated')
import sys
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, GENERATED)
from MiniLangLexer import MiniLangLexer
from MiniLangParser import MiniLangParser
from antlr4.error.ErrorListener import ErrorListener
from compiler.semantic_analyzer import SemanticAnalyzer


class ColetorDeErros(ErrorListener):
    def __init__(self):
        super().__init__()
        self.erros = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.erros.append(f"Linha {line}:{column} — {msg}")


def parse_code(code):
    input_stream = InputStream(code)
    lexer = MiniLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniLangParser(stream)
    parser.removeErrorListeners()
    coletor = ColetorDeErros()
    parser.addErrorListener(coletor)
    tree = parser.program()
    return tree, parser, coletor.erros


def test_semantic_valid_program():
    codigo = '''
funcao soma(a: int, b: int): int
  retorne a + b
fim

var x: int
x = soma(1, 2)
escreva(x)
'''
    tree, parser, errors = parse_code(codigo)
    assert errors == []

    analyzer = SemanticAnalyzer()
    analyzer.visit(tree)
    assert analyzer.errors == []


def test_semantic_undefined_variable():
    codigo = '''
var x: int
x = y + 1
'''
    tree, parser, errors = parse_code(codigo)
    assert errors == []

    analyzer = SemanticAnalyzer()
    analyzer.visit(tree)
    assert any('não declarado' in err or 'não declarada' in err for err in analyzer.errors)
