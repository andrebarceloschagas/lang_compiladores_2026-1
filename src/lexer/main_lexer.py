"""
main_lexer.py — Testador do Analisador Léxico da MiniLang
Disciplina: Compiladores | UFT — Palmas/TO

Pré-requisitos:
    pip install antlr4-python3-runtime==4.13.1
    java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -o generated MiniLangLexer.g4

Uso:
    python main_lexer.py exemplo1_fatorial.minilang
    python main_lexer.py exemplo1_fatorial.minilang --salvar saida.txt
"""

import sys
import os
import argparse

# Adiciona a pasta generated ao path para importar os arquivos gerados pelo ANTLR
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'gramatica', 'generated'))

from antlr4 import CommonTokenStream, InputStream

try:
    from MiniLangLexerLexer import MiniLangLexerLexer
except ImportError:
    print("ERRO: Arquivos gerados pelo ANTLR não encontrados.")
    print("Execute primeiro:")
    print("  java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -o generated MiniLangLexer.g4")
    sys.exit(1)


def tokenizar(codigo: str, nome_arquivo: str = "<stdin>") -> list[dict]:
    """
    Recebe o código-fonte como string e retorna a lista de tokens
    no formato: [ { 'tipo': str, 'lexema': str, 'linha': int } ]
    """
    entrada = InputStream(codigo)
    lexer   = MiniLangLexerLexer(entrada)
    stream  = CommonTokenStream(lexer)
    stream.fill()

    nomes  = lexer.symbolicNames   # mapeia tipo numérico → nome do token
    tokens = []

    for tok in stream.tokens:
        # Ignora o token EOF
        if tok.type == -1:
            break

        tipo   = nomes[tok.type] if 0 < tok.type < len(nomes) else f"TOKEN_{tok.type}"
        lexema = tok.text
        linha  = tok.line

        # Verifica erro léxico
        if tipo == 'ERRO':
            print(f"[ERRO LÉXICO] Caractere inesperado '{lexema}' na linha {linha} de '{nome_arquivo}'",
                  file=sys.stderr)

        tokens.append({ 'tipo': tipo, 'lexema': lexema, 'linha': linha })

    return tokens


def formatar_saida(tokens: list[dict]) -> str:
    """Formata a lista de tokens no padrão <TIPO,lexema>  (linha N)"""
    linhas = []
    for tok in tokens:
        entrada = f"<{tok['tipo']},{tok['lexema']}>"
        linhas.append(f"{entrada:<30}  (linha {tok['linha']})")
    return "\n".join(linhas)


def main():
    parser = argparse.ArgumentParser(description="Analisador Léxico da MiniLang")
    parser.add_argument("arquivo", help="Arquivo .minilang de entrada")
    parser.add_argument("--salvar", metavar="SAIDA", help="Salvar saída em arquivo .txt")
    args = parser.parse_args()

    # Lê o arquivo de entrada
    if not os.path.exists(args.arquivo):
        print(f"ERRO: Arquivo '{args.arquivo}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    with open(args.arquivo, encoding="utf-8") as f:
        codigo = f.read()

    print(f"{'='*55}")
    print(f"  Analisador Léxico — MiniLang")
    print(f"  Arquivo: {args.arquivo}")
    print(f"{'='*55}")

    tokens = tokenizar(codigo, args.arquivo)
    saida  = formatar_saida(tokens)

    print(saida)
    print(f"{'='*55}")
    print(f"  Total de tokens: {len(tokens)}")
    print(f"{'='*55}")

    # Salva em arquivo se solicitado
    if args.salvar:
        with open(args.salvar, "w", encoding="utf-8") as f:
            f.write(saida + "\n")
        print(f"\nSaída salva em: {args.salvar}")


if __name__ == "__main__":
    main()
