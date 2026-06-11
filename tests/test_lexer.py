import os
from antlr4 import CommonTokenStream, InputStream

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATED = os.path.join(BASE_DIR, 'src', 'gramatica', 'generated')
import sys
sys.path.insert(0, GENERATED)
from MiniLangLexer import MiniLangLexer


def load_tokens(path):
    with open(path, encoding='utf-8') as f:
        return [line.strip() for line in f if line.startswith('<')]


def tokenize(code):
    lexer = MiniLangLexer(InputStream(code))
    stream = CommonTokenStream(lexer)
    stream.fill()
    tokens = []
    for tok in stream.tokens:
        if tok.type == -1:
            break
        token_type = lexer.symbolicNames[tok.type] if 0 < tok.type < len(lexer.symbolicNames) else f'TOKEN_{tok.type}'
        tokens.append(f"<{token_type},{tok.text}>")
    return tokens


def test_exemplo1_tokens():
    exemplo = os.path.join(BASE_DIR, 'tests', 'exemplos', 'exemplo1_fatorial.minilang')
    esperada = os.path.join(BASE_DIR, 'tests', 'saidas_esperadas', 'exemplo1_tokens.txt')

    with open(exemplo, encoding='utf-8') as f:
        codigo = f.read()

    tokens = tokenize(codigo)
    esperados = [line.split('  ')[0].strip() for line in load_tokens(esperada)]

    assert tokens == esperados
