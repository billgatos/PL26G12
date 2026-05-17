# analisador_semantico.py
from gramatica import *
from avaliador import avaliar

# Tabela global que guarda o estado do programa (variáveis, funções e os seus tipos)
tabela = {}

def processar(no):
    """
    Função principal do Analisador Semântico.
    O seu papel é intercetar Declarações (gerir a tabela de símbolos) 
    e enviar Expressões puras para o Avaliador.
    """

    # 1. EXPRESSÃO SOLTA (ex: 3 + 4; ou inc(5);)
    # Se o utilizador apenas digitou uma expressão matemática/lógica/chamada,
    # nós delegamos diretamente para o avaliador e mostramos o resultado.
    if isinstance(no, (Literal, BinOp, UnaryOp, FunCall, IfExpr, WhenExpr, Identifier, ConsExpr, EmptyList)):
        val, tipo = avaliar(no, tabela)
        
        if val is not None:
            # Formatação simpática para booleanos ficarem parecidos com a linguagem alvo
            val_str = str(val).lower() if tipo == 'Bool' else str(val)
            print(f"resultado: {val_str}  tipo: {tipo}")


    # 2. DECLARAÇÃO DE VARIÁVEL (ex: let x : Int = 10;)
    elif isinstance(no, LetVarDecl):
        # Proteção contra reatribuição de variáveis
        if no.id_name in tabela:
            print(f"ERRO SEMÂNTICO: O identificador '{no.id_name}' já foi definido e não pode ser reatribuído.")
            return

        # Avaliamos o lado direito (a expressão)
        val, tipo_real = avaliar(no.expr, tabela)
        tipo_declarado = str(no.var_type)
        
        if val is None:
            return # Erro propagado pelo avaliador
        
        # Verificação de Tipagem (Type Checking)
        if tipo_real != tipo_declarado:
            print(f"ERRO SEMÂNTICO: '{no.id_name}' declarado como {tipo_declarado} mas expressão avaliada resultou num tipo {tipo_real}")
            return
        
        # Guardar na tabela com sucesso
        tabela[no.id_name] = {'valor': val, 'tipo': tipo_real}
        
        # Imprimir feedback no terminal
        val_str = str(val).lower() if tipo_real == 'Bool' else str(val)
        print(f"-- Variável '{no.id_name}' guardada: tipo {tipo_real}, valor: {val_str}")


    # 3. ASSINATURA DE FUNÇÃO (ex: fun inc : Int -> Int;)
    elif isinstance(no, FunSignature):
        # Proteção contra reatribuição de assinatura
        if no.id_name in tabela:
            print(f"ERRO SEMÂNTICO: A assinatura de '{no.id_name}' já foi definida.")
            return
            
        # Cria a "carcaça" da função. O corpo será preenchido pelo FunDef
        tabela[no.id_name] = {
            'tipo':     f"{no.arg_type}->{no.return_type}",
            'arg_tipo': no.arg_type,
            'ret_tipo': no.return_type,
            'arg':      None,  # Nome do parâmetro (ainda desconhecido)
            'corpo':    None   # AST do corpo (ainda desconhecido)
        }


    # 4. DEFINIÇÃO DE FUNÇÃO (ex: let inc x = x + 1;)
    elif isinstance(no, FunDef):
        # A função obrigatoriamente tem de ter uma assinatura declarada antes
        if no.id_name not in tabela:
            print(f"ERRO SEMÂNTICO: Função '{no.id_name}' definida sem assinatura prévia 'fun'.")
            return
            
        # Verificação de Imutabilidade - Não aceita duas definições para a mesma função
        if tabela[no.id_name]['corpo'] is not None:
            print(f"ERRO SEMÂNTICO: A função '{no.id_name}' já possui um corpo definido e não pode ser reatribuída.")
            return

        # Atualiza a "base/corpo" existente com os dados lógicos
        tabela[no.id_name]['arg']   = no.arg_name
        tabela[no.id_name]['corpo'] = no.expr
        
        print(f"-- Função '{no.id_name}' definida com sucesso.")


    # 5. COMENTÁRIOS
    elif isinstance(no, Comentario):
        # Imprime o comentário em negrito para destacar, mas não faz mais nada]")
        print(f"\n\033[1m** {no.texto} **\033[0m") 
        
        # pass # Não fazemos nada, o objetivo do comentário é ser ignorado

    else:
        print(f"ERRO: Nó de declaração desconhecido pelo Analisador Semântico: {type(no)}")