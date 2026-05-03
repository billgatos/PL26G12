# analisador_sintatico.py
import ply.yacc as yacc
import sys
from analisador_lexico import tokens
from gramatica import Identifier, IfExpr, LetVarDecl, FunSignature, FunDef, FunCall, BinOp, UnaryOp 
from gramatica import Literal, Identifier, IfExpr, WhenExpr, Case, DefaultPattern 
from gramatica import ListType, EmptyList, ConsExpr, EmptyListPattern, ConsPattern

precedence = (
    ('left', 'EQ', 'LT', 'GT'),
    ('right', 'COLON'),
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

# ira contemplar as listas mais tarde, por agora so o que ja tinhamos
def p_type(p):
    '''type : TYPE_INT
            | TYPE_BOOL
            | LBRACK type RBRACK''' # exemplo [Tipo] para listas
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ListType(p[2])

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
    
def p_expression_list_empty(p):
    '''expression : LBRACK RBRACK'''
    p[0] = EmptyList()

# testar bem as listas depois, por agora so o que ja tinhamos
def p_expression_list_cons(p):
    #'''expression : expression COLON expression'''
    #p[0] = ConsExpr(p[1], p[3])
    '''expression : LBRACK expression COMMA expression RBRACK'''
    p[0] = ConsExpr(p[2], p[4])

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

# def p_pattern(p):
#     '''pattern : expression
#                | UNDERSCORE
#                | LBRACK RBRACK
#                | ID COLON ID'''
#     # if p[1] == '_':
#     #     p[0] = DefaultPattern()
#     # else:
#     #     p[0] = p[1]
#     if len(p) == 2:
#         if p[1] == '_':
#             p[0] = DefaultPattern()
#         else:
#             p[0] = p[1]
#     elif len(p) == 3:
#         p[0] = EmptyListPattern()
#     elif len(p) == 4:
#         p[0] = ConsPattern(p[1], p[3])
# também não funciona

# def p_pattern(p):
#     '''pattern : expression
#                | UNDERSCORE'''
#     if p[1] == '_':
#         p[0] = DefaultPattern()
#     else:
#         # Depois de ler como uma expressão genérica, transformamos no nó de Padrão correto
#         if isinstance(p[1], EmptyList):
#             p[0] = EmptyListPattern()
#         elif isinstance(p[1], ConsExpr):
#             # Assumimos que o ConsExpr apanhou dois Identificadores (h e t)
#             p[0] = ConsPattern(p[1].head, p[1].tail)
#         else:
#             p[0] = p[1]


# ==========================================
# REGRAS DE PADRÕES (PATTERNS) PARA O WHEN
# ==========================================

# Padrão: Números inteiros (ex: 1, 0)
def p_pattern_literal(p):
    '''pattern : NUMBER'''
    p[0] = Literal(p[1], 'Int')

# Padrão: Números negativos (ex: -1)
def p_pattern_negative(p):
    '''pattern : MINUS NUMBER'''
    p[0] = UnaryOp('-', Literal(p[2], 'Int'))

# Padrão: Booleanos (ex: true, false)
def p_pattern_bool(p):
    '''pattern : TRUE
               | FALSE'''
    p[0] = Literal(p[1] == 'true', 'Bool')

# Padrão: O caso por defeito ( _ )
def p_pattern_underscore(p):
    '''pattern : UNDERSCORE'''
    p[0] = DefaultPattern()

# Padrão: Lista vazia ( [] )
def p_pattern_empty_list(p):
    '''pattern : LBRACK RBRACK'''
    p[0] = EmptyListPattern()

# Padrão: Cabeça e Cauda de uma lista ( h:t )
def p_pattern_cons(p):
    '''pattern : ID COLON ID'''
    p[0] = ConsPattern(p[1], p[3])


# Expressão: Lista vazia
def p_expression_list_empty(p):
    '''expression : LBRACK RBRACK'''
    p[0] = EmptyList()

# Expressão: Construção de lista (h:t)
def p_expression_list_cons(p):
    '''expression : expression COLON expression'''
    p[0] = ConsExpr(p[1], p[3])
    
# Fim das regras de padrões    
    
def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo ao token '{p.value}' (linha {p.lineno})")
    else:
        print("Erro de sintaxe: Fim de ficheiro inesperado")

parser = yacc.yacc()

## Menu anterior para testes rápidos, mas agora existe 
## um menu interativo mais completo

            # # ==========================================
            # # Execução e Teste com o novo cenário
            # # ==========================================
            # if __name__ == "__main__":
            #     codigo_teste = """
            #     fun inc : Int -> Int;
            #     let inc x = x + 1;
            #     inc(5);
                
            #     fun dobro : Int -> Int;
            #     let dobro n = n * 2;
            #     dobro(7);
                
            #     fun ePositivo : Int -> Bool;
            #     let ePositivo n = n > 0;
            #     ePositivo(-2);
                
            #     fun absoluto : Int -> Int;
            #     let absoluto n = if n < 0 then 0 - n else n;
                
            #     absoluto(-5);
            #     absoluto(8);    
                
            #     fun avalia : Int -> Bool;
            #     let avalia x = 
            #         when ( x ) is
            #             -1,
            #             1  -> true ;
            #             0  -> false ;
            #             _  -> true ;
            #         end;
                    
            #     avalia(-1);
            #     avalia(0);
                
            #     {- Função que calcula o tamanho de uma lista usando recursividade e pattern matching -}
            #     fun tamanho : [Int] -> Int;
            #     let tamanho lista = 
            #         when ( lista ) is
            #             []   -> 0 ;
            #             h:t  -> 1 + tamanho(t) ;
            #         end;
                    
            #     -- Criando e testando a lista [10, 20, 30]
            #     let osMeusNumeros : [Int] = 10 : 20 : 30 : [];
                
            #     tamanho(osMeusNumeros);
            #     """
                
            #     print("A analisar o seguinte código LFun com funções:\n" + codigo_teste)
                
            #     resultado_ast = parser.parse(codigo_teste)
                
            #     print("\nÁrvore Sintática gerada (AST):")
            #     if resultado_ast:
            #         for stmt in resultado_ast:
            #             print(stmt)
                        
            
            
## novo formato de main
## Pede ao utilizdor a escolha de entre 3 opções
## Carregar código de um ficheiro, introduzir código diretamente na consola ou executar um exemplo embutido


# ==========================================
# Execução e Interface com o Utilizador
# ==========================================

def processar_codigo(codigo, fonte):
    """Função auxiliar para fazer o parse e imprimir a AST de forma limpa."""
    print(f"\n{'-'*50}")
    print(f"--- A analisar código ({fonte}) ---")
    print(f"{'-'*50}")
    
    if not codigo.strip():
        print("Erro: Nenhum código fornecido.")
        return
        
    resultado_ast = parser.parse(codigo)
    
    print("\nÁrvore Sintática gerada (AST):")
    if resultado_ast:
        for stmt in resultado_ast:
            print(stmt)
    else:
        print("A AST está vazia ou ocorreu um erro de sintaxe impeditivo.")
    print(f"{'-'*50}\n")


if __name__ == "__main__":
    codigo_exemplo = """
    
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

    {- Função que calcula o tamanho de uma lista usando recursividade e pattern matching -}
    fun tamanho : [Int] -> Int;
    let tamanho lista = 
    when ( lista ) is
        []   -> 0 ;
        h:t  -> 1 + tamanho(t) ;
    end;

    {- Exemplo Completo: Recursividade e Listas -}
    fun tamanho : [Int] -> Int;
    let tamanho lista = 
        when ( lista ) is
            []   -> 0 ;
            h:t  -> 1 + tamanho(t) ;
        end;
        
    let osMeusNumeros : [Int] = 10 : 20 : 30 : [];
    tamanho(osMeusNumeros);
    """

    while True:
        print("\n" + "="*30)
        print("   ANALISADOR SINTÁTICO LFun")
        print("="*30)
        print("1. Carregar de um ficheiro (.lfun)")
        print("2. Introduzir código na consola")
        print("3. Executar o exemplo embutido")
        print("0. Sair")
        print("="*30)
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            caminho = input("Introduza o caminho do ficheiro (ex: teste.lfun): ")
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    codigo = f.read()
                processar_codigo(codigo, caminho)
            except FileNotFoundError:
                print(f"\n[ERRO] O ficheiro '{caminho}' não foi encontrado.")
            except Exception as e:
                print(f"\n[ERRO] Ocorreu um problema ao ler o ficheiro: {e}")
                
        elif escolha == '2':
            print("\nIntroduza o seu código LFun abaixo.")
            print("(Pressione Ctrl+D no Linux/Mac ou Ctrl+Z seguido de Enter no Windows numa linha vazia para submeter)")
            print("-" * 40)
            try:
                codigo = sys.stdin.read()
                processar_codigo(codigo, "Consola")
            except KeyboardInterrupt:
                print("\nOperação cancelada.")
                
        elif escolha == '3':
            processar_codigo(codigo_exemplo, "Exemplo Embutido")
            
        elif escolha == '0':
            print("\nA encerrar o analisador. Bom trabalho com o projeto!")
            break
            
        else:
            print("\n[ERRO] Opção inválida. Por favor, escolha 0, 1, 2 ou 3.")