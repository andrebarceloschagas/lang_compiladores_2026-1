# Semana 5: Tradução Dirigida por Sintaxe e Tabela de Símbolos

## 1. Ações Semânticas
Foi desenvolvido o módulo `transpilador.py`, que atua como o motor de tradução dirigida por sintaxe do compilador, navegando sobre a AST gerada.

## 2. Tabela de Símbolos
A tabela de símbolos foi implementada utilizando um dicionário em Python (`self.tabela_simbolos`). 
* **Funcionamento:** Sempre que um nó do tipo `VarDecl` é visitado, o identificador e o seu respectivo tipo são guardados na tabela.
* **Verificação:** Nas operações de atribuição (`Assign`), o compilador verifica ativamente a tabela. Caso haja tentativa de uso de uma variável não declarada, um Erro Semântico é acionado.
