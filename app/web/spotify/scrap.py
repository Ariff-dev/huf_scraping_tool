import os
import urllib.parse
import re
from playwright.sync_api import sync_playwright

class SpotifyScraper:
    def __init__(self, headless: bool = None):
        # Si no se define al instanciar la clase, asume los valores del entorno
        if headless is None:
            env_headless = os.environ.get("SCRAPER_HEADLESS", "True").strip().lower()
            self.headless = env_headless in ("true", "1", "yes")
        else:
            self.headless = headless

    def search_artist(self, artist_name: str) -> dict:
        """
        Recibe el nombre del artista, formatea la URL, inicia Playwright en Chromium,
        y accede a la página de búsqueda de artistas.
        """
        query_encoded = urllib.parse.quote(artist_name)
        url = f"https://open.spotify.com/search/{query_encoded}/artists"
        
        result_data = {
            "search_url": url,
            "status": "pending_extraction",
            "page_title": None,
        }
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            # Dirigir a la URL generada
            page.goto(url)
            
            # 1. Esperamos a que el contenedor principal '#searchPage' esté presente
            page.wait_for_selector('#searchPage', timeout=10000)
            
            # 2. Busca y haz clic en el artista
            first_card_selector = 'div[data-testid="search-category-card-0"]'
            page.wait_for_selector(first_card_selector)
            page.click(first_card_selector)
            
            # 3. Esperar el título del artista
            page.wait_for_selector('h1', timeout=10000) 
            page.wait_for_load_state("networkidle")
            
            # 4. Scroll para About
            page.mouse.move(500, 500)
            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(1000)
            
            about_header = page.locator('h2', has_text=re.compile(r'^(About|Acerca de)$', re.IGNORECASE)).first
            about_header.wait_for(timeout=10000)
            
            parent_container = about_header.locator('..')
            about_button = parent_container.locator('button').first
            
            artist_name_about = about_button.get_attribute('aria-label')
            
            image_style = about_button.get_attribute('style') or ""
            image_url = ""
            match = re.search(r'url\([\'"&quot;]*(.*?)[\'"&quot;]*\)', image_style)
            if match:
                image_url = match.group(1)
                
            bio_locator = about_button.locator('div[dir="auto"]').first
            bio = bio_locator.inner_text() if bio_locator.count() > 0 else ""
            
            listeners_locator = about_button.locator('div[data-encore-id="text"]').first
            listeners = listeners_locator.inner_text() if listeners_locator.count() > 0 else ""
            
            result_data.update({
                "profile_url": page.url,
                "page_title": page.title(),
                "status": "success",
                "extracted": {
                    "artist_name": artist_name_about,
                    "image_url": image_url,
                    "bio": bio,
                    "monthly_listeners": listeners
                }
            })
            
            browser.close()
            
        return result_data

    def search_song(self, artist_name: str, song_name: str) -> dict:
        """
        Inicia Playwright, concatena la canción y el artista ("{song} de {artist}")
        y busca ese string directamente en los resultados generales de Spotify.
        """
        query = f"{song_name} de {artist_name}"
        query_encoded = urllib.parse.quote(query)
        url = f"https://open.spotify.com/search/{query_encoded}"
        
        result_data = {
            "search_url": url,
            "query": query,
            "status": "pending_extraction",
            "page_title": None,
        }
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            page.goto(url)
            page.wait_for_load_state("networkidle")
            
            # Simple click ciego sin pausas visuales
            try:
                page.wait_for_selector('#searchPage', timeout=5000)
                top_result_selector = 'div[data-testid="top-result-card"]'
                page.click(top_result_selector, timeout=3000)
                page.wait_for_load_state("networkidle")
            except:
                pass
            
            result_data["song_url"] = page.url
            result_data["page_title"] = page.title()
            result_data["status"] = "success"
            
            browser.close()
            
        return result_data
