"""
Pré-requisitos:
    pip install antlr4-python3-runtime==4.13.1
    java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -o generated MiniLang.g4

Uso:
    python main_parser.py exemplo1_fatorial.minilang
    python main_parser.py exemplo1_fatorial.minilang --salvar saida_ast.txt
    python main_parser.py exemplo4_erro_sintatico.minilang   # exibe erros
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gramatica', 'generated'))

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

try:
    from MiniLangLexer import MiniLangLexer
    from MiniLangParser import MiniLangParser
except ImportError:
    print("ERRO: Arquivos gerados pelo ANTLR não encontrados.")
    print("Execute primeiro:")
    print("  java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -o generated MiniLang.g4")
    sys.exit(1)

from ast_printer import ASTPrinter


# ── Listener de erros customizado ────────────────────────────

class MiniLangErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.erros = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        erro = f"[ERRO SINTÁTICO] linha {line}:{column} — {msg}"
        self.erros.append(erro)
        print(erro, file=sys.stderr)


# ── Parsing ───────────────────────────────────────────────────

def parsear(codigo: str, nome_arquivo: str = "<stdin>"):
    """
    Retorna (arvore_parse, lista_de_erros).
    """
    entrada = InputStream(codigo)
    lexer   = MiniLangLexer(entrada)
    lexer.removeErrorListeners()

    error_listener = MiniLangErrorListener()
    lexer.addErrorListener(error_listener)

    stream = CommonTokenStream(lexer)
    parser = MiniLangParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    # Ponto de entrada: regra 'program'
    arvore = parser.program()

    return arvore, error_listener.erros


# ── Main ──────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Analisador Sintático da MiniLang")
    ap.add_argument("arquivo", help="Arquivo .minilang de entrada")
    ap.add_argument("--salvar", metavar="SAIDA", help="Salvar AST em arquivo .txt")
    args = ap.parse_args()

    if not os.path.exists(args.arquivo):
        print(f"ERRO: Arquivo '{args.arquivo}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    with open(args.arquivo, encoding="utf-8") as f:
        codigo = f.read()

    sep = "=" * 60
    print(sep)
    print(f"  Analisador Sintático — MiniLang")
    print(f"  Arquivo : {args.arquivo}")
    print(sep)

    arvore, erros = parsear(codigo, args.arquivo)

    if erros:
        print(f"\n  {len(erros)} erro(s) sintático(s) encontrado(s).")
        print(sep)
        sys.exit(1)

    printer   = ASTPrinter()
    saida_ast = printer.imprimir(arvore)

    print(saida_ast)
    print(sep)
    print("  Análise sintática concluída sem erros.")
    print(sep)

    if args.salvar:
        with open(args.salvar, "w", encoding="utf-8") as f:
            f.write(saida_ast + "\n")
        print(f"\n  AST salva em: {args.salvar}")


if __name__ == "__main__":
    main()
