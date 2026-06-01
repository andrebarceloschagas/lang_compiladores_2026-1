"""
ast_printer.py — Imprime a AST da MiniLang em formato compacto de árvore
Disciplina: Compiladores | UFT — Palmas/TO
"""

import sys
import os

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
GENERATED = os.path.normpath(os.path.join(BASE_DIR, '..', 'gramatica', 'generated'))
sys.path.insert(0, GENERATED)

from antlr4 import TerminalNode

try:
    from MiniLangParser import MiniLangParser
except ImportError:
    pass


class _Syn:
    """Nó sintético para rotular partes semânticas (Cond:, Then:, Else:, De:, Ate:, Body:)."""
    def __init__(self, label, children):
        self.label    = label
        self.children = children


class ASTPrinter:

    def imprimir(self, tree, parser) -> str:
        linhas = ["Program"]
        filhos = self._filhos(tree)
        n = len(filhos)
        for i, filho in enumerate(filhos):
            self._render(filho, "", i == n - 1, linhas)
        return "\n".join(linhas)

    # ── Renderização ─────────────────────────────────────────────────────────

    def _render(self, node, prefixo, ultimo, linhas):
        conector = "└── " if ultimo else "├── "
        extensao = "    " if ultimo else "│   "

        if isinstance(node, _Syn):
            linhas.append(prefixo + conector + node.label)
            filhos = node.children
        else:
            node   = self._norm(node)
            linhas.append(prefixo + conector + self._rotulo(node))
            filhos = self._filhos(node)

        n = len(filhos)
        for i, filho in enumerate(filhos):
            self._render(filho, prefixo + extensao, i == n - 1, linhas)

    # ── Normalização (nós transparentes) ─────────────────────────────────────

    def _norm(self, ctx):
        """Remove nós de passagem (pass-through) até o nó significativo."""
        P = MiniLangParser
        while True:
            if isinstance(ctx, P.DeclarationContext):
                ctx = ctx.varDecl() or ctx.funcDecl()
            elif isinstance(ctx, P.StmtVarDeclContext):
                ctx = ctx.varDecl()
            elif isinstance(ctx, P.StmtFuncCallContext):
                ctx = ctx.funcCall()
            elif isinstance(ctx, P.ExprPrimaryContext):
                ctx = ctx.primary()
            elif isinstance(ctx, P.PrimFuncCallContext):
                ctx = ctx.funcCall()
            elif isinstance(ctx, P.PrimParensContext):
                ctx = ctx.expression()
            else:
                break
        return ctx

    # ── Rótulos ──────────────────────────────────────────────────────────────

    def _rotulo(self, ctx) -> str:
        P = MiniLangParser

        if isinstance(ctx, P.FuncDeclContext):
            return f"FuncDecl: {ctx.IDENT().getText()} : {ctx.type_().getText()}"
        if isinstance(ctx, P.VarDeclContext):
            return f"VarDecl: {ctx.IDENT().getText()} : {ctx.type_().getText()}"
        if isinstance(ctx, P.ParamsContext):
            return "Params"
        if isinstance(ctx, P.ParamContext):
            return f"Param: {ctx.IDENT().getText()} : {ctx.type_().getText()}"
        if isinstance(ctx, P.BlockContext):
            return "Block"
        if isinstance(ctx, P.StmtIfContext):
            return "IfStmt"
        if isinstance(ctx, P.StmtIfElseContext):
            return "IfElseStmt"
        if isinstance(ctx, P.StmtWhileContext):
            return "WhileStmt"
        if isinstance(ctx, P.StmtForContext):
            return f"ForStmt: {ctx.IDENT().getText()}"
        if isinstance(ctx, P.StmtReturnContext):
            return "ReturnStmt"
        if isinstance(ctx, P.StmtEscrevaContext):
            return "Escreva"
        if isinstance(ctx, P.StmtLeiaContext):
            return f"Leia: {ctx.IDENT().getText()}"
        if isinstance(ctx, P.StmtAssignContext):
            return f"Assign: {ctx.IDENT().getText()}"
        if isinstance(ctx, P.FuncCallContext):
            return f"FuncCall: {ctx.IDENT().getText()}"
        if isinstance(ctx, P.ExprLogicoContext):
            op = ctx.E_LOG() or ctx.OU_LOG()
            return f"BinOp({op.getText()})"
        if isinstance(ctx, P.ExprIgualdadeContext):
            op = ctx.EQ() or ctx.NEQ()
            return f"BinOp({op.getText()})"
        if isinstance(ctx, P.ExprRelacionalContext):
            for tok in (ctx.LEQ(), ctx.GEQ(), ctx.LT(), ctx.GT()):
                if tok:
                    return f"BinOp({tok.getText()})"
        if isinstance(ctx, P.ExprAditivoContext):
            op = ctx.PLUS() or ctx.MINUS()
            return f"BinOp({op.getText()})"
        if isinstance(ctx, P.ExprMultiplicativoContext):
            op = ctx.STAR() or ctx.SLASH()
            return f"BinOp({op.getText()})"
        if isinstance(ctx, P.ExprNegacaoContext):
            return "UnaryOp(-)"
        if isinstance(ctx, P.PrimIntContext):
            return f"Int({ctx.INT_LIT().getText()})"
        if isinstance(ctx, P.PrimFloatContext):
            return f"Float({ctx.FLOAT_LIT().getText()})"
        if isinstance(ctx, P.PrimStringContext):
            return f"Str({ctx.STR_LIT().getText()})"
        if isinstance(ctx, P.PrimVerdadeiroContext):
            return "Bool(verdadeiro)"
        if isinstance(ctx, P.PrimFalsoContext):
            return "Bool(falso)"
        if isinstance(ctx, P.PrimIdentContext):
            return f"Ident({ctx.IDENT().getText()})"

        return type(ctx).__name__.replace("Context", "")

    # ── Filhos ───────────────────────────────────────────────────────────────

    def _filhos(self, ctx) -> list:
        if isinstance(ctx, _Syn):
            return ctx.children

        P = MiniLangParser

        if isinstance(ctx, P.ProgramContext):
            return [ctx.getChild(i)
                    for i in range(ctx.getChildCount())
                    if not isinstance(ctx.getChild(i), TerminalNode)]

        if isinstance(ctx, P.FuncDeclContext):
            filhos = []
            if ctx.params().param():
                filhos.append(ctx.params())
            filhos.append(ctx.block())
            return filhos

        if isinstance(ctx, P.ParamsContext):
            return list(ctx.param())

        if isinstance(ctx, P.BlockContext):
            return list(ctx.statement())

        if isinstance(ctx, P.StmtIfContext):
            return [
                _Syn("Cond:", [ctx.expression()]),
                _Syn("Then:", [ctx.block()]),
            ]

        if isinstance(ctx, P.StmtIfElseContext):
            return [
                _Syn("Cond:", [ctx.expression()]),
                _Syn("Then:", [ctx.block(0)]),
                _Syn("Else:", [ctx.block(1)]),
            ]

        if isinstance(ctx, P.StmtWhileContext):
            return [
                _Syn("Cond:", [ctx.expression()]),
                _Syn("Body:", [ctx.block()]),
            ]

        if isinstance(ctx, P.StmtForContext):
            return [
                _Syn("De:", [ctx.expression(0)]),
                _Syn("Ate:", [ctx.expression(1)]),
                _Syn("Body:", [ctx.block()]),
            ]

        if isinstance(ctx, P.StmtReturnContext):
            return [ctx.expression()]

        if isinstance(ctx, P.StmtEscrevaContext):
            return [ctx.expression()]

        if isinstance(ctx, P.StmtAssignContext):
            return [ctx.expression()]

        if isinstance(ctx, P.FuncCallContext):
            return list(ctx.argList().expression())

        if isinstance(ctx, (P.ExprLogicoContext, P.ExprIgualdadeContext,
                             P.ExprRelacionalContext, P.ExprAditivoContext,
                             P.ExprMultiplicativoContext)):
            return [ctx.expression(0), ctx.expression(1)]

        if isinstance(ctx, P.ExprNegacaoContext):
            return [ctx.expression()]

        return []
