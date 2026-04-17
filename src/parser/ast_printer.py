"""
ast_printer.py — Imprime a AST da MiniLang em formato de árvore
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


class ASTPrinter:

    def imprimir(self, tree, parser) -> str:
        linhas = ["└── Program"]
        filhos = self._filhos(tree)
        for i, filho in enumerate(filhos):
            ultimo = (i == len(filhos) - 1)
            self._visitar(filho, parser, "    ", ultimo, linhas)
        return "\n".join(linhas)

    def _visitar(self, node, parser, prefixo, ultimo, linhas):
        conector = "└── " if ultimo else "├── "
        extensao = "    " if ultimo else "│   "

        label = self._rotulo(node, parser)
        linhas.append(prefixo + conector + label)

        filhos = self._filhos(node)
        for i, filho in enumerate(filhos):
            self._visitar(filho, parser, prefixo + extensao, i == len(filhos) - 1, linhas)

    def _filhos(self, node):
        if isinstance(node, TerminalNode):
            return []
        resultado = []
        for i in range(node.getChildCount()):
            filho = node.getChild(i)
            if isinstance(filho, TerminalNode):
                if self._token_relevante(filho):
                    resultado.append(filho)
            else:
                resultado.append(filho)
        return resultado

    def _token_relevante(self, node):
        try:
            P = MiniLangParser
            ignorar = {
                P.LPAREN, P.RPAREN, P.COMMA, P.COLON,
                P.VAR, P.FUNCAO, P.SE, P.ENTAO, P.SENAO, P.FIM,
                P.ENQUANTO, P.FACA, P.PARA, P.DE, P.ATE,
                P.RETORNE, P.ESCREVA, P.LEIA,
            }
            return node.getSymbol().type not in ignorar
        except Exception:
            return True

    def _rotulo(self, node, parser):
        if isinstance(node, TerminalNode):
            return f"Token({node.getSymbol().text})"

        ctx = node
        try:
            P = MiniLangParser

            if isinstance(ctx, P.ProgramContext):
                return "Program"
            elif isinstance(ctx, P.FuncDeclContext):
                return f"FuncDecl: {ctx.IDENT().getText()} → {ctx.type_().getText()}"
            elif isinstance(ctx, P.VarDeclContext):
                return f"VarDecl: {ctx.IDENT().getText()}: {ctx.type_().getText()}"
            elif isinstance(ctx, P.ParamContext):
                return f"Param: {ctx.IDENT().getText()}: {ctx.type_().getText()}"
            elif isinstance(ctx, P.ParamsContext):
                return "Params"
            elif isinstance(ctx, P.BlockContext):
                return "Block"
            elif isinstance(ctx, P.AssignmentContext):
                return f"Assign: {ctx.IDENT().getText()} ="
            elif isinstance(ctx, P.IfStmtContext):
                return "IfStmt" + (" (com senao)" if ctx.SENAO() else "")
            elif isinstance(ctx, P.WhileStmtContext):
                return "WhileStmt"
            elif isinstance(ctx, P.ForStmtContext):
                return f"ForStmt: {ctx.IDENT().getText()}"
            elif isinstance(ctx, P.ReturnStmtContext):
                return "ReturnStmt"
            elif isinstance(ctx, P.EscrevaStmtContext):
                return "EscrevaStmt"
            elif isinstance(ctx, P.LeiaStmtContext):
                return f"LeiaStmt: {ctx.IDENT().getText()}"
            elif isinstance(ctx, P.FuncCallStmtContext):
                return f"FuncCallStmt: {ctx.IDENT().getText()}(...)"
            elif isinstance(ctx, P.UnaryExprContext):
                return "UnaryExpr: -"
            elif isinstance(ctx, P.MulExprContext):
                return f"BinOp: {ctx.op.text}"
            elif isinstance(ctx, P.AddExprContext):
                return f"BinOp: {ctx.op.text}"
            elif isinstance(ctx, P.RelExprContext):
                return f"BinOp: {ctx.op.text}"
            elif isinstance(ctx, P.EqExprContext):
                return f"BinOp: {ctx.op.text}"
            elif isinstance(ctx, P.AndExprContext):
                return "BinOp: e"
            elif isinstance(ctx, P.OrExprContext):
                return "BinOp: ou"
            elif isinstance(ctx, P.IntLitContext):
                return f"IntLit: {ctx.INT_LIT().getText()}"
            elif isinstance(ctx, P.FloatLitContext):
                return f"FloatLit: {ctx.FLOAT_LIT().getText()}"
            elif isinstance(ctx, P.StrLitContext):
                return f"StrLit: {ctx.STR_LIT().getText()}"
            elif isinstance(ctx, P.BoolTrueContext):
                return "BoolLit: verdadeiro"
            elif isinstance(ctx, P.BoolFalseContext):
                return "BoolLit: falso"
            elif isinstance(ctx, P.IdentExprContext):
                return f"Ident: {ctx.IDENT().getText()}"
            elif isinstance(ctx, P.FuncCallExprContext):
                return f"FuncCall: {ctx.IDENT().getText()}(...)"
            elif isinstance(ctx, P.ParenExprContext):
                return "ParenExpr"
            elif isinstance(ctx, P.ArgListContext):
                n = len(ctx.expression())
                return f"ArgList ({n} arg{'s' if n != 1 else ''})"
            elif isinstance(ctx, P.TypeContext):
                return f"Type: {ctx.getText()}"
        except Exception:
            pass

        return type(ctx).__name__.replace("Context", "")
        