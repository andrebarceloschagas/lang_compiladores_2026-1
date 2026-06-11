# MiniLang Compiler

Mini-compilador desenvolvido na disciplina de Compiladores — UFT/2026

Linguagem: MiniLang (imperativa estruturada)

Ferramenta: ANTLR 4 + Python 3

Alunos: [Antonio André](https://github.com/andrebarceloschagas), [Ranor Victor](https://github.com/ranorvictor), [Natália Nerys](https://github.com/natalia-nerys), [Luiz Fernando](https://github.com/lfocarvalho)

## Descrição da Linguagem

## Instalação

1. Crie e ative um ambiente virtual Python (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate     # Windows PowerShell
   ```
2. Instale as dependências:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Gere os arquivos do ANTLR se precisar atualizar a gramática:
   ```bash
   java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -o src/gramatica/generated src/gramatica/MiniLang.g4
   ```

## Como usar

- Compilar um arquivo MiniLang para Python:
  ```bash
  python src/compiler/main_compiler.py tests/exemplos/exemplo1_fatorial.minilang --py tests/exemplos/exemplo1_fatorial_compiled.py --tokens tests/saida_tokens.txt --ast tests/saida_ast.txt
  ```
- Gerar relatório de execução completo:
  ```bash
  python scripts/relatorio_execucao.py tests/exemplos/exemplo1_fatorial.minilang --report relatorio_execucao_exemplo1_fatorial.md
  ```

## Como rodar os testes

- Execute todos os testes com `pytest`:
  ```bash
  pytest
  ```

## Estrutura do projeto

- `src/lexer/` — analisador léxico e ferramentas de tokenização
- `src/parser/` — analisador sintático, impressor de AST e definição da gramática
- `src/compiler/` — análise semântica, geração de código e compilador completo
- `tests/` — casos de teste automatizados para léxico, parser, semântica e geração
- `src/gramatica/` — gramática ANTLR e diretório `generated/` com código gerado

> Observação: o diretório `src/gramatica/generated/` contém arquivos gerados pelo ANTLR. Se você atualizar `MiniLang.g4`, regenere esse diretório conforme a instrução acima.

