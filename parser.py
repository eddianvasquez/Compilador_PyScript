import ply.yacc as yacc
from lexer import tokens
import lexer # Importamos el lexer para reiniciar el contador de líneas

# --- MEMORIA Y ESTADO ---
variables = {}
salida_consola = []
mensajes_error = []
hubo_error = False

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# --- REGLAS SINTÁCTICAS ---
def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statement_pyscript(p):
    '''statement : PYSCRIPT_OPEN statements PYSCRIPT_CLOSE'''
    p[0] = p[2]

def p_statement_assign(p):
    '''statement : ID EQUALS expression'''
    if not hubo_error:
        variables[p[1]] = p[3]

def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN'''
    if not hubo_error:
        salida_consola.append(str(p[3]))

# --- REGLAS MATEMÁTICAS Y SEMÁNTICAS ---
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    global hubo_error
    if p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            hubo_error = True
            linea = p.lineno(2) # Obtenemos la línea del signo de división
            mensajes_error.append(f"Error Semantico: Division por cero en la linea {linea}")
            p[0] = 0
        else:
            p[0] = p[1] / p[3]

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = p[1].strip('"\'')

def p_expression_id(p):
    '''expression : ID'''
    global hubo_error
    try:
        p[0] = variables[p[1]]
    except LookupError:
        hubo_error = True
        linea = p.lineno(1) # Obtenemos la línea de la variable
        mensajes_error.append(f"Error Semantico: Variable '{p[1]}' no definida en la linea {linea}")
        p[0] = 0

# --- MANEJO DE ERRORES SINTÁCTICOS ---
def p_error(p):
    global hubo_error
    hubo_error = True
    if p:
        mensajes_error.append(f"Error de Sintaxis: Simbolo inesperado '{p.value}' en la linea {p.lineno}")
    else:
        mensajes_error.append("Error de Sintaxis: Codigo incompleto o mal cerrado al final del archivo")

parser_engine = yacc.yacc()

# --- FUNCIÓN PRINCIPAL EXPORTADA A APP.PY ---
def compilar_codigo(codigo):
    global salida_consola, variables, hubo_error, mensajes_error
    
    # Limpiamos la memoria
    salida_consola = []
    mensajes_error = []
    variables.clear()  
    hubo_error = False
    
    # Reiniciamos el contador de líneas a 1 antes de cada ejecución
    lexer.lexer.lineno = 1 
    
    parser_engine.parse(codigo)
    
    if hubo_error:
        return "\n".join(mensajes_error)
        
    return "\n".join(salida_consola)