import os
from flask import Flask
from dotenv import load_dotenv
from app.routes.spotify import spotify_bp

# Cargar variables de entorno locales desde el archivo .env si existe
load_dotenv()

app = Flask(__name__)

# Registrar Blueprints de las rutas
# Accesible bajo el prefijo /api, por lo tanto el endpoint será /api/infart/
app.register_blueprint(spotify_bp, url_prefix='/api')
app.register_blueprint(huf_bp, url_prefix='/api')


if __name__ == '__main__':
    # Obtener puerto y host desde entorno o establecer por defecto
    port = int(os.environ.get("FLASK_PORT", 5000))
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    debug_mode = os.environ.get("FLASK_ENV", "development") == "development"
    
    # Ejecutamos el orquestador principal
    app.run(host=host, port=port, debug=debug_mode)
