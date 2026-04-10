# MiniLang — Análise Sintática com ANTLR 4

Disciplina: Compiladores | UFT — Palmas/TO  
Prof. Dr. Antonio Marcos A. Ferreira

Alunos: [Antonio André](https://github.com/andrebarceloschagas), [Ranor Victor](https://github.com/ranorvictor), [Natália Nerys](https://github.com/natalia-nerys), [Luiz Fernando](https://github.com/lfocarvalho)

Entrega: Semana 4

---

## 1. Introdução

Na Semana 4, a gramática léxica (`MiniLangLexer.g4`) foi expandida para uma **gramática completa** (`MiniLang.g4`), incorporando as regras sintáticas do parser. O ANTLR 4 gera automaticamente o parser LL(*) a partir dessa gramática, construindo a **Árvore Sintática Abstrata (AST)** do programa-fonte.

| Conceito em aula | Implementação no projeto |
|---|---|
| Gramática Livre de Contexto (Tipo 2) | Regras do parser em `MiniLang.g4` |
| Análise descendente (top-down) | ANTLR gera parser LL(*) recursivo |
| Recursão à esquerda | Resolvida automaticamente pelo ANTLR 4 |
| Conjuntos First() e Follow() | Calculados internamente pelo ANTLR |
| Árvore de derivação | ParseTree convertida em AST via `ASTPrinter` |
| Ambiguidade | Resolvida pela ordem das alternativas na gramática |

---

## 2. Técnica de Parsing — LL(*) via ANTLR 4

O ANTLR 4 gera um parser **LL(*)**, uma generalização do LL(1) que usa lookahead adaptativo. Isso resolve casos onde LL(1) falharia por ambiguidade de lookahead fixo.

### 2.1 Como o ANTLR resolve recursão à esquerda

A BNF clássica de `<expr>` tem recursão à esquerda:
```bnf
<expr> ::= <expr> "+" <term> | <term>
```
Isso causa loop infinito em parsers descendentes. O ANTLR 4 reescreve automaticamente para iteração, sem alterar a semântica.

### 2.2 Precedência por ordem das alternativas

Na regra `expression`, **alternativas mais abaixo têm maior precedência**:

```
expression
  ├── e / ou          (menor precedência)
  ├── == / !=
  ├── < > <= >=
  ├── + -
  ├── * /
  ├── - (unário)
  └── primary         (maior precedência)
```

---

## 3. Labels nas alternativas (`# nome`)

As alternativas de `statement` e `expression` são rotuladas:

```antlr
statement
    : IDENT ASSIGN expression    # stmtAssign
    | SE ... FIM                 # stmtIf
    | SE ... SENAO ... FIM       # stmtIfElse
    ;
```

Os labels fazem o ANTLR gerar subclasses específicas (`StmtAssignContext`, `StmtIfContext`, etc.), permitindo que o `ASTPrinter` use `isinstance` para identificar cada tipo de nó com precisão.

---

## 4. Como Executar

```bash
# 1. Gerar lexer + parser (uma única vez)
cd src/gramatica
java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -o generated MiniLang.g4

# 2. Executar sobre um exemplo válido
cd ../../
python src/parser/main_parser.py tests/exemplos/exemplo1_fatorial.minilang

# 3. Salvar a AST
python src/parser/main_parser.py tests/exemplos/exemplo1_fatorial.minilang \
       --salvar tests/saidas_esperadas/exemplo1_ast_obtida.txt

# 4. Comparar com o esperado
diff tests/saidas_esperadas/exemplo1_ast.txt \
     tests/saidas_esperadas/exemplo1_ast_obtida.txt

# 5. Testar com programa com erro
python src/parser/main_parser.py tests/exemplos/exemplo4_erro_sintatico.minilang
```

---

## 5. Relatório de Testes

### Teste 1 — `exemplo1_fatorial.minilang`

| Item | Resultado |
|---|---|
| Erros sintáticos | 0 |
| Nós na AST | 28 |
| FuncDecl reconhecida | OK: `fatorial : int` |
| IfStmt com ReturnStmt | OK |
| BinOp(`*`) com FuncCall recursiva | OK |
| Status | PASSOU |

### Teste 2 — `exemplo2_laco.minilang`

| Item | Resultado |
|---|---|
| Erros sintáticos | 0 |
| Nós na AST | 19 |
| ForStmt com De/Ate/Body | OK |
| VarDecl dentro de block | OK |
| Status | PASSOU |

### Teste 3 — `exemplo3_condicional.minilang`

| Item | Resultado |
|---|---|
| Erros sintáticos | 0 |
| Nós na AST | 20 |
| IfElseStmt com Then e Else | OK |
| Bool(verdadeiro) / Bool(falso) | OK |
| Status | PASSOU |

### Teste 4 — `exemplo4_erro_sintatico.minilang`

| Item | Resultado |
|---|---|
| Erros esperados | 4 |
| Erros detectados | 4 |
| Mensagem com linha e coluna | OK |
| Parser se recupera após erro | OK |
| Status | PASSOU (erros corretamente detectados) |

Saída esperada:
```
[ERRO SINTÁTICO] linha 6:0  — missing 'entao' at '\n'
[ERRO SINTÁTICO] linha 14:0 — missing 'fim' at 'var'
[ERRO SINTÁTICO] linha 19:0 — mismatched input '\n' expecting expression
[ERRO SINTÁTICO] linha 25:20 — extraneous input ')' expecting ')'
```

---

## 6. Dificuldades Encontradas e Soluções

| Dificuldade | Causa | Solução |
|---|---|---|
| `StmtIf` e `StmtIfElse` indistinguíveis | Sem labels nas alternativas | Adicionar `# stmtIf` e `# stmtIfElse` |
| Precedência de `*` e `+` invertida | Ordem errada das alternativas | Reordenar: `* /` abaixo de `+ -` |
| `type` conflitava com built-in Python | Nome reservado | Chamar `type_()` no código Python |
| AST com nós duplicados | `_visitar_filhos` incluía terminais | Filtrar apenas `ParserRuleContext` |
| `isinstance` não distinguia expressões | Sem labels em `expression` | Adicionar `# exprAditivo`, `# exprLogico`, etc. |
