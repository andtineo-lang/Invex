from flask import Flask, request, jsonify
from flask_cors import CORS
# Importaciones para la versión más reciente del SDK de Transbank
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_type import IntegrationType

# --- Configuración Inicial ---
app = Flask(__name__)
CORS(app)


# --- Ruta para Crear la Transacción ---
@app.route('/api/create-transaction', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()
        buy_order = data.get('buy_order')
        session_id = data.get('session_id')
        amount = data.get('amount')
        return_url = 'http://localhost:8080/pago/confirmacion' 

        if not all([buy_order, session_id, amount]):
            return jsonify({"error": "Faltan datos para crear la transacción"}), 400

        # Configura y crea la transacción en el ambiente de pruebas
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        response = tx.create(buy_order, session_id, amount, return_url)

        if response.get('url') and response.get('token'):
            return jsonify({
                "url_redirect": f"{response['url']}?token_ws={response['token']}"
            })
        else:
            raise Exception("La respuesta de Transbank no fue exitosa.")

    except Exception as e:
        print(f"Error al crear la transacción: {e}")
        return jsonify({"error": str(e)}), 500


# --- Ruta para Confirmar la Transacción ---
@app.route('/api/confirm-transaction', methods=['POST'])
def confirm_transaction():
    try:
        data = request.get_json()
        token = data.get('token')

        if not token:
            return jsonify({"error": "No se recibió el token"}), 400

        # Configura y confirma la transacción en el ambiente de pruebas
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        response = tx.commit(token)

        return jsonify(response)

    except Exception as e:
        print(f"Error al confirmar la transacción: {e}")
        return jsonify({"error": str(e)}), 500

# --- Ruta para el Login (Simulado) ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    password = data.get('password')

    if password == "Invex2025*":
        return jsonify({
            "message": "Inicio de sesión exitoso",
            "token": "fake-jwt-token-for-user",
            "redirect_url": "/inventario"
        }), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401


# --- Iniciar el Servidor ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)

