# WhatsApp Webhook API

API de Flask para manejar webhooks de WhatsApp Business API.

## Configuración para Producción

### Variables de Entorno Requeridas

- `PORT`: Puerto donde correrá la aplicación (por defecto: 3000)
- `VERIFY_TOKEN`: Token de verificación para el webhook de WhatsApp

### Despliegue en Railway

1. Conecta tu repositorio de GitHub a Railway
2. Configura las variables de entorno en el dashboard de Railway
3. Railway detectará automáticamente que es una aplicación Flask y la desplegará

### Despliegue en Render

1. Conecta tu repositorio de GitHub a Render
2. Selecciona "Web Service"
3. Configura las variables de entorno
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`

### Despliegue en Heroku

1. Instala Heroku CLI
2. Ejecuta los siguientes comandos:

```bash
heroku create tu-app-name
heroku config:set VERIFY_TOKEN=tu_token_aqui
git push heroku main
```

## Endpoints

- `GET /` - Verificación del webhook
- `POST /` - Recepción de mensajes del webhook

## Desarrollo Local

1. Instala las dependencias: `pip install -r requirements.txt`
2. Copia `.env.example` a `.env` y configura las variables
3. Ejecuta: `python app.py`
