# analisador_lexico.py
import ply.lex as lex

# Palavras reservadas
reserved = {
    'let': 'LET',
    'fun': 'FUN',
    'Int': 'TYPE_INT',
    'Bool': 'TYPE_BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',       # <-- Adicionado
    'then': 'THEN',   # <-- Adicionado
    'else': 'ELSE',    # <-- Adicionado
    'when': 'WHEN', 
    'is': 'IS', 
    'end': 'END' # <-- Adicionado
}

# Lista de Tokens
tokens = [
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES',
    'LT', 'GT', 'EQ', 'ARROW',
    'ASSIGN', 'COLON', 'SEMI',
    'LPAREN', 'RPAREN',
    'COMMA', 'UNDERSCORE',  # <-- Adicionado
    'LBRACK', 'RBRACK',      # <-- Adicionado para listas
    'COMMENT' # para uso nos comentários de linha
] + list(reserved.values())

# Expressões Regulares
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_LT      = r'<'
t_GT      = r'>'
t_EQ      = r'=='
t_ARROW   = r'->'
t_ASSIGN  = r'='
t_COLON   = r':'
t_SEMI    = r';'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA   = r','
t_UNDERSCORE = r'_'
t_LBRACK = r'\['
t_RBRACK = r'\]'

t_ignore  = ' \t'

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# comentários em bloco {- ... -} e linha -- ...
def t_COMMENT_MULTI(t):
    r'\{-(.|\n)*?-\}'
    t.lexer.lineno += t.value.count('\n')
    t.type = 'COMMENT'
    return t

#comentários simples
def t_COMMENT_SINGLE(t):
    r'--.*'
    t.type = 'COMMENT'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caráter ilegal encontrado: '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# Teste simples
if __name__ == "__main__":
    data = "fun inc : Int -> Int; let inc x = x + 1;"    
    lexer.input(data)
    for tok in lexer:
        print(tok)