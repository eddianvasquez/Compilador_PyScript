import ply.yacc as yacc
from lexer import tokens # Importamos los tokens que ya definiste

# --- ANÁLISIS SEMÁNTICO: Memoria ---
# Diccionario para guardar nuestras variables (ej: x = 10)
variables = {}
# Lista para guardar lo que hace la función 'print' y enviarlo a la web
salida_consola = []

# Reglas de precedencia matemática (multiplicación y división van antes que suma y resta)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# --- ANÁLISIS SINTÁCTICO: Reglas Gramaticales ---
# Regla principal: Un programa puede tener una o varias instrucciones
def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

# Permitir que el código esté envuelto en las etiquetas de tu lexer
def p_statement_pyscript(p):
    '''statement : PYSCRIPT_OPEN statements PYSCRIPT_CLOSE'''
    p[0] = p[2]

# Regla: Asignación de variables (ej: variable = numero + numero)
def p_statement_assign(p):
    '''statement : ID EQUALS expression'''
    variables[p[1]] = p[3]  # Lógica Semántica: Guardar el valor en el diccionario
    p[0] = f"Asignación: {p[1]} = {p[3]}"

# Regla: Función Print (ej: print(variable))
def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN'''
    salida_consola.append(str(p[3])) # Lógica Semántica: Guardar resultado para la web
    p[0] = p[3]

# Regla: Expresiones matemáticas
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    # Lógica Semántica: Ejecutar la matemática real
    if p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            salida_consola.append("Error Semántico: División por cero")
            p[0] = 0
        else:
            p[0] = p[1] / p[3]

# Agrupación con paréntesis
def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

# Tipos de datos base
def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = p[1].strip('"\'') # Quitar comillas del texto

# Obtener el valor de una variable guardada
def p_expression_id(p):
    '''expression : ID'''
    try:
        p[0] = variables[p[1]] # Buscar la variable en memoria
    except LookupError:
        salida_consola.append(f"Error Semántico: Variable '{p[1]}' no definida")
        p[0] = 0

# Manejo de errores de sintaxis
def p_error(p):
    if p:
        salida_consola.append(f"Error de Sintaxis cerca de '{p.value}'")
    else:
        salida_consola.append("Error de Sintaxis al final del código")

# Construir el parser
parser_engine = yacc.yacc()

# Función para ejecutar el parser desde app.py
def compilar_codigo(codigo):
    global salida_consola
    salida_consola = []  # Limpiamos la consola antes de cada ejecución
    parser_engine.parse(codigo)
    return "\n".join(salida_consola)