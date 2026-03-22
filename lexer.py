import ply.lex as lex

# 1. Palabras reservadas reales de Python/PyScript
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

# 2. Lista completa de tokens que tu compañero usará en el Parser
tokens = [
    # Etiquetas web
    'PYSCRIPT_OPEN', 'PYSCRIPT_CLOSE',
    
    # Datos y variables
    'ID', 'NUMBER', 'STRING',
    
    # Matemáticas
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    
    # Agrupación y asignación
    'LPAREN', 'RPAREN', 'EQUALS', 'COLON',
    
    # Comparaciones lógicas
    'EQEQ', 'GT', 'LT', 'NEQ'
] + list(reserved.values())

# 3. Reglas simples (Símbolos matemáticos y operadores)
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

# 4. Reglas para detectar las etiquetas de PyScript
def t_PYSCRIPT_OPEN(t):
    r'<py-script>'
    return t

def t_PYSCRIPT_CLOSE(t):
    r'</py-script>'
    return t

# 5. Regla para detectar texto entre comillas (strings)
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    return t

# 6. Regla para detectar variables (ID) o palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Revisa si la palabra está en las reservadas
    return t

# 7. Regla para detectar números (enteros)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# NUEVO: Regla para contar los saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 9. Manejo de errores si escriben símbolos raros
def t_error(t):
    print(f"Error léxico: Símbolo no reconocido '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer (El motor que exportamos a app.py)
lexer = lex.lex()