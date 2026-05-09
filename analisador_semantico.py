# analisador_semantico.py
from gramatica import *
from avaliador import avaliar


tabela = {}


def processar(no):


    # Expressão solta: ex: dobro(7); ou 3+4;
    if isinstance(no, (Literal, BinOp, UnaryOp, FunCall, IfExpr, WhenExpr, Identifier, ConsExpr, EmptyList)):
        val, tipo = avaliar(no, tabela)
        if val is not None:
            # booleanos: mostrar true/false em minúsculas
            val_str = str(val).lower() if tipo == 'Bool' else str(val)
            print(f"resultado: {val_str}  tipo: {tipo}")


    # let x : Int = 10;
    elif isinstance(no, LetVarDecl):
        val, tipo_real = avaliar(no.expr, tabela)
        
        tipo_declarado = str(no.var_type)
        
        if val is None:
            # O erro de 'nó desconhecido' no avaliador resulta em None aqui
            return
        
        if tipo_real != tipo_declarado:
            print(f"ERRO semântico: '{no.id_name}' declarado como {no.var_type} mas expressão é do tipo {tipo_real}")
            return
        
        tabela[no.id_name] = {'valor': val, 'tipo': tipo_real}
        val_str = str(val).lower() if tipo_real == 'Bool' else str(val)
        print(f"-- {no.id_name}: tipo {tipo_real}, valor: {val_str}")


    # fun inc : Int -> Int;
    elif isinstance(no, FunSignature):
        tabela[no.id_name] = {
            'tipo':     f"{no.arg_type}->{no.return_type}",
            'arg_tipo': no.arg_type,
            'ret_tipo': no.return_type,
            'arg':      None,
            'corpo':    None
        }


    # let inc x = x + 1;
    elif isinstance(no, FunDef):
        if no.id_name not in tabela:
            print(f"ERRO: função '{no.id_name}' usada sem assinatura 'fun'")
            return
        # Associar o nome do argumento e o corpo à assinatura existente
        tabela[no.id_name]['arg']   = no.arg_name
        tabela[no.id_name]['corpo'] = no.expr
        # --- Comentários ---
    elif isinstance(no, Comentario):
        pass 

    else:
        print(f"ERRO: nó de declaração desconhecido {type(no)}")