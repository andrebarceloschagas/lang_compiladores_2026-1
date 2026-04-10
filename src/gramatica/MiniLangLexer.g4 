// ============================================================
// Como gerar:
//   java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -o generated MiniLangLexer.g4
// ============================================================

lexer grammar MiniLangLexer;


// ── Palavras-chave ───────────────────────────────────────────
// IMPORTANTE: devem vir ANTES da regra IDENT para ter prioridade

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


// ── Tipos ────────────────────────────────────────────────────

INT_TYPE   : 'int'    ;
FLOAT_TYPE : 'float'  ;
BOOL_TYPE  : 'bool'   ;
STR_TYPE   : 'string' ;


// ── Operadores Relacionais ───────────────────────────────────
// IMPORTANTE: operadores de dois caracteres (==, !=, <=, >=)
// devem vir ANTES dos de um caractere (=, <, >)

EQ  : '==' ;
NEQ : '!=' ;
LEQ : '<=' ;
GEQ : '>=' ;
LT  : '<'  ;
GT  : '>'  ;


// ── Operadores Aritméticos e Atribuição ──────────────────────

PLUS   : '+' ;
MINUS  : '-' ;
STAR   : '*' ;
SLASH  : '/' ;
ASSIGN : '=' ;


// ── Delimitadores ────────────────────────────────────────────

LPAREN : '(' ;
RPAREN : ')' ;
COMMA  : ',' ;
COLON  : ':' ;


// ── Literais ─────────────────────────────────────────────────
// IMPORTANTE: FLOAT_LIT deve vir ANTES de INT_LIT
// para que "3.14" não seja tokenizado como INT "3" + PONTO + INT "14"

FLOAT_LIT : [0-9]+ '.' [0-9]+ ;
INT_LIT   : [0-9]+             ;
STR_LIT   : '"' (~["\\\n])* '"' ;


// ── Identificadores ──────────────────────────────────────────
// Vem após palavras-chave: o ANTLR aplica a regra que aparece
// primeiro em caso de empate, então keywords têm prioridade

IDENT : [a-zA-Z_][a-zA-Z0-9_]* ;


// ── Ignorados ────────────────────────────────────────────────

COMMENT : '#' ~[\n]* -> skip ;
WS      : [ \t\r\n]+ -> skip ;


// ── Erro Léxico ──────────────────────────────────────────────
// Captura qualquer caractere não reconhecido e emite erro

ERRO : . ;
