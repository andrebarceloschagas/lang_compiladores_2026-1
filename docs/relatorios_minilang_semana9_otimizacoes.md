# Semana 9: Otimizações Independentes de Máquina

## 1. Otimização Implícita
A vantagem imediata da transpilação Source-to-Source para Python é a herança do ecossistema de otimizações da linguagem alvo.

## 2. Constant Folding e Código Morto
A PVM (*Python Virtual Machine*) aplica automaticamente técnicas de dobramento de constantes (Constant Folding) e propagação em tempo de compilação do seu próprio *bytecode*. Se o script gerado tiver variáveis ou importações não utilizadas (Código Morto), ferramentas auxiliares do ecossistema e o próprio JIT do interpretador conseguem minimizar esse impacto sem necessidade de rotinas complexas no compilador MiniLang original.

## 3. Paralelismo e Memória
A localidade de memória e as otimizações de *cache* de processador ficam a cargo do interpretador CPython no ambiente Linux, garantindo máxima estabilidade para operações matemáticas recursivas, como o fatorial.
