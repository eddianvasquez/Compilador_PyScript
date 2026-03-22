from flask import Flask, render_template, request, jsonify
import parser  # <-- ¡Aquí conectamos tu nuevo analizador sintáctico/semántico!

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compilar', methods=['POST'])
def compilar():
    datos = request.json
    codigo_usuario = datos.get('codigo', '')
    
    # Ejecutamos el parser (que usa automáticamente el lexer por detrás)
    salida_parser = parser.compilar_codigo(codigo_usuario)
    
    # Preparamos el texto a devolver a la consola web
    resultado_consola = "--- RESULTADO DE EJECUCIÓN ---\n\n"
    
    if salida_parser:
        resultado_consola += salida_parser
    else:
        # Si el usuario no usó "print" pero declaró variables, 
        # mostramos la memoria interna para comprobar que el Análisis Semántico funcionó.
        resultado_consola += "Ejecución finalizada sin errores.\n"
        resultado_consola += f"\n[Memoria interna de variables guardadas]:\n{parser.variables}"
        
    return jsonify({'resultado': resultado_consola})

if __name__ == '__main__':
    app.run(debug=True)