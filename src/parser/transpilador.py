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
        self.scopes = []

    def add_linha(self, texto):
        self.codigo_gerado.append("    " * self.indentacao + texto)

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if self.scopes:
            self.scopes.pop()

    def current_scope(self):
        return self.scopes[-1] if self.scopes else self.tabela_simbolos

    def define_symbol(self, nome, tipo):
        self.current_scope()[nome] = tipo

    def lookup_symbol(self, nome):
        for scope in reversed(self.scopes):
            if nome in scope:
                return scope[nome]
        return self.tabela_simbolos.get(nome)

    def _strip_parens(self, s: str) -> str:
        s = s.strip()
        while s.startswith('(') and s.endswith(')'):
            s = s[1:-1].strip()
        return s

    def _is_int(self, s: str) -> bool:
        s = self._strip_parens(s)
        try:
            int(s)
            return True
        except Exception:
            return False

    def _is_float(self, s: str) -> bool:
        s = self._strip_parens(s)
        try:
            float(s)
            return '.' in s or 'e' in s.lower()
        except Exception:
            return False

    def _is_str(self, s: str) -> bool:
        s = s.strip()
        return len(s) >= 2 and s[0] == '"' and s[-1] == '"'

    def _to_number(self, s: str):
        s = self._strip_parens(s)
        if self._is_int(s):
            return int(s)
        return float(s)

    def _fold_binop(self, left: str, op: str, right: str):
        if self._is_str(left) and self._is_str(right) and op == '+':
            a = left.strip()[1:-1]
            b = right.strip()[1:-1]
            return '"' + (a + b) + '"'

        if (self._is_int(left) or self._is_float(left)) and (self._is_int(right) or self._is_float(right)):
            a = self._to_number(left)
            b = self._to_number(right)
            try:
                if op == '+':
                    res = a + b
                elif op == '-':
                    res = a - b
                elif op == '*':
                    res = a * b
                elif op == '/':
                    res = a / b
                elif op in ('<', '>', '<=', '>=', '==', '!='):
                    if op == '<':
                        return str(a < b)
                    if op == '>':
                        return str(a > b)
                    if op == '<=':
                        return str(a <= b)
                    if op == '>=':
                        return str(a >= b)
                    if op == '==':
                        return str(a == b)
                    if op == '!=':
                        return str(a != b)
                else:
                    return None
                if isinstance(res, float) and res.is_integer():
                    return str(int(res))
                return str(res)
            except Exception:
                return None
        return None

    def _input_for_type(self, tipo: str) -> str:
        if tipo == 'int':
            return 'int(input())'
        if tipo == 'float':
            return 'float(input())'
        if tipo == 'bool':
            return '(input().strip().lower() in ("verdadeiro", "true", "1"))'
        return 'input()'

    def visitProgram(self, ctx):
        self.add_linha("# Código gerado pelo compilador MiniLang")
        self.add_linha("import sys\n")
        for child in ctx.getChildren():
            if child.getText() != '<EOF>':
                self.visit(child)
        return "\n".join(self.codigo_gerado)

    def visitVarDecl(self, ctx):
        nome = ctx.IDENT().getText()
        tipo = ctx.type_().getText()
        if not self.scopes:
            self.tabela_simbolos[nome] = tipo
            valor = "0.0" if tipo == "float" else "0"
            self.add_linha(f"{nome} = {valor}")
        else:
            self.define_symbol(nome, tipo)
        return None

    def visitFuncDecl(self, ctx):
        nome = ctx.IDENT().getText()
        params = []
        if ctx.params() and ctx.params().param():
            for p in ctx.params().param():
                params.append(p.IDENT().getText())
        self.add_linha(f"def {nome}({', '.join(params)}):")
        self.indentacao += 1
        self.push_scope()
        if ctx.params() and ctx.params().param():
            for p in ctx.params().param():
                self.define_symbol(p.IDENT().getText(), p.type_().getText())
        self.visit(ctx.block())
        self.pop_scope()
        self.indentacao -= 1
        self.add_linha("")
        return None

    def visitBlock(self, ctx):
        self.push_scope()
        for stmt in ctx.statement():
            self.visit(stmt)
        self.pop_scope()
        return None

    def visitStmtIf(self, ctx):
        cond = self.visit(ctx.expression())
        self.add_linha(f"if {cond}:")
        self.indentacao += 1
        self.visit(ctx.block())
        self.indentacao -= 1
        return None

    def visitStmtIfElse(self, ctx):
        cond = self.visit(ctx.expression())
        self.add_linha(f"if {cond}:")
        self.indentacao += 1
        self.visit(ctx.block(0))
        self.indentacao -= 1
        self.add_linha("else:")
        self.indentacao += 1
        self.visit(ctx.block(1))
        self.indentacao -= 1
        return None

    def visitStmtWhile(self, ctx):
        cond = self.visit(ctx.expression())
        self.add_linha(f"while {cond}:")
        self.indentacao += 1
        self.visit(ctx.block())
        self.indentacao -= 1
        return None

    def visitStmtFor(self, ctx):
        nome = ctx.IDENT().getText()
        inicio = self.visit(ctx.expression(0))
        fim = self.visit(ctx.expression(1))
        self.add_linha(f"for {nome} in range({inicio}, {fim} + 1):")
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

    def visitStmtLeia(self, ctx):
        nome = ctx.IDENT().getText()
        tipo = self.lookup_symbol(nome)
        entrada = self._input_for_type(tipo) if tipo else 'input()'
        self.add_linha(f"{nome} = {entrada}")
        return None

    def visitStmtFuncCall(self, ctx):
        self.add_linha(self.visit(ctx.funcCall()))
        return None

    def visitFuncCall(self, ctx):
        nome = ctx.IDENT().getText()
        args = []
        if ctx.argList():
            for expr in ctx.argList().expression():
                args.append(str(self.visit(expr)))
        return f"{nome}({', '.join(args)})"

    def visitExprLogico(self, ctx):
        esq = self.visit(ctx.expression(0))
        dir = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        op = 'and' if op == 'e' else 'or'
        return f"({esq} {op} {dir})"

    def visitExprIgualdade(self, ctx):
        esq = self.visit(ctx.expression(0))
        dir = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        return f"({esq} {op} {dir})"

    def visitExprRelacional(self, ctx):
        esq = self.visit(ctx.expression(0))
        dir = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        return f"({esq} {op} {dir})"

    def visitExprAditivo(self, ctx):
        esq = self.visit(ctx.expression(0))
        dir = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        folded = self._fold_binop(esq, op, dir)
        if folded is not None:
            return folded
        return f"({esq} {op} {dir})"

    def visitExprMultiplicativo(self, ctx):
        esq = self.visit(ctx.expression(0))
        dir = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        folded = self._fold_binop(esq, op, dir)
        if folded is not None:
            return folded
        return f"({esq} {op} {dir})"

    def visitExprNegacao(self, ctx):
        return f"(-{self.visit(ctx.expression())})"

    def visitPrimInt(self, ctx):
        return ctx.INT_LIT().getText()

    def visitPrimFloat(self, ctx):
        return ctx.FLOAT_LIT().getText()

    def visitPrimString(self, ctx):
        return ctx.STR_LIT().getText()

    def visitPrimVerdadeiro(self, ctx):
        return 'True'

    def visitPrimFalso(self, ctx):
        return 'False'

    def visitPrimIdent(self, ctx):
        return ctx.IDENT().getText()

    def visitPrimParens(self, ctx):
        return f"({self.visit(ctx.expression())})"

    def visitPrimFloat(self, ctx):
        return ctx.FLOAT_LIT().getText()

    def visitPrimString(self, ctx):
        return ctx.STR_LIT().getText()

    def visitPrimVerdadeiro(self, ctx):
        return "True"

    def visitPrimFalso(self, ctx):
        return "False"

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