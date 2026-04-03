from flask import Blueprint, request, jsonify
from app.web.huf.huf import ArtistasDB, CancionesDB

huf_bp = Blueprint('huf', __name__)

# ─────────────────────────────────────────────
#  ARTISTAS
# ─────────────────────────────────────────────

@huf_bp.route('/artcr/', methods=['POST'])
def create_artista():
    data = request.get_json()
    if not data or 'nombre' not in data:
        return jsonify({"error": "'nombre' is required"}), 400
    try:
        db = ArtistasDB()
        result = db.create(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            foto_url=data.get('foto_url'),
            url_spotify=data.get('url_spotify'),
            url_instagram=data.get('url_instagram'),
            url_facebook=data.get('url_facebook'),
            url_youtube=data.get('url_youtube'),
            url_tiktok=data.get('url_tiktok'),
            url_sitio_web=data.get('url_sitio_web'),
        )
        return jsonify({"success": True, "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ─────────────────────────────────────────────
#  CANCIONES
# ─────────────────────────────────────────────

@huf_bp.route('/songcr/', methods=['POST'])
def create_cancion():
    data = request.get_json()
    if not data or 'nombre' not in data:
        return jsonify({"error": "'nombre' is required"}), 400
    try:
        db = CancionesDB()
        result = db.create(
            nombre=data['nombre'],
            artista_id=data.get('artista_id'),
            descripcion=data.get('descripcion'),
            descripcion_corta=data.get('descripcion_corta'),
            creditos=data.get('creditos'),
            foto_url=data.get('foto_url'),
            url_tiktok=data.get('url_tiktok'),
            url_spotify=data.get('url_spotify'),
            url_youtube=data.get('url_youtube'),
        )
        return jsonify({"success": True, "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


