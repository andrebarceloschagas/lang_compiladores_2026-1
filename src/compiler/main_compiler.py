"""Compilador completo de MiniLang para Python.

Esta ferramenta executa análise léxica, sintática, semântica e geração de código.
"""

import argparse
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.normpath(os.path.join(BASE_DIR, '..'))
GRAMMAR_DIR = os.path.normpath(os.path.join(SRC_DIR, 'gramatica', 'generated'))
sys.path.insert(0, GRAMMAR_DIR)
sys.path.insert(0, SRC_DIR)

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from MiniLangLexer import MiniLangLexer
from MiniLangParser import MiniLangParser
from parser.ast_printer import ASTPrinter
from compiler.transpilador import MiniLangCompiler
from compiler.semantic_analyzer import SemanticAnalyzer


class ColetorDeErros(ErrorListener):
    def __init__(self):
        super().__init__()
        self.erros = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.erros.append(f"linha {line}:{column} — {msg}")


def format_tokens(lexer, tokens):
    nomes = lexer.symbolicNames
    lines = []
    for tok in tokens:
        if tok.type == -1:
            break
        tipo = nomes[tok.type] if 0 < tok.type < len(nomes) else f"TOKEN_{tok.type}"
        lines.append(f"<{tipo},{tok.text}> (linha {tok.line})")
    return "\n".join(lines)


def salvar_tokens(arquivo, destino):
    with open(arquivo, encoding='utf-8') as f:
        codigo = f.read()
    lexer = MiniLangLexer(InputStream(codigo))
    stream = CommonTokenStream(lexer)
    stream.fill()
    tokens = stream.tokens
    with open(destino, 'w', encoding='utf-8') as f:
        f.write(format_tokens(lexer, tokens) + '\n')
    return format_tokens(lexer, tokens)


def parsear(arquivo):
    with open(arquivo, encoding='utf-8') as f:
        codigo = f.read()
    entrada = InputStream(codigo)
    lexer = MiniLangLexer(entrada)
    stream = CommonTokenStream(lexer)
    parser = MiniLangParser(stream)
    parser.removeErrorListeners()
    coletor = ColetorDeErros()
    parser.addErrorListener(coletor)
    tree = parser.program()
    return tree, parser, coletor.erros


def main():
    arg_parser = argparse.ArgumentParser(description='Compilador completo MiniLang')
    arg_parser.add_argument('arquivo', help='Arquivo .minilang de entrada')
    arg_parser.add_argument('--tokens', metavar='TOKENS', help='Salvar tokens em arquivo')
    arg_parser.add_argument('--ast', metavar='AST', help='Salvar AST formato texto em arquivo')
    arg_parser.add_argument('--py', metavar='PY', help='Salvar código Python gerado em arquivo')
    arg_parser.add_argument('--report', metavar='REPORT', help='Salvar relatório de compilação em Markdown')
    args = arg_parser.parse_args()

    if not os.path.exists(args.arquivo):
        print(f"ERRO: Arquivo '{args.arquivo}' não encontrado.")
        sys.exit(1)

    output_py = args.py or args.arquivo.replace('.minilang', '.py')
    report_path = args.report
    tokens_path = args.tokens
    ast_path = args.ast

    report = [f"# Relatório de compilação: {os.path.basename(args.arquivo)}", '']
    report.append(f"- Entrada: `{os.path.abspath(args.arquivo)}`")
    report.append(f"- Saída Python: `{os.path.abspath(output_py)}`")
    report.append('')

    if tokens_path:
        token_text = salvar_tokens(args.arquivo, tokens_path)
        report.append('## Tokens gerados')
        report.append('```')
        report.append(token_text)
        report.append('```')
        report.append('')

    tree, parser, errors = parsear(args.arquivo)
    if errors:
        print('Erros sintáticos encontrados:')
        for err in errors:
            print(err)
        if report_path:
            report.append('## Erros sintáticos')
            report.extend([f'- {err}' for err in errors])
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report))
        sys.exit(1)

    if ast_path:
        printer = ASTPrinter()
        ast_str = printer.imprimir(tree, parser)
        with open(ast_path, 'w', encoding='utf-8') as f:
            f.write(ast_str + '\n')
        report.append('## AST')
        report.append('```')
        report.append(ast_str)
        report.append('```')
        report.append('')

    semantic = SemanticAnalyzer()
    semantic.visit(tree)
    if semantic.errors:
        print('Erros semânticos encontrados:')
        for err in semantic.errors:
            print(err)
        if report_path:
            report.append('## Erros semânticos')
            report.extend([f'- {err}' for err in semantic.errors])
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report))
        sys.exit(1)

    compiler = MiniLangCompiler()
    python_code = compiler.visit(tree)
    with open(output_py, 'w', encoding='utf-8') as f:
        f.write(python_code)

    print(f'Compilação concluída. Código Python salvo em: {output_py}')
    if report_path:
        report.append('## Resultado')
        report.append(f'- Código Python gerado em `{os.path.abspath(output_py)}`')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))


if __name__ == '__main__':
    main()
