"""
main_lexer.py — Testador do Analisador Léxico da MiniLang
Disciplina: Compiladores | UFT — Palmas/TO

Pré-requisitos:
    pip install antlr4-python3-runtime==4.13.1
    java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -o src/gramatica/generated src/gramatica/MiniLangLexer.g4

Uso:
    python src/lexer/main_lexer.py tests/exemplos/exemplo1_fatorial.minilang
    python src/lexer/main_lexer.py tests/exemplos/exemplo1_fatorial.minilang --salvar saida.txt
"""

import sys
import os
import argparse

# Caminho absoluto até a pasta generated, independente de onde o script é chamado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED = os.path.join(BASE_DIR, '..', 'gramatica', 'generated')
sys.path.insert(0, os.path.normpath(GENERATED))

from antlr4 import CommonTokenStream, InputStream

try:
    # ANTLR gera o arquivo com o mesmo nome da grammar: MiniLangLexer.py
    from MiniLangLexer import MiniLangLexer
except ImportError:
    print("ERRO: Arquivos gerados pelo ANTLR não encontrados.")
    print("Execute primeiro (a partir da raiz do projeto):")
    print("  java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -o src/gramatica/generated src/gramatica/MiniLangLexer.g4")
    sys.exit(1)


def tokenizar(codigo: str, nome_arquivo: str = "<stdin>") -> list:
    entrada = InputStream(codigo)
    lexer   = MiniLangLexer(entrada)
    stream  = CommonTokenStream(lexer)
    stream.fill()

    nomes  = lexer.symbolicNames
    tokens = []

    for tok in stream.tokens:
        if tok.type == -1:
            break

        tipo   = nomes[tok.type] if 0 < tok.type < len(nomes) else f"TOKEN_{tok.type}"
        lexema = tok.text
        linha  = tok.line

        if tipo == 'ERRO':
            print(f"[ERRO LÉXICO] Caractere inesperado '{lexema}' na linha {linha}", file=sys.stderr)

        tokens.append({'tipo': tipo, 'lexema': lexema, 'linha': linha})

    return tokens


def formatar_saida(tokens: list) -> str:
    linhas = []
    for tok in tokens:
        entrada = f"<{tok['tipo']},{tok['lexema']}>"
        linhas.append(f"{entrada:<35}  (linha {tok['linha']})")
    return "\n".join(linhas)


def main():
    parser = argparse.ArgumentParser(description="Analisador Léxico — MiniLang")
    parser.add_argument("arquivo", help="Arquivo .minilang de entrada")
    parser.add_argument("--salvar", metavar="SAIDA", help="Salvar saída em arquivo .txt")
    args = parser.parse_args()

    if not os.path.exists(args.arquivo):
        print(f"ERRO: Arquivo '{args.arquivo}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    with open(args.arquivo, encoding="utf-8") as f:
        codigo = f.read()

    print(f"{'='*57}")
    print(f"  Analisador Léxico — MiniLang")
    print(f"  Arquivo: {args.arquivo}")
    print(f"{'='*57}")

    tokens = tokenizar(codigo, args.arquivo)
    saida  = formatar_saida(tokens)

    print(saida)
    print(f"{'='*57}")
    print(f"  Total de tokens: {len(tokens)}")
    print(f"{'='*57}")

    if args.salvar:
        with open(args.salvar, "w", encoding="utf-8") as f:
            f.write(saida + "\n")
        print(f"\nSaída salva em: {args.salvar}")


if __name__ == "__main__":
    main()
