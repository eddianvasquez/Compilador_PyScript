import ply.lex as lex

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
    'ID', 'NUMBER', 'FLOAT', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'POWER',
    'PLUSEQUALS', 'MINUSEQUALS', 
    'EQEQ', 'GT', 'LT', 'NEQ', 'EQUALS',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 
    'COLON', 'COMMA'
] + list(reserved.values())

t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_MODULO      = r'%'
t_POWER       = r'\*\*'

t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACKET    = r'\['
t_RBRACKET    = r'\]'
t_EQUALS      = r'='
t_COLON       = r':'
t_COMMA       = r','

t_EQEQ        = r'=='
t_GT          = r'>'
t_LT          = r'<'
t_NEQ         = r'!='

t_PLUSEQUALS  = r'\+=' 
t_MINUSEQUALS = r'-='  

t_ignore  = ' \t'

def t_ignore_COMMENT(t):
    r'\#.*'
    pass

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

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input_str, token):
    line_start = input_str.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_error(t):
    columna = find_column(t.lexer.lexdata, t)
    print(f"Error léxico: Símbolo no reconocido '{t.value[0]}' en la Línea {t.lineno}, Columna {columna}")
    t.lexer.skip(1)

lexer = lex.lex()