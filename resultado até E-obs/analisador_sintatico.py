# analisador_sintatico.py
import ply.yacc as yacc
from analisador_lexico import tokens
from gramatica import Identifier, IfExpr, LetVarDecl, FunSignature, FunDef, FunCall, BinOp, Literal, UnaryOp 
from gramatica import UnaryOp, Literal, Identifier, IfExpr, WhenExpr, Case, DefaultPattern

precedence = (
    ('left', 'EQ', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES'),
    ('right', 'UMINUS'),
)

def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# Instrução: Expressão solta
def p_statement_expr(p):
    '''statement : expression SEMI'''
    p[0] = p[1]

# Instrução: Declaração de Variável (let x : Int = 10;)
def p_statement_let_var(p):
    '''statement : LET ID COLON type ASSIGN expression SEMI'''
    p[0] = LetVarDecl(p[2], p[4], p[6])

# Instrução: Assinatura de Função (fun inc : Int -> Int;)
def p_statement_fun_sig(p):
    '''statement : FUN ID COLON type ARROW type SEMI'''
    p[0] = FunSignature(p[2], p[4], p[6])

# Instrução: Definição de Função (let inc x = x + 1;)
def p_statement_fun_def(p):
    '''statement : LET ID ID ASSIGN expression SEMI'''
    p[0] = FunDef(p[2], p[3], p[5])

def p_type(p):
    '''type : TYPE_INT
            | TYPE_BOOL'''
    p[0] = p[1]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression LT expression
                  | expression GT expression
                  | expression EQ expression'''
    p[0] = BinOp(p[2], p[1], p[3])
    
def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = UnaryOp('-', p[2])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

# Expressão: Chamada de Função (inc(5))
def p_expression_funcall(p):
    '''expression : ID LPAREN expression RPAREN'''
    p[0] = FunCall(p[1], p[3])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = Literal(p[1], 'Int')

def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = Literal(p[1] == 'true', 'Bool')

def p_expression_id(p):
    '''expression : ID'''
    p[0] = Identifier(p[1])

def p_expression_if(p):
    '''expression : IF expression THEN expression ELSE expression'''
    p[0] = IfExpr(p[2], p[4], p[6])
    
def p_expression_when(p):
    '''expression : WHEN expression IS cases END'''
    p[0] = WhenExpr(p[2], p[4])

def p_cases(p):
    '''cases : case
             | cases case'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_case(p):
    '''case : patterns ARROW expression SEMI'''
    p[0] = Case(p[1], p[3])

def p_patterns(p):
    '''patterns : pattern
                | patterns COMMA pattern'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_pattern(p):
    '''pattern : expression
               | UNDERSCORE'''
    if p[1] == '_':
        p[0] = DefaultPattern()
    else:
        p[0] = p[1]
    
def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo ao token '{p.value}' (linha {p.lineno})")
    else:
        print("Erro de sintaxe: Fim de ficheiro inesperado")

parser = yacc.yacc()

# ==========================================
# Execução e Teste com o novo cenário
# ==========================================
if __name__ == "__main__":
    codigo_teste = """
    fun inc : Int -> Int;
    let inc x = x + 1;
    inc(5);
    
    fun dobro : Int -> Int;
    let dobro n = n * 2;
    dobro(7);
    
    fun ePositivo : Int -> Bool;
    let ePositivo n = n > 0;
    ePositivo(-2);
    
    fun absoluto : Int -> Int;
    let absoluto n = if n < 0 then 0 - n else n;
    
    absoluto(-5);
    absoluto(8);    
    
    fun avalia : Int -> Bool;
    let avalia x = 
        when ( x ) is
            -1,
            1  -> true ;
            0  -> false ;
            _  -> true ;
        end;
        
    avalia(-1);
    avalia(0);
    
    """
    
    print("A analisar o seguinte código LFun com funções:\n" + codigo_teste)
    
    resultado_ast = parser.parse(codigo_teste)
    
    print("\nÁrvore Sintática gerada (AST):")
    if resultado_ast:
        for stmt in resultado_ast:
            print(stmt)