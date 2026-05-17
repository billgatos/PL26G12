# gramatica.py

"""
Gramática LFun (Atualizada com Funções):

Programa     -> ListaDecl
ListaDecl    -> Declaracao ListaDecl | Declaracao
Declaracao   -> Expressao ';' 
              | 'let' ID ':' Tipo '=' Expressao ';'      (Variável)
              | 'fun' ID ':' Tipo '->' Tipo ';'          (Assinatura de Função)
              | 'let' ID ID '=' Expressao ';'            (Definição de Função)
Tipo         -> 'Int' | 'Bool'
Expressao    -> Expressao '+' Expressao
              | Expressao '-' Expressao
              | Expressao '*' Expressao
              | Expressao '<' Expressao
              | Expressao '==' Expressao
              | '(' Expressao ')'
              | ID '(' Expressao ')'                     (Chamada de Função)
              | NUMERO
              | BOOLEANO
              | ID
"""

class Node:
    pass

class LetVarDecl(Node):
    """Representa a declaração de uma variável: let x : Int = 5;"""
    def __init__(self, id_name, var_type, expr):
        self.id_name = id_name      # Nome da variável (ex: x)
        self.var_type = var_type    # Tipo esperado (ex: Int)
        self.expr = expr            # Expressão a avaliar (ex: 5)
        
    def __repr__(self):
        return f"LetVar({self.id_name}: {self.var_type} = {self.expr})"

class FunSignature(Node):
    """Representa a assinatura de uma função: fun inc : Int -> Int;"""
    def __init__(self, id_name, arg_type, return_type):
        self.id_name = id_name          # Nome da função
        self.arg_type = arg_type        # Tipo do argumento de entrada
        self.return_type = return_type  # Tipo do retorno
        
    def __repr__(self):
        return f"FunSig({self.id_name} : {self.arg_type} -> {self.return_type})"

class FunDef(Node):
    """Representa a definição (corpo) de uma função: let inc x = x + 1;"""
    def __init__(self, id_name, arg_name, expr):
        self.id_name = id_name      # Nome da função
        self.arg_name = arg_name    # Nome do parâmetro/argumento
        self.expr = expr            # Corpo da função (expressão a avaliar)
        
    def __repr__(self):
        return f"FunDef({self.id_name}({self.arg_name}) = {self.expr})"

# ==========================================
# EXPRESSÕES
# ==========================================

class FunCall(Node):
    """Representa a chamada de uma função: inc(5)"""
    def __init__(self, id_name, arg_expr):
        self.id_name = id_name      # Nome da função a chamar
        self.arg_expr = arg_expr    # Argumento passado à função
        
    def __repr__(self):
        return f"Call({self.id_name}({self.arg_expr}))"

class BinOp(Node):
    """Representa operações binárias matemáticas ou lógicas (+, -, *, <, ==, etc.)"""
    def __init__(self, op, left, right):
        self.op = op          # Operador em string (ex: '+')
        self.left = left      # Nó da esquerda
        self.right = right    # Nó da direita
        
    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"
    
class UnaryOp(Node):
    """Representa operações unárias (como números negativos: -5)"""
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
        
    def __repr__(self):
        return f"({self.op}{self.expr})"

class Literal(Node):
    """Representa valores diretos (inteiros ou booleanos: 5, true, false)"""
    def __init__(self, value, type_val):
        self.value = value        # O valor real em Python
        self.type_val = type_val  # String representando o tipo ('Int' ou 'Bool')
        
    def __repr__(self):
        return str(self.value)

class Identifier(Node):
    """Representa o uso de uma variável (quando a chamamos pelo nome)"""
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f"ID({self.name})"
    
class IfExpr(Node):
    """Representa a expressão condicional: if (cond) then (expr1) else (expr2)"""
    def __init__(self, cond, then_expr, else_expr):
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr
        
    def __repr__(self):
        return f"If(Cond: {self.cond} Then: {self.then_expr} Else: {self.else_expr})"
    
class WhenExpr(Node):
    """Representa a expressão `when`: when (expr) { case1 => expr1; case2 => expr2; ... }"""
    def __init__(self, cond_expr, cases):
        self.cond_expr = cond_expr  # Expressão que será testada
        self.cases = cases          # Lista de casos, onde cada caso é uma tupla (padrão, expressão_resultado)
        
    def __repr__(self):
        cases_str = ", ".join(str(c) for c in self.cases)
        return f"When(Cond: {self.cond_expr} Cases: [{cases_str}])"

class Case(Node):
    """Representa um caso dentro de um `when`: padrões -> resultado"""
    def __init__(self, patterns, result_expr):
        self.patterns = patterns
        self.result_expr = result_expr
        
    def __repr__(self):
        pats_str = " | ".join(str(p) for p in self.patterns)
        return f"Case({pats_str} -> {self.result_expr})"

# ==========================================
# LISTAS E COMENTÁRIOS
# ==========================================

class Comentario(Node):
    """Representa um comentário no código"""
    def __init__(self, texto):
        self.texto = texto.strip()
    def __repr__(self):
        return f"Comentario({self.texto})"

# Novos Nós para Listas: Tipos
class ListType(Node):
    """Representa o tipo de uma lista na declaração: [Int]"""
    def __init__(self, element_type):
        self.element_type = element_type
    def __repr__(self):
        return f"[{self.element_type}]"

# Novos Nós para Listas: Expressões
class EmptyList(Node):
    """Representa uma lista vazia: []"""
    def __repr__(self):
        return "[]"

class ConsExpr(Node):
    """Representa a construção de uma lista com um elemento no início e 
    outra lista no final: head : tail"""
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
    def __repr__(self):
        return f"({self.head} : {self.tail})"

# ==========================================
# PADRÕES (PATTERNS) PARA O WHEN
# ==========================================

# Novos Nós para Listas: Padrões do `when`
class EmptyListPattern(Node):
    def __repr__(self):
        return "[]"

class ConsPattern(Node):
    def __init__(self, head_id, tail_id):
        self.head_id = head_id
        self.tail_id = tail_id
    def __repr__(self):
        return f"({self.head_id}:{self.tail_id})"

class DefaultPattern(Node):
    def __repr__(self):
        return "_"