# Front-end da Linguagem LFun (Analisador Léxico e Sintático)

Este repositório contém a implementação do *Front-end* para a linguagem funcional **LFun**, desenvolvido em Python com recurso à biblioteca **PLY (Python Lex-Yacc)**. O objetivo deste módulo é ler código-fonte em LFun, validá-lo e gerar a respetiva Árvore Sintática Abstrata (AST).

## 🚀 Arquitetura e Passos da Solução

A solução foi modularizada em três ficheiros principais, separando as preocupações de acordo com a teoria clássica de compiladores:

1. **Definição da AST (`gramatica.py`)**
   * Define as estruturas de dados (classes Python) que representam os nós da árvore (ex: `FunDef`, `IfExpr`, `WhenExpr`, `ConsExpr`).
   * Serve como documentação semântica e hierárquica do que a linguagem suporta.

2. **Analisador Léxico (`analisador_lexico.py`)**
   * Recorre ao `ply.lex` para ler os caracteres do ficheiro e agrupar em *tokens*.
   * Lida com a ignorância de espaços em branco, contagem de linhas e remoção de comentários (quer de linha única `--` quer de múltiplas linhas `{- ... -}`).

3. **Analisador Sintático (`analisador_sintatico.py`)**
   * Utiliza o `ply.yacc` para receber os *tokens* e aplicar as regras gramaticais (Notação BNF).
   * Lida com regras de precedência e associatividade (ex: avaliação do operador `:` da direita para a esquerda, precedência matemática).
   * Resolve ambiguidades entre expressões matemáticas puras e os padrões usados na estrutura de seleção `when`. O *output* final é a Árvore Sintática gerada.

---

## 🌟 Extensões Implementadas e Justificação

Para enriquecer a linguagem base, decidimos focar a implementação nas características fundamentais do paradigma funcional. As duas extensões escolhidas oferecem o maior poder computacional e expressividade possíveis à linguagem.

### 1. Funções Recursivas
* **A Razão da Escolha:** Como a LFun não possui estruturas de controlo iterativas tradicionais (como ciclos `for` ou `while`), a recursividade é o **mecanismo essencial** para iteração. Sem ela, seria impossível escrever algoritmos que dependam de ciclos arbitrários ou manipulação de dados de tamanho variável.
* **Implementação Sintática:** O *parser* foi desenhado para aceitar chamadas de funções genéricas (`FunCall`) em qualquer parte de uma expressão. A sintaxe não sofreu alterações, delegando para a próxima fase (Analisador Semântico/Interpretador) a correta resolução do ambiente/escopo da função para permitir a auto-invocação.

### 2. Listas e *Pattern Matching* (`[T]`, `[]`, `h:t`)
* **A Razão da Escolha:** As listas são a estrutura de dados por excelência na programação funcional. A escolha prende-se pela **sinergia perfeita com a expressão `when`**. Ter listas permite tirar o verdadeiro proveito do *Pattern Matching*, permitindo escrever código elegante que distingue entre uma lista vazia e uma lista com elementos.
* **Implementação Sintática:** Foram introduzidos os *tokens* de parênteses retos (`[` e `]`) e o operador dois pontos (`:`). A gramática foi expandida para suportar não só a criação de listas matemáticas genéricas (`1 : 2 : []`), mas também a sua desconstrução explícita nos padrões do *when* (os casos `[]` e `h:t`), isolando-os semanticamente de ambiguidades (*reduce/reduce conflicts*).

---

## 🛠️ Como Executar

**Pré-requisitos:**
É necessário ter a biblioteca PLY instalada:
```bash
pip install ply
