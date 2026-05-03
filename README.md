# Front-end da Linguagem LFun (Analisador Léxico e Sintático)

Este repositório contém a implementação do *Front-end* para a linguagem funcional **LFun**, desenvolvido em Python com recurso à biblioteca **PLY (Python Lex-Yacc)**. 
O objetivo deste módulo é ler código-fonte em LFun, validá-lo e gerar a respetiva Árvore Sintática Abstrata (AST).

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
* **Implementação Sintática:** O *parser* foi desenhado para aceitar chamadas de funções genéricas (`FunCall`) em qualquer parte de uma expressão. A sintaxe não sofreu alterações, delegando para a próxima fase a correta resolução do ambiente/escopo da função para permitir a auto-invocação.

### 2. Listas e *Pattern Matching* (`[T]`, `[]`, `h:t`)
* **A Razão da Escolha:** As listas são a estrutura de dados por excelência na programação funcional. A escolha prende-se pela **sinergia perfeita com a expressão `when`**. Ter listas permite tirar o verdadeiro proveito do *Pattern Matching*, escrevendo código elegante que distingue entre uma lista vazia e uma lista com elementos.
* **Implementação Sintática:** Foram introduzidos os *tokens* de parênteses retos (`[` e `]`) e o operador dois pontos (`:`). A gramática suporta a criação de listas genéricas e a sua desconstrução explícita nos padrões do *when*, isolando-os semanticamente de ambiguidades.

## 💻 3. Interface Interativa (CLI) e Como Executar

Para facilitar a avaliação e o teste do *parser*, implementámos um menu interativo diretamente no terminal. 

### Pré-requisitos
Certifique-se de que tem a biblioteca PLY instalada no seu ambiente:
```bash
pip install ply
```

### Iniciar o Analisador
Execute o script principal no seu terminal:
```bash
python analisador_sintatico.py
```

### Utilização do Menu
Ao iniciar, será apresentado um menu com as seguintes opções:
```text
==============================
   ANALISADOR SINTÁTICO LFun
==============================
1. Carregar de um ficheiro (.lfun)
2. Introduzir código na consola
3. Executar o exemplo embutido
0. Sair
==============================
```

* **`1` - Ficheiro:** Solicita o caminho de um ficheiro (ex: `teste.lfun`) e processa o seu conteúdo em bloco. Ideal para validar programas mais extensos.
* **`2` - Consola:** Abre um modo de inserção livre (múltiplas linhas) para testar *snippets* na hora. 
  > 💡 **Nota:** Para terminar a introdução de exemplos e submeter, basta pressionar as teclas `CTRL+D` em Linux/Mac ou `CTRL+Z` seguido de Enter no terminal do Windows (numa linha vazia).
* **`3` - Exemplo embutido:** Executa instantaneamente um código de demonstração pré-configurado que ilustra o funcionamento em conjunto das listas e da recursividade.
* **`0` - Sair:** Encerra a ferramenta em segurança.


