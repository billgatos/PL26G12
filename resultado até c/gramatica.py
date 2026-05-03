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
    def __init__(self, id_name, var_type, expr):
        self.id_name = id_name
        self.var_type = var_type
        self.expr = expr
        
    def __repr__(self):
        return f"LetVar({self.id_name}: {self.var_type} = {self.expr})"

class FunSignature(Node):
    def __init__(self, id_name, arg_type, return_type):
        self.id_name = id_name
        self.arg_type = arg_type
        self.return_type = return_type
        
    def __repr__(self):
        return f"FunSig({self.id_name} : {self.arg_type} -> {self.return_type})"

class FunDef(Node):
    def __init__(self, id_name, arg_name, expr):
        self.id_name = id_name
        self.arg_name = arg_name
        self.expr = expr
        
    def __repr__(self):
        return f"FunDef({self.id_name}({self.arg_name}) = {self.expr})"

class FunCall(Node):
    def __init__(self, id_name, arg_expr):
        self.id_name = id_name
        self.arg_expr = arg_expr
        
    def __repr__(self):
        return f"Call({self.id_name}({self.arg_expr}))"

class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        
    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"
    
class UnaryOp(Node):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
        
    def __repr__(self):
        return f"({self.op}{self.expr})"

class Literal(Node):
    def __init__(self, value, type_val):
        self.value = value
        self.type_val = type_val
        
    def __repr__(self):
        return str(self.value)

class Identifier(Node):
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f"ID({self.name})"