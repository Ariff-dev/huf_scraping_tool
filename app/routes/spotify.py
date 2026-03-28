import concurrent.futures
from flask import Blueprint, request, jsonify
from app.web.spotify.scrap import SpotifyScraper

spotify_bp = Blueprint('spotify', __name__)

@spotify_bp.route('/inf/', methods=['POST'])
def info_general():
    data = request.get_json()
    
    # Validamos ambos campos para no tener que consultarlo en dos rutas distintas
    if not data or 'artist' not in data or 'song' not in data:
        return jsonify({"error": "Se requieren los atributos 'artist' y 'song' en el JSON. Ejemplo: {'artist': 'Borja Picó', 'song': 'Sonrisas'}"}), 400
        
    artist_name = data['artist']
    song_name = data['song']
    
    try:
        scraper = SpotifyScraper()
        
        # Ejecutar los dos métodos en paralelo (al mismo tiempo) usando 2 hilos.
        # Esto reduce el tiempo de la llamada POST a la mitad.
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_artist = executor.submit(scraper.search_artist, artist_name)
            future_song = executor.submit(scraper.search_song, artist_name=artist_name, song_name=song_name)
            
            # Esperamos a que los dos terminen de scrapear
            artist_result = future_artist.result()
            song_result = future_song.result()
            
        # Armamos el JSON súper completo con toda la info
        return jsonify({
            "success": True, 
            "artist": artist_name,
            "song": song_name,
            "artist_data": artist_result,
            "song_data": song_result
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e)
        }), 500
