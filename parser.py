import ply.yacc as yacc
from lexer import tokens
import lexer 

# --- MEMORIA Y ESTADO ---
variables = {}
salida_consola = []
mensajes_error = []
hubo_error = False
ejecutar_bloque = True  # Interruptor maestro para el IF y el WHILE

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

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
    if not hubo_error and ejecutar_bloque:
        variables[p[1]] = p[3]

# --- NUEVO: ASIGNACIONES CORTAS (Req. 5) ---
def p_statement_assign_short(p):
    '''statement : ID PLUSEQUALS expression
                 | ID MINUSEQUALS expression'''
    global hubo_error
    if not hubo_error and ejecutar_bloque:
        # Verificamos que la variable exista antes de sumarle o restarle
        try:
            if p[2] == '+=':
                variables[p[1]] += p[3]
            elif p[2] == '-=':
                variables[p[1]] -= p[3]
        except KeyError:
            hubo_error = True
            linea = p.lineno(1)
            mensajes_error.append(f"Error Semantico: La variable '{p[1]}' debe existir antes de usar {p[2]} en la linea {linea}")

def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN'''
    if not hubo_error and ejecutar_bloque:
        salida_consola.append(str(p[3]))

# --- ESTRUCTURA SELECTIVA (IF) ---
def p_statement_if(p):
    '''statement : IF expression COLON validacion_if statement'''
    global ejecutar_bloque
    ejecutar_bloque = True 

def p_validacion_if(p):
    '''validacion_if : '''
    global ejecutar_bloque
    if p[-2] == True:
        ejecutar_bloque = True  
    else:
        ejecutar_bloque = False 

# --- NUEVO: ESTRUCTURA REPETITIVA (WHILE) (Req. 3) ---
def p_statement_while(p):
    '''statement : WHILE expression COLON validacion_while statement'''
    global ejecutar_bloque
    # Al igual que en el IF, al terminar la regla devolvemos el interruptor a la normalidad
    ejecutar_bloque = True

def p_validacion_while(p):
    '''validacion_while : '''
    global ejecutar_bloque
    # Validamos si la condición del WHILE es verdadera
    if p[-2] == True:
        ejecutar_bloque = True
    else:
        ejecutar_bloque = False

# --- REGLAS RELACIONALES (LÓGICA) ---
def p_expression_relational(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression EQEQ expression
                  | expression NEQ expression'''
    global hubo_error
    if p[2] == '>': p[0] = p[1] > p[3]
    elif p[2] == '<': p[0] = p[1] < p[3]
    elif p[2] == '==': p[0] = p[1] == p[3]
    elif p[2] == '!=': p[0] = p[1] != p[3]

# --- REGLAS MATEMATICAS Y SEMANTICAS ---
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
            linea = p.lineno(2) 
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
        linea = p.lineno(1) 
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
    global salida_consola, variables, hubo_error, mensajes_error, ejecutar_bloque
    
    salida_consola = []
    mensajes_error = []
    variables.clear()  
    hubo_error = False
    ejecutar_bloque = True 
    
    lexer.lexer.lineno = 1 
    
    parser_engine.parse(codigo)
    
    if hubo_error:
        return "\n".join(mensajes_error)
        
    return "\n".join(salida_consola)