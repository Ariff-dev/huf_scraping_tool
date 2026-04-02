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
    """Operations on the `artistas` table."""

    def __init__(self):
        self.db: Client = get_supabase_client()    # Public
        self.admin: Client = get_admin_client()     # Admin
        self.table = "artistas"

    # ---------- READ ----------

    def get_all(self) -> list:
        """Gives all the artists."""
        response = self.db.table(self.table).select("*").execute()
        return response.data

    def get_by_id(self, artista_id: int) -> dict | None:
        """Gives an artist by ID."""
        response = (
            self.db.table(self.table)
            .select("*")
            .eq("id", artista_id)
            .single()
            .execute()
        )
        return response.data

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

    def update(self, artista_id: int, **fields) -> dict:
        """
        Updates an artist by ID.
        """
        response = (
            self.admin.table(self.table)
            .update(fields)
            .eq("id", artista_id)
            .execute()
        )
        return response.data

    def delete(self, artista_id: int) -> dict:
        """
        Deletes an artist by ID.
        """
        response = (
            self.admin.table(self.table)
            .delete()
            .eq("id", artista_id)
            .execute()
        )
        return response.data


# ─────────────────────────────────────────────
#  CANCIONES
# ─────────────────────────────────────────────

class CancionesDB:
    """Operations on the `canciones` table."""

    def __init__(self):
        self.db: Client = get_supabase_client()    # Public
        self.admin: Client = get_admin_client()     # Admin
        self.table = "canciones"

    # ---------- READ ----------

    def get_all(self) -> list:
        """Gives all the songs, including the artist's name and photo."""
        response = (
            self.db.table(self.table)
            .select("*, artistas(id, nombre, foto_url)")
            .execute()
        )
        return response.data

    def get_by_id(self, cancion_id: int) -> dict | None:
        """Gives a song by ID."""
        response = (
            self.db.table(self.table)
            .select("*, artistas(id, nombre, foto_url)")
            .eq("id", cancion_id)
            .single()
            .execute()
        )
        return response.data

    def get_by_artista(self, artista_id: int) -> list:
        """Gives all the songs of a specific artist."""
        response = (
            self.db.table(self.table)
            .select("*")
            .eq("artista_id", artista_id)
            .execute()
        )
        return response.data

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

    def update(self, cancion_id: int, **fields) -> dict:
        """
        Updates a song by ID.
        """
        response = (
            self.admin.table(self.table)
            .update(fields)
            .eq("id", cancion_id)
            .execute()
        )
        return response.data

    def delete(self, cancion_id: int) -> dict:
        """
        Deletes a song by ID.
        """
        response = (
            self.admin.table(self.table)
            .delete()
            .eq("id", cancion_id)
            .execute()
        )
        return response.data