# Semana 8: Geração de Código

## 1. Tradução Final
A geração de código é concluída convertendo os nós sintáticos da MiniLang para equivalentes diretos em Python (`.py`).

## 2. Preservação de Escopo e Semântica
O back-end do nosso transpilador inclui um sistema de controle de identação (`self.indentacao`) para garantir que os blocos de código condicional e laços da MiniLang (delimitados por `entao...fim`) sejam corretamente convertidos para a estrutura baseada em espaços em branco exigida pela linguagem Python.

## 3. Entrega
O resultado desta etapa é um script Python (`.py`) autossuficiente e funcional que pode ser executado diretamente no interpretador do sistema operacional, exibindo no terminal o output exato planejado no arquivo original `.minilang`.
