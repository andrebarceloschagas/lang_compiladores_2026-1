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
from parser.ast_printer import ASTPrinter


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


def test_exemplo1_parser_ast():
    exemplo = os.path.join(BASE_DIR, 'tests', 'exemplos', 'exemplo1_fatorial.minilang')
    expected_ast = os.path.join(BASE_DIR, 'tests', 'saidas_esperadas', 'exemplo1_ast.txt')

    with open(exemplo, encoding='utf-8') as f:
        codigo = f.read()

    tree, parser, errors = parse_code(codigo)
    assert errors == []

    printer = ASTPrinter()
    ast_str = printer.imprimir(tree, parser)

    import re

    def normalize_ast(lines):
        normalized = []
        for line in lines:
            text = line.strip()
            text = re.sub(r'^[│\s]*[├└]──\s*', '', text)
            normalized.append(text)
        return normalized

    with open(expected_ast, encoding='utf-8') as f:
        esperada = [line for line in f.read().splitlines() if not line.startswith('#') and line.strip()]

    ast_clean = [line for line in ast_str.splitlines() if line.strip()]

    assert normalize_ast(ast_clean) == normalize_ast(esperada)
