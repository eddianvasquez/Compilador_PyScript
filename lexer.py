import ply.lex as lex

# 1. Palabras reservadas de Python/PyScript
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT',
    'while': 'WHILE',
    'for': 'FOR',
    'def': 'DEF',
    'return': 'RETURN',
    'True': 'TRUE',
    'False': 'FALSE',
    'and': 'AND',
    'or': 'OR'
}

tokens = [
    'PYSCRIPT_OPEN', 'PYSCRIPT_CLOSE',

    'ID', 'NUMBER', 'STRING',
    
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    
    'LPAREN', 'RPAREN', 'EQUALS', 'COLON',
    
    'EQEQ', 'GT', 'LT', 'NEQ',
    
    'PLUSEQUALS', 'MINUSEQUALS' # <-- AÑADIDO: Formas cortas
] + list(reserved.values())

# 3. Reglas simples (Simbolos matematicos y operadores)
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUALS  = r'='
t_COLON   = r':'

t_EQEQ    = r'=='
t_GT      = r'>'
t_LT      = r'<'
t_NEQ     = r'!='

t_PLUSEQUALS  = r'\+=' # <-- AÑADIDO
t_MINUSEQUALS = r'-='  # <-- AÑADIDO


def t_PYSCRIPT_OPEN(t):
    r'<py-script>'
    return t

def t_PYSCRIPT_CLOSE(t):
    r'</py-script>'
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico: Símbolo no reconocido '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()