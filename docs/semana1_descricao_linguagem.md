# MiniLang — Descrição da Linguagem

Disciplina: Compiladores | UFT — Palmas/TO  
Prof. Dr. Antonio Marcos A. Ferreira

Alunos: [Antonio André](https://github.com/andrebarceloschagas), [Ranor Victor](https://github.com/ranorvictor), [Natália Nerys](https://github.com/natalia-nerys), [Luiz Fernando](https://github.com/lfocarvalho)

Entrega: Semana 1

---

## 1. Visão Geral

**MiniLang** é uma linguagem de programação simplificada, criada para o projeto de mini-compilador da disciplina de Compiladores. O nome reflete o objetivo: uma linguagem *mínima*, mas completa o suficiente para exercitar todas as fases de um compilador moderno.

- **Paradigma:** Imperativo e estruturado
- **Tipagem:** Estática e explícita
- **Extensão de arquivo:** `.minilang`
- **Ferramenta de compilação:** ANTLR 4 + Python 3

---

## 2. Tipos de Dados

| Tipo     | Descrição                        | Exemplos de valores         |
|----------|----------------------------------|-----------------------------|
| `int`    | Número inteiro                   | `0`, `42`, `-10`            |
| `float`  | Número de ponto flutuante        | `3.14`, `0.5`, `100.0`      |
| `bool`   | Valor lógico                     | `verdadeiro`, `falso`       |
| `string` | Cadeia de caracteres             | `"ola"`, `"hello world"`    |

---

## 3. Palavras-Chave Reservadas

```
var       funcao    se        entao     senao
fim       enquanto  faca      para      de
ate       retorne   escreva   leia      verdadeiro
falso     e         ou        int       float
bool      string
```

---

## 4. Estruturas da Linguagem

### 4.1 Declaração de Variáveis

```
var <nome> : <tipo>
```

```pascal
var x : int
var nome : string
var ativo : bool
```

### 4.2 Atribuição

```pascal
x = 10
nome = "Maria"
ativo = verdadeiro
```

### 4.3 Entrada e Saída

```pascal
leia(x)           # lê um valor do teclado e armazena em x
escreva(x + 1)    # imprime o resultado da expressão
escreva("texto")  # imprime uma string literal
```

### 4.4 Condicional

```pascal
se (<condição>) entao
  <bloco>
fim

se (<condição>) entao
  <bloco>
senao
  <bloco>
fim
```

### 4.5 Repetição — enquanto

```pascal
enquanto (<condição>) faca
  <bloco>
fim
```

### 4.6 Repetição — para

```pascal
para <variável> de <inicio> ate <fim> faca
  <bloco>
fim
```

### 4.7 Funções

```pascal
funcao <nome>(<param>: <tipo>, ...) : <tipo_retorno>
  <bloco>
fim
```

### 4.8 Comentários

```pascal
# isto é um comentário de linha inteira
x = 10  # comentário ao final de uma linha
```

---

## 5. Operadores

### Aritméticos
| Operador | Descrição     |
|----------|---------------|
| `+`      | Adição        |
| `-`      | Subtração     |
| `*`      | Multiplicação |
| `/`      | Divisão       |

### Relacionais
| Operador | Descrição      |
|----------|----------------|
| `==`     | Igual          |
| `!=`     | Diferente      |
| `<`      | Menor que      |
| `>`      | Maior que      |
| `<=`     | Menor ou igual |
| `>=`     | Maior ou igual |

### Lógicos
| Operador | Descrição  |
|----------|------------|
| `e`      | E lógico   |
| `ou`     | OU lógico  |

### Precedência (maior para menor)
1. `( )` — agrupamento
2. `-` unário
3. `*`, `/`
4. `+`, `-`
5. `<`, `>`, `<=`, `>=`, `==`, `!=`
6. `e`
7. `ou`

---

## 6. Regras Gerais

- Toda variável deve ser declarada com `var` antes de ser usada.
- Funções devem ser declaradas antes de serem chamadas.
- O tipo de retorno de uma função é obrigatório.
- Não há inferência de tipos — toda declaração é explícita.
- Strings são delimitadas por aspas duplas `"`.
- Não há suporte a arrays, ponteiros ou orientação a objetos.

---

## 7. Exemplos de Programas

### Exemplo 1 — Cálculo de Fatorial (função recursiva)

```pascal
# Calcula o fatorial de um numero
funcao fatorial(n: int): int
  se (n <= 1) entao
    retorne 1
  fim
  retorne n * fatorial(n - 1)
fim

var resultado: int
resultado = fatorial(5)
escreva(resultado)    # Saida esperada: 120
```

### Exemplo 2 — Soma de valores com laço

```pascal
# Le 10 numeros e calcula a soma
var i: int
var soma: float
soma = 0.0

para i de 1 ate 10 faca
  var x: float
  leia(x)
  soma = soma + x
fim

escreva(soma)
```

### Exemplo 3 — Verificação de maioridade

```pascal
# Verifica se a pessoa e maior de idade
var idade: int
var maior: bool

leia(idade)

se (idade >= 18) entao
  maior = verdadeiro
  escreva("Maior de idade")
senao
  maior = falso
  escreva("Menor de idade")
fim
```