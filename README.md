# 🚀 Interpretador da Linguagem LFun (Front-end e Avaliação Inteira)

Este repositório contém a implementação completa de um interpretador para a linguagem funcional **LFun**, desenvolvido em Python com recurso à biblioteca **PLY (Python Lex-Yacc)**. 
O projeto evoluiu da simples validação sintática (Front-end) para um motor de execução completo, capaz de gerir escopos, validar semântica, inferir tipos e avaliar expressões complexas, listas e funções recursivas.

## 🏗️ Arquitetura e Pipeline de Execução

A solução foi modularizada em cinco ficheiros principais, separando responsabilidades de forma elegante e seguindo a teoria clássica de compiladores e interpretadores:

1. **Árvore Sintática Abstrata - AST (`gramatica.py`)**
   * Define as estruturas de dados (classes Python) que representam os nós da árvore (ex: `FunDef`, `IfExpr`, `WhenExpr`, `ConsExpr`).
   * Serve como base de dados estrutural e semântica do que a linguagem suporta.

2. **Analisador Léxico (`analisador_lexico.py`)**
   * Recorre ao `ply.lex` para ler os caracteres do ficheiro e agrupar em *tokens* (agora incluindo o operador de divisão `/`).
   * Lida com a ignorância de espaços em branco, contagem de linhas e interceção de comentários (linha única `--` e múltiplas linhas `{- ... -}`).

3. **Analisador Sintático (`analisador_sintatico.py`)**
   * Utiliza o `ply.yacc` para aplicar regras gramaticais (BNF) aos *tokens*.
   * Resolve precedências matemáticas (onde `*` e `/` operam antes de `+` e `-`) e associatividade.
   * Orquestra o ciclo principal de execução, ligando a AST ao analisador semântico.

4. **Analisador Semântico e Tabela de Símbolos (`analisador_semantico.py`)**
   * O "Cérebro" do estado do programa. É responsável por intercetar declarações (variáveis e funções).
   * **Validação de Tipos:** Garante que o tipo declarado bate certo com a expressão avaliada.
   * **Imutabilidade:** Bloqueia reatribuições ilegais de variáveis ou de funções já definidas, lançando *Erros Semânticos* claros.
   * **Formatação Visual:** Transforma comentários multi-linha da linguagem em cabeçalhos elegantes na consola, separando visualmente o *output*.

5. **Motor de Avaliação (`avaliador.py`)**
   * A "Máquina de Calcular". Recebe expressões e o escopo atual, devolvendo tuplos com o `(valor_calculado, tipo_inferido)`.
   * Resolve chamadas de função dinâmicas (injetando argumentos em tabelas de símbolos locais para garantir o escopo fechado).
   * Executa todo o *Pattern Matching* do `when` e manipulação de listas na memória.

---

## 🌟 Extensões Implementadas e Funcionalidades Core

A linguagem foi desenhada com um foco claro nas características fundamentais do paradigma funcional, garantindo previsibilidade e ausência de efeitos secundários (imutabilidade).

### 1. Funções Recursivas e Imutabilidade
* Sem ciclos `for` ou `while`, a recursividade é o **mecanismo de iteração**. O nosso avaliador suporta auto-invocação com gestão correta do escopo (passagem por valor e isolamento de variáveis).
* **Imutabilidade estrita:** O Analisador Semântico garante que funções (`fun` / `let`) e variáveis não podem ter a sua assinatura ou corpo reescritos após a primeira declaração.

### 2. Listas e *Pattern Matching* (`[T]`, `[]`, `h:t`)
* As listas são a estrutura de dados por excelência. A sintaxe suporta o uso de parênteses retos (`[`, `]`) e o operador `cons` (`:`).
* O **Pattern Matching** na estrutura `when` permite desconstruir listas de forma elegante (separando a *cabeça* da *cauda*), avaliar casos base (`[]`) e lidar com padrões por defeito (`_`).

### 3. Sistema de Tipos Dinâmico mas Seguro (Type Checking)
* O avaliador infere o tipo em tempo de execução e devolve os resultados de forma clara (`Int`, `Bool`, `[Int]`). 
* Implementação completa de operadores lógicos (`<`, `>`, `==`) e matemáticos (`+`, `-`, `*`, e **divisão inteira `/`** com proteção contra divisão por zero).

---

## 💻 Interface Interativa (CLI) e Execução

Implementámos um menu interativo diretamente no terminal para uma experiência de desenvolvimento e teste fluida. A consola exibe a AST, o resultado da avaliação, o tipo inferido e eventuais mensagens de erro semântico de forma estruturada.

### Pré-requisitos
Certifique-se de que tem a biblioteca PLY instalada no seu ambiente Python:
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
  
## 🎨 Dica Pro: Documentação Visual na Consola
** O analisador utiliza os comentários multi-linha da linguagem para criar separadores visuais na consola. Se escrever no seu código LFun:
* {- --- Cálculo do Fatorial --- -}
* O motor de execução transformará esse comentário num cabeçalho em negrito, ajudando a organizar blocos de output durante os testes!


