# Semana 10: Aplicações e Conclusão

## 1. Relação com Casos Reais
O compilador MiniLang reflete uma arquitetura muito comum no desenvolvimento de software moderno: a transpilação. 
Ferramentas como TypeScript (compilado para JavaScript) e Vala (compilado para C) usam exatamente os mesmos conceitos aplicados neste projeto: análise léxica, sintática, checagem semântica rigorosa (Tabela de Símbolos) e posterior conversão para uma linguagem alvo mais flexível.

## 2. Considerações Finais
A experiência demonstrou a eficiência de se usar geradores de *parsers* como o ANTLR 4 e a aplicação do *Design Pattern Visitor* para percorrer estruturas complexas de grafos (AST) e gerar código funcional de maneira modular e controlada.
