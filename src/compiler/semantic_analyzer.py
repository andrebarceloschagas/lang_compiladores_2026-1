"""Análise semântica da MiniLang.

Este módulo valida tipos, escopos, declarações e chamadas de função antes da geração de código.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAMMAR_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'gramatica', 'generated'))
sys.path.insert(0, GRAMMAR_DIR)

from antlr4 import ParserRuleContext
from MiniLangParser import MiniLangParser
from MiniLangVisitor import MiniLangVisitor


class FunctionSymbol:
    def __init__(self, name, param_names, param_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = param_types
        self.return_type = return_type


class SemanticAnalyzer(MiniLangVisitor):
    def __init__(self):
        self.functions = {}
        self.global_scope = {}
        self.scopes = []
        self.errors = []
        self.current_function = None
        self.current_return_type = None

    def error(self, ctx, message):
        line = getattr(getattr(ctx, 'start', None), 'line', '?')
        self.errors.append(f"linha {line}: {message}")

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if self.scopes:
            self.scopes.pop()

    def current_scope(self):
        return self.scopes[-1] if self.scopes else self.global_scope

    def lookup_symbol(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return self.global_scope.get(name)

    def define_symbol(self, name, typ, ctx):
        scope = self.current_scope()
        if name in scope:
            self.error(ctx, f"Identificador '{name}' já declarado no mesmo escopo")
            return
        scope[name] = typ

    def lookup_function(self, name):
        return self.functions.get(name)

    def can_assign(self, target_type, expr_type):
        if target_type == expr_type:
            return True
        if target_type == 'float' and expr_type == 'int':
            return True
        return False

    def visitProgram(self, ctx):
        P = MiniLangParser

        # Definir declarações globais e assinaturas de funções primeiro
        for child in ctx.getChildren():
            if isinstance(child, ParserRuleContext):
                if isinstance(child, P.DeclarationContext):
                    if child.varDecl():
                        self.visit(child.varDecl())
                    elif child.funcDecl():
                        self._declare_function(child.funcDecl())

        # Em seguida, visitar o corpo para validar declarações e expressões
        for child in ctx.getChildren():
            if isinstance(child, ParserRuleContext):
                if isinstance(child, P.DeclarationContext) and child.funcDecl():
                    self.visit(child.funcDecl())
                elif isinstance(child, P.StatementContext):
                    self.visit(child)
        return None

    def _declare_function(self, ctx):
        name = ctx.IDENT().getText()
        if name in self.functions:
            self.error(ctx, f"Função '{name}' já declarada")
            return
        params = []
        types = []
        if ctx.params() and ctx.params().param():
            for param in ctx.params().param():
                params.append(param.IDENT().getText())
                types.append(param.type_().getText())
        self.functions[name] = FunctionSymbol(name, params, types, ctx.type_().getText())

    def visitDeclaration(self, ctx):
        if ctx.varDecl():
            return self.visit(ctx.varDecl())
        if ctx.funcDecl():
            return self.visit(ctx.funcDecl())
        return None

    def visitVarDecl(self, ctx):
        name = ctx.IDENT().getText()
        tipo = ctx.type_().getText()
        self.define_symbol(name, tipo, ctx)
        return None

    def visitFuncDecl(self, ctx):
        name = ctx.IDENT().getText()
        func = self.lookup_function(name)
        if func is None:
            self.error(ctx, f"Função '{name}' não declarada")
            return None

        self.current_function = name
        self.current_return_type = func.return_type

        self.push_scope()
        for param_name, param_type in zip(func.param_names, func.param_types):
            if param_name in self.current_scope():
                self.error(ctx, f"Parâmetro '{param_name}' redeclarado")
            self.current_scope()[param_name] = param_type

        self.visit(ctx.block())
        self.pop_scope()

        self.current_function = None
        self.current_return_type = None
        return None

    def visitStmtVarDecl(self, ctx):
        return self.visit(ctx.varDecl())

    def visitStmtAssign(self, ctx):
        name = ctx.IDENT().getText()
        target_type = self.lookup_symbol(name)
        if target_type is None:
            self.error(ctx, f"Variável '{name}' não declarada")
        expr_type = self.visit(ctx.expression())
        if target_type and expr_type:
            if not self.can_assign(target_type, expr_type):
                self.error(ctx, f"Atribuição inválida: não é possível atribuir '{expr_type}' a '{target_type}'")
        return None

    def visitStmtIf(self, ctx):
        cond_type = self.visit(ctx.expression())
        if cond_type and cond_type != 'bool':
            self.error(ctx.expression(), "Condição do 'se' deve ser do tipo bool")
        self.push_scope()
        self.visit(ctx.block())
        self.pop_scope()
        return None

    def visitStmtIfElse(self, ctx):
        cond_type = self.visit(ctx.expression())
        if cond_type and cond_type != 'bool':
            self.error(ctx.expression(), "Condição do 'se' deve ser do tipo bool")
        self.push_scope()
        self.visit(ctx.block(0))
        self.pop_scope()
        self.push_scope()
        self.visit(ctx.block(1))
        self.pop_scope()
        return None

    def visitStmtWhile(self, ctx):
        cond_type = self.visit(ctx.expression())
        if cond_type and cond_type != 'bool':
            self.error(ctx.expression(), "Condição do 'enquanto' deve ser do tipo bool")
        self.push_scope()
        self.visit(ctx.block())
        self.pop_scope()
        return None

    def visitStmtFor(self, ctx):
        name = ctx.IDENT().getText()
        var_type = self.lookup_symbol(name)
        if var_type is None:
            self.error(ctx, f"Variável de controle '{name}' não declarada")
        elif var_type != 'int':
            self.error(ctx, f"Variável de controle do 'para' deve ser do tipo int")

        de_type = self.visit(ctx.expression(0))
        ate_type = self.visit(ctx.expression(1))
        if de_type and de_type != 'int':
            self.error(ctx.expression(0), "Limite 'de' do 'para' deve ser int")
        if ate_type and ate_type != 'int':
            self.error(ctx.expression(1), "Limite 'ate' do 'para' deve ser int")

        self.push_scope()
        self.visit(ctx.block())
        self.pop_scope()
        return None

    def visitStmtReturn(self, ctx):
        if self.current_return_type is None:
            self.error(ctx, "'retorne' fora de uma função")
            return None
        expr_type = self.visit(ctx.expression())
        if expr_type and not self.can_assign(self.current_return_type, expr_type):
            self.error(ctx, f"Tipo de retorno inválido: esperado '{self.current_return_type}', encontrado '{expr_type}'")
        return None

    def visitStmtEscreva(self, ctx):
        self.visit(ctx.expression())
        return None

    def visitStmtLeia(self, ctx):
        name = ctx.IDENT().getText()
        if self.lookup_symbol(name) is None:
            self.error(ctx, f"Variável '{name}' não declarada")
        return None

    def visitStmtFuncCall(self, ctx):
        self.visit(ctx.funcCall())
        return None

    def visitFuncCall(self, ctx):
        name = ctx.IDENT().getText()
        func = self.lookup_function(name)
        if func is None:
            self.error(ctx, f"Função '{name}' não declarada")
            return None

        args = list(ctx.argList().expression()) if ctx.argList() else []
        if len(args) != len(func.param_types):
            self.error(ctx, f"Função '{name}' espera {len(func.param_types)} argumento(s), recebeu {len(args)}")
            return func.return_type

        for expr, expected_type, param_name in zip(args, func.param_types, func.param_names):
            expr_type = self.visit(expr)
            if expr_type and not self.can_assign(expected_type, expr_type):
                self.error(expr, f"Argumento '{param_name}' da função '{name}' espera '{expected_type}', recebeu '{expr_type}'")
        return func.return_type

    def visitExprLogico(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if left != 'bool' or right != 'bool':
            self.error(ctx, "Operadores lógicos 'e'/'ou' exigem operandos do tipo bool")
        return 'bool'

    def visitExprIgualdade(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if left is None or right is None:
            return None
        if left != right:
            self.error(ctx, "Operadores de igualdade exigem operandos do mesmo tipo")
        return 'bool'

    def visitExprRelacional(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if left is None or right is None:
            return None
        if left not in ('int', 'float') or right not in ('int', 'float'):
            self.error(ctx, "Operadores relacionais exigem operandos numéricos")
            return None
        return 'bool'

    def visitExprAditivo(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        op = ctx.getChild(1).getText()
        if left is None or right is None:
            return None
        if op == '+':
            if left == right and left in ('int', 'float', 'string'):
                return left
            if left == 'int' and right == 'float':
                return 'float'
            if left == 'float' and right == 'int':
                return 'float'
            self.error(ctx, "Operador '+' exige operandos numéricos compatíveis ou duas strings")
            return None
        if op == '-':
            if left in ('int', 'float') and right in ('int', 'float'):
                return 'float' if 'float' in (left, right) else 'int'
            self.error(ctx, "Operador '-' exige operandos numéricos")
            return None
        return None

    def visitExprMultiplicativo(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if left in ('int', 'float') and right in ('int', 'float'):
            return 'float' if 'float' in (left, right) else 'int'
        self.error(ctx, "Operadores '*' e '/' exigem operandos numéricos")
        return None

    def visitExprNegacao(self, ctx):
        expr_type = self.visit(ctx.expression())
        if expr_type not in ('int', 'float'):
            self.error(ctx, "Negação unária exige operando numérico")
            return None
        return expr_type

    def visitPrimInt(self, ctx):
        return 'int'

    def visitPrimFloat(self, ctx):
        return 'float'

    def visitPrimString(self, ctx):
        return 'string'

    def visitPrimVerdadeiro(self, ctx):
        return 'bool'

    def visitPrimFalso(self, ctx):
        return 'bool'

    def visitPrimIdent(self, ctx):
        name = ctx.IDENT().getText()
        typ = self.lookup_symbol(name)
        if typ is None:
            self.error(ctx, f"Identificador '{name}' não declarado")
        return typ

    def visitPrimParens(self, ctx):
        return self.visit(ctx.expression())

    def visitBlock(self, ctx):
        self.push_scope()
        for stmt in ctx.statement():
            self.visit(stmt)
        self.pop_scope()
        return None
