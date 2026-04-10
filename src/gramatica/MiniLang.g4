// ============================================================
// MiniLang — Gramática Completa (Lexer + Parser) — ANTLR 4
// Disciplina: Compiladores | UFT — Palmas/TO
// Arquivo: MiniLang.g4
//
// Como gerar:
//   java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 \
//        -visitor -o generated MiniLang.g4
//
// A flag -visitor gera a interface Visitor para percorrer a AST
// ============================================================

grammar MiniLang;


// ════════════════════════════════════════════════════════════
// REGRAS SINTÁTICAS (Parser)
// ════════════════════════════════════════════════════════════

// ── Programa ─────────────────────────────────────────────────

program
    : (declaration | statement)* EOF
    ;


// ── Declarações ──────────────────────────────────────────────

declaration
    : varDecl
    | funcDecl
    ;

varDecl
    : VAR IDENT COLON type
    ;

funcDecl
    : FUNCAO IDENT LPAREN params RPAREN COLON type
        block
      FIM
    ;

params
    : param (COMMA param)*
    |
    ;

param
    : IDENT COLON type
    ;


// ── Tipos ─────────────────────────────────────────────────────

type
    : INT_TYPE
    | FLOAT_TYPE
    | BOOL_TYPE
    | STR_TYPE
    ;


// ── Bloco e Comandos ──────────────────────────────────────────

block
    : statement*
    ;

statement
    : varDecl                                                      # stmtVarDecl
    | IDENT ASSIGN expression                                      # stmtAssign
    | SE LPAREN expression RPAREN ENTAO block FIM                 # stmtIf
    | SE LPAREN expression RPAREN ENTAO block SENAO block FIM     # stmtIfElse
    | ENQUANTO LPAREN expression RPAREN FACA block FIM            # stmtWhile
    | PARA IDENT DE expression ATE expression FACA block FIM      # stmtFor
    | RETORNE expression                                           # stmtReturn
    | ESCREVA LPAREN expression RPAREN                            # stmtEscreva
    | LEIA LPAREN IDENT RPAREN                                    # stmtLeia
    | funcCall                                                     # stmtFuncCall
    ;


// ── Chamada de Função ─────────────────────────────────────────

funcCall
    : IDENT LPAREN argList RPAREN
    ;

argList
    : expression (COMMA expression)*
    |
    ;


// ── Expressões ────────────────────────────────────────────────
// O ANTLR 4 resolve recursão à esquerda automaticamente.
// A ordem das alternativas define a precedência:
// alternativas mais abaixo têm maior precedência.

expression
    : expression (E_LOG | OU_LOG) expression      # exprLogico
    | expression (EQ | NEQ)       expression      # exprIgualdade
    | expression (LT | GT | LEQ | GEQ) expression # exprRelacional
    | expression (PLUS | MINUS)   expression      # exprAditivo
    | expression (STAR | SLASH)   expression      # exprMultiplicativo
    | MINUS expression                            # exprNegacao
    | primary                                     # exprPrimary
    ;

primary
    : INT_LIT                                     # primInt
    | FLOAT_LIT                                   # primFloat
    | STR_LIT                                     # primString
    | VERDADEIRO                                  # primVerdadeiro
    | FALSO                                       # primFalso
    | funcCall                                    # primFuncCall
    | IDENT                                       # primIdent
    | LPAREN expression RPAREN                    # primParens
    ;


// ════════════════════════════════════════════════════════════
// REGRAS LÉXICAS (Lexer)
// ════════════════════════════════════════════════════════════

VAR        : 'var'        ;
FUNCAO     : 'funcao'     ;
SE         : 'se'         ;
ENTAO      : 'entao'      ;
SENAO      : 'senao'      ;
FIM        : 'fim'        ;
ENQUANTO   : 'enquanto'   ;
FACA       : 'faca'       ;
PARA       : 'para'       ;
DE         : 'de'         ;
ATE        : 'ate'        ;
RETORNE    : 'retorne'    ;
ESCREVA    : 'escreva'    ;
LEIA       : 'leia'       ;
VERDADEIRO : 'verdadeiro' ;
FALSO      : 'falso'      ;
E_LOG      : 'e'          ;
OU_LOG     : 'ou'         ;

INT_TYPE   : 'int'    ;
FLOAT_TYPE : 'float'  ;
BOOL_TYPE  : 'bool'   ;
STR_TYPE   : 'string' ;

EQ  : '==' ;
NEQ : '!=' ;
LEQ : '<=' ;
GEQ : '>=' ;
LT  : '<'  ;
GT  : '>'  ;

PLUS   : '+' ;
MINUS  : '-' ;
STAR   : '*' ;
SLASH  : '/' ;
ASSIGN : '=' ;

LPAREN : '(' ;
RPAREN : ')' ;
COMMA  : ',' ;
COLON  : ':' ;

FLOAT_LIT : [0-9]+ '.' [0-9]+ ;
INT_LIT   : [0-9]+             ;
STR_LIT   : '"' (~["\\\n])* '"' ;

IDENT : [a-zA-Z_][a-zA-Z0-9_]* ;

COMMENT : '#' ~[\n]* -> skip ;
WS      : [ \t\r\n]+ -> skip ;

ERRO : . ;
