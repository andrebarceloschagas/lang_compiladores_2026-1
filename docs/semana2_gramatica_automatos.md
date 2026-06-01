# MiniLang — Gramática Formal e Autômatos

Disciplina: Compiladores | UFT — Palmas/TO  
Prof. Dr. Antonio Marcos A. Ferreira

Alunos: [Antonio André](https://github.com/andrebarceloschagas), [Ranor Victor](https://github.com/ranorvictor), [Natália Nerys](https://github.com/natalia-nerys), [Luiz Fernando](https://github.com/lfocarvalho)

Entrega: Semana 2

---

## 1. Alfabeto Formal

O alfabeto da MiniLang (Σ) é o conjunto de todos os símbolos válidos no código-fonte:

```
Σ = { a..z, A..Z, 0..9, +, -, *, /, =, !, <, >, (, ), ,, :, ", #, _, espaço, tab, \n }
```

---

## 2. Hierarquia de Chomsky

A gramática da MiniLang é classificada em dois níveis distintos:

| Fase              | Tipo de Gramática            | Tipo Chomsky | Reconhecedor          |
|-------------------|------------------------------|--------------|-----------------------|
| Análise Léxica    | Gramática Regular            | Tipo 3       | AFD / AFN             |
| Análise Sintática | Gramática Livre de Contexto  | Tipo 2       | Autômato de Pilha (PDA) |

- Os **tokens** (identificadores, números, palavras-chave) são descritos por **expressões regulares** e reconhecidos por **autômatos finitos** — Tipo 3.
- A **estrutura dos programas** (funções, condicionais, laços) é descrita por uma **gramática livre de contexto** — Tipo 2.

---

## 3. Paradigma de Programação

A MiniLang adota o paradigma **imperativo e estruturado**:

- O programa é uma sequência de instruções que alteram o estado por meio de atribuições e fluxo de controle.
- Não há orientação a objetos, funções de primeira classe, nem inferência de tipos.
- Esta escolha cobre todas as fases do compilador com complexidade gerenciável: tabela de símbolos com escopos, pilha de chamadas, geração de código em três endereços.

---

## 4. Tokens e Expressões Regulares

| Categoria          | Expressão Regular              | Exemplos                      |
|--------------------|--------------------------------|-------------------------------|
| Palavras-chave     | lista fixa (ver seção 3)       | `se`, `funcao`, `enquanto`    |
| Identificadores    | `[a-zA-Z_][a-zA-Z0-9_]*`      | `x`, `soma`, `total_valor`    |
| Inteiro            | `[0-9]+`                       | `0`, `42`, `1000`             |
| Float              | `[0-9]+\.[0-9]+`               | `3.14`, `0.5`, `100.0`        |
| String             | `"[^"]*"`                      | `"ola"`, `"hello world"`      |
| Operadores Rel.    | `==\|!=\|<=\|>=\|<\|>`         | `==`, `!=`, `<=`              |
| Operadores Arit.   | `[+\-*/]`                      | `+`, `-`, `*`, `/`            |
| Atribuição         | `=`                            | `x = 10`                      |
| Delimitadores      | `[(),:] `                      | `(`, `)`, `,`, `:`            |
| Comentário         | `#[^\n]*`                      | `# comentario`                |
| Ignorados (WS)     | `[ \t\r\n]+`                   | espaços, tabs, quebras        |

---

## 5. Autômatos Finitos Determinísticos (AFDs)

### 5.1 AFD para Identificadores

**Expressão regular:** `[a-zA-Z_][a-zA-Z0-9_]*`

```
         letra ou _              letra, dígito ou _
  (q0) ─────────────→ ((q1)) ──────────────────────→ ((q1))
                          │
                          └─── outro símbolo → ACEITA token
```

**Tabela de transição:**

| Estado       | letra / `_` | dígito | outro         |
|--------------|-------------|--------|---------------|
| → q0 inicial | q1          | erro   | erro          |
| \* q1 aceita | q1          | q1     | aceita IDENT  |

> Após aceitar em q1, o lexer verifica na tabela de palavras-chave: se o lexema for `se`, `funcao`, etc., o token é KEYWORD; caso contrário, é IDENT.

---

### 5.2 AFD para Números Inteiros

**Expressão regular:** `[0-9]+`

```
        dígito              dígito
  (q0) ──────→ ((q1)) ──────────────→ ((q1))
                   │
                   └─── outro símbolo → ACEITA token
```

**Tabela de transição:**

| Estado       | dígito `[0-9]` | outro          |
|--------------|----------------|----------------|
| → q0 inicial | q1             | erro           |
| \* q1 aceita | q1             | aceita INT_LIT |

---

### 5.3 AFD para Números Float

**Expressão regular:** `[0-9]+\.[0-9]+`

```
        dígito            ponto (.)          dígito
  (q0) ──────→ (q1) ─────────────→ (q2) ──────────→ ((q3))
                │                                        │
                └── outro → aceita INT                   └── dígito → q3
                                                             outro  → ACEITA FLOAT
```

**Tabela de transição:**

| Estado              | dígito | ponto `.` | outro           |
|---------------------|--------|-----------|-----------------|
| → q0 inicial        | q1     | erro      | erro            |
| q1 (parte inteira)  | q1     | q2        | aceita INT_LIT  |
| q2 (leu ponto)      | q3     | erro      | erro            |
| \* q3 aceita        | q3     | erro      | aceita FLOAT_LIT|

---

## 6. Gramática Formal

### 6.1 EBNF — Visão Completa

```ebnf
program      ::= { declaration | statement }

declaration  ::= var_decl | func_decl

var_decl     ::= "var" IDENT ":" type

func_decl    ::= "funcao" IDENT "(" params ")" ":" type block "fim"

params       ::= [ IDENT ":" type { "," IDENT ":" type } ]

type         ::= "int" | "float" | "bool" | "string"

block        ::= { statement }

statement    ::= assignment
               | if_stmt
               | while_stmt
               | for_stmt
               | return_stmt
               | io_stmt
               | func_call

assignment   ::= IDENT "=" expression

if_stmt      ::= "se" "(" expression ")" "entao" block [ "senao" block ] "fim"

while_stmt   ::= "enquanto" "(" expression ")" "faca" block "fim"

for_stmt     ::= "para" IDENT "de" expression "ate" expression "faca" block "fim"

return_stmt  ::= "retorne" expression

io_stmt      ::= "escreva" "(" expression ")"
               | "leia" "(" IDENT ")"

func_call    ::= IDENT "(" [ expression { "," expression } ] ")"

expression   ::= comparison { ( "e" | "ou" ) comparison }

comparison   ::= arith { ( "<" | ">" | "<=" | ">=" | "==" | "!=" ) arith }

arith        ::= term { ( "+" | "-" ) term }

term         ::= unary { ( "*" | "/" ) unary }

unary        ::= "-" unary | primary

primary      ::= NUMBER_INT
               | NUMBER_FLOAT
               | STRING
               | "verdadeiro"
               | "falso"
               | IDENT
               | func_call
               | "(" expression ")"
```

---

### 6.2 BNF — Regras Principais

```bnf
<program>    ::= <decl-list>
<decl-list>  ::= <decl> <decl-list> | <decl>
<decl>       ::= <var-decl> | <func-decl>

<var-decl>   ::= "var" id ":" <type>
<func-decl>  ::= "funcao" id "(" <params> ")" ":" <type> <block> "fim"
<params>     ::= id ":" <type> | id ":" <type> "," <params> | ε

<type>       ::= "int" | "float" | "bool" | "string"

<block>      ::= <stmt-list>
<stmt-list>  ::= <stmt> <stmt-list> | <stmt>

<stmt>       ::= <assignment>
               | <if-stmt>
               | <while-stmt>
               | <for-stmt>
               | <return-stmt>
               | <io-stmt>

<assignment> ::= id "=" <expr>

<if-stmt>    ::= "se" "(" <expr> ")" "entao" <block> "fim"
               | "se" "(" <expr> ")" "entao" <block> "senao" <block> "fim"

<while-stmt> ::= "enquanto" "(" <expr> ")" "faca" <block> "fim"

<for-stmt>   ::= "para" id "de" <expr> "ate" <expr> "faca" <block> "fim"

<return-stmt>::= "retorne" <expr>

<io-stmt>    ::= "escreva" "(" <expr> ")"
               | "leia" "(" id ")"

<expr>       ::= <expr> "+" <term>
               | <expr> "-" <term>
               | <term>

<term>       ::= <term> "*" <factor>
               | <term> "/" <factor>
               | <factor>

<factor>     ::= id | num | "(" <expr> ")"
```

> **Obs.:** A BNF apresenta recursão à esquerda em `<expr>` e `<term>` para fidelidade à notação formal. Na implementação com ANTLR 4, a recursão à esquerda é resolvida automaticamente pela ferramenta.

---

## 7. Exemplo Completo Anotado

Código-fonte:

```pascal
var soma: int
soma = 3 + 4
escreva(soma)
```

**a) Alfabeto presente:**
```
Σ_usado = { v,a,r,s,o,m, ,i,n,t, =,3,+,4,e,c,w,( ,) }
```

**b) Tokens gerados:**
```
<VAR, "var">        linha 1
<IDENT, "soma">     linha 1
<COLON, ":">        linha 1
<INT_TYPE, "int">   linha 1
<IDENT, "soma">     linha 2
<ASSIGN, "=">       linha 2
<INT_LIT, "3">      linha 2
<PLUS, "+">         linha 2
<INT_LIT, "4">      linha 2
<ESCREVA, "escreva"> linha 3
<LPAREN, "(">       linha 3
<IDENT, "soma">     linha 3
<RPAREN, ")">       linha 3
```

**c) AFD aplicado:** identificador → `soma` reconhecido por q0 → q1 (aceita como IDENT, verifica na tabela: não é keyword).

**d) Regra gramatical aplicada:**
```bnf
<stmt>       → <assignment>
<assignment> → id "=" <expr>
<expr>       → <expr> "+" <term>   (3 + 4)
```
