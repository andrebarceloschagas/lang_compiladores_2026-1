# MiniLang Compiler

Mini-compilador desenvolvido na disciplina de Compiladores — UFT/2026

Linguagem: MiniLang (imperativa estruturada)

Ferramenta: ANTLR 4 + Python 3

Alunos: [Antonio André](https://github.com/andrebarceloschagas), [Ranor Victor](https://github.com/ranorvictor), [Natália Nerys](https://github.com/natalia-nerys), [Luiz Fernando](https://github.com/lfocarvalho)

## Descrição da Linguagem

## Como usar

- Compilar um arquivo MiniLang para Python:
  ```bash
  python src/compiler/main_compiler.py tests/exemplos/exemplo1_fatorial.minilang --py tests/exemplos/exemplo1_fatorial_compiled.py --tokens tests/saida_tokens.txt --ast tests/saida_ast.txt
  ```
- Gerar relatório de execução completo:
  ```bash
  python scripts/relatorio_execucao.py tests/exemplos/exemplo1_fatorial.minilang --report relatorio_execucao_exemplo1_fatorial.md
  ```

