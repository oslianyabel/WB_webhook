from flask import Flask, request, jsonify
import os
from datetime import datetime
import logging

# Configurar logging para producción
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuración
port = int(os.environ.get("PORT", 3000))
verify_token = os.environ.get("VERIFY_TOKEN")

# Verificar que el token esté configurado
if not verify_token:
    logger.warning("VERIFY_TOKEN no está configurado. El webhook no funcionará correctamente.")


# Ruta para GET - Verificación del webhook
@app.route("/", methods=["GET"])
def verify_webhook():
    try:
        mode = request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        token = request.args.get("hub.verify_token")

        if mode == "subscribe" and token == verify_token:
            logger.info("WEBHOOK VERIFIED")
            return challenge, 200
        else:
            logger.warning(f"Verificación fallida - Mode: {mode}, Token match: {token == verify_token}")
            return "", 403
    except Exception as e:
        logger.error(f"Error en verificación del webhook: {str(e)}")
        return "", 500


# Ruta para POST - Recepción de mensajes
@app.route("/", methods=["POST"])
def receive_webhook():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = request.get_json()
        
        logger.info(f"Webhook recibido en {timestamp}")
        logger.info(f"Datos recibidos: {data}")
        
        # Aquí puedes agregar tu lógica de procesamiento
        
        return "", 200
    except Exception as e:
        logger.error(f"Error procesando webhook: {str(e)}")
        return "", 500


# Endpoint de salud para monitoreo
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "WhatsApp Webhook API"
    }), 200


if __name__ == "__main__":
    logger.info(f"Iniciando servidor en puerto {port}")
    # Para desarrollo local
    app.run(host="0.0.0.0", port=port, debug=False)
else:
    # Para producción con gunicorn
    logger.info("Aplicación iniciada en modo producción")
