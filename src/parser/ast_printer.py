from antlr4 import ParserRuleContext, TerminalNode

try:
    from MiniLangParser import MiniLangParser
except ImportError:
    pass   # Tolerado — o import real acontece em tempo de execução


class ASTPrinter:
    """
    Percorre a ParseTree do ANTLR e gera uma string com a AST formatada.
    Uso:
        printer = ASTPrinter()
        texto   = printer.imprimir(arvore)
        print(texto)
    """

    # Prefixos de indentação (estilo árvore)
    _ULTIMO  = "└── "
    _NORMAL  = "├── "
    _CONT    = "│   "
    _ESPACO  = "    "

    def imprimir(self, arvore) -> str:
        linhas = []
        self._visitar(arvore, "", True, linhas, raiz=True)
        return "\n".join(linhas)

    # ── Dispatcher principal ──────────────────────────────────

    def _visitar(self, no, prefixo, ultimo, linhas, raiz=False):
        P = MiniLangParser

        if raiz:
            linhas.append("Program")
            filhos = list(no.getChildren())
            # Remove EOF
            filhos = [f for f in filhos if not (isinstance(f, TerminalNode)
                       and f.symbol.type == -1)]
            for i, filho in enumerate(filhos):
                eh_ultimo = (i == len(filhos) - 1)
                self._visitar(filho, "", eh_ultimo, linhas)
            return

        conector = self._ULTIMO if ultimo else self._NORMAL
        prox     = prefixo + (self._ESPACO if ultimo else self._CONT)

        # ── program ──────────────────────────────────────────
        if isinstance(no, P.ProgramContext):
            linhas.append(prefixo + conector + "Program")
            self._visitar_filhos(no, prox, linhas)

        # ── varDecl ──────────────────────────────────────────
        elif isinstance(no, P.VarDeclContext):
            nome = no.IDENT().getText()
            tipo = no.type_().getText()
            linhas.append(prefixo + conector + f"VarDecl: {nome} : {tipo}")

        # ── funcDecl ─────────────────────────────────────────
        elif isinstance(no, P.FuncDeclContext):
            nome = no.IDENT().getText()
            tipo = no.type_().getText()
            linhas.append(prefixo + conector + f"FuncDecl: {nome} : {tipo}")
            # params
            self._visitar(no.params(), prox, False, linhas)
            # block
            self._visitar(no.block(), prox, True, linhas)

        # ── params ────────────────────────────────────────────
        elif isinstance(no, P.ParamsContext):
            ps = no.param()
            if ps:
                linhas.append(prefixo + conector + "Params")
                for i, p in enumerate(ps):
                    self._visitar(p, prox, i == len(ps)-1, linhas)
            else:
                linhas.append(prefixo + conector + "Params: (vazio)")

        # ── param ─────────────────────────────────────────────
        elif isinstance(no, P.ParamContext):
            nome = no.IDENT().getText()
            tipo = no.type_().getText()
            linhas.append(prefixo + conector + f"Param: {nome} : {tipo}")

        # ── block ─────────────────────────────────────────────
        elif isinstance(no, P.BlockContext):
            stmts = no.statement()
            if stmts:
                linhas.append(prefixo + conector + "Block")
                for i, s in enumerate(stmts):
                    self._visitar(s, prox, i == len(stmts)-1, linhas)
            else:
                linhas.append(prefixo + conector + "Block: (vazio)")

        # ── stmtAssign ───────────────────────────────────────
        elif isinstance(no, P.StmtAssignContext):
            ident = no.IDENT().getText()
            linhas.append(prefixo + conector + f"Assign: {ident}")
            self._visitar(no.expression(), prox, True, linhas)

        # ── stmtIf ───────────────────────────────────────────
        elif isinstance(no, P.StmtIfContext):
            linhas.append(prefixo + conector + "IfStmt")
            linhas.append(prox + self._NORMAL + "Cond:")
            self._visitar(no.expression(), prox + self._CONT, True, linhas)
            linhas.append(prox + self._ULTIMO + "Then:")
            self._visitar(no.block(), prox + self._ESPACO, True, linhas)

        # ── stmtIfElse ───────────────────────────────────────
        elif isinstance(no, P.StmtIfElseContext):
            linhas.append(prefixo + conector + "IfElseStmt")
            linhas.append(prox + self._NORMAL + "Cond:")
            self._visitar(no.expression(), prox + self._CONT, True, linhas)
            blocos = no.block()
            linhas.append(prox + self._NORMAL + "Then:")
            self._visitar(blocos[0], prox + self._CONT, False, linhas)
            linhas.append(prox + self._ULTIMO + "Else:")
            self._visitar(blocos[1], prox + self._ESPACO, True, linhas)

        # ── stmtWhile ────────────────────────────────────────
        elif isinstance(no, P.StmtWhileContext):
            linhas.append(prefixo + conector + "WhileStmt")
            linhas.append(prox + self._NORMAL + "Cond:")
            self._visitar(no.expression(), prox + self._CONT, True, linhas)
            linhas.append(prox + self._ULTIMO + "Body:")
            self._visitar(no.block(), prox + self._ESPACO, True, linhas)

        # ── stmtFor ──────────────────────────────────────────
        elif isinstance(no, P.StmtForContext):
            var = no.IDENT().getText()
            linhas.append(prefixo + conector + f"ForStmt: {var}")
            exprs = no.expression()
            linhas.append(prox + self._NORMAL + "De:")
            self._visitar(exprs[0], prox + self._CONT, True, linhas)
            linhas.append(prox + self._NORMAL + "Ate:")
            self._visitar(exprs[1], prox + self._CONT, True, linhas)
            linhas.append(prox + self._ULTIMO + "Body:")
            self._visitar(no.block(), prox + self._ESPACO, True, linhas)

        # ── stmtReturn ───────────────────────────────────────
        elif isinstance(no, P.StmtReturnContext):
            linhas.append(prefixo + conector + "ReturnStmt")
            self._visitar(no.expression(), prox, True, linhas)

        # ── stmtEscreva ──────────────────────────────────────
        elif isinstance(no, P.StmtEscrevaContext):
            linhas.append(prefixo + conector + "Escreva")
            self._visitar(no.expression(), prox, True, linhas)

        # ── stmtLeia ─────────────────────────────────────────
        elif isinstance(no, P.StmtLeiaContext):
            ident = no.IDENT().getText()
            linhas.append(prefixo + conector + f"Leia: {ident}")

        # ── stmtFuncCall ─────────────────────────────────────
        elif isinstance(no, P.StmtFuncCallContext):
            self._visitar(no.funcCall(), prox, ultimo, linhas)

        # ── funcCall ─────────────────────────────────────────
        elif isinstance(no, P.FuncCallContext):
            nome = no.IDENT().getText()
            linhas.append(prefixo + conector + f"FuncCall: {nome}")
            args = no.argList().expression() if no.argList() else []
            for i, a in enumerate(args):
                self._visitar(a, prox, i == len(args)-1, linhas)

        # ── expressões binárias ───────────────────────────────
        elif isinstance(no, (P.ExprLogicoContext,
                              P.ExprIgualdadeContext,
                              P.ExprRelacionalContext,
                              P.ExprAditivoContext,
                              P.ExprMultiplicativoContext)):
            op = no.getChild(1).getText()
            linhas.append(prefixo + conector + f"BinOp({op})")
            self._visitar(no.getChild(0), prox, False, linhas)
            self._visitar(no.getChild(2), prox, True,  linhas)

        # ── negação unária ────────────────────────────────────
        elif isinstance(no, P.ExprNegacaoContext):
            linhas.append(prefixo + conector + "Neg(-)")
            self._visitar(no.expression(), prox, True, linhas)

        # ── exprPrimary / primParens ──────────────────────────
        elif isinstance(no, P.ExprPrimaryContext):
            self._visitar(no.primary(), prox, ultimo, linhas)

        elif isinstance(no, P.PrimParensContext):
            linhas.append(prefixo + conector + "Parens")
            self._visitar(no.expression(), prox, True, linhas)

        # ── literais e identificadores ────────────────────────
        elif isinstance(no, P.PrimIntContext):
            linhas.append(prefixo + conector + f"Int({no.INT_LIT().getText()})")

        elif isinstance(no, P.PrimFloatContext):
            linhas.append(prefixo + conector + f"Float({no.FLOAT_LIT().getText()})")

        elif isinstance(no, P.PrimStringContext):
            linhas.append(prefixo + conector + f"Str({no.STR_LIT().getText()})")

        elif isinstance(no, P.PrimVerdadeiroContext):
            linhas.append(prefixo + conector + "Bool(verdadeiro)")

        elif isinstance(no, P.PrimFalsoContext):
            linhas.append(prefixo + conector + "Bool(falso)")

        elif isinstance(no, P.PrimIdentContext):
            linhas.append(prefixo + conector + f"Ident({no.IDENT().getText()})")

        elif isinstance(no, P.PrimFuncCallContext):
            self._visitar(no.funcCall(), prox, ultimo, linhas)

        # ── stmtVarDecl (wrapper) ─────────────────────────────
        elif isinstance(no, P.StmtVarDeclContext):
            self._visitar(no.varDecl(), prox, ultimo, linhas)

        # ── nó genérico (fallback) ────────────────────────────
        elif isinstance(no, ParserRuleContext):
            label = type(no).__name__.replace("Context", "")
            linhas.append(prefixo + conector + label)
            self._visitar_filhos(no, prox, linhas)

        # ── terminal (folha) — ignorado na AST ───────────────
        # (tokens já estão representados nos nós acima)

    def _visitar_filhos(self, no, prefixo, linhas):
        filhos = [f for f in no.getChildren()
                  if isinstance(f, ParserRuleContext)]
        for i, filho in enumerate(filhos):
            self._visitar(filho, prefixo, i == len(filhos)-1, linhas)
