# Relatório de execução: exemplo1_fatorial.minilang

## Entrada
- Arquivo MiniLang: `C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\tests\exemplos\exemplo1_fatorial.minilang`
- Diretório do projeto: `C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main`

## Comandos executados
### Lexer
- Comando: `C:\Users\Ranor Victor\AppData\Local\Programs\Python\Python312\python.exe src/lexer/main_lexer.py C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\tests\exemplos\exemplo1_fatorial.minilang --salvar C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\saida_tokens.txt`
- Status: ✅ Sucesso (exit code 0)
- Saída padrão:
```
=========================================================
  Analisador Léxico — MiniLang
  Arquivo: C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\tests\exemplos\exemplo1_fatorial.minilang
=========================================================
<FUNCAO,funcao>                (linha 2)
<IDENT,fatorial>               (linha 2)
<LPAREN,(>                     (linha 2)
<IDENT,n>                      (linha 2)
<COLON,:>                      (linha 2)
<INT_TYPE,int>                 (linha 2)
<RPAREN,)>                     (linha 2)
<COLON,:>                      (linha 2)
<INT_TYPE,int>                 (linha 2)
<SE,se>                        (linha 3)
<LPAREN,(>                     (linha 3)
<IDENT,n>                      (linha 3)
<LEQ,<=>                       (linha 3)
<INT_LIT,1>                    (linha 3)
<RPAREN,)>                     (linha 3)
<ENTAO,entao>                  (linha 3)
<RETORNE,retorne>              (linha 4)
<INT_LIT,1>                    (linha 4)
<FIM,fim>                      (linha 5)
<RETORNE,retorne>              (linha 6)
<IDENT,n>                      (linha 6)
<STAR,*>                       (linha 6)
<IDENT,fatorial>               (linha 6)
<LPAREN,(>                     (linha 6)
<IDENT,n>                      (linha 6)
<MINUS,->                      (linha 6)
<INT_LIT,1>                    (linha 6)
<RPAREN,)>                     (linha 6)
<FIM,fim>                      (linha 7)
<VAR,var>                      (linha 9)
<IDENT,resultado>              (linha 9)
<COLON,:>                      (linha 9)
<INT_TYPE,int>                 (linha 9)
<IDENT,resultado>              (linha 10)
<ASSIGN,=>                     (linha 10)
<IDENT,fatorial>               (linha 10)
<LPAREN,(>                     (linha 10)
<INT_LIT,5>                    (linha 10)
<RPAREN,)>                     (linha 10)
<ESCREVA,escreva>              (linha 11)
<LPAREN,(>                     (linha 11)
<IDENT,resultado>              (linha 11)
<RPAREN,)>                     (linha 11)
=========================================================
  Total de tokens: 43
=========================================================

Saída salva em: C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\saida_tokens.txt
```

### Compilador completo
- Comando: `C:\Users\Ranor Victor\AppData\Local\Programs\Python\Python312\python.exe src/compiler/main_compiler.py C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\tests\exemplos\exemplo1_fatorial.minilang --py C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\tests\exemplos\exemplo1_fatorial.py --tokens C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\saida_tokens.txt --ast C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\saida_ast.txt`
- Status: ✅ Sucesso (exit code 0)
- Saída padrão:
```
Compilação concluída. Código Python salvo em: C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\tests\exemplos\exemplo1_fatorial.py
```

## Arquivos gerados
- Tokens salvos em: `C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\saida_tokens.txt`
- AST salva em: `C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\saida_ast.txt`
- Código Python gerado em: `C:\Users\Ranor Victor\Downloads\lang_compiladores_2026-1-main\tests\exemplos\exemplo1_fatorial.py`

## Amostra de tokens gerados
```
<FUNCAO,funcao> (linha 2)
<IDENT,fatorial> (linha 2)
<LPAREN,(> (linha 2)
<IDENT,n> (linha 2)
<COLON,:> (linha 2)
<INT_TYPE,int> (linha 2)
<RPAREN,)> (linha 2)
<COLON,:> (linha 2)
<INT_TYPE,int> (linha 2)
<SE,se> (linha 3)
<LPAREN,(> (linha 3)
<IDENT,n> (linha 3)
<LEQ,<=> (linha 3)
<INT_LIT,1> (linha 3)
<RPAREN,)> (linha 3)
<ENTAO,entao> (linha 3)
<RETORNE,retorne> (linha 4)
<INT_LIT,1> (linha 4)
<FIM,fim> (linha 5)
<RETORNE,retorne> (linha 6)
<IDENT,n> (linha 6)
<STAR,*> (linha 6)
<IDENT,fatorial> (linha 6)
<LPAREN,(> (linha 6)
<IDENT,n> (linha 6)
<MINUS,-> (linha 6)
<INT_LIT,1> (linha 6)
<RPAREN,)> (linha 6)
<FIM,fim> (linha 7)
<VAR,var> (linha 9)
```

## Amostra de AST gerada
```
Program
├── FuncDecl: fatorial : int
│   ├── Params
│   │   └── Param: n : int
│   └── Block
│       ├── IfStmt
│       │   ├── Cond:
│       │   │   └── BinOp(<=)
│       │   │       ├── Ident(n)
│       │   │       └── Int(1)
│       │   └── Then:
│       │       └── Block
│       │           └── ReturnStmt
│       │               └── Int(1)
│       └── ReturnStmt
│           └── BinOp(*)
│               ├── Ident(n)
│               └── FuncCall: fatorial
│                   └── BinOp(-)
│                       ├── Ident(n)
│                       └── Int(1)
├── VarDecl: resultado : int
├── Assign: resultado
│   └── FuncCall: fatorial
│       └── Int(5)
└── Escreva
    └── Ident(resultado)
```

## Código Python transpilado
```python
# Código gerado pelo compilador MiniLang
import sys

def fatorial(n):
    if (n <= 1):
        return 1
    return (n * fatorial((n - 1)))

resultado = 0
resultado = fatorial(5)
print(resultado)
```
