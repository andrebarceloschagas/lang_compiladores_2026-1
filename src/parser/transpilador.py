"""
transpilador.py — Tabela de Símbolos e Geração de Código
Disciplina: Compiladores | UFT — Palmas/TO
"""
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED = os.path.normpath(os.path.join(BASE_DIR, '..', 'gramatica', 'generated'))
sys.path.insert(0, GENERATED)

from antlr4 import *
from MiniLangLexer import MiniLangLexer
from MiniLangParser import MiniLangParser
from MiniLangVisitor import MiniLangVisitor

class MiniLangCompiler(MiniLangVisitor):
    def __init__(self):
        self.tabela_simbolos = {}
        self.codigo_gerado = []
        self.indentacao = 0

    def add_linha(self, texto):
        self.codigo_gerado.append("    " * self.indentacao + texto)

    def visitProgram(self, ctx):
        self.add_linha("# Código gerado pelo compilador MiniLang")
        self.add_linha("import sys\n")
        # Visita declarações e comandos globalmente
        for child in ctx.getChildren():
            if child.getText() != '<EOF>':
                self.visit(child)
        return "\n".join(self.codigo_gerado)

    def visitVarDecl(self, ctx):
        nome = ctx.IDENT().getText()
        tipo = ctx.type_().getText()
        self.tabela_simbolos[nome] = tipo
        # Inicializa a variável com valor padrão no escopo global
        if self.indentacao == 0:
            valor = "0.0" if tipo == "float" else "0"
            self.add_linha(f"{nome} = {valor}")
        return None

    def visitFuncDecl(self, ctx):
        nome = ctx.IDENT().getText()
        params = []
        # Captura os parâmetros da função, se existirem
        if ctx.params() and ctx.params().param():
            for p in ctx.params().param():
                params.append(p.IDENT().getText())
        
        self.add_linha(f"def {nome}({', '.join(params)}):")
        self.indentacao += 1
        self.visit(ctx.block())
        self.indentacao -= 1
        self.add_linha("")
        return None

    def visitBlock(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)
        return None

    def visitStmtIf(self, ctx):
        cond = self.visit(ctx.expression())
        self.add_linha(f"if {cond}:")
        self.indentacao += 1
        self.visit(ctx.block())
        self.indentacao -= 1
        return None

    def visitStmtReturn(self, ctx):
        expr = self.visit(ctx.expression())
        self.add_linha(f"return {expr}")
        return None

    def visitStmtAssign(self, ctx):
        nome = ctx.IDENT().getText()
        expr = self.visit(ctx.expression())
        self.add_linha(f"{nome} = {expr}")
        return None

    def visitStmtEscreva(self, ctx):
        expr = self.visit(ctx.expression())
        self.add_linha(f"print({expr})")
        return None

    def visitFuncCall(self, ctx):
        nome = ctx.IDENT().getText()
        args = []
        if ctx.argList():
            for expr in ctx.argList().expression():
                args.append(str(self.visit(expr)))
        return f"{nome}({', '.join(args)})"

    def visitExprAditivo(self, ctx):
        esq = self.visit(ctx.expression(0))
        dir = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        return f"({esq} {op} {dir})"

    def visitExprMultiplicativo(self, ctx):
        esq = self.visit(ctx.expression(0))
        dir = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        return f"({esq} {op} {dir})"

    def visitExprRelacional(self, ctx):
        esq = self.visit(ctx.expression(0))
        dir = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        return f"({esq} {op} {dir})"

    def visitPrimInt(self, ctx):
        return ctx.INT_LIT().getText()

    def visitPrimIdent(self, ctx):
        return ctx.IDENT().getText()

    def visitPrimParens(self, ctx):
        return f"({self.visit(ctx.expression())})"

# ── Execução ──────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python transpilador.py arquivo.minilang")
        sys.exit(1)

    arquivo = sys.argv[1]
    entrada = InputStream(open(arquivo, encoding="utf-8").read())
    lexer = MiniLangLexer(entrada)
    stream = CommonTokenStream(lexer)
    parser = MiniLangParser(stream)
    tree = parser.program()

    compilador = MiniLangCompiler()
    codigo_python = compilador.visit(tree)

    saida_py = arquivo.replace('.minilang', '.py')
    with open(saida_py, 'w', encoding="utf-8") as f:
        f.write(codigo_python)
        
    print(f" Compilação concluída! Código executável salvo em: {saida_py}")