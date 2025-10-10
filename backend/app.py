from flask import Flask, request, jsonify
from flask_cors import CORS
# Importaciones corregidas para la versión más reciente del SDK
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
# Se añade la importación para el tipo de integración
from transbank.common.integration_type import IntegrationType

# --- Configuración Inicial ---
# 1. Crea la aplicación Flask
app = Flask(__name__)
# 2. Habilita CORS para permitir que tu frontend se comunique con este backend
CORS(app)


# --- Ruta para Crear la Transacción en Transbank ---
@app.route('/api/create-transaction', methods=['POST'])
def create_transaction():
    try:
        # Obtiene los datos enviados desde el frontend (Vue)
        data = request.get_json()
        buy_order = data.get('buy_order')
        session_id = data.get('session_id')
        amount = data.get('amount')
        # La URL a la que Transbank redirigirá al usuario después del pago
        return_url = 'http://localhost:8080/pago/confirmacion' 

        if not all([buy_order, session_id, amount, return_url]):
            return jsonify({"error": "Faltan datos para crear la transacción"}), 400

        # Crea la transacción, pasando las opciones de integración incluyendo el tipo TEST
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        response = tx.create(buy_order, session_id, amount, return_url)

        # Si la respuesta de Transbank tiene la URL y el Token, todo está bien
        if response.get('url') and response.get('token'):
            # Devuelve la respuesta al frontend
            return jsonify({
                "url_redirect": f"{response['url']}?token_ws={response['token']}"
            })
        else:
            raise Exception("La respuesta de Transbank no fue exitosa.")

    except Exception as e:
        print(f"Error al crear la transacción: {e}")
        return jsonify({"error": str(e)}), 500

# --- Ruta para Confirmar la Transacción (después del pago) ---
@app.route('/api/confirm-transaction', methods=['POST'])
def confirm_transaction():
    try:
        data = request.get_json()
        token = data.get('token')

        if not token:
            return jsonify({"error": "No se recibió el token de la transacción"}), 400

        # Confirma la transacción con el token, pasando las opciones de integración incluyendo el tipo TEST
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        response = tx.commit(token)

        # Aquí puedes procesar la respuesta de la confirmación
        if response.get('status') == 'AUTHORIZED':
            print("Pago APROBADO:", response)
        else:
            print("Pago RECHAZADO:", response)
        
        return jsonify(response)

    except Exception as e:
        print(f"Error al confirmar la transacción: {e}")
        return jsonify({"error": str(e)}), 500

# --- Iniciar el Servidor ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)

