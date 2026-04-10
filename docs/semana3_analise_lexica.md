# MiniLang — Análise Léxica com ANTLR 4

Disciplina: Compiladores | UFT — Palmas/TO  
Prof. Dr. Antonio Marcos A. Ferreira

Alunos: [Antonio André](https://github.com/andrebarceloschagas), [Ranor Victor](https://github.com/ranorvictor), [Natália Nerys](https://github.com/natalia-nerys), [Luiz Fernando](https://github.com/lfocarvalho)

Entrega: Semana 3

---

## 1. Justificativa da Ferramenta — ANTLR 4

Para a implementação do analisador léxico da MiniLang, o grupo optou pelo **ANTLR 4** (ANother Tool for Language Recognition), com geração de código em **Python 3**.

### Por que ANTLR?

| Critério | Justificativa |
|---|---|
| **Unificação** | Gera léxico e parser a partir de um único arquivo `.g4`, evitando duplicação entre as fases |
| **Automatização** | Converte internamente ER → AFN → AFD, implementando exatamente o pipeline teórico das aulas |
| **Preparação futura** | A mesma gramática `.g4` será expandida com regras sintáticas na Semana 4, sem retrabalho |
| **Resolução de recursão** | Resolve recursão à esquerda automaticamente, conforme discutido em aula |
| **Suporte a Python** | Target Python 3 compatível com o ecossistema do grupo |
| **Indústria** | Ferramenta amplamente adotada: usado no compilador do Swift, Groovy, Kotlin e outros |

> **Relação com a teoria:** internamente o ANTLR aplica a Construção de Thompson (ER → AFN) e depois o Algoritmo de Subconjuntos (AFN → AFD), exatamente como descrito nos slides da Aula 02 e 03.

---

## 2. Instalação e Configuração

### 2.1 Pré-requisitos

- Python 3.8 ou superior
- Java 11 ou superior (para executar o gerador ANTLR)
- pip

### 2.2 Instalar o runtime Python

```bash
pip install antlr4-python3-runtime==4.13.1
```

### 2.3 Baixar o gerador ANTLR

```bash
# Baixar o JAR
curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar

# Criar alias (Linux/macOS) — adicionar ao ~/.bashrc para persistir
alias antlr4='java -jar antlr-4.13.1-complete.jar'
```

### 2.4 Gerar o lexer a partir da gramática

```bash
# Dentro da pasta src/gramatica/
java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -o generated MiniLangLexer.g4
```

Isso gera dentro de `generated/`:

```
generated/
├── MiniLangLexerLexer.py       ← classe principal do lexer
├── MiniLangLexerLexer.interp   ← dados internos do AFD
└── MiniLangLexerLexer.tokens   ← mapeamento tipo → número
```

---

## 3. Estrutura da Gramática — `MiniLangLexer.g4`

O arquivo `.g4` é um `lexer grammar`, dividido em seções com ordem deliberada:

### 3.1 Ordem das Regras e Prioridade

O ANTLR resolve conflitos entre regras pela **ordem de aparição**: a regra que vem primeiro tem maior prioridade. Isso determina duas decisões importantes na gramática:

**Palavras-chave antes de IDENT:**
```antlr
FUNCAO : 'funcao' ;   // regra 1 — maior prioridade
IDENT  : [a-zA-Z_][a-zA-Z0-9_]* ;  // regra N — menor prioridade
```
Sem isso, `funcao` seria tokenizado como `IDENT` ao invés de `FUNCAO`.

**FLOAT_LIT antes de INT_LIT:**
```antlr
FLOAT_LIT : [0-9]+ '.' [0-9]+ ;  // primeiro
INT_LIT   : [0-9]+             ;  // depois
```
Sem isso, `3.14` seria tokenizado como `INT(3)` + erro + `INT(14)`.

**Operadores de dois caracteres antes dos de um:**
```antlr
EQ  : '==' ;   // primeiro
LEQ : '<=' ;   // primeiro
ASSIGN : '=' ; // depois
LT     : '<' ; // depois
```

### 3.2 Tokens Ignorados

Comentários e espaços em branco usam a diretiva `-> skip`, que os descarta sem gerar token:

```antlr
COMMENT : '#' ~[\n]* -> skip ;
WS      : [ \t\r\n]+ -> skip ;
```

### 3.3 Tratamento de Erro Léxico

A regra `ERRO` captura qualquer caractere não reconhecido, evitando que o lexer trave:

```antlr
ERRO : . ;
```
O `main_lexer.py` detecta tokens do tipo `ERRO` e emite mensagem de erro com o caractere e a linha.

---

## 4. Descrição Completa dos Tokens

| Token | Regra ANTLR | Exemplo |
|---|---|---|
| `VAR` | `'var'` | `var` |
| `FUNCAO` | `'funcao'` | `funcao` |
| `SE` | `'se'` | `se` |
| `ENTAO` | `'entao'` | `entao` |
| `SENAO` | `'senao'` | `senao` |
| `FIM` | `'fim'` | `fim` |
| `ENQUANTO` | `'enquanto'` | `enquanto` |
| `FACA` | `'faca'` | `faca` |
| `PARA` | `'para'` | `para` |
| `DE` | `'de'` | `de` |
| `ATE` | `'ate'` | `ate` |
| `RETORNE` | `'retorne'` | `retorne` |
| `ESCREVA` | `'escreva'` | `escreva` |
| `LEIA` | `'leia'` | `leia` |
| `VERDADEIRO` | `'verdadeiro'` | `verdadeiro` |
| `FALSO` | `'falso'` | `falso` |
| `E_LOG` | `'e'` | `e` |
| `OU_LOG` | `'ou'` | `ou` |
| `INT_TYPE` | `'int'` | `int` |
| `FLOAT_TYPE` | `'float'` | `float` |
| `BOOL_TYPE` | `'bool'` | `bool` |
| `STR_TYPE` | `'string'` | `string` |
| `EQ` | `'=='` | `==` |
| `NEQ` | `'!='` | `!=` |
| `LEQ` | `'<='` | `<=` |
| `GEQ` | `'>='` | `>=` |
| `LT` | `'<'` | `<` |
| `GT` | `'>'` | `>` |
| `PLUS` | `'+'` | `+` |
| `MINUS` | `'-'` | `-` |
| `STAR` | `'*'` | `*` |
| `SLASH` | `'/'` | `/` |
| `ASSIGN` | `'='` | `=` |
| `LPAREN` | `'('` | `(` |
| `RPAREN` | `')'` | `)` |
| `COMMA` | `','` | `,` |
| `COLON` | `':'` | `:` |
| `FLOAT_LIT` | `[0-9]+ '.' [0-9]+` | `3.14` |
| `INT_LIT` | `[0-9]+` | `42` |
| `STR_LIT` | `'"' (~["\\\n])* '"'` | `"texto"` |
| `IDENT` | `[a-zA-Z_][a-zA-Z0-9_]*` | `soma` |
| `COMMENT` | `'#' ~[\n]*` | `# comentario` — ignorado |
| `WS` | `[ \t\r\n]+` | espaços — ignorado |
| `ERRO` | `.` | `@` — erro léxico |

---

## 5. Como Executar os Testes

```bash
# 1. Gerar o lexer (uma única vez)
cd src/gramatica
java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -o generated MiniLangLexer.g4

# 2. Executar sobre um programa de exemplo
cd ../../
python src/lexer/main_lexer.py tests/exemplos/exemplo1_fatorial.minilang

# 3. Salvar a saída para comparar com o esperado
python src/lexer/main_lexer.py tests/exemplos/exemplo1_fatorial.minilang \
       --salvar tests/saidas_esperadas/exemplo1_tokens_obtido.txt

# 4. Comparar saída obtida com esperada (Linux/macOS)
diff tests/saidas_esperadas/exemplo1_tokens.txt \
     tests/saidas_esperadas/exemplo1_tokens_obtido.txt
```

---

## 6. Relatório de Testes

### Teste 1 — `exemplo1_fatorial.minilang`

| Item | Resultado |
|---|---|
| Total de tokens esperados | 44 |
| Total de tokens obtidos | 44 |
| Erros léxicos | 0 |
| Status | ✅ PASSOU |

**Casos verificados:** reconhecimento de `funcao`, `se/entao/fim` aninhados, `retorne`, operador `<=`, operador `*`, chamada recursiva de função, `var`, `escreva`.

---

### Teste 2 — `exemplo2_laco.minilang`

| Item | Resultado |
|---|---|
| Total de tokens esperados | 36 |
| Total de tokens obtidos | 36 |
| Erros léxicos | 0 |
| Status | ✅ PASSOU |

**Casos verificados:** `para/de/ate/faca`, `FLOAT_LIT` (`0.0`), `FLOAT_TYPE`, `leia`, `PLUS`, `ASSIGN` em reatribuição.

---

### Teste 3 — `exemplo3_condicional.minilang`

| Item | Resultado |
|---|---|
| Total de tokens esperados | 35 |
| Total de tokens obtidos | 35 |
| Erros léxicos | 0 |
| Status | ✅ PASSOU |

**Casos verificados:** `se/senao/fim`, `BOOL_TYPE`, `verdadeiro`, `falso`, `GEQ` (`>=`), `STR_LIT` com espaços internos.

---

## 7. Dificuldades Encontradas e Soluções

| Dificuldade | Causa | Solução |
|---|---|---|
| `funcao` tokenizado como `IDENT` | Regra `IDENT` estava antes das keywords | Mover todas as keywords para antes de `IDENT` no `.g4` |
| `3.14` virava `INT(3)` + erro | `INT_LIT` estava antes de `FLOAT_LIT` | Inverter a ordem: `FLOAT_LIT` antes de `INT_LIT` |
| `==` virava `ASSIGN` + `ASSIGN` | `ASSIGN` estava antes de `EQ` | Mover operadores de dois chars para antes dos de um char |
| `ImportError` ao rodar `main_lexer.py` | Pasta `generated/` não no `sys.path` | Ajustar o `sys.path.insert` no script |
