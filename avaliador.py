# avaliador.py
from gramatica import *

def avaliar(no, tabela):
    """
    Motor de execução do programa.
    Recebe um nó de Expressão da AST e a tabela de símbolos atual,
    e devolve um tuplo: (valor_calculado, tipo_do_valor)
    """
    
    # 1. VALORES DIRETOS E VARIÁVEIS
    
    # # Número ou booleano literal: devolve o valor diretamente
    if isinstance(no, Literal):
        return no.value, no.type_val
    
    # Identificador: vai buscar à tabela de símbolos
    if isinstance(no, Identifier):
        if no.name not in tabela:
            print(f"ERRO: '{no.name}' não foi definido")
            return None, None
        entrada = tabela[no.name]
        return entrada['valor'], entrada['tipo']
    
    # 2. EXPRESSÕES MATEMÁTICAS E LÓGICAS

    # Menos unário: ex: -5
    if isinstance(no, UnaryOp):
        val, tipo = avaliar(no.expr, tabela)
        if val is None: return None, None
        return -val, tipo

    # Operações binárias: +, -, *, <, >, ==
    if isinstance(no, BinOp):
        esq_val, esq_tipo = avaliar(no.left, tabela)
        dir_val, dir_tipo = avaliar(no.right, tabela)
        if esq_val is None or dir_val is None: return None, None
        if no.op == '+':  return esq_val + dir_val, 'Int'
        if no.op == '-':  return esq_val - dir_val, 'Int'
        if no.op == '*':  return esq_val * dir_val, 'Int'
        if no.op == '/':  
            if dir_val == 0:
                print("ERRO DE EXECUÇÃO: Divisão por zero")
                return None, None    
            return esq_val // dir_val, 'Int'  # divisão inteira
        
        if no.op == '<':  return esq_val < dir_val,  'Bool'
        if no.op == '>':  return esq_val > dir_val,  'Bool'
        if no.op == '==': return esq_val == dir_val, 'Bool'
    
    
    # 3. CONTROLO DE FLUXO E CHAMADAS DE FUNÇÃO
    # if condição then exp1 else exp2
    
    if isinstance(no, IfExpr):
        cond, _ = avaliar(no.cond, tabela)
        if cond:
            return avaliar(no.then_expr, tabela)
        else:
            return avaliar(no.else_expr, tabela)
        
    # chamada de função: inc(5)
    
    if isinstance(no, FunCall):
        if no.id_name not in tabela:
            print(f"ERRO: função '{no.id_name}' não definida")
            return None, None
        fun = tabela[no.id_name]
        
        if fun['corpo'] is None:
            print(f"ERRO DE EXECUÇÃO: A função '{no.id_name}' tem assinatura, mas não tem corpo definido.")
            return None, None
        
        # Avaliamos o argumento que está a ser passado para a função
        arg_val, arg_tipo = avaliar(no.arg_expr, tabela)
        
        # SCOPE (Escopo): Criamos uma cópia da tabela atual para injetar o parâmetro.
        # Assim, o parâmetro "x" só existe dentro da execução desta função.
        # cria tabela local com o argumento da função
        tabela_local = dict(tabela)
        tabela_local[fun['arg']] = {'valor': arg_val, 'tipo': fun['arg_tipo']}
        # Executamos o corpo da função usando a nova tabela
        return avaliar(fun['corpo'], tabela_local)
    
    # 4. TRATAMENTO DE LISTAS
    # --- Listas (Novos Nós) ---
    if isinstance(no, EmptyList):
        return [], 'List'

    if isinstance(no, ConsExpr):
        h_val, h_tipo = avaliar(no.head, tabela)
        t_val, t_tipo = avaliar(no.tail, tabela)
        
        if h_val is None or t_val is None: 
            return None, None
        
        # Retorna a lista Python e o tipo formatado como "[Tipo]"
        return [h_val] + t_val, f"[{h_tipo}]"

    # 5. PATTERN MATCHING (WHEN)

    # when (expr) is padrões -> resultado end
    if isinstance(no, WhenExpr):
        val_alvo, tipo_alvo = avaliar(no.cond_expr, tabela)
        if val_alvo is None: return None, None

        for case in no.cases:
            for padrao in case.patterns:
                
                # Caso por defeito _
                if isinstance(padrao, DefaultPattern):
                    return avaliar(case.result_expr, tabela)

                # Lista Vazia []
                elif isinstance(padrao, EmptyListPattern):
                    if isinstance(val_alvo, list) and len(val_alvo) == 0:
                        return avaliar(case.result_expr, tabela)

                # Cabeça e Cauda h:t
                elif isinstance(padrao, ConsPattern):
                    if isinstance(val_alvo, list) and len(val_alvo) > 0:
                        tabela_local = dict(tabela)
                        tabela_local[padrao.head_id] = {'valor': val_alvo[0], 'tipo': 'Int'} 
                        tabela_local[padrao.tail_id] = {'valor': val_alvo[1:], 'tipo': tipo_alvo}
                        return avaliar(case.result_expr, tabela_local)

                # Avaliar apenas se for um número ou booleano
                elif isinstance(padrao, (Literal, UnaryOp)):
                    p_val, _ = avaliar(padrao, tabela)
                    if p_val == val_alvo:
                        return avaliar(case.result_expr, tabela)

        print("ERRO: nenhum padrão do when fez match")
        return None, None

    
    # Fallback caso encontre algo inesperado
    print(f"ERRO INTERNO: Nó de expressão não suportado pelo Avaliador: {type(no)}")
    return None, None  