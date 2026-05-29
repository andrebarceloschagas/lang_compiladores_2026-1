# Semana 7: Ambientes de Execução

## 1. Estrutura de Memória
A MiniLang utiliza uma abordagem de compilação Source-to-Source (Transpilação). O código alvo é a linguagem de alto nível Python.
Dessa forma, o ambiente de execução não requer uma manipulação direta de ponteiros de Call Stack no nível do hardware por parte do nosso compilador.

## 2. Delegação para a Máquina Virtual
Ao gerar código Python, o ambiente de execução delega automaticamente para a Python Virtual Machine (PVM):
* A alocação de registros de ativação para chamadas recursivas.
* O controle de escopo léxico e tempo de vida de variáveis.
* O gerenciamento de memória em tempo de execução via *Garbage Collection*.
