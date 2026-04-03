# HUF Scraping Tool API

A Flask-based REST API that combines **web scraping** (Playwright + Spotify) with a **database layer** (Supabase) and **media management** (Cloudinary). Designed to be called from automated workflows like n8n.

## 🚀 Features

- **Spotify Scraper** — Extracts artist bios, listener counts, and song metadata via headless Playwright browser sessions, executed concurrently with `ThreadPoolExecutor`.
- **HUF Database Layer** — Full CRUD interface over Supabase for `artistas` and `canciones` tables, using `service_role` key for secure server-side writes.
- **Cloudinary Image Upload** — Accepts an `image_url` in the request body, downloads it server-side, uploads it to Cloudinary, and stores the `public_id` in Supabase.
- **Environment-based config** — All secrets managed via `.env`, never hardcoded.

## 🛠️ Requirements

- Python 3.10+
- Chromium via Playwright
- Supabase project (tables: `artistas`, `canciones`)
- Cloudinary account

## 📦 Installation

```bash
# 1. Clone
git clone https://github.com/Ariff-dev/huf_scraping_tool.git
cd huf_scraping_tool

# 2. Virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
# source venv/bin/activate    # Linux / macOS

# 3. Dependencies
pip install -r requirements.txt

# 4. Playwright browser
playwright install chromium

# 5. Environment variables
# Copy .env.example → .env and fill in your values
```

## ⚙️ Running

```bash
.\venv\Scripts\python.exe .\main.py   # Windows
# python main.py                       # Linux / macOS
```

Server starts at `http://0.0.0.0:5000`.

---

## 📡 Endpoints

### Spotify

#### `POST /api/inf/`
Scrapes artist info and song metadata simultaneously.

```json
{ "artist": "Borja Picó", "song": "Sonrisas" }
```

---

### HUF — Artists

#### `POST /huf/artcr/`
Creates a new artist. If `image_url` is provided, the image is downloaded and uploaded to Cloudinary automatically.

```json
{
  "nombre": "Artist Name",
  "descripcion": "Bio text...",
  "image_url": "https://example.com/photo.jpg",
  "url_spotify": "https://open.spotify.com/...",
  "url_instagram": "https://instagram.com/...",
  "url_tiktok": "https://tiktok.com/...",
  "url_youtube": "https://youtube.com/...",
  "url_facebook": "https://facebook.com/...",
  "url_sitio_web": "https://artist.com"
}
```

---

### HUF — Songs

#### `POST /huf/songcr/`
Creates a new song. If `image_url` is provided, the cover is uploaded to Cloudinary automatically.

```json
{
  "nombre": "Song Title",
  "artista_id": 1,
  "descripcion": "Full description...",
  "descripcion_corta": "Short version",
  "creditos": "Written by...",
  "image_url": "https://example.com/cover.jpg",
  "url_spotify": "https://open.spotify.com/...",
  "url_tiktok": "https://tiktok.com/...",
  "url_youtube": "https://youtube.com/..."
}
```

---

## 🐳 Docker

```bash
docker compose up --build
```

## ⚖️ Disclaimer

This repository is for educational and research purposes. Always abide by the terms of service of any platform you interact with.
