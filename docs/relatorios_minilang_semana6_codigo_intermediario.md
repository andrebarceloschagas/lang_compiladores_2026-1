# Semana 6: Código Intermediário

## 1. Representação Intermediária (RI)
Em arquiteturas de compiladores modernos, a etapa de geração textual de código de três endereços pode ser omitida se a Árvore Sintática Abstrata for rica o suficiente para atuar como RI.
Na MiniLang, decidimos usar a própria **AST estruturada em memória** como a nossa Representação Intermediária.

## 2. Eliminação de Variáveis Temporárias Artificiais
Como o nosso *target* (alvo) é a linguagem Python, que já suporta expressões aninhadas e chamadas de função encadeadas recursivamente (ex: `n * fatorial(n - 1)`), não foi necessário decompor as expressões matemáticas em dezenas de variáveis temporárias textuais (`t1`, `t2`, etc.). O *Visitor* percorre a AST e constrói as expressões hierarquicamente.
