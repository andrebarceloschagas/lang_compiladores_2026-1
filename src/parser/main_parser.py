"""
main_parser.py — Testador do Analisador Sintático da MiniLang
Disciplina: Compiladores | UFT — Palmas/TO

Pré-requisitos:
    java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -o src/gramatica/generated src/gramatica/MiniLang.g4

Uso:
    python src/parser/main_parser.py tests/exemplos/exemplo1_fatorial.minilang
    python src/parser/main_parser.py tests/exemplos/exemplo1_fatorial.minilang --ast
    python src/parser/main_parser.py tests/exemplos/exemplo4_erro_sintatico.minilang
"""

import sys
import os
import argparse

# Caminho absoluto até a pasta generated
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
GENERATED = os.path.normpath(os.path.join(BASE_DIR, '..', 'gramatica', 'generated'))
sys.path.insert(0, GENERATED)

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

try:
    from MiniLangLexer  import MiniLangLexer
    from MiniLangParser import MiniLangParser
except ImportError as e:
    print(f"ERRO: Arquivos gerados pelo ANTLR não encontrados: {e}")
    print("Execute primeiro (a partir da raiz do projeto):")
    print("  java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -o src/gramatica/generated src/gramatica/MiniLang.g4")
    sys.exit(1)

from ast_printer import ASTPrinter


# ── Coletor de erros sintáticos ──────────────────────────────

class ColetorDeErros(ErrorListener):
    def __init__(self):
        super().__init__()
        self.erros = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.erros.append(f"  Linha {line}:{column} — {msg}")


# ── Parsing ───────────────────────────────────────────────────

def parsear(codigo: str):
    entrada = InputStream(codigo)
    lexer   = MiniLangLexer(entrada)
    lexer.removeErrorListeners()

    stream = CommonTokenStream(lexer)
    parser = MiniLangParser(stream)
    parser.removeErrorListeners()

    coletor = ColetorDeErros()
    parser.addErrorListener(coletor)

    tree = parser.program()
    return tree, parser, coletor.erros


# ── Main ──────────────────────────────────────────────────────

def main():
    arg_parser = argparse.ArgumentParser(description="Analisador Sintático — MiniLang")
    arg_parser.add_argument("arquivo",          help="Arquivo .minilang de entrada")
    arg_parser.add_argument("--ast",            action="store_true", help="Exibir a AST formatada")
    arg_parser.add_argument("--salvar",         metavar="SAIDA",     help="Salvar AST em arquivo .txt")
    args = arg_parser.parse_args()

    if not os.path.exists(args.arquivo):
        print(f"ERRO: Arquivo '{args.arquivo}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    with open(args.arquivo, encoding="utf-8") as f:
        codigo = f.read()

    print(f"{'='*60}")
    print(f"  Analisador Sintático — MiniLang")
    print(f"  Arquivo : {args.arquivo}")
    print(f"{'='*60}")

    tree, parser, erros = parsear(codigo)

    if erros:
        print(f"\n❌  Parsing FALHOU — {len(erros)} erro(s) sintático(s):\n")
        for e in erros:
            print(e)
        print()
    else:
        print(f"\n✅  Parsing concluído com sucesso — nenhum erro sintático.\n")

    if args.ast or args.salvar:
        printer = ASTPrinter()
        ast_str = printer.imprimir(tree, parser)

        if args.ast:
            print("── AST ──────────────────────────────────────────────────")
            print(ast_str)
            print()

        if args.salvar:
            with open(args.salvar, "w", encoding="utf-8") as f:
                f.write(ast_str + "\n")
            print(f"AST salva em: {args.salvar}")

    print(f"{'='*60}")


if __name__ == "__main__":
    main()
