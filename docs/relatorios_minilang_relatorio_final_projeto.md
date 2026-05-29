# Projeto de Compiladores — Relatório Final Executivo

**Universidade Federal do Tocantins (UFT) — Palmas/TO**
**Disciplina:** Compiladores
**Equipe:** Antonio André, Ranor Victor, Natália Nerys, Luiz Fernando

---

## 1. Introdução e Especificação da Linguagem (Semanas 1 e 2)
A equipe definiu e implementou a **MiniLang**, uma linguagem com foco educacional de paradigma imperativo. Utilizando a notação EBNF, definimos uma gramática livre de contexto robusta o suficiente para lidar com declarações estáticas de variáveis, laços de repetição, controle de fluxo e funções recursivas.

## 2. Front-End: Análise Léxica e Sintática (Semanas 3 e 4)
Utilizando o framework **ANTLR 4**, construímos os analisadores através do arquivo `MiniLang.g4`. O gerador produziu um lexer capaz de identificar consistentemente expressões numéricas, palavras-chave e símbolos matemáticos (removendo comentários e espaços brancos). Na etapa sintática, implementamos rotinas de geração da Árvore Sintática Abstrata (AST) acopladas a relatórios de erro elegantes e visuais no terminal Linux.

## 3. Middle-End: Semântica e RI (Semanas 5 e 6)
O coração da análise semântica foi estabelecido no script `transpilador.py`. Uma Tabela de Símbolos em memória (dicionário Hash) foi alocada para capturar e validar os tipos de dados declarados durante o percurso da AST via *Visitor*. Decidimos adotar a própria AST validada como a nossa Representação Intermediária (RI), eliminando a necessidade de gerar textualmente variáveis temporárias (`t1, t2`) comuns no código de três endereços tradicional.

## 4. Back-End: Geração de Código e Ambiente de Execução (Semanas 7, 8 e 9)
A geração final de código segue a estratégia de um Transpilador (Source-to-Source). A MiniLang é convertida de forma limpa e corretamente identada para a linguagem Python. Esta escolha delega à *Python Virtual Machine* (PVM) as atribuições mais complexas de baixo nível: *Garbage Collection*, alocação de registros de ativação de pilha e otimizações de tempo de compilação como o *Constant Folding*. O executável final reflete exatamente a lógica escrita na nossa gramática nativa.

## 5. Conclusão (Semana 10)
O projeto cobriu o fluxo ponta-a-ponta esperado na disciplina. A arquitetura validada assemelha-se a linguagens reais utilizadas na indústria, unindo conceitos teóricos profundos (Autômatos e Árvores) à agilidade de ferramentas modernas (ANTLR4 e Python), consolidando o aprendizado da equipe no domínio do funcionamento interno da tradução de software.
