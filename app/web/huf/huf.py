import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")             
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL o SUPABASE_KEY no están configurados.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_admin_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise ValueError("SUPABASE_URL o SUPABASE_SERVICE_KEY no están configurados.")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


# ─────────────────────────────────────────────
#  ARTISTAS
# ─────────────────────────────────────────────

class ArtistasDB:
    def __init__(self):
        self.admin: Client = get_admin_client()     # Admin
        self.table = "artistas"

    # ---------- WRITE ----------

    def create(self, nombre: str, descripcion: str = None, foto_url: str = None,
               url_spotify: str = None, url_instagram: str = None,
               url_facebook: str = None, url_youtube: str = None,
               url_tiktok: str = None, url_sitio_web: str = None) -> dict:
        """
        Inserts a new artist.
        """
        data = {
            "nombre": nombre,
            "descripcion": descripcion,
            "foto_url": foto_url,
            "url_spotify": url_spotify,
            "url_instagram": url_instagram,
            "url_facebook": url_facebook,
            "url_youtube": url_youtube,
            "url_tiktok": url_tiktok,
            "url_sitio_web": url_sitio_web,
        }
        # Eliminar claves con valor None para no sobreescribir defaults de BD
        data = {k: v for k, v in data.items() if v is not None}
        response = self.admin.table(self.table).insert(data).execute()
        return response.data

# ─────────────────────────────────────────────
#  CANCIONES
# ─────────────────────────────────────────────

class CancionesDB:
    def __init__(self):
        self.admin: Client = get_admin_client()     # Admin
        self.table = "canciones"

    # ---------- WRITE ----------

    def create(self, nombre: str, artista_id: int = None, descripcion: str = None,
               descripcion_corta: str = None, creditos: str = None,
               foto_url: str = None, url_tiktok: str = None,
               url_spotify: str = None, url_youtube: str = None) -> dict:
        """
        Inserts a new song.
        """
        data = {
            "nombre": nombre,
            "artista_id": artista_id,
            "descripcion": descripcion,
            "descripcion_corta": descripcion_corta,
            "creditos": creditos,
            "foto_url": foto_url,
            "url_tiktok": url_tiktok,
            "url_spotify": url_spotify,
            "url_youtube": url_youtube,
        }
        data = {k: v for k, v in data.items() if v is not None}
        response = self.admin.table(self.table).insert(data).execute()
        return response.data