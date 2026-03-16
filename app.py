from flask import Flask, render_template, request, jsonify
import lexer  # <-- ¡Aquí conectamos tu analizador léxico!

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compilar', methods=['POST'])
def compilar():
    datos = request.json
    codigo_usuario = datos.get('codigo', '')
    
    # 1. Le metemos el texto de la página web a tu analizador léxico
    lexer.lexer.input(codigo_usuario)
    
    # 2. Creamos un texto para ir guardando los resultados
    resultado_consola = "--- RESULTADO DEL ANÁLISIS LÉXICO ---\n\n"
    
    # 3. Recorremos cada token que tu lexer haya encontrado y lo formateamos
    hay_tokens = False
    for tok in lexer.lexer:
        hay_tokens = True
        resultado_consola += f"➤ Token: {tok.type:<15} | Valor: {tok.value}\n"
        
    if not hay_tokens:
        resultado_consola += "No se detectó ningún código válido."
        
    # 4. Devolvemos el resultado a la consola negra de tu página web
    return jsonify({'resultado': resultado_consola})

if __name__ == '__main__':
    app.run(debug=True)