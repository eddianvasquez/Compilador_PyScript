import ply.lex as lex

# Requerimiento 5: Palabras reservadas
# Aquí definimos las palabras clave de "PyScript"
reserved = {
    'si': 'IF',          # Para cumplir con el requerimiento 7: Selectiva
    'sino': 'ELSE',
    'imprimir': 'PRINT',
    'mientras': 'WHILE'
}

# Lista de todos los tokens (símbolos que el compilador entiende)
tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'LPAREN', 'RPAREN', 'EQUALS'
] + list(reserved.values())

# Reglas simples para símbolos matemáticos y de agrupación
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUALS  = r'='

# Caracteres a ignorar (espacios y tabulaciones)
t_ignore  = ' \t'

# Regla para detectar variables (ID) o palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Revisa si la palabra está en las reservadas
    return t

# Regla para detectar números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Manejo de errores si el usuario escribe algo raro
def t_error(t):
    print(f"Error léxico: Carácter no válido '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# --- Modo Interactivo (Requerimiento 6) ---
if __name__ == '__main__':
    print("Simulador PyScript - Analizador Léxico")
    print("Escribe 'salir' para terminar.")
    while True:
        try:
            texto = input('PyScript > ')
        except EOFError:
            break
        if texto.lower() == 'salir':
            break
        
        lexer.input(texto)
        for tok in lexer:
            print(tok)