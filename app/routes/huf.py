from flask import Blueprint, request, jsonify
from app.web.huf.huf import ArtistasDB, CancionesDB
from app.web.tools.imagedwn import upload_image_from_url

huf_bp = Blueprint('huf', __name__)

# ─────────────────────────────────────────────
#  ARTISTAS
# ─────────────────────────────────────────────

@huf_bp.route('/artcr/', methods=['POST'])
def create_artista():
    """
    Crate a new artist. if image_url is provided, upload it to cloudinary and save the public_id as foto_url.
    """
    data = request.get_json()
    if not data or 'nombre' not in data:
        return jsonify({"error": "'nombre' is required"}), 400

    try:
        # Si viene una URL de imagen, subirla a Cloudinary primero
        if data.get('image_url'):
            img = upload_image_from_url(data['image_url'], folder='artistas')
            data['foto_url'] = img['public_id']

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
    """
    Crate a new song. if image_url is provided, upload it to cloudinary and save the public_id as foto_url.
    """
    data = request.get_json()
    if not data or 'nombre' not in data:
        return jsonify({"error": "'nombre' is required"}), 400

    try:
        # Si viene una URL de imagen, subirla a Cloudinary primero
        if data.get('image_url'):
            img = upload_image_from_url(data['image_url'], folder='canciones')
            data['foto_url'] = img['public_id']

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
